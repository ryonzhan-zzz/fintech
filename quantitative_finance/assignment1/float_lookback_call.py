import numpy as np


def initialize_parameters():
    """
    初始化期权定价所需的参数。

    返回:
        dict: 包含所有参数的字典。
    """
    params = {
        'S0': 100,  # 初始资产价格
        'r': 0.05,  # 无风险利率
        'sigma': 0.2,  # 波动率
        'T': 1,  # 到期时间
        'N': 50  # 时间步数
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
    d = np.exp(-params['sigma'] * np.sqrt(params['dt']))  # 下跌因子
    p = (np.exp(params['r'] * params['dt']) - d) / (u - d)  # 风险中性概率
    discount = np.exp(-params['r'] * params['dt'])  # 贴现因子
    return u, d, p, discount


def initialize_value_matrix(params):
    """
    初始化期权价值矩阵，并设置终端条件。

    参数:
        params (dict): 包含期权定价参数的字典。

    返回:
        np.ndarray: 初始化后的期权价值矩阵。
    """
    W = np.zeros((params['N'] + 1, params['N'] + 1))
    # 终端条件 w(x,T) = 1 - x = 1 - d^j
    for j in range(params['N'] + 1):
        W[params['N'], j] = 1 - params['d'] ** j
    return W


def backward_induction(W, params, u, d, p, discount):
    """
    进行逆向推导，计算期权在每个时间步的价值。

    参数:
        W (np.ndarray): 期权价值矩阵。
        params (dict): 包含期权定价参数的字典。
        u (float): 上涨因子。
        d (float): 下跌因子。
        p (float): 风险中性概率。
        discount (float): 贴现因子。

    返回:
        np.ndarray: 计算完成后的期权价值矩阵。
    """
    for n in range(params['N'] - 1, -1, -1):
        for j in range(n + 1):
            if j == 0:
                W[n, j] = discount * (p * u * W[n + 1, j + 1] + (1 - p) * d * W[n + 1, j])
            else:
                W[n, j] = discount * (p * u * W[n + 1, j + 1] + (1 - p) * d * W[n + 1, j - 1])
    return W


# 主程序
if __name__ == "__main__":
    # 初始化参数
    params = initialize_parameters()
    # 计算二叉树参数
    u, d, p, discount = calculate_binomial_parameters(params)
    params['u'] = u
    params['d'] = d
    # 初始化期权价值矩阵
    W = initialize_value_matrix(params)
    # 进行逆向推导
    W = backward_induction(W, params, u, d, p, discount)
    # 计算期权价格
    price = params['S0'] * W[0, 0]
    print(f'The price of the floating - strike lookback call is: {price}')
