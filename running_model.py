# import rlohhell
# from stable_baselines3 import DQN, PPO, A2C, DDPG
# from stable_baselines3.common.env_util import make_vec_env
# from stable_baselines3.ppo.policies import MlpPolicy
# import torch
# import numpy as np
# from rlohhell.games.ohhell.utils import ACTION_LIST, ACTION_SPACE

# # print(torch.cuda.is_available())
# # print(torch.cuda.current_device())
# # print(torch.cuda.get_device_name(0))



# env = rlohhell.envs.ohhell.OhHellEnv2()
# # env = make_vec_env(lambda: env, n_envs=4)

# # model = PPO(MlpPolicy, env, verbose=1, tensorboard_log="./ppo_ohhell_tensorboard/")
# # model.learn(total_timesteps=10000000)  
# # model.save("ppo_ohhell")

    
# model = PPO.load("ppo_ohhell")

# # Enjoy trained agent
# obs = env.reset()
# i = 0
# while True:

#     avail_actions = list(env._get_legal_actions())

#     mask = np.array([True if action in avail_actions else False for action in list(ACTION_SPACE.values()) ])
    
#     print(mask)

#     action, _states = model.predict(observation=obs, mask=mask, deterministic=True)

#     print(action)
#     break
#     # i += 1
#     # if i > 4:
#     #     print([card.get_index() for card in env.game.played_cards])
#     #     print([card.get_index() for card in env.game.players[env.game.current_player].hand])
#     # print(env._decode_action(action))
#     obs, rewards, dones, info = env.step(action)


import torch
import numpy as np
from stable_baselines3.common.env_util import make_vec_env

import rlohhell
from rlohhell.games.ohhell.utils import ACTION_LIST, ACTION_SPACE
from PPO2 import BasePolicy, ActorCriticPolicy, FeedForwardPolicy, PPO2


# Starting the environment
env = rlohhell.envs.ohhell.OhHellEnv2()
env = make_vec_env(lambda: env, n_envs=4)

# Building the custom model
