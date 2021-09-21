from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env
import torch as th
from torch import nn

from rlohhell.envs.ohhell import OhHellEnv2

env = OhHellEnv2()
check_env(env)

# env = make_vec_env(OhHellEnv2)

# policy_kwargs = dict(activation_fn=th.nn.ReLU,
#                      net_arch=[700, 350, dict(pi=[63], vf=[175, 35])])

# model = PPO('MlpPolicy', env, policy_kwargs=policy_kwargs, tensorboard_log="./tmp/", verbose=1)
# model.learn(total_timesteps=250000)


# model.save("ppo_ohhell")


# #  Using the model
# model = PPO.load("ppo_ohhell")
# obs = env.reset()
# for _ in range(1000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)