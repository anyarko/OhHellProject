import json
import os
import numpy as np
from collections import OrderedDict

import rlcard
from rlcard.envs import Env
from rlcard.games.ohhell import Game
from rlcard.games.ohhell.utils import ACTION_SPACE, ACTION_LIST
from rlcard.games.ohhell.utils import cards2list

DEFAULT_GAME_CONFIG = {
        'game_num_players': 4,
        }

class OhHellEnv(Env):
    ''' OhHell Environment
    '''

    def __init__(self, config):
        ''' Initialize the Limitholdem environment
        '''
        self.name = 'ohhell'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.state_shape = [[107] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

        with open(os.path.join(rlcard.__path__[0], 'games/ohhell/card2index.json'), 'r') as file:
            self.card2index = json.load(file)


    def _extract_state(self, state):
        # obs = np.zeros((4, 4, 15), dtype=int)
        # encode_hand(obs[:3], state['hand'])
        # encode_trump_card(obs[3], state['trump_card'])
        played_cards = state['played_cards']
        hand = state['hand']
        trump_card = state['trump_card']
        tricks_won = state['tricks_won']
        proposed_tricks = state['proposed_tricks']
        
        idx1 = [self.card2index[card] for card in played_cards]
        idx2 = np.array([self.card2index[card] for card in hand]) + 51
        
        obs = np.zeros(107)
        obs[idx1] = 1
        obs[idx2] = 1
        obs[104] = self.card2index[trump_card] 
        obs[105] = tricks_won
        obs[106] = proposed_tricks

        
        legal_action_id = self._get_legal_actions()
        extracted_state = {'obs': obs, 'legal_actions': legal_action_id}


        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]
        extracted_state['action_record'] = self.action_recorder
        return extracted_state



    def _get_legal_actions(self):
        ''' Get all legal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        '''
        legal_actions = self.game.get_legal_actions()
        legal_ids = {ACTION_SPACE[action]: None for action in legal_actions}
        return OrderedDict(legal_ids)

    def get_payoffs(self):
        ''' Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        '''
        return self.game.get_payoffs()

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return ACTION_LIST[action_id]
        # if (len(self.game.dealer.deck) + len(self.game.round.played_cards)) > 17:
        #    return ACTION_LIST[60]
        return ACTION_LIST[np.random.choice(legal_ids)]

    def get_perfect_information(self):
        ''' Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        state['tricks_won'] = [self.game.players[i].tricks_won for i in range(self.num_players)]
        state['trump_card'] = self.game.trump_card
        state['played_cards'] = cards2list(self.game.round.played_cards)
        state['hand_cards'] = [[c.get_index() for c in self.game.players[i].hand] for i in range(self.num_players)]
        state['current_player'] = self.game.current_player
        state['legal_actions'] = self.game.get_legal_actions()
        return state
