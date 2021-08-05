from simulation_env import CFD_env, nb_actuations

import os
import numpy as np
from tensorforce.agents import PPOAgent
from tensorforce.execution import Runner

testlist=[]
for i in range(30):
    testlist.append(i)

for ipath in testlist:
    print("Create CFD env")
    environment = CFD_env(False)

    print("define network specs")
    network_spec = [
        dict(type='dense', size=512),
        dict(type='dense', size=512),
    ]

    print(environment.states)
    print(environment.actions)
    print(network_spec)

    deterministic=True

    agent = PPOAgent(
        states=environment.states,
        actions=environment.actions,
        network=network_spec,
        # Agent
        states_preprocessing=None,
        actions_exploration=None,
        reward_preprocessing=None,
        # MemoryModel
        update_mode=dict(
            unit='episodes',
            # 10 episodes per update
            batch_size=20,
            # Every 10 episodes
            frequency=20
        ),
        memory=dict(
            type='latest',
            include_next_states=False,
            capacity=10000
        ),
        # DistributionModel
        distributions=None,
        entropy_regularization=0.01,
        # PGModel
        baseline_mode='states',
        baseline=dict(
            type='mlp',
            sizes=[32, 32]
        ),
        baseline_optimizer=dict(
            type='multi_step',
            optimizer=dict(
                type='adam',
                learning_rate=1e-3
            ),
            num_steps=5
        ),
        gae_lambda=0.97,
        # PGLRModel
        likelihood_ratio_clipping=0.2,
        # PPOAgent
        step_optimizer=dict(
            type='adam',
            learning_rate=1e-3
        ),
        subsampling_fraction=0.2,
        optimization_steps=25,
        execution=dict(
            type='single',
            session_config=None,
            distributed_spec=None
        )
    )

    restore_path = './saved_models'+str(ipath)
    if restore_path is not None:
        print("restore the selected model")
        agent.restore_model(restore_path)
    else :
        print('Trained Network not found...')

    def one_run():

        print("start simulation")
        state = environment.reset()
        environment.render = True

        for k in range(4*nb_actuations):
            action = agent.act(state, deterministic=deterministic)
            state, terminal, reward = environment.execute(action)
            #myfile='{0:05}'.format(k+2)
            #os.system('cp flowcontrol/restart.fld flowcontrol/flowcontrol0.f{0}'.format(myfile))
        #myfile='{0:05}'.format(1)
        #os.system('cp flowcontrol/intitial.fld flowcontrol/flowcontrol0.f{0}'.format(myfile))

    one_run()
    #os.system('cp -r flowcontrol flowcontrol{0}'.format(str(ipath+1)))
    os.system('mv test_hist.plt test_hist{0}.plt'.format(str(ipath)))
    
    
