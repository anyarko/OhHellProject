import json
import os
import numpy as np
import random
from collections import OrderedDict

import rlohhell
from rlohhell.envs import Env
from rlohhell.games.ohhell import Game
from rlohhell.games.base import Card
from rlohhell.games.ohhell.utils import ACTION_SPACE, ACTION_LIST, cards2list
from rlohhell.utils.utils import rank2int, int2rank


import gym
from gym.utils import seeding

class OhHellEnv2(gym.Env):


    def __init__(self):
        self.game = Game()
        self.game.init_game()
        self.seed()
        self.action_recorder = []
        self.timestep = 0

        self.observation_space = None
        self.action_space = ACTION_SPACE

        
        with open(os.path.join(rlohhell.__path__[0], 'games/ohhell/card2index.json'), 'r') as file:
            self.card2index = json.load(file)
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    
    def _extract_state(self, state):
        # obs = np.zeros((4, 4, 15), dtype=int)
        # encode_hand(obs[:3], state['hand'])
        # encode_trump_card(obs[3], state['trump_card'])
        # played_cards = state['played_cards']
        # hand = state['hand']
        # trump_card = state['trump_card']
        # tricks_won = state['tricks_won']
        # proposed_tricks = state['proposed_tricks']
        # players_tricks_won = state['players_tricks_won']
        
        # idx1 = [self.card2index[card] for card in played_cards]
        # idx2 = list(np.array([self.card2index[card] for card in hand]) + 51)
        
        # obs = np.zeros(111)
        # obs[idx1] = 1
        # obs[idx2] = 1
        # obs[104] = self.card2index[trump_card] 
        # obs[105] = tricks_won
        # obs[106] = proposed_tricks
        # obs[107:] = players_tricks_won

        
        # legal_action_id = self._get_legal_actions()
        # extracted_state = {'obs': obs, 'legal_actions': legal_action_id}


        # extracted_state['raw_obs'] = state
        # extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]
        # extracted_state['action_record'] = self.action_recorder
        # return extracted_state

        ''' get_state(player_id) is called on game and returns a dictonary with

        state['hand'] = [c.get_index() for c in players[player_id].hand]
        state['played_cards'] = [c.get_index() for c in self.played_cards]
        state['proposed_tricks'] = players[player_id].proposed_tricks
        state['tricks_won'] = players[player_id].tricks_won
        state['players_tricks_won'] = [player.tricks_won for player in players]
        state['legal_actions'] = self.get_legal_actions(players, player_id) 
        state['current_player'] = self.round.current_player
        state['trump_card'] = self.trump_card.get_index()
        state['previous_cards_played'] = [c.get_index() for c in self.previous_cards_played]


        get_index returns suit+rank for the card for instance S2 or SA 

        we can encode the information from this and return an extracted state, the previous version is above for tips.
        '''


        obs = np.zeros(404)

        trump_suit = state['trump_card'][0]
        agent_trump_cards = [ card for card in state['hand'] if trump_suit == card[0] ]
        no_trump_cards = len(agent_trump_cards)
        top_trump_cards = [ rank2int(card[1]) for card in agent_trump_cards if rank2int(card[1]) > 9 ]
        high_cards = [ card for card in state['hand'] if rank2int(card[1]) > 12 ]
        no_high_cards = len(high_cards)
        idx1 = list(np.array([self.card2index[card] for card in state['hand']]) + 44)
        idx2 = list(np.array([self.card2index[card] for card in agent_trump_cards]) + 96)
        idx3 = list(np.array([self.card2index[card] for card in agent_trump_cards]) + 148)
        high_cards_set = {'SA', 'SK', 'HA', 'HK', 'CA', 'CK', 'DA', 'DK'}

        # Encoding
        # obs 0-9
        if no_trump_cards > 0:
            obs[no_trump_cards-1] = 1
        
        # obs 10-14
        if len(top_trump_cards) > 0:
            obs[top_trump_cards] = 1

        # obs 15-24
        if no_high_cards > 0:
            obs[14 + no_high_cards] = 1

        # obs 25-34
        if state['proposed_tricks'] > 0:
            obs[24 + state['proposed_tricks']] = 1

        # obs 35-44
        if state['tricks_won'] > 0:
            obs[34 + state['tricks_won']] = 1

        # obs 44-95
        obs[idx1] = 1

        # obs 96-147
        obs[idx2] = 1

        # obs 148-155
        matches = [ high_cards_set.index(card) for card in agent_trump_cards ]
        obs[147 + np.array(matches)] = 1

        for player in self.game.num_players:
            







        
        








    
    def reset(self):
        ''' Start a new game

        Returns:
            (tuple): Tuple containing:

                (numpy.array): The begining state of the game
                (int): The begining player
        '''
        state, player_id = self.game.init_game()
        self.action_recorder = []
        return self._extract_state(state), player_id


    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if self.game.round.players_proposed == self.game.num_players:
            if action_id in list(legal_ids):
                return Card(ACTION_LIST[action_id][0], ACTION_LIST[action_id][1])
            else:
                random_card = ACTION_LIST[random.choice(list(legal_ids))]
                return Card(random_card[0], random_card[1])
        else:
            if action_id in list(legal_ids):
                return int(ACTION_LIST[action_id])
            else:
                return int(ACTION_LIST[random.choice(list(legal_ids))])

    
    def step(self, action, raw_action=False):
        ''' Step forward

        Args:
            action (int): The action taken by the current player
            raw_action (boolean): True if the action is a raw action

        Returns:
            (tuple): Tuple containing:

                (dict): The next state
                (int): The ID of the next player
        '''
        if not raw_action:
            action = self._decode_action(action)

        self.timestep += 1
        # Record the action for human interface
        self.action_recorder.append((self.get_player_id(), action))
        next_state, player_id = self.game.step(action)

        return self._extract_state(next_state), player_id


    def _get_legal_actions(self):
        ''' Get all legal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        '''
        legal_actions = self.game.get_legal_actions()
        if self.game.round.players_proposed == self.game.num_players:
            legal_ids = {ACTION_SPACE[action.get_index()]: None for action in legal_actions}
        else:
            legal_ids = {ACTION_SPACE[str(action)]: None for action in legal_actions}
        return OrderedDict(legal_ids)
