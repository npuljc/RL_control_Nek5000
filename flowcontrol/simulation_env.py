from EnvNek import EnvNek5000
import numpy as np
import math


nstate =172   # number of enviorment states
naction = 1   # number of controlable variables

nb_actuations = 80 


def CFD_env(training_flag):
    reward_function = 'energy'
    simu_name = 'CylinderSimulation'
    if training_flag:
        # This is a training run
        historyfile='train_hist.plt'
    else:
        # This is a testing run
        historyfile='test_hist.plt'
    params={'nstates': nstate,
            'nactions': naction,
            'nactuations':nb_actuations,
            'min_actions': -0.15,
            'max_actions': 0.15,
            'nb_actuations':nb_actuations,
            'simulationfolder':'cylinder',
            'ncpu':1,
            'action_file':'Q.txt',
            'cdcl_file':'cdcl.dat',
            'state_file':'probe_values.dat',
            'initial_state_file':'intitial_probe_values.dat',
            'initial_filed':'intitial.fld',
            'restart_filed':'restart.fld',
            'num_mean':-8,
            'run_hist':historyfile,
            'Model_save':20,
            'snapshot':'snapshots.dat',
            'DMDdt':0.2,
            'TrainFlag':training_flag,
            'flow_file':'newflow.plt',
            'Penalty_energy':800.0,
    }

    the_env = EnvNek5000(params, reward_function=reward_function, simu_name=simu_name)

    return(the_env)
