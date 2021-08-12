from copy import deepcopy, copy
import numpy as np
import random

from rlohhell.games.ohhell import Dealer
from rlohhell.games.ohhell import Player
from rlohhell.games.ohhell import Judger
from rlohhell.games.ohhell import Round


class OhHellGame:

    def __init__(self, allow_step_back=False, num_players=4):
        ''' Initialize the class ohhell Game
        '''
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = num_players
        self.payoffs = [0 for _ in range(num_players)]
        self.current_player = random.randint(0, self.num_players-1)


    def configure(self, game_config):
        ''' Specifiy some game specific parameters, such as number of players
        '''
        self.num_players = game_config['game_num_players']

    def init_game(self):
        ''' Initialilze the game of Oh Hell

        This version supports up to four-player OhHell

        Returns:
            (tuple): Tuple containing:

                (dict): The first state of the game
                (int): Current player's id
        '''
        # Initilize a dealer that can deal cards
        self.dealer = Dealer(self.np_random)

        # Initilize four players to play the game
        self.players = [Player(i, self.np_random) for i in range(self.num_players)]

        # Initialize a judger class which will decide who wins in the end
        self.judger = Judger(self.np_random)

        # Deal cards to each player to prepare for the round
        for i in range(10 * self.num_players):
            self.players[i % self.num_players].hand.append(self.dealer.deal_card())


        self.trump_card = self.dealer.flip_trump_card()

        # Initilize public cards
        self.played_cards = []

        self.round = Round(np_random= self.np_random, 
                           dealer= self.dealer,
                           num_players= self.num_players,
                           round_number= 10,
                           last_winner= self.current_player,
                           current_player= self.current_player)

        # Count the round. There are 10 rounds in each game.
        self.round_counter = 0

        self.history = []


        # Save history of players that won
        self.last_winner = 0

        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id



    def step(self, action):
        ''' Get the next state

        Args:
            action (str): A specific action

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        '''

        if self.allow_step_back:
            # First snapshot the current state
            r = deepcopy(self.round)
            b = self.round.current_player
            r_c = self.round_counter
            d = deepcopy(self.dealer)
            p = deepcopy(self.played_cards)
            ps = deepcopy(self.players)
            lw = copy(self.last_winner)
            self.history.append((r, b, r_c, d, p, ps, lw))

        # Then we proceed to the next round
        self.current_player = self.round.proceed_round(self.players, action)
        self.played_cards = self.round.played_cards
        
        # If a round is over, we refresh the played cards
        if self.round.is_over():
            self.last_winner = (self.round.last_winner + self.judger.judge_round(self.round.played_cards, self.trump_card)) % self.num_players
            self.round.last_winner = self.last_winner
            self.current_player = self.last_winner
            self.round.current_player = self.last_winner
            self.players[self.last_winner].tricks_won += 1
            self.played_cards = []
            self.round.played_cards = []
            self.round_counter += 1




        state = self.get_state(self.current_player)

        return state, self.current_player


    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''

        state = self.round.get_state(self.players, player_id)
        state['current_player'] = self.round.current_player
        state['trump_card'] = self.trump_card.get_index()
        return state

    
    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if len(self.history) > 0:
            self.round, self.current_player, self.round_counter, self.dealer, self.played_cards, self.players, self.history_winners = self.history.pop()
            return True
        return False
    
    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.current_player

    
    def get_num_players(self):
        ''' Return the number of players in Oh Hell

        Returns:
            (int): The number of players in the game
        '''
        return self.num_players

    
    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''

        # If all rounds are finshed
        if self.round_counter >= 10:
            return True
        return False

    def get_payoffs(self):
        ''' Return the scores of the players

        Returns:
            (list): The final scores of the players
        '''
        return self.judger.judge_game(self.players)
    

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''
        return self.round.get_legal_actions(self.players, self.round.current_player)

    @staticmethod
    def get_num_actions():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. There are at most 63 possible actions.
        '''
        return 63

    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.round.current_player

