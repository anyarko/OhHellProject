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


        obs = np.zeros(350)

        current_player = state['current_player']
        hand = state['hand']
        bid = state['proposed_tricks']
        tricks_won =  state['tricks_won']
        num_cards_left = len(hand)
        trump_suit = state['trump_card'][0]
        agent_trump_cards = [ card for card in state['hand'] if trump_suit == card[0] ]
        num_trump_cards = len(agent_trump_cards)
        top_trump_cards = [ rank2int(card[1]) for card in agent_trump_cards if rank2int(card[1]) > 9 ]
        high_cards = [ card for card in state['hand'] if rank2int(card[1]) > 12 ]
        num_high_cards = len(high_cards)
        idx1 = list(np.array([self.card2index[card] for card in state['hand']]) + 43)
        idx2 = list(np.array([rank2int(card[1]) for card in agent_trump_cards]) + 107)
        idx3 = list(np.array([self.card2index[card] for card in agent_trump_cards]) + 148)
        high_cards_set = {'SA', 'SK', 'HA', 'HK', 'CA', 'CK', 'DA', 'DK'}
        suits_set = {'S', 'H', 'D', 'C'}

        # Encoding
        # obs 0-9
        # Adding num of trump card's in player's hand
        if num_trump_cards > 0:
            obs[num_trump_cards-1] = 1
        
        # obs 10-14
        # Adding top trump cards in player's hand, cards greater than 9
        if len(top_trump_cards) > 0:
            obs[top_trump_cards] = 1

        # obs 15-22
        # Adding the num of ace and kings in player's hand 
        if num_high_cards > 0:
            obs[14 + num_high_cards] = 1

        # obs 23-32
        # Adding the player's estimate of tricks to win
        if bid > 0:
            obs[22 + bid] = 1

        # obs 33-42
        # Adding tricks won by player
        if tricks_won > 0:
            obs[32 + tricks_won] = 1

        # obs 43-94
        # Adding player's hand using card2index file
        obs[idx1] = 1

        # obs 95-104
        # Adding the numnber of card left in the player's hand
        if num_cards_left > 0:
            obs[105 - no_cards_left] = 1

        # obs 105-108
        # Adding the position of the player in the game 
        obs[105 + current_player] = 1

        # obs 109-125
        # Adding the trump card in the player's hand
        obs[idx2] = 1
        trump_suit_index = suits_set.index(trump_suit)
        obs[122 + trump_suit_index] = 1

        # obs 126-133
        # Adding the high cards in the player's hand
        matches = [ high_cards_set.index(card) for card in agent_trump_cards ]
        obs[147 + np.array(matches)] = 1

        # obs 
        # Adding opponent specfic data, bid, trump cards played, tricks won
        for opponent_id in range(self.game.num_players):
            if opponent_id == current_player:
                continue

        # obs 
        # Adding the cards plaued in the round data


        # obs
        # Adding all the card played so far in the game
            
            







        
    

    
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
