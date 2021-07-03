class OhHellPlayer:

    def __init__(self, player_id, np_random):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []

        # The tricks that the player has proposed for the round
        self.in_tricks = 0

    
    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id

    

    def get_state(self, played_cards, proposed_tricks, legal_actions):
        ''' Encode the state for the player

        Args:
            public_cards (list): A list of public cards that seen by all the players
            all_chips (int): The chips that all players have put in

        Returns:
            (dict): The state of the player
        '''
        state = {}
        state['hand'] = [c.get_index() for c in self.hand]
        state['public_cards'] = [c.get_index() for c in played_cards]
        state['proposed_tricks'] = proposed_tricks
        state['my_tricks'] = self.in_tricks
        state['legal_actions'] = legal_actions
        return state