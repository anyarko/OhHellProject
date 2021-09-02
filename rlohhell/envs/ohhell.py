import json
import os
import numpy as np
import random
from collections import OrderedDict

import rlohhell
from gym.spaces import MultiBinary, Discrete
from rlohhell.envs import Env
from rlohhell.games.ohhell import Game
from rlohhell.games.base import Card
from rlohhell.games.ohhell.utils import ACTION_SPACE, ACTION_LIST, cards2list, trumps_in_hand
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

        self.observation_space = gym.spaces.MultiBinary(350)
        self.action_space = gym.spaces.Discrete(63)

        
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
        state['previously_played_cards'] = [c.get_index() for c in self.previously_played_cards]
        state['players_tricks_proposed'] = [player.proposed_tricks for player in self.players]
        state['players_previously_played_cards'] = [player.played_cards for player in self.players]


        get_index returns suit+rank for the card for instance S2 or SA 

        we can encode the information from this and return an extracted state, the previous version is above for tips.
        '''


        obs = np.zeros(350)

        current_player = state['current_player']
        hand = state['hand']
        bid = state['proposed_tricks']
        tricks_won =  state['tricks_won']
        num_cards_left = len(hand)
        trump_suit = state['trump_card'].suit
        agent_trump_cards = trumps_in_hand(hand, trump_suit)
        num_trump_cards = len(agent_trump_cards)
        top_trump_cards = [ card for card in agent_trump_cards if rank2int(card.rank) > 9 ]
        rank_top_trump_cards = [ rank2int(card.rank) for card in agent_trump_cards if rank2int(card.rank) > 9 ]
        high_cards = [ card for card in state['hand'] if rank2int(card.rank) > 12 ]
        num_high_cards = len(high_cards)
        idx1 = list(np.array([self.card2index[card.get_index()] for card in state['hand']]) + 34)
        idx2 = list(np.array([rank2int(card.rank) for card in agent_trump_cards]) + 109)
        idx3 = list(np.array([self.card2index[card.get_index()] for card in agent_trump_cards]) + 148)
        high_cards_set = ('SA', 'SK', 'HA', 'HK', 'CA', 'CK', 'DA', 'DK')
        suits_set = ('S', 'H', 'D', 'C')
        played_cards = state['played_cards']
        num_played_cards_round = len(played_cards)
        players_tricks_won = state['players_tricks_won']
        players_tricks_proposed = state['players_tricks_proposed']
        players_previously_played_cards = state['players_previously_played_cards'] 
        previously_played_cards = state['previously_played_cards']
        idx5 = list(np.array([self.card2index[card.get_index()] for card in previously_played_cards]) + 298)

        # Encoding

        '''Section a - agent bidding
        Number of trump cards in agent's hand
        High valued trump cards (10-A) in agent's hand
        High valued cards (A/K) in agent's hand
        Agent's prediction for no. of tricks to be won'''

        # obs 0-9
        # Adding num of trump card's in player's hand
        if num_trump_cards > 0:
            obs[num_trump_cards-1] = 1
        
        # obs 10-14
        # Adding top trump cards in player's hand, cards greater than 9
        if len(rank_top_trump_cards) > 0:
            obs[rank_top_trump_cards] = 1

        # obs 15-22
        # Adding the num of aces and kings in player's hand 
        if num_high_cards > 0:
            obs[14 + num_high_cards] = 1

        # obs 23-33
        # Adding the player's estimate of tricks to win
        obs[23 + bid] = 1

        '''Section b - agent
        Map the agents cards
        Number of cards agent has played
        Agents position relative to the first hand
        Number of tricks the agent has won'''

        # obs 34-85
        # Adding player's hand using card2index file
        obs[idx1] = 1

        # obs 86-95
        # Adding the numnber of card left in the player's hand
        if num_cards_left > 0:
            obs[96 - num_cards_left] = 1

        # obs 96-99
        # Adding the position of the player in the game 
        obs[96 + num_played_cards_round] = 1

        # obs 100-110
        # Adding tricks won by player
        obs[100 + tricks_won] = 1


        '''Section c - trump cards
        Trump cards visible to agent (face card, played, in hand)'''

        # obs 111-127
        # Adding the trump card in the player's hand
        obs[idx2] = 1
        trump_suit_index = suits_set.index(trump_suit)
        obs[124 + trump_suit_index] = 1


        '''Section d - high cards
        High cards (A/K) visible to agent (face card, played, in hand)'''

        # obs 128-135
        # Adding the high cards in the player's hand
        matches = 128 + np.array([ high_cards_set.index(card.get_index()) for card in high_cards ])
        if len(matches) > 0:
            obs[matches] = 1


        '''Section e - opponents
        For each opponent [x3]
        Number of tricks bid
        Number of tricks won
        Trump cards played'''

        # obs 136-240
        # Adding opponent specfic data, bid, trump cards played, tricks won
        start_encoding_here = 136
        for opponent_id in range(self.game.num_players):
            if opponent_id == current_player:
                continue
            
            # obs 136-146
            # Adding the tricks proposed by the opponent
            obs[start_encoding_here + players_tricks_proposed[opponent_id]] = 1
            
            # obs 147-157
            # Adding the tricks won by the opponent
            obs[start_encoding_here + 10 + players_tricks_won[opponent_id]] = 1
            
            # obs 158-170
            # Adding the trumps played by the opponent
            opponents_played_trumps = trumps_in_hand(players_previously_played_cards[opponent_id], trump_suit)
            idx4 = list(np.array([rank2int(card.rank) for card in opponents_played_trumps]) + start_encoding_here + 20)
            obs[idx4] = 1
            
            # Skipping to the next part of the obs vector for a new opponent encoding
            start_encoding_here += 35



        '''Section f - previous turns
        The value and suits of up to the previous 3 hands
        Also determine whether card is the highest trump card or leading suit card played'''

        # obs 241-297
        # Adding the cards played in the round
        if num_played_cards_round > 0:
            card_1 = played_cards[0]
            obs[239 + rank2int(card_1.rank)] = 1 
            obs[254 + suits_set.index(card_1.suit)] = 1
            if trump_suit == card_1.suit:
                obs[258] = 1
            obs[259] = 1

        if num_played_cards_round > 1:
            card_2 = played_cards[1]
            obs[258 + rank2int(card_2.rank)] = 1 
            obs[273 + suits_set.index(card_2.suit)] = 1
            if trump_suit == card_2.suit:
                obs[277] = 1

        if num_played_cards_round > 2:
            card_3 = played_cards[2]
            obs[277 + rank2int(card_3.rank)] = 1 
            obs[292 + suits_set.index(card_3.suit)] = 1
            if trump_suit == card_3.suit:
                obs[296] = 1

        
        '''Section g - used
        Cards used (in hand, trump card, played)'''

        # obs 298-349
        # Adding all the card played so far in the game
        obs[idx5] = 1
            

        
        return obs

    
    def reset(self):
        ''' Start a new game

        Returns:
            (numpy.array): The begining state of the game
        '''
        state, player_id = self.game.init_game()
        self.action_recorder = []
        return self._extract_state(state)


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
        
        
        current_tricks_won = self.game.players[self.get_player_id()].tricks_won
        next_state, player_id = self.game.step(action)
        new_tricks_won = self.game.players[self.get_player_id()].tricks_won
        reward = new_tricks_won - current_tricks_won

        done = self.game.is_over()
        info = {}

        return self._extract_state(next_state), reward, done, info


    def get_player_id(self):

        return self.game.current_player


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


# if __name__ == '__main__':
#     env = OhHellEnv2()
#     print(env._decode_action(62))