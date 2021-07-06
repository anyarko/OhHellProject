from rlcard.games.ohhell.utils import determine_winner
import numpy as np

class OhHellJudger:
    ''' The Judger class for Oh Hell!
    '''
    def __init__(self, np_random):
        ''' Initialize a judger class
        '''
        self.np_random = np_random

    def judge_game(self, players, played_cards, order):
        ''' Return the winner of the game

        Args:
            players (list): The list of players who play the game
            played_cards (list): The list of cards played
            order (list): The id's of the players in the order they played
            hands (list): The list of hands that from the players
        '''

        winner = determine_winner(played_cards, trump_card)

        return order[winner]