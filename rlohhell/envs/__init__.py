''' Register new environments
'''
from rlohhell.envs.env import Env
from rlohhell.envs.registration import register, make

register(
    env_id='ohhell',
    entry_point='rlohhell.envs.ohhell:OhHellEnv',
)
