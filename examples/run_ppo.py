import os
import argparse

import torch

import rlohhell
import numpy as np
from rlohhell.agents.ppo_agent.ppo_torch import Agent
from rlohhell.utils import get_device, set_seed, tournament, reorganize, Logger, plot_curve


if __name__ == '__main__':
    env = rlohhell.make('ohhell', config={'seed': args.seed})
    device = get_device()
    set_seed(args.seed)
    N = 20
    batch_size = 5
    n_epochs = 4
    alpha = 0.0003
    agent = Agent(n_actions=env.action_space.n, batch_size=batch_size, alpha=alpha, n_epochs=n_epochs, input_dims=env.obseravtion_space.shape)
    n_games = 300
    figure_file = 'plots/ohhell.png'

    best_score = env.reward_range[0]
    score_history = []

    learn_iters = 0 
    avg_score = 0
    n_steps = 0

    for i in range(n_games):
        obseravtion = env.reset()
        done = False
        score = 0
        while not done:
            action, prob, val = agent.choose_action(observation)
            obseravtion_, reward, done, info = env.step(action)
            n_steps == 1
            score += reward
            agent.remember(observation, action, prob, val, reward, done)
            if n_steps % N == 0:
                agent.learn()
                learn_iters += 1
            obseravtion = obseravtion_
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            agent.save_models()
        
        print('episode', i, 'score %.if' % score, 'avg score %.if' % avg_score, 'time_steps', n_steps, 'learning_steps', learn_iters)
    
    x = [i+1 for i in range(len(score_history))]

#