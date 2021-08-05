"""
Author: Dr. Jichao Li <cfdljc@gmail.com>
Date:   2019-12-03
"""
from tensorforce.environments import Environment
from DMD import DMD_analysis
import tensorforce
import numpy as np
import sys
import os
import random as random
import time
import math
import csv

class EnvNek5000(Environment):
    """Nek5000 Environment for CFD simulations."""

    def __init__(self, params, reward_function='energy', simu_name="CFDSimulation"):

        print("--- Nek5000 CFD env init ---")

        self.params = params
        self.reward_function = reward_function
        self.simu_name = simu_name
        self.drag = 0.0
        self.lift = 0.0
        self.ncrash = 0
        self.probes_values = np.zeros(self.params['nstates'])
        self.rewardd = 0.0
        self.DMDeigen = 0.0
        self.energy = 0.0
        self.baseflow = np.loadtxt(self.params['simulationfolder']+'/base.plt')
        self.start_class(complete_reset=True)

        print("--- Nek5000 CFD env init done! ---")

    def start_class(self, complete_reset=True):
        self.episode_number = 0
        self.action_number  = 0
        
        self.previous_modes_number = 0
        
        if self.params['TrainFlag']:
            # We do this if it is a training run
            # Check how many saved models exist. We want to start with the latest one.
            for ic in range(100,0,-1):
                if os.path.isfile('./saved_models'+str(ic)+'/ppo_model.meta'):
                    self.previous_modes_number = ic
                    break

            if self.previous_modes_number == 0:
                # It means there is no useful previously-saved models. We just creat the file.
                f = open(self.params['run_hist'],'w')
                f.close()
            else:
                # We rewrite the history file to remove the unsaved training history
                tempdata = np.loadtxt(self.params['run_hist'])
                f = open(self.params['run_hist'],'w')
                for i in range(self.previous_modes_number*self.params['Model_save']*(self.params['nb_actuations']+1)):
                    f.write('%.15f %.15f %.15f\n'%(tempdata[i,0],tempdata[i,1],tempdata[i,2]))
                f.close()
                
                # We re-save the lasted model as the 'save_models', so that we could start from this model
                os.system('rm -r saved_models')
                os.system('cp -r saved_models{0} saved_models'.format(str(self.previous_modes_number)))    
        else:
            # Otherwise, do not copy anything
            f = open(self.params['run_hist'],'w')
            f.close()
        
        self.ready_to_use = True
        self.initialize_flow(complete_reset=True)

    def write_history_parameters(self):
        return None

    def close(self):
        """
        Close environment. No other method calls possible afterwards.
        """

        self.ready_to_use = False

    def seed(self, seed):
        """
        Sets the random seed of the environment to the given value (current time, if seed=None).
        Naturally deterministic Environments don't have to implement this method.

        Args:
            seed (int): The seed to use for initializing the pseudo-random number generator (default=epoch time in sec).
        Returns: The actual seed (int) used OR None if Environment did not override this method (no seeding supported).
        """

        # we have a deterministic environment: no need to implement

        return None

    def reset(self):
        """
        Reset environment and setup for new episode.

        Returns:
            initial state of reset environment.
        """
        
        chance = random.random()
        probability_hard_reset = 0.2
        if chance < probability_hard_reset:
            self.initialize_flow(complete_reset=True)
        else:
            self.initialize_flow(complete_reset=False)

        next_state = np.transpose(self.probes_values)
        self.episode_number += 1

        # Save intermediate models
        if (self.episode_number > 1) and (self.episode_number%(self.params['Model_save']) ==1):
            os.system('cp -r saved_models saved_models{0}'.format(str(self.previous_modes_number+self.episode_number//self.params['Model_save'])))

        return(next_state)

    def initialize_flow(self, complete_reset=True):
        """
        Initialize the flow
        """
        if complete_reset:
            os.system('cp {0}/{1} {0}/{2}'.format(self.params['simulationfolder'],self.params['initial_filed'],self.params['restart_filed']))
            cps  = np.loadtxt(self.params['simulationfolder']+'/'+self.params['initial_state_file'])
            self.probes_values = cps[:,2].copy()
            self.real_actions  = np.zeros(self.params['nactions'])
            self.last_actions  = np.zeros(self.params['nactions'])
            self.snapshots=[]

        else:
            pass
        

    def writeActions(self,actions):
        '''
        This function is to write the parameters that will be used in the CFD simulations.
        '''
        self.last_actions = self.real_actions
        self.real_actions = actions
        fact=open(self.params['simulationfolder']+'/'+self.params['action_file'],'w')
        for iact in range(self.params['nactions']):
            fact.write('%.15f %.15f\n'%(self.real_actions[iact],self.last_actions[iact]))
        if self.params['nactions'] == 1:
            # dummy data
            fact.write('%.15f %.15f\n'%(0.0,0.0))
        fact.close()
        '''
        Clean the dir
        '''
        os.system('rm {0}/{1}'.format(self.params['simulationfolder'],self.params['cdcl_file']))
        os.system('rm {0}/{1}'.format(self.params['simulationfolder'],self.params['state_file']))
    
    def exeCFD(self):
        '''
        Run CFD simulations
        '''
        os.chdir(self.params['simulationfolder'])
        if self.params['ncpu']==1:
            os.system('./nek5000')
        else:
            os.system('nekmpi {0} {1}'.format(self.params['simulationfolder'], self.params['ncpu']))
        
        # save the flow filed to a format handy to read via `np.loadtxt()`
        os.system("sed -e '1,45d' < {0}.fld01 > {1}".format(self.params['simulationfolder'],self.params['flow_file']))
        os.chdir('..')

    def computeEnergy(self,newflow):
        # a plain sum of _the shedding energy_
        TKE = 0.0
        for i in range(self.baseflow.shape[0]):
            tempx = newflow[i,2] - self.baseflow[i,2]
            tempy = newflow[i,3] - self.baseflow[i,3]
            TKE += tempx*tempx + tempy*tempy
        return TKE
        
    def readEnv(self):
        '''
        This function is to read the results of the CFD simulation.
        These results may include some pressures/velocity and lift/drag coefficients.
        We will use them to perceive the environments and also to compute the reward.
        '''
        try:
            flagnan = False
            cdcl = np.loadtxt(self.params['simulationfolder']+'/'+self.params['cdcl_file'])
            flagnan = np.isnan(cdcl).any()
        except:
            flagnan = True
        
        if not flagnan:
            newflow = np.loadtxt(self.params['simulationfolder']+'/'+self.params['flow_file'])
            self.energy = self.computeEnergy(newflow)
            if self.reward_function == 'energyDMD':
                # we need snapshots for DMD analysis
                thissanp = newflow[:,2]
                self.snapshots.append(thissanp)

            states  = np.loadtxt(self.params['simulationfolder']+'/'+self.params['state_file'])
            self.lift = np.mean(cdcl[self.params['num_mean']:,2])
            self.drag = np.mean(cdcl[self.params['num_mean']:,1])
            self.probes_values = states[:,2].copy()
            os.system('mv {0}/{0}.fld01 {0}/{1}'.format(self.params['simulationfolder'],self.params['restart_filed']))
        else:
            print("CFD simulation didn't converge! Terminated.")
            sys.exit()

        terminal = False
        f = open(self.params['run_hist'],'a+')
        mytime = self.previous_modes_number*self.params['Model_save'] + self.action_number//(self.params['nactuations']+1) + \
                  (self.action_number%((self.params['nactuations']+1)))/(self.params['nactuations']+1)
        f.write('%.15f %.15f %.15f %.15f\n'%(mytime,self.drag,self.lift,self.energy))

        return terminal      

    def output_data(self):
        avg_drag = self.drag
        avg_lift = self.lift
        avg_energy = self.energy
        name = "output.plt"
        if(not os.path.exists("saved_models")):
            os.mkdir("saved_models")
        if(not os.path.exists("saved_models/"+name)):
            with open("saved_models/"+name, "w") as csv_file:
                spam_writer=csv.writer(csv_file, delimiter=",", lineterminator="\n")
                spam_writer.writerow(['Variables=Actions', 'Drag', 'Lift', 'Energy', 'Action1', 'Reward', 'DMDeigen', 'Episode'])
                spam_writer.writerow([self.action_number, avg_drag, avg_lift, avg_energy, self.real_actions[0],self.rewardd,self.DMDeigen,self.episode_number])
        else:
            with open("saved_models/"+name, "a") as csv_file:
                spam_writer=csv.writer(csv_file, delimiter=",", lineterminator="\n")
                spam_writer.writerow([self.action_number, avg_drag, avg_lift, avg_energy, self.real_actions[0],self.rewardd,self.DMDeigen,self.episode_number])
        
    def execute(self, actions=None):

        if actions is None:
            nbr_jets = self.params['nactions']
            actions = np.zeros(nbr_jets)

        #Write actions for CFD simulations
        self.writeActions(actions)
        #Execute CFD simulations
        self.exeCFD()
        #Read CFD results
        terminal = self.readEnv()
        next_state = self.probes_values
        reward = self.compute_reward()
        self.rewardd = reward
        self.output_data()
        self.action_number += 1

        return(next_state, terminal, reward)


    def getDMDcoef(self):
        nr = 5
        dt = self.params['DMDdt']
        nsnap = len(self.snapshots)
        nsnapused = 30        
        if nsnap > nsnapused:
            newdata = np.array(self.snapshots[nsnap-nsnapused:])
            data1 = np.transpose(newdata[:nsnapused-1,:])
            data2 = np.transpose(newdata[1:nsnapused,:])
            myDMD = DMD_analysis(dt,nr,data1,data2)
            myDMD.compute()
            myrate = myDMD.growthrate()
            coef = math.exp(myrate)
        else:
            coef = 1.0
        #print('DMD coef:',coef)
        self.DMDeigen = coef
        return coef
        
    def compute_reward(self):
        if self.reward_function == 'energy': 
            return self.params['Penalty_energy'] - self.energy
        elif self.reward_function == 'energyDMD': 
            coef = self.getDMDcoef()
            return self.params['Penalty_energy'] - self.energy*coef
        else:
            raise RuntimeError("reward function {} not yet implemented".format(self.reward_function))

    @property
    def states(self):
        """
        Return the state space. Might include subdicts if multiple states are available simultaneously.

        Returns: dict of state properties (shape and type).

        """

        return dict(type='float', shape=(self.params['nstates']*1, ) )

    @property
    def actions(self):
        """
        Return the action space. Might include subdicts if multiple actions are available simultaneously.

        Returns: dict of action properties (continuous, number of actions).
        """

        # NOTE: we could also have several levels of dict in dict, for example:
        # return { str(i): dict(continuous=True, min_value=0, max_value=1) for i in range(self.n + 1) }

        return dict(type='float',
                    shape=(self.params['nactions'], ),
                    min_value=self.params["min_actions"],
                    max_value=self.params["max_actions"])


