import os
import json
import numpy as np
from collections import OrderedDict


from rlcard.utils.utils import rank2int

class Hand:
    def __init__(self, cards_left):
        self.cards_left = cards_left  # The set of cards not played yet
        

        self.RANK_TO_STRING = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6",
                               7: "7", 8: "8", 9: "9", 10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}
        self.STRING_TO_RANK = {v:k for k, v in self.RANK_TO_STRING.items()}
        self.RANK_LOOKUP = "23456789TJQKA"
        self.SUIT_LOOKUP = "SCDH"


    def _sort_cards(self):
        '''
        Sort all the seven cards ascendingly according to RANK_LOOKUP
        '''
        self.cards_left = sorted(
            self.cards_left, key=lambda card: self.RANK_LOOKUP.index(card[1]))


def determine_winner(played_cards, trump_card):
    '''
    Return the index of the player that wins in that round

    trump_card (list): A list of just one card 
    played_cards (list): A list of cards played in the round so far
    '''


    trump_suit = trump_card[0][0]
    first_suit = played_cards[0][0]
    
    trump_cards_played = [rank2int(k) for v,k in played_cards if trump_suit == v]
    same_as_first_suit = [rank2int(k) for v,k in played_cards if first_suit == v]

    if trump_cards_played:
        highest = max(trump_cards_played)
        return played_cards.index(trump_suit + highest)
    else:
        highest = max(same_as_first_suit)
        return played_cards.index(first_suit + highest)
        
        




