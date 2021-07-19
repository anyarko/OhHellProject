from rlohhell.utils.utils import init_standard_deck

class OhHellDealer:

    def __init__(self, np_random):
        ''' Initialize a limitholdem dealer class
        '''
        self.np_random = np_random
        self.deck = init_standard_deck()
        self.shuffle()

    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def flip_trump_card(self):
        ''' Flip trump card when a new game starts

        Returns:
            (object): The card to be used as the trump card 
        '''
        trump_card = self.deck.pop()
        return trump_card

    def deal_cards(self, player, num):
        ''' Deal some cards from deck to one player

        Args:
            player (object): The object of DoudizhuPlayer
            num (int): The number of cards to be dealed
        '''
        for _ in range(num):
            player.hand.append(self.deck.pop())

    
    def deal_card(self):
        ''' Deal one card from the deck

        Returns:
            (Card): The drawn card from the deck
        '''
        return self.deck.pop()