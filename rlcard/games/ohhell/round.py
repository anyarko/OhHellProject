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
        self.players_proposed = 0


    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            action (str/int): The action(card) or bid choosen by the player
        '''

        legal_actions = self.get_legal_actions(players, self.current_player)
        if action not in legal_actions:
            raise Exception('{} is not legal action. Legal actions: {}'.format(action, legal_actions))
        
        if isinstance(action, int):
            players[self.current_player].proposed_tricks = action
            self.proposed_tricks[self.current_player] = action
            players[self.current_player].has_proposed = True
            self.players_proposed += 1
        else:
            self.played_cards.append(action)
            players[self.current_player].hand.remove(action)

        self.current_player = (self.current_player + 1) % self.num_players 

        return self.current_player

    
    
    def get_legal_actions(self, players, player_id):
        ''' Returns the list of actions possible for the player
        '''
        if players[player_id].has_proposed == False:
            full_list = list(range(0, self.round_number+1))
            if self.players_proposed == self.num_players - 1:
                total_tricks = sum(self.proposed_tricks)
                dissallowed_bid = self.round_number - total_tricks
                if dissallowed_bid > 0 & dissallowed_bid <= self.round_number:
                    full_list.remove(dissallowed_bid)
                    return full_list
            return full_list

        full_list = players[player_id].hand

        if player_id == self.last_winner:
            return full_list
        else:
            if len(self.played_cards) == 0:
                return full_list
            starting_suit = self.played_cards[0].suit
            hand_same_as_starter = [card for card in full_list if starting_suit == card.suit ]
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
        state['players_tricks_won'] = [player.tricks_won for player in players]
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        return state

    def is_over(self):
        ''' Check whether the round is over

        Returns:
            (boolean): True if the current round is over
        '''
        if len(self.played_cards) == self.num_players:
            return True
        return False
