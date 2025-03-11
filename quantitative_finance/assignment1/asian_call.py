import numpy as np


def initialize_parameters():
    """
    初始化亚式期权定价所需的参数。

    返回:
        dict: 包含所有参数的字典。
    """
    params = {
        'S0': 100,  # 初始股票价格
        'X': 100,  # 执行价格
        'r': 0.05,  # 无风险利率
        'sigma': 0.2,  # 波动率
        'M': 252,  # 时间步数
        'T': 1,  # 到期时间（年）
        'numPaths': 100000  # 模拟路径数量
    }
    params['dt'] = params['T'] / params['M']  # 时间间隔
    return params


# 模拟股票价格路径并计算亚式期权价格的函数
def asian_call_option_price(params):
    # 初始化股票价格矩阵
    S = np.zeros((params['numPaths'], params['M'] + 1))
    S[:, 0] = params['S0']
    # 生成随机数矩阵
    randMatrix = np.random.randn(params['numPaths'], params['M'])
    # 模拟股票价格路径
    for i in range(params['M']):
        S[:, i + 1] = S[:, i] * np.exp(
            (params['r'] - 0.5 * params['sigma'] ** 2) * params['dt'] + params['sigma'] * np.sqrt(
                params['dt']) * randMatrix[:, i])
    # 计算每条路径的平均股票价格
    average_S = np.mean(S, axis=1)
    # 计算收益
    payoffs = np.maximum(average_S - params['X'], 0)
    # 计算折现因子
    discountFactor = np.exp(-params['r'] * params['T'])
    # 返回期权价格
    return discountFactor * np.mean(payoffs)


if __name__ == '__main__':
    # 调用初始化函数获取参数
    params = initialize_parameters()
    # 调用函数计算并打印亚式看涨期权价格
    price = asian_call_option_price(params)
    print(f'The price of the fixed-strike arithmetic Asian call option is: {price}')
