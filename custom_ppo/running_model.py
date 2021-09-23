from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback, EvalCallback
import torch as th

from rlohhell.envs.ohhell import OhHellEnv2



env = OhHellEnv2()
env = make_vec_env(OhHellEnv2)
# The environment for evaluating training agents
eval_env = OhHellEnv2()
eval_env = make_vec_env(OhHellEnv2)

checkpoint_callback = CheckpointCallback(save_freq=204800, save_path='./logs/logs_ppo/500_350/',
                                         name_prefix='training')
# Separate evaluation env
eval_callback = EvalCallback(eval_env, best_model_save_path='./logs/logs_ppo/500_350/best_model',
                             log_path='./logs/logs_ppo/500_350/', eval_freq=1024000,
                             deterministic=True, render=False)

# Create the callback list
callback = CallbackList([checkpoint_callback, eval_callback])



policy_kwargs = dict(activation_fn=th.nn.ReLU,
                     net_arch=[500, dict(pi=[350, 63], vf=[350,100])])

model = PPO('MlpPolicy', env, policy_kwargs=policy_kwargs, tensorboard_log="./tmp/", 
             verbose=1)

model.learn(total_timesteps=2000000000, callback=callback)
model.save("ppo_ohhell_500_350")


# # Using the model
# model = PPO.load("ppo_ohhell_500_350")
# obs = env.reset()
# for _ in range(11):
#     action, _states = model.predict(obs)
#     print(env._decode_action(action))
#     obs, reward, dones, info = env.step(action)
#     print(reward)