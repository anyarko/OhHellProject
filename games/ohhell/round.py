# -*- coding: utf-8 -*-
''' Implement Oh Hell Round class
'''

import numpy as np

class OhHellRound:
    ''' Round can call other Classes' functions to keep the game running
    '''
    
    def __init__(self, round_number, num_players, np_random, dealer, last_winner=0):
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
        self.current_player = 0
        self.proposed_tricks = [0 for _ in range(self.num_players)]


    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            action (str): The action(card) choosen by the player
        '''

        if action not in self.get_legal_actions():
            raise Exception('{} is not legal action. Legal actions: {}'.format(action, self.get_legal_actions()))
        
        self.played_cards = players[self.current_player].hand.pop(action)

        self.current_player = (self.current_player + 1) % self.num_players 


    
    
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
            if not hand_same_as_starter:
                return hand_same_as_starter
            else:
                return full_list


    def is_over(self):
        ''' Check whether the round is over

        Returns:
            (boolean): True if the current round is over
        '''
        if len(self.played_cards) == self.num_players:
            return True
        return False
