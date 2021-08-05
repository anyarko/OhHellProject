''' OhHell rule models
'''

import numpy as np
import random

import rlohhell
from rlohhell.models.model import model

class OhHellRuleAgentV1(object):
    ''' OhHell Rule agent version 1
    '''

    def __init__(self):
        self.use_raw = True

    def step(self, state):
        ''' Predict the action given raw state. A naive rule. Choose the color
            that appears least in the hand from legal actions. Try to keep wild
            cards as long as it can.

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''

        

        legal_actions = state['raw_legal_actions']

        if isinstance(random.choice(legal_actions), int):

        hand = state['hand']

        # If we have wild-4 simply play it and choose color that appears most in hand
        for action in legal_actions:
            if action.split('-')[1] == 'wild_draw_4':
                color_nums = self.count_colors(self.filter_wild(hand))
                action = max(color_nums, key=color_nums.get) + '-wild_draw_4'
                return action

        # Without wild-4, we randomly choose one
        action = np.random.choice(self.filter_wild(legal_actions))
        return action

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []


class OhHellRuleModelV1(Model):
    ''' UNO Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlohhell.make('ohhell')

        rule_agent = OhHellRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.num_players)]

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents

    @property
    def use_raw(self):
        ''' Indicate whether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True

