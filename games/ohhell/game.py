from copy import deepcopy, copy
import numpy as np

from rlcard.games.ohhell import Dealer
from rlcard.games.ohhell import Player, PlayerStatus
from rlcard.games.ohhell import Judger
from rlcard.games.ohhell import Round

class OhHellGame:

    def __init__(self, allow_step_back=False, num_players=3):
        ''' Initialize the class ohhell Game
        '''
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = num_players
        self.history_tricks = [0 for _ in range(num_players)]


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

        # Initilize two players to play the game
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
                           played_cards= self.played_cards,
                           trump_card= self.trump_card,
                           num_players= self.num_players,
                           round_number= 10,
                           current_player= self.current_player,
                           last_winner= self.last_winner)
        




        self.round.start_new_round(self.players)

        self.round_counter = 0

        self.history = []

        state = self.get_state(self.players, self.player_id)

        return state




        