import random

import unittest

import rlohhell
import gym
from stable_baselines3.common.env_checker import check_env
from rlohhell.agents.random_agent import RandomAgent
from rlohhell.games.ohhell.utils import ACTION_SPACE, ACTION_LIST, cards2list

# from determism_util import is_deterministic

# class TestOhHellEnv(unittest.TestCase):


    # def test_env_functions(self):
    #     env = rlohhell.envs.ohhell.OhHellEnv2()
    #     print(env.timestep)

    # def test_reset_and_extract_state(self):
    #     env = rlohhell.make('ohhell')
    #     state, _ = env.reset()
    #     self.assertEqual(state['obs'].size, 111)
    #     for action in state['legal_actions']:
    #         self.assertLess(action, env.num_actions)

    # # def test_is_deterministic(self):
    # #     self.assertTrue(is_deterministic('ohhell'))

    # def test_get_legal_actions(self):
    #     env = rlohhell.make('ohhell')
    #     env.set_agents([RandomAgent(env.num_actions) for _ in range(env.num_players)])
    #     env.reset()
    #     legal_actions = env._get_legal_actions()
    #     for legal_action in legal_actions:
    #         self.assertLessEqual(legal_action, 63)

    # def test_decode_action(self):
    #     env = rlohhell.make('ohhell')
    #     env.reset()
    #     legal_actions = env._get_legal_actions()
    #     for legal_action in legal_actions:
    #         decoded = env._decode_action(legal_action)
    #         self.assertEqual(decoded, int(ACTION_LIST[legal_action]))

    # def test_step(self):
    #     env = rlohhell.envs.ohhell.OhHellEnv2()
    #     while env.game.is_over():
    #         action = random.choice(list(state['legal_actions']))
    #         obs, reward, done, info = env.step(action)
    #         print(reward)
            

    # def test_step_back(self):
    #     env = rlohhell.make('ohhell', config={'allow_step_back':True})
    #     _, player_id = env.reset()
    #     env.step('0')
    #     _, back_player_id = env.step_back()
    #     self.assertEqual(player_id, back_player_id)
    #     self.assertEqual(env.step_back(), False)

    #     env = rlohhell.make('ohhell')
    #     with self.assertRaises(Exception):
    #         env.step_back()

    # def test_run(self):
    #     env = rlohhell.make('ohhell')
    #     agents = [RandomAgent(env.num_actions) for _ in range(env.num_players)]
    #     env.set_agents(agents)
    #     trajectories, payoffs = env.run(is_training=False)
    #     self.assertEqual(len(trajectories), 4)
    #     total = 0
    #     for payoff in payoffs:
    #         total += payoff
    #     self.assertGreaterEqual(total, 10)

    # def test_get_perfect_information(self):
    #     env = rlohhell.make('ohhell')
    #     _, player_id = env.reset()
    #     self.assertEqual(player_id, env.get_perfect_information()['current_player'])

    # def test_multiplayers(self):
    #     env = rlohhell.make('ohhell', config={'game_num_players':3})
    #     num_players = env.game.get_num_players()
    #     self.assertEqual(num_players, 3)

if __name__ == '__main__':
    # unittest.main()
    env = rlohhell.envs.ohhell.OhHellEnv2()

    check_env(env)
    i=0
    # while not env.game.is_over():
    #     legal_actions = env.game.get_legal_actions()
    #     print(legal_actions)
    #     action = random.choice(legal_actions)
    #     obs, reward, done, info = env.step(action)
    #     print(reward)
    #     i+=1
    #     if i==25: break
    