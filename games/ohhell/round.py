# -*- coding: utf-8 -*-
''' Implement Oh Hell Round class
'''

import numpy as np
from rlcard.games.base import Card

class OhHellRound:
    ''' Round can call other Classes' functions to keep the game running
    '''
    
    def __init__(self, round_number, num_players, np_random, dealer, last_winner=0, current_player=0):
        ''' Initilize the round class

        Args:
            round_number (int): The round number hence the max number of tricks 
            num_players (int): The number of players
            played_cards (list): The list of the cards played in the round
            trump_card (list): the card that upgrades the suit of the same kind
        '''
        self.np_random = np_random
        self.dealer = dealer
        self.played_cards = []
        self.trump_card = None
        self.round_number = round_number
        self.num_players = num_players
        self.last_winner = last_winner
        self.current_player = current_player
        self.proposed_tricks = [0 for _ in range(self.num_players)]


    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            action (str/int): The action(card) or bid choosen by the player
        '''

        if action not in self.get_legal_actions():
            raise Exception('{} is not legal action. Legal actions: {}'.format(action, self.get_legal_actions()))
        
        if isinstance(action, int):
            players[self.current_player].proposed_tricks = action
            self.proposed_tricks[self.current_player] = action
        else:
            self.played_cards.append(players[self.current_player].hand.pop(action))

        self.current_player = (self.current_player + 1) % self.num_players 

        return self.current_player

    
    
    def get_legal_actions(self, players, player_id):
        ''' Returns the list of actions possible for the player
        '''
        if players[player_id].has_proposed == False:
            players[player_id].has_proposed = True
            return list(range(1, self.round_number+1))

        full_list = players[player_id].hand

        if player_id == self.last_winner:
            return full_list
        else:
            starting_suit = self.played_cards[0][0]
            hand_same_as_starter = [card for card in players[player_id].hand if starting_suit in card]
            if hand_same_as_starter:
                return hand_same_as_starter
            else:
                return full_list

    def get_state(self, players, player_id):
        ''' Encode the state for the player

        Args:
            players (list): A list of the players
            player_id (int): The id of the player

        Returns:
            (dict): The state of the player
        '''
        state = {}
        state['hand'] = [c.get_index() for c in players[player_id].hand]
        state['played_cards'] = [c.get_index() for c in self.played_cards]
        state['proposed_tricks'] = players[player_id].proposed_tricks
        state['tricks_won'] = players[player_id].tricks_won
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        state['trump_card'] = self.trump_card
        return state

    def is_over(self):
        ''' Check whether the round is over

        Returns:
            (boolean): True if the current round is over
        '''
        if len(self.played_cards) == self.num_players:
            return True
        return False
