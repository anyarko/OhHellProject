import unittest 
import numpy as np 

from rlcard.games.ohhell.game import OhHellGame as Game
from rlcard.games.ohhell.player import OhHellPlayer as Player
from rlcard.games.ohhell.utils import ACTION_LIST

class TestOhHellMethods(unittest.TestCase):

    def test_get_num_actions(self):
        game = Game()
        num_players = game.get_num_players()
        self.assertEqual(num_players, 4)

    def test_get_num_actions(self):
        game = Game()
        num_actions = game.get_num_actions()
        self.assertEqual(num_actions, 62)

    def test_init_game(self):
        game = Game()
        state, _ = game.init_game()

    def test_step(self):
        game = Game()

        # bid
        game.init_game()
        init_tricks = game.round.proposed_tricks[0]
        game.step('1')
        trick_raised = game.round.proposed_tricks[0]
        self.assertEqual(init_tricks+1, trick_raised)

        


if __name__ == '__main__':
    unittest.main() 