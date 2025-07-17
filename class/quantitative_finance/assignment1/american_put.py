import matplotlib.pyplot as plt
import numpy as np


def initialize_parameters():
    """
    初始化期权定价所需的参数。

    返回:
        dict: 包含所有参数的字典。
    """
    params = {
        'r': 0.03,  # 无风险利率
        'q': 0,  # 股息率
        'X': 1,  # 执行价格
        'sigma': 0.3,  # 波动率
        'N': 3000,  # 时间步数
        'T': 1,  # 到期时间
        'S0': 1  # 初始资产价格
    }
    params['dt'] = params['T'] / params['N']  # 时间间隔
    return params


def calculate_binomial_parameters(params):
    """
    计算二叉树模型所需的参数。

    参数:
        params (dict): 包含期权定价参数的字典。

    返回:
        tuple: (上涨因子, 下跌因子, 风险中性概率, 贴现因子)
    """
    u = np.exp(params['sigma'] * np.sqrt(params['dt']))  # 上涨因子
    d = 1 / u  # 下跌因子
    p = (np.exp((params['r'] - params['q']) * params['dt']) - d) / (u - d)  # 风险中性概率
    disc = np.exp(-params['r'] * params['dt'])  # 贴现因子
    return u, d, p, disc


def build_price_tree(params, u, d):
    """
    构建资产价格二叉树。

    参数:
        params (dict): 包含期权定价参数的字典。
        u (float): 上涨因子。
        d (float): 下跌因子。

    返回:
        np.ndarray: 资产价格二叉树矩阵。
    """
    S = np.full((params['N'] + 1, params['N'] + 1), np.nan)
    S[0, 0] = params['S0']
    for i in range(1, params['N'] + 1):
        for j in range(i + 1):
            S[i, j] = params['S0'] * (u ** j) * (d ** (i - j))
    return S


def calculate_option_values_put(params, S, p, disc):
    """
    计算美式看跌期权的价值。

    参数:
        params (dict): 包含期权定价参数的字典。
        S (np.ndarray): 资产价格二叉树矩阵。
        p (float): 风险中性概率。
        disc (float): 贴现因子。

    返回:
        tuple: (期权价值矩阵, 行权边界)
    """
    V = np.full((params['N'] + 1, params['N'] + 1), np.nan)
    # 设置到期日期权价值
    for j in range(params['N'] + 1):
        V[params['N'], j] = max(params['X'] - S[params['N'], j], 0)

    exercise_boundary = np.full(params['N'], np.nan)
    for i in range(params['N'] - 1, -1, -1):
        exercise_indices = []
        for j in range(i + 1):
            # 继续持有价值
            continuation = disc * (p * V[i + 1, j + 1] + (1 - p) * V[i + 1, j])
            # 立即行权价值
            immediate_exercise = max(params['X'] - S[i, j], 0)
            # 美式期权取最大值
            V[i, j] = max(continuation, immediate_exercise)
            # 记录最优行权节点
            if immediate_exercise >= continuation:
                exercise_indices.append(j)
        # 记录行权边界
        if exercise_indices:
            max_index = max(exercise_indices)
            exercise_boundary[i] = S[i, max_index]
    return V, exercise_boundary


def calculate_option_values_call(params, S, p, disc):
    V = np.full((params['N'] + 1, params['N'] + 1), np.nan)
    # 设置到期日期权价值
    for j in range(params['N'] + 1):
        V[params['N'], j] = max(S[params['N'], j] - params['X'], 0)

    exercise_boundary = np.full(params['N'], np.nan)
    for i in range(params['N'] - 1, -1, -1):
        exercise_indices = []
        for j in range(i + 1):
            # 继续持有价值
            continuation = disc * (p * V[i + 1, j + 1] + (1 - p) * V[i + 1, j])
            # 立即行权价值
            immediate_exercise = max(S[i, j] - params['X'], 0)
            # 美式期权取最大值
            V[i, j] = max(continuation, immediate_exercise)
            # 记录最优行权节点
            if immediate_exercise >= continuation:
                exercise_indices.append(j)
                # 记录行权边界
        if exercise_indices:
            max_index = max(exercise_indices)
            exercise_boundary[i] = S[i, max_index]
    return V, exercise_boundary


def plot_exercise_boundary(exercise_boundary, params):
    """
    绘制最优行权边界的图像。

    参数:
        exercise_boundary (np.ndarray): 行权边界数组。
        params (dict): 包含期权定价参数的字典。
    """
    time_steps = np.arange(0, params['N'])
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, exercise_boundary)
    plt.xlabel('Time Step')
    plt.ylabel('Optimal Exercise Boundary')
    plt.title('Optimal Exercise Boundary for American Option')
    plt.grid(True)
    plt.show()


# 主程序
if __name__ == "__main__":
    option = "put"
    # 初始化参数
    params = initialize_parameters()
    # 计算二叉树参数
    u, d, p, disc = calculate_binomial_parameters(params)
    # 构建资产价格二叉树
    S = build_price_tree(params, u, d)
    # 计算期权价值
    if option == "put":
        V, exercise_boundary = calculate_option_values_put(params, S, p, disc)
    else:
        V, exercise_boundary = calculate_option_values_call(params, S, p, disc)
    # 输出最终期权价格
    print(f"美式{option}期权价格: {V[0, 0]:.4f}")
    # 绘制最优行权边界图像
    plot_exercise_boundary(exercise_boundary, params)
