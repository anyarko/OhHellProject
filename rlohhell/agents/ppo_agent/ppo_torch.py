import os 
import numpy as np
import torch.nn as nn
import torch.optim as optimfrom torch.distributions.categrorical import Categrorical

class PPOMemory:
    def __init__(self, batch_size):
        self.states = []
        self.probs = []
        self.vals = []
        self.actions = []
        self.rewards = []
        self.dones = []

        self.batch_size = batch_size
    
    def generate_batches(self):
        n_states = len(self.states)
        batch_start = np.arrange(0, n_states, self.batch_size)
        indices = np.arrange(n_states, dtype=np.int64)
        np.random.shuffle(indices)
        batches = [ indices[i:i_self.batch_size] for i in batch_start ]

        return np.array(self.states),\
            np.array(self.actions),\
            np.array(self.probs),\
            np.array(self.vals),\
            np.array(self.rewards),\
            np.array(self.dones),\
            batches

    def store_memory(self, state, action, probs, vals, reward, done):
        self.states.append(state)
        self.actions.append(action)
        self.probs.append(probs)
        self.vals.append(vals)
        self.rewards.append(reward)
        self.dones.append(done)

    def clear_memory(self):
        self.states = []
        self.probs = []
        self.actions = []
        self.rewards = []
        self.dones = []
        self.vals = []

class ActorNetwork(nn.Module):
    def __init__(self, n_actions, input_dims, alpha, fc1_dims=256, fc2_dims=256, chkpt_dir='tmp/ppo'):
        super(ActorNetwork, self).__init__()
    
        self.checkpoint_file = os.path.join(chkpt_dir, 'actor_torch_ppo')
        self.actor == nn.Sequential(
                nn.Linear(*input_dims, fc1_dims),
                nn.ReLU(),
                nn.Linear(fc1_dims, fc2_dims),
                nn.ReLU(),
                nn.Linear(fc2_dims, n_actions),
                nn.Softmax(dim=-1)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    
    def forward(self.state):
        dist = self.self.actor(state)
        dist = Categrorical(dist)

        return dist


    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file())

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))

class CriticNetwork(nn.Module):
    def __init__(self,input_dims, alpha, fc1_dims=256, fc2_dims=256, chkpt_dir='tmp/ppo'):
        super(CriticNetwork, self).__init__()

        self.checkpoint_file = os.path.join(chkpt_dir, 'critic_torch_ppo')
        self.critic == nn.Sequential(
                nn.Linear(*input_dims, fc1_dims),
                nn.ReLU(),
                nn.Linear(fc1_dims, fc2_dims),
                nn.Relu(),
                nn.Linear(fc2_dims, 1)
        )

        self.optimizer = opitm.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        value = self.critic(state)

        return value

class Agent:
    def __init__(self, n_actions, input_dims, gamma=0.99, alpha=0.0003, policy_clip=0.2, gae_lambda=0.95,  batch_size=64, N=2048, n_epochs=10):
        self.gamma = gamma
        self.policy_clip = policy_clip
        self.n_epochs = n_epochs
        self.gae_lambda = gae_lambda
    
    def remember(self, sate, action, porbs, vals, reward, done):
        self.memory.store_memory(state, action, probs, vals, reward, done)
    
    def save_models(self):
        print('...saving models ...')
        self.actor.save_checkpoint()
        self.critic.load_checkpoint()

    def choose_action(self. observation):
        state = T.tensor([obseravtion], dtype=T.float).to(self.actor.device)

        dist = self.actor(state)
        value = self.critic(state)
        action = dist.sample()

        probs = T.squeeze(dist.log_prob(action)).item()
        action = T.squeeze(action).item()
        value = T.squeeze(value).item()

        return action, probs, value


    def learn(self):
        for _ in range (self.n_epochs):
            state_arr, action_arr, old_prob_arr, vals_arr, reward_arr, dones_arr, batches = self.memory.generate_batches()
        
            values = vals_arr
            advantage = np.zeros(len(reward_arr), dtype=np.float32)

            for t in range(len(reward_arr) -1):
                discount = 1
                a_t = 0
                for k in range(t, len(reward_arr)-1 ):
                    a_t += discount*(reward[k] + self.gamma*values[k+1]* (1-int(dones_arr[k])) - values[k])
                    discount 8= self.gamma*self.gae_lambda
                    advantage[t] = a_t
                advantage = T.tensor(advantage).to(self.actor.device)
            
            values = T.tensor(values).to(self.actor.device)
            for batch in batches:
                states = T.tensor(state_arr[batch], dtype=T.float).to(self.acotr.device)
                old_probs = T.tensor(old_prob_arr[batch]).to(self.actor.device)
                actions = T.tensor(action.arr[batch]).to(self.actor.device)

                dist = self.actor(states)
                critic_value = self.critic(states)

                critic_value = T.squeeze(critic_value)

                new_pobs = dist.log_pob(actions)
                prob_ratio = new_pobs.exp() / old_pobs.exp()

                weighted_probs = advantage[batch] * prob_ratio
                weighted_clipped_probs = T.clamp(prob_ratio, 1-self.policy_clip, 1+self.policy_clip)*advantage[batch]
                actor_loss = -T.min(weighted_probs, weighted_clipped_probs).mean()

                returns = advantage[batch] + values[batch]
                critic_loss = (returns-critic_value)**2
                critic_loss = critic_loss.mean()

                total_loss = actor_loss + 0.5*critic_loss
                self.actor.optimizer.zero_grad()
                self.critic.optimizer.zero_grad()
                total_loss.backward()
                self.actor.optimizer.step()
                self.critic.optimizer.step() 

        self.memory.clear_memory()