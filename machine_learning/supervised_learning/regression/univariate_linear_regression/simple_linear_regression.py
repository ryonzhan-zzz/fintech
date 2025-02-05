import matplotlib.pyplot as plt
import numpy as np


def generate_data():
    """
    生成一元线性回归的示例数据
    :return: 自变量 x 和因变量 y
    """
    # 定义给定的五个点
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([4, 6, 7, 10, 18])

    # 绘制原始数据点图
    plt.scatter(x, y, color='b', label='Original Data')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Original Data Points')
    plt.legend()
    plt.show()

    return x, y


def calculate_mean(data):
    """
    计算数据的均值
    :param data: 输入的数据数组
    :return: 数据的均值
    """
    return sum(data) / len(data)


def calculate_slope(x, y, x_mean, y_mean):
    """
    计算一元线性回归的斜率
    :param x: 自变量数组
    :param y: 因变量数组
    :param x_mean: 自变量的均值
    :param y_mean: 因变量的均值
    :return: 斜率
    """
    # 检查输入的 x 和 y 数组长度是否一致
    if len(x) != len(y):
        raise ValueError("输入的 x 和 y 数组长度必须相同。")

    # 初始化分子和分母的值为 0
    numerator = 0
    denominator = 0

    # 遍历 x 和 y 数组中的每个元素
    for i in range(len(x)):
        # 计算 x[i] 与 x_mean 的差值
        x_diff = x[i] - x_mean
        # 计算 y[i] 与 y_mean 的差值
        y_diff = y[i] - y_mean

        # 计算 (x[i] - x_mean) * (y[i] - y_mean) 并累加到分子上
        numerator += x_diff * y_diff
        # 通过乘法实现平方，计算 (x[i] - x_mean) ^2 并累加到分母上
        denominator += x_diff * x_diff

    # 检查分母是否为 0，如果为 0 则无法计算斜率，抛出异常
    if denominator == 0:
        raise ValueError("分母为 0，无法计算斜率。")

    # 返回斜率，即分子除以分母
    return numerator / denominator



def calculate_intercept(x_mean, y_mean, slope):
    """
    计算一元线性回归的截距
    :param x_mean: 自变量的均值
    :param y_mean: 因变量的均值
    :param slope: 斜率
    :return: 截距
    """
    return y_mean - slope * x_mean


def simple_linear_regression(x, y):
    """
    执行一元线性回归
    :param x: 自变量数组
    :param y: 因变量数组
    :return: 斜率和截距
    """
    x_mean = calculate_mean(x)
    y_mean = calculate_mean(y)
    slope = calculate_slope(x, y, x_mean, y_mean)
    intercept = calculate_intercept(x_mean, y_mean, slope)
    return slope, intercept


def predict(x, slope, intercept):
    """
    根据一元线性回归模型进行预测
    :param x: 自变量值
    :param slope: 斜率
    :param intercept: 截距
    :return: 预测的因变量值
    """
    return slope * x + intercept


def plot_regression_line(x, y, slope, intercept):
    """
    绘制原始数据点和回归直线
    :param x: 自变量数组
    :param y: 因变量数组
    :param slope: 斜率
    :param intercept: 截距
    """
    plt.scatter(x, y, color='b', label='Original Data')
    y_pred = predict(x, slope, intercept)
    plt.plot(x, y_pred, color='r', label='Regression Line')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Simple Linear Regression')
    plt.legend()
    plt.show()


def main():
    # 生成数据
    x, y = generate_data()
    # 执行线性回归
    slope, intercept = simple_linear_regression(x, y)
    print(f"斜率: {slope}")
    print(f"截距: {intercept}")
    # 绘制回归直线图
    plot_regression_line(x, y, slope, intercept)
    # 进行预测示例
    test_x = 5
    predicted_y = predict(test_x, slope, intercept)
    print(f"当 x = {test_x} 时，预测的 y 值为: {predicted_y}")


if __name__ == "__main__":
    main()