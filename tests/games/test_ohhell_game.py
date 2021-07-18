import unittest 
import numpy as np 
import random

from rlcard.games.ohhell.game import OhHellGame as Game
from rlcard.games.ohhell.player import OhHellPlayer as Player
from rlcard.games.ohhell.judger import OhHellJudger as Judger
from rlcard.games.ohhell.utils import ACTION_LIST, determine_winner, int2rank
from rlcard.games.base import Card

class TestOhHellMethods(unittest.TestCase):

    def test_get_num_actions(self):
        game = Game()
        num_players = game.get_num_players()
        self.assertEqual(num_players, 4)

    def test_get_num_actions(self):
        game = Game()
        num_actions = game.get_num_actions()
        self.assertEqual(num_actions, 63)

    def test_init_game(self):
        game = Game()
        state, _ = game.init_game()
        game.proposed_tricks = [2,2,2,0]
        game.players[0].has_proposed = True
        game.players[1].has_proposed = True
        game.players[2].has_proposed = True
        game.current_player = 3
        actions = game.get_legal_actions()
        self.assertNotIn(3, actions)
        
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
        init_tricks += 1
        init_tricks = list(init_tricks)
        self.assertListEqual(init_tricks, proposed_tricks)
        action = random.choice(game.get_legal_actions())
        state, next_player_id = game.step(action)
        current = game.round.current_player
        self.assertEqual(len(state['played_cards']), 1)
        self.assertEqual(next_player_id, current)

    def test_get_payoffs(self):
        game = Game()
        game.init_game()
        while not game.is_over():
            actions = game.get_legal_actions()
            action = random.choice(actions)
            state, _ = game.step(action)
        payoffs = game.get_payoffs()
        proposed_tricks = game.round.proposed_tricks
        tricks_won = [player.tricks_won for player in game.players]
        expected_payoff = [ tricks+10 if tricks == proposed_tricks[k] else tricks for k, tricks in enumerate(tricks_won) ]
        self.assertListEqual(expected_payoff, payoffs)

    def test_step_back(self):
        game = Game(allow_step_back=True)
        _, player_id = game.init_game()
        action = random.choice(game.get_legal_actions())
        game.step(action)
        game.step_back()
        self.assertEqual(game.round.current_player, player_id)
        self.assertEqual(len(game.history), 0)
        success = game.step_back()
        self.assertEqual(success, False)  

    def test_determine_winner(self):
        trump_card = Card('D', 'T')
        played_cards = [Card('D','A'), Card('S','2'), Card('D','3'), Card('H','4')]
        winner = determine_winner(played_cards, trump_card)
        self.assertEqual(winner, 0)

    def test_player_get_player_id(self):
        player = Player(0, np.random.RandomState())
        self.assertEqual(0, player.get_player_id())

    
if __name__ == '__main__':
    unittest.main() 