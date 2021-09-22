from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env
import torch as th

from rlohhell.envs.ohhell import OhHellEnv2



env = OhHellEnv2()
check_env(env)
env = make_vec_env(OhHellEnv2)

policy_kwargs = dict(activation_fn=th.nn.ReLU,
                     net_arch=[500, dict(pi=[350, 63], vf=[350,100])])

model = PPO('MlpPolicy', env, policy_kwargs=policy_kwargs, tensorboard_log="./tmp/", verbose=1)

model.learn(total_timesteps=5000000)
model.save("ppo_ohhell_500_350")


# # Using the model
# model = PPO.load("ppo_ohhell_700_350")
# obs = env.reset()
# for _ in range(11):
#     action, _states = model.predict(obs)
#     print(env._decode_action(action))
#     obs, reward, dones, info = env.step(action)
#     print(reward)