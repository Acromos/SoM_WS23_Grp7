import numpy as np
import random

# AI-class for SOM
# Q-Learning-Code based on:
# https://towardsdatascience.com/reinforcement-learning-teach-a-taxi-cab-to-drive-around-with-q-learning-9913e611028f
class SOMPiBrain(object):
    def __init__(self, state_num, action_num, alpha=0.1, gamma=0.6, epsilon=0.6): 
        self.alpha = alpha 
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros([state_num, action_num])
        self.action_num=action_num
        
    # Get the best or a random action for the current state     
    def get_action(self, state, explore=True):    
       
        if  (random.uniform(0, 1) < self.epsilon)and explore==True: 
            action = random.randint(0, self.action_num-1) # Explore action space
        else:
            action = np.argmax(self.q_table[state])%9 # Exploit learned values          
        
        return action
        
    # Reward the last action with the participating states   
    def reward_action(self, state, next_state, action, reward):
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state])
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state, action] = new_value
        
        return next_state