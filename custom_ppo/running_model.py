import time

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback, EvalCallback
import torch as th

from rlohhell.envs.ohhell import OhHellEnv2


'''Creates a single environment and then uses the function make_venv_env to 
create multiple environments so they can be trained in parallel
''' 
env = OhHellEnv2()
env = make_vec_env(OhHellEnv2)


'''This is a second environment that is used when training to evaluate any saved agents
It has to be the same form as the original environment hence the vectorisation'''
eval_env = OhHellEnv2()
eval_env = make_vec_env(OhHellEnv2)


'''This is a callback to save the model every specificed number of timesteps and it creates
the directory if it is missing'''
checkpoint_callback = CheckpointCallback(save_freq=204800, save_path='./logs/logs_ppo/500_350/',
                                         name_prefix='training')

'''A second callback that evaluates the saved models and saves the best one 
in a seperate folder'''
eval_callback = EvalCallback(eval_env, best_model_save_path='./logs/logs_ppo/500_350/best_model',
                             log_path='./logs/logs_ppo/500_350/', eval_freq=1024000,
                             deterministic=True, render=False)

# Chaining the callbacks so that they can be used in conjuction
callback = CallbackList([checkpoint_callback, eval_callback])



'''This argument is passed to PPO/A2C or whatever model and it specifies the layout of the neural
network, right now is means 500 shared layer -> splits into 350 -> 63 for the policy network and
separately 350 -> 100 for the value function'''
policy_kwargs = dict(activation_fn=th.nn.ReLU,
                     net_arch=[500, dict(pi=[350, 63], vf=[350,100])])


'''Instatiating the model with a type of neural network, environment, structure of neural network,
and a place to log information for tensorboard'''
model = PPO('MlpPolicy', env, policy_kwargs=policy_kwargs, tensorboard_log="./tmp/", 
             verbose=1)

# Runnnig and timing the learning of the model
start = time.time()
model.learn(total_timesteps=2000000000, callback=callback)
end = time.time()
print("Time Taken: %f" % (end-start))        


# Saving the model to the current working directory
model.save("ppo_ohhell_500_350")


# # Using the model
# model = PPO.load("ppo_ohhell_500_350")
# obs = env.reset()
# for _ in range(11):
#     action, _states = model.predict(obs)
#     print(env._decode_action(action))
#     obs, reward, dones, info = env.step(action)
#     print(reward)