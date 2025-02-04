import numpy as np
import matplotlib.pyplot as plt


def generate_data():
    """
    生成一元线性回归的示例数据
    :return: 自变量 x 和因变量 y
    """
    np.random.seed(0)
    x = np.linspace(0, 10, 100)
    y = 2 * x + 1 + np.random.randn(100) * 1
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
    # 计算分子
    # 分子为 (x[i] - x_mean) * (y[i] - y_mean) 的和
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))

    # 计算分母
    # 分母为 (x[i] - x_mean) ** 2 的和
    denominator = sum((x[i] - x_mean) ** 2 for i in range(len(x)))

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