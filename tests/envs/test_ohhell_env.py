import random

import unittest
from stable_baselines3.common.env_checker import check_env


from rlohhell.envs.ohhell import OhHellEnv2
from rlohhell.games.ohhell.utils import ACTION_LIST
from rlohhell.games.base import Card

# class TestOhHellEnv(unittest.TestCase):


    # def test_reset_and_extract_state(self):
    #     env = OhHellEnv2()
    #     state = env.reset()
    #     self.assertEqual(state.size, 350)
    #     state = env.game.get_state(env.game.current_player)
    #     for key in state.keys():
    #         if isinstance(state[key], list) and state[key] and isinstance(random.choice(state[key]), Card):
    #             state[key] = [ card.get_index() for card in state[key] ]

    #     state['trump_card'] = state['trump_card'].get_index()
        

    # def test_get_legal_actions(self):
    #     env = OhHellEnv2()
    #     state = env.reset()
    #     legal_actions = env._get_legal_actions()
    #     for legal_action in legal_actions:
    #         self.assertLessEqual(legal_action, 63)

    # def test_decode_action(self):
    #     env = OhHellEnv2()
    #     state = env.reset()
    #     legal_actions = list(env._get_legal_actions())
    #     for legal_action in legal_actions:
    #         decoded = env._decode_action(legal_action)
    #         self.assertEqual(decoded, int(ACTION_LIST[legal_action]))

    # def test_step(self):
    #     env = OhHellEnv2()
    #     state = env.reset()
    #     while not env.game.is_over():
    #         action = random.choice(list(env._get_legal_actions()))
    #         obs, reward, done, info = env.step(action)

    # def test_check_env(self):
    #     env = OhHellEnv2()
    #     check_env(env)

# if __name__ == '__main__':
    # unittest.main()
