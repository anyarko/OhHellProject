from enum import Enum


class PlayerStatus(Enum):
    # Status based on the number of tricks proposed by the player and how many they have achieved
    NOTHING = 0
    BELOW = 1
    MET = 2
    PAST = 3



class OhHellPlayer:

    def __init__(self, player_id, np_random):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.status = PlayerStatus.NOTHING

        # The tricks that the player has proposed for the round
        self.in_tricks = 0

    
    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id

    

