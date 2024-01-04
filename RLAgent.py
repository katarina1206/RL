from Dog import Dog

import numpy as np
import random

#RL_training

class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.1, dog_instance=None):
        self.state_space = state_space
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.dog_instance = dog_instance  # Set the dog_instance attribute

        # Initialize Q-values as a dictionary with default values of 0
        self.q_values = {(state, action): 0 for state in state_space for action in action_space}

    def select_action(self, state):
        if state in ['vet_visit', 'sudden_illness']:
            # For decision states, choose the action with the highest Q-value
            state_actions = [(state, action) for action in ['yes', 'no']]
            q_values = {action: self.q_values[action] for action in state_actions}
            return max(q_values, key=q_values.get)
        else:
            # Explore with a certain probability, otherwise exploit the best-known action
            if np.random.rand() < self.exploration_prob:
                return np.random.choice(self.action_space)
            else:
                # Exploit the best-known action for the current state
                state_actions = [(state, action) for action in self.action_space]
                q_values = {action: self.q_values[action] for action in state_actions}
                #return max(q_values, key=q_values.get)
                return max(q_values, key=q_values.get)[1]

    def update_q_values(self, state, action, next_state):
        # Q-value update formula: Q(s, a) = Q(s, a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))
        current_q_value = self.q_values[(state, action)]

        # Calculate the immediate reward
        immediate_reward = self.dog_instance.calculate_reward(action, next_state)

        # Estimate the future reward using the maximum Q-value for the next state
        max_future_q_value = max([self.q_values[(next_state, a)] for a in self.action_space])

        # Update the Q-value
        new_q_value = current_q_value + self.learning_rate * (immediate_reward + self.discount_factor * max_future_q_value - current_q_value)
        self.q_values[(state, action)] = new_q_value

    def print_q_values(self):
        for state in self.state_space:
            for action in self.action_space:
                print(f"Q({state}, {action}) = {self.q_values[(state, action)]}")

# Add other necessary imports and define your state and action space in the Dog class
# ...
        
# Create an instance of the Dog class
#my_dog = Dog()

# Create an instance of the QLearningAgent and pass the dog_instance
#rl_agent = QLearningAgent(state_space=["normal", "vet_visit", "sudden_illness", "flea_event"],
#                          action_space=["feed", "walk", "play", "sleep", "groom", "socialise", "flea treatment"],
#                          dog_instance=my_dog)