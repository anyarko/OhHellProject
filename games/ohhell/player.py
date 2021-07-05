class OhHellPlayer:

    def __init__(self, player_id, np_random):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.has_proposed = False

        # The tricks that the player has proposed for the round
        self.in_tricks = 0
        self.tricks_won = 0

    
    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id

    

    def get_state(self, played_cards, proposed_tricks, trump_card, legal_actions):
        ''' Encode the state for the player

        Args:
            played_cards (list): A list of cards that have been played in the round
            proposed_tricks (int): The tricks that all players have proposed

        Returns:
            (dict): The state of the player
        '''
        state = {}
        state['hand'] = [c.get_index() for c in self.hand]
        state['played_cards'] = [c.get_index() for c in played_cards]
        state['proposed_tricks'] = proposed_tricks
        state['my_tricks'] = self.in_tricks
        state['tricks_won'] = self.tricks_won
        state['legal_actions'] = legal_actions
        state['trump_card'] = trump_card
        return state