from simulation_env import CFD_env, nb_actuations

import os
import numpy as np
from tensorforce.agents import PPOAgent
from tensorforce.execution import Runner


print("Create CFD env")
environment = CFD_env(True)

print("define network specs")
network_spec = [
    dict(type='dense', size=512),
    dict(type='dense', size=512),
]

print(environment.states)
print(environment.actions)
print(network_spec)

print("define agent")
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
        # how many episodes per update
        batch_size=environment.params['Model_save'],
        # how many episodes
        frequency=environment.params['Model_save']
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

if(os.path.exists('saved_models/checkpoint')):
    restore_path = './saved_models'
else:
    restore_path = None

if restore_path is not None:
    print("restore the model")
    agent.restore_model(restore_path)

print("define runner")

runner = Runner(agent=agent, environment=environment)


def episode_finished(r):
    print("Finished episode {ep} after {ts} timesteps (reward: {reward})".format(ep=r.episode, ts=r.episode_timestep,
                                                                                 reward=r.episode_rewards[-1]))
    print("save the mode")

    name_save = "./saved_models/ppo_model"
    # NOTE: need to check if should create the dir
    r.agent.save_model(name_save, append_timestep=False)

    return True


# Start learning
print("start learning")
runner.run(episodes=500, max_episode_timesteps=nb_actuations, episode_finished=episode_finished)
runner.close()

# Print statistics
print("Learning finished. Total episodes: {ep}. Average reward of last 100 episodes: {ar}.".format(
    ep=runner.episode,
    ar=np.mean(runner.episode_rewards[-100:]))
)


