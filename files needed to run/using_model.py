import time

from stable_baselines3 import PPO
import torch as th

from rlohhell.envs.ohhell import OhHellEnv2


'''Creates a single environment'''
env = OhHellEnv2()

# Using the model
model = PPO.load("best_model1.zip")
obs = env.reset()
total_reward = 0
times_illegal_action = 0
for _ in range(11):
    action, _states = model.predict(obs)
    print(env._decode_action(action))
    obs, reward, dones, info = env.step(action)
    total_reward += reward
    print(reward)
    if reward < 0:
        times_illegal_action += 1

print('The total reward was ' + str(total_reward))
print('The agent illegally choose ' + str(times_illegal_action))
