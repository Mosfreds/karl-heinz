import gym
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, LinearAnnealedPolicy
from rl.memory import SequentialMemory


ENV_NAME = 'CartPole-v0'
#ENV_NAME = 'FrozenLake-v0'
env = gym.make(ENV_NAME)
nb_actions = env.action_space.n
state_size = env.observation_space.shape[0] #env.observation_space.shape[0] #int
action_size = env.action_space.n


model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape)) #env.observation_space.shape
model.add(Dense(50, input_dim=state_size, activation='relu'))
model.add(Dense(50, activation='relu'))
#model.add(Activation('relu'))
model.add(Dense(nb_actions, activation='linear'))
#model.add(Activation('linear'))
print(model.summary())


policy = EpsGreedyQPolicy()
memory = SequentialMemory(limit=50000, window_length=1) #Sequential Memory merkt sich die Ergebnisse, der performten Aktionen
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=1000,
target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mse'])

dqn.fit(env, nb_steps=5000, visualize=True, verbose=2)

dqn.test(env, nb_episodes=5, visualize=True)
