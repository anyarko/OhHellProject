''' An example of training a reinforcement learning agent on the environments in rlohhell
'''
import os
import argparse

import torch

import rlohhell
from rlohhell.agents import RandomAgent
from rlohhell.utils import get_device, set_seed, tournament, reorganize, Logger, plot_curve

def train(args):

    # Check whether gpu is available
    device = get_device()
        
    # Seed numpy, torch, random
    set_seed(args.seed)

    # Make the environment with seed
    env = rlohhell.make(args.env, config={'seed': args.seed})

    # Initialize the agent and use random agents as opponents
    if args.algorithm == 'dqn':
        from rlohhell.agents import DQNAgent
        agent = DQNAgent(num_actions=env.num_actions,
                         state_shape=env.state_shape[0],
                         mlp_layers=[64,64],
                         device=device)
    elif args.algorithm == 'nfsp':
        from rlohhell.agents import NFSPAgent
        agent = NFSPAgent(num_actions=env.num_actions,
                          state_shape=env.state_shape[0],
                          hidden_layers_sizes=[64,64],
                          q_mlp_layers=[64,64],
                          device=device)
    agents = [agent]
    for _ in range(env.num_players):
        agents.append(RandomAgent(num_actions=env.num_actions))
    env.set_agents(agents)

    # Start training
    with Logger(args.log_dir) as logger:
        for episode in range(args.num_episodes):

            if args.algorithm == 'nfsp':
                agents[0].sample_episode_policy()

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            # Here, we assume that DQN always plays the first position
            # and the other players play randomly (if any)
            for ts in trajectories[0]:
                agent.feed(ts)

            # Evaluate the performance. Play with random agents.
            if episode % args.evaluate_every == 0:
                logger.log_performance(env.timestep, tournament(env, args.num_eval_games)[0])

            # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path

    # Plot the learning curve
    plot_curve(csv_path, fig_path, args.algorithm)

    # Save model
    save_path = os.path.join(args.log_dir, 'model.pth')
    torch.save(agent, save_path)
    print('Model saved in', save_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("DQN/NFSP example in rlohhell")
    parser.add_argument('--env', type=str, default='leduc-holdem',
            choices=['ohhell', 'blackjack', 'leduc-holdem', 'limit-holdem', 'doudizhu', 'mahjong', 'no-limit-holdem', 'uno', 'gin-rummy'])
    parser.add_argument('--algorithm', type=str, default='dqn', choices=['dqn', 'nfsp'])
    parser.add_argument('--cuda', type=str, default='')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--num_episodes', type=int, default=5000)
    parser.add_argument('--num_eval_games', type=int, default=2000)
    parser.add_argument('--evaluate_every', type=int, default=100)
    parser.add_argument('--log_dir', type=str, default='experiments/ohhell_dqn_result/')

    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda
    train(args)

