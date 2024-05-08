import gym
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np

from setuptools import setup


class TwohoirzontalcartEnv_chen(Env):
    def __init__(self):
        # Actions we can take, down, stay, up
        self.action_space = Box(low=np.array([-100]), high=np.array([100]), shape=(1,))
        # Temperature array
        self.observation_space = Box(low=np.array([-100, -100]), high=np.array([100, 100]), shape=(2,))
        # Set start temp
        self.state = np.zeros((2,))
        # Set shower length
        self.shower_length = 60

        self.A = np.array([[0, 1],
                           [-1, -0.2]])
        self.B = np.array([[0],
                           [1]])

    def step(self, action):
        # Compute the next state
        u = np.array([action])
        xdot = np.dot(self.A, self.state) + np.dot(self.B, u)
        self.state = xdot  # * 0.01  # Euler integration with time step of 0.01

        # Define reward and done condition (example)
        reward = -np.sum(self.state ** 2)  # penalize large states
        done = False  # let's say the episode never ends automatically

        return self.state, reward, done, {}

    def reset(self):
        # Reset the state to a random value within some bounds
        self.state = np.zeros((2,))
        return self.state

    def render(self, mode='human'):
        # This is just an example; customize based on visualization requirements
        print(f"Current State: {self.state}")

""" 
setup(
    name="gym_examples",
    version="0.0.1",
    install_requires=["gymnasium==0.26.0"],
)
 """
# Now you can use gym.make to create your environment
#my_env = gym.make('TwohoirzontalcartEnv_chen-v0')

"""env2 = gym.make('CartPole-v0')
print('d') """

""" env = TwohoirzontalcartEnv_chen()
state = env.reset()
for _ in range(100):
    action = env.action_space.sample()  # Sample random action
    state, reward, done, info = env.step(action)
    env.render() """