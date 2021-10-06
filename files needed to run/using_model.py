import time

from stable_baselines3 import PPO
import torch as th
import numpy as np
import matplotlib.pyplot as plt

from rlohhell.envs.ohhell import OhHellEnv2


'''Creates a single environment'''
env = OhHellEnv2()

# Using the model
model = PPO.load("average_score_3")
illegals = []
for i in range(500):
    obs = env.reset()
    total_reward = 0
    times_illegal_action = 0
    for _ in range(11):
        available_actions = list(env._get_legal_actions())
        # print(available_actions)
        mask = [1 if action in available_actions else 0 for action in range(63)]
        action, _states = model.predict(obs, mask=mask)
        # print(action)
        # print(env._decode_action(action))
        obs, reward, dones, info = env.step(action)
        total_reward += reward
        # print(reward)
        if reward < 0:
            times_illegal_action += 1

    illegals.append(times_illegal_action)
    
print("On average " + str(np.round(np.mean(illegals), 2)) + " illegal actions were selected.")
print("The standard deviation was " + str(np.round(np.std(illegals), 2)))


plt.hist(illegals)
plt.show()

# print('The total reward was ' + str(total_reward))
