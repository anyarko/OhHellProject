import unittest 
import numpy as np 

from rlcard.games.ohhell.game import OhHellGame as Game
from rlcard.games.ohhell.player import OhHellPlayer as Player
from rlcard.games.ohhell.judger import OhHellJudger as Judger
from rlcard.games.ohhell.utils import ACTION_LIST, determine_winner, int2rank

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
        init_tricks = np.array(game.round.proposed_tricks)
        game.step(1)
        game.step(1)
        game.step(1)
        game.step(1)
        proposed_tricks = game.round.proposed_tricks
        self.assertEqual(init_tricks+1, proposed_tricks)
        action = np.random.choice(game.get_legal_actions())
        state, next_player_id = game.step(action)
        current = game.round.current_player
        self.assertEqual(len(state['played_cards']), 1)
        self.assertEqual(next_player_id, current)

    def test_get_payoffs(self):
        game = Game()
        game.init_game()
        while not game.is_over():
            actions = game.get_legal_actions()
            action = np.random.choice(actions)
            state, _ = game.step(action)
        payoffs = game.get_payoffs()
        proposed_tricks = game.round.proposed_tricks
        tricks_won = [player.tricks_won for player in game.players]
        expected_payoff = [ tricks+10 for k, tricks in enumerate(tricks_won) if tricks == proposed_tricks[k] else tricks ]
        self.assertListEqual(expected_payoff, payoffs)

    def test_step_back(self):
        game = Game(allow_step_back=True)
        _, player_id = game.init_game()
        action = np.random.choice(game.get_legal_actions())
        game.step(action)
        game.step_back()
        self.assertEqual(game.round.current_player, player_id)
        self.assertEqual(len(game.history), 0)
        success = game.step_back()
        self.assertEqual(success, False)  

    def test_determine_winner(self):
        trump_card = 'D10' 
        played_cards = ['DA', 'S2', 'D3', 'H4']
        winner = determine_winner(played_cards, trump_card)
        self.assertEqual(winnner, 0)

    def test_player_get_player_id(self):
        player = Player(0, np.random.RandomState())
        self.assertEqual(0, player.get_player_id())

    
if __name__ == '__main__':
    unittest.main() 