import gym
import matplotlib.pyplot as plt
import numpy as np


class QLearningAgent:
    def __init__(self, env, gamma=0.9, learning_rate=0.1, epsilon=0.01):
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.action_n = env.action_space.n
        self.q = np.zeros((env.observation_space.n, env.action_space.n))

    def decide(self, state):
        if np.random.uniform() > self.epsilon:
            action = self.q[state].argmax()
        else:
            action = np.random.randint(self.action_n)
        return action

    def learn(self, state, action, reward, next_state, terminated, truncated):
        done = terminated or truncated  # 合并终止和截断标志
        u = reward + self.gamma * self.q[next_state].max() * (1. - done)
        td_error = u - self.q[state, action]
        self.q[state, action] += self.learning_rate * td_error


# training
# 训练函数适配新版返回值
def play_qlearning(env, agent, train=False, render=False):
    episode_reward = 0
    state, info = env.reset()  # 新版reset返回state和info
    while True:
        if render:
            env.render()
        action = agent.decide(state)
        # 新版step返回5个参数
        next_state, reward, terminated, truncated, info = env.step(action)
        episode_reward += reward
        if train:
            agent.learn(state, action, reward, next_state, terminated, truncated)
        if terminated or truncated:  # 终止或截断都结束回合
            break
        state = next_state
    return episode_reward


if __name__ == '__main__':
    # 创建新版环境（Taxi-v3在gymnasium中仍可用）
    env = gym.make('Taxi-v3')
    agent = QLearningAgent(env)

    # 训练循环保持不变
    episodes = 10000
    episode_rewards = []
    for episode in range(episodes):
        episode_reward = play_qlearning(env, agent, train=True)
        episode_rewards.append(episode_reward)

    # 可视化结果
    plt.plot(episode_rewards)
    plt.ylabel('Episode Return')
    plt.xlabel('Episode')
    plt.show()
