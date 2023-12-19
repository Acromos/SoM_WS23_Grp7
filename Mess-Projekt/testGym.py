import gym
from IPython.display import clear_output
import SOMPiBrain

print("Training started.\n")
# Hide the output in the console with 'ansi' (bug)
env = gym.make("Taxi-v3", render_mode="ansi").env
# State- and Action-Space
state_num=env.observation_space.n
action_num=env.action_space.n
# Initialize the AI-class
brain=SOMPiBrain.SOMPiBrain(state_num,action_num)

# Start the game Loop
for i in range(1, 100001):
    state = env.reset()[0]
    epochs = 0
    reward = 0
    done = False
    
    while not done:
        action=brain.get_action(state)
        next_state, reward, done, newparameter, info = env.step(action) 
        state=brain.reward_action( state, next_state, action,reward)
        
        epochs += 1
    if i % 10000 == 0:
        clear_output(wait=True)
        print(f"Episode: {i}")
print("Training finished.\n")

print("Evaluate agent's performance after Q-learning.\n")
#Show the environment with 'human'
env = gym.make("Taxi-v3", render_mode="human").env

total_epochs, total_penalties = 0, 0
episodes = 10
for _ in range(episodes):
    state = env.reset()[0]
    epochs, penalties, reward = 0, 0, 0
    done = False
    
    while not done:
        action=brain.get_action(state, False)
        state, reward, done, newparameter, info = env.step(action)
        if reward == -10:
            penalties += 1
        epochs += 1
    total_penalties += penalties
    total_epochs += epochs

print(f"Results after {episodes} episodes:")
print(f"Average timesteps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")
