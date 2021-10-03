class OhHellPlayer:

    def __init__(self, player_id, np_random):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.np_random = np_random
        
        # The unique identifier of the player in the game and environment
        self.player_id = player_id
        
        # The cards the player hasn't used 
        self.hand = []

        # The cards the player has used
        self.played_cards = []

        # Whether or not the player has bid a number of tricks
        self.has_proposed = False

        # During training all but one of the players will be kept as 'Trained'
        # as their actions are from previously trained models
        self.name = 'Trained'

        # The tricks that the player has proposed for the round
        self.proposed_tricks = 0
    
        # The tricks won by the player
        self.tricks_won = 0

        # During training this will increase everytime the agent selects an action
        # that wasn't avaiable
        self.wrong_actions_chosen = 0

    
    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id

    