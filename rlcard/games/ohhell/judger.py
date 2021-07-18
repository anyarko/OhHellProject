from rlcard.games.ohhell.utils import determine_winner

class OhHellJudger:
    ''' The Judger class for Oh Hell!
    '''
    def __init__(self, np_random):
        ''' Initialize a judger class
        '''
        self.np_random = np_random

    def judge_round(self, played_cards, trump_card):
        ''' Return the winner of the game

        Args:
            players (list): The list of players who play the game
            played_cards (list): The list of cards played
            trump_card (card): The trump card for the game
        '''

        winner = determine_winner(played_cards, trump_card)

        return winner



    def judge_game(self, players):
        ''' Return the winner of the game

        Args:
            players (list): The list of players who play the game
        '''

        for player in players:
            if player.tricks_won == player.proposed_tricks:
                player.tricks_won += 10

        final_scores = [player.tricks_won for player in players]

        return final_scores
