import numpy as np


class BernoulliBandit:
    """ 伯努利多臂老虎机,输入K表示拉杆个数 """

    def __init__(self, K):
        self.probs = np.random.uniform(size=K)  # 随机生成K个0～1的数,作为拉动每根拉杆的获奖
        # 概率
        self.best_idx = np.argmax(self.probs)  # 获奖概率最大的拉杆
        self.best_prob = self.probs[self.best_idx]  # 最大的获奖概率
        self.K = K

    def step(self, k):
        # 当玩家选择了k号拉杆后,根据拉动该老虎机的k号拉杆获得奖励的概率返回1（获奖）或0（未获奖）
        if np.random.rand() < self.probs[k]:
            return 1
        else:
            return 0


class Solver:
    """ 多臂老虎机算法基本框架 """

    def __init__(self, bandit):
        self.bandit = bandit
        # 每根拉杆的尝试次数
        self.counts = np.zeros(self.bandit.K)
        # 当前步的累积懊悔
        self.regret = 0.
        # 维护一个列表，记录每一步的动作
        self.actions = []
        # 维护一个列表，记录每一步的累积懊悔
        self.regrets = []

    def update_regret(self, k):
        """
        计算累积懊悔并保存，k为本次动作选择的拉杆的编号
        """
        self.regret += self.bandit.best_prob - self.bandit.probs[k]
        self.regrets.append(self.regret)

    def run_one_step(self):
        """
        返回当前动作选择哪一根拉杆，由每个具体的策略实现
        """
        raise NotImplementedError

    def run(self, num_steps):
        """
        运行一定次数，num_steps为总运行次数
        """
        for _ in range(num_steps):
            k = self.run_one_step()
            self.counts[k] += 1
            self.actions.append(k)
            self.update_regret(k)


if __name__ == '__main__':
    b = BernoulliBandit(3)
    s = Solver(b)
    s.run(10000)
