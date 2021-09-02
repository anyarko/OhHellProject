import rlohhell
from stable_baselines3 import DQN, PPO, A2C, DDPG
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.ppo.policies import MlpPolicy
import torch

torch.cuda.is_available()
torch.cuda.current_device()
torch.cuda.get_device_name(0)



env = rlohhell.envs.ohhell.OhHellEnv2()
env = make_vec_env(lambda: env, n_envs=4)

model = PPO(MlpPolicy, env, verbose=1, tensorboard_log="./ppo_ohhell_tensorboard/")
model.learn(total_timesteps=10000000)  
model.save("ppo_ohhell")

    
# model = PPO.load("ppo_ohhell")

# Enjoy trained agent
# obs = env.reset()
# while True:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()
