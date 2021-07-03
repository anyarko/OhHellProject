from copy import deepcopy, copy
import numpy as np

from rlcard.games.ohhell import Dealer
from rlcard.games.ohhell import Player
from rlcard.games.ohhell import Judger
from rlcard.games.ohhell import Round

class OhHellGame:

    def __init__(self, allow_step_back=False, num_players=4):
        ''' Initialize the class ohhell Game
        '''
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = num_players
        self.payoffs = [0 for _ in range(num_players)]


    def configure(self, game_config):
        ''' Specifiy some game specific parameters, such as number of players
        '''
        self.num_players = game_config['game_num_players']

    def init_game(self):
        ''' Initialilze the game of Oh Hell

        This version supports three-player OhHell

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
        for player in self.players:
            self.dealer.deal_cards(player, 10)

        # Initilize public cards
        self.played_cards = []

        self.round = Round(np_random= self.np_random, 
                           dealer= self.dealer,
                           num_players= self.num_players,
                           round_number= 10,
                           last_winner= self.last_winner)

        self.round.start_new_round(self.players)

        self.history = []

        state = self.get_state(self.players, self.player_id)

        # Save history of tricks won
        self.tricks_won = [0 for _ in range(self.num_players)]

        return state









    def get_state(self, player):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        proposed_tricks = [self.players[i].in_tricks for i in range(self.num_players)]

        legal_actions = self.get_legal_actions()
        state = self.players[player].get_state(self.played_cards, proposed_tricks, legal_actions)
        state['tricks_won'] = self.tricks_won
        state['current_player'] = self.round.current_player

        return state


        