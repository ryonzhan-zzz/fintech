import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义给定的数据点
x = np.array([1, 2, 3, 4, 5])
y = np.array([4, 6, 7, 10, 18])

# 初始化参数
b = 0  # 截距
k = 0  # 斜率
alpha = 0.01  # 学习率
num_iters = 1000  # 迭代次数


# 定义梯度下降函数
def gradient_descent(x, y, b, k, alpha, num_iters):
    m = len(y)  # 样本数量
    b_history = []
    k_history = []
    for i in range(num_iters):
        # 计算预测值
        h = b + k * x
        # 计算误差
        error_b = h - y
        error_k = (h - y) * x
        # 更新参数
        b = b - alpha * (1 / m) * np.sum(error_b)
        k = k - alpha * (1 / m) * np.sum(error_k)
        if i % 200 == 0:
            b_history.append(b)
            k_history.append(k)
    return b, k, b_history, k_history


# 定义均方误差损失函数
def mse_loss(x, y, b, k):
    m = len(y)
    h = b + k * x
    return np.sum((h - y) ** 2) / (2 * m)


# 执行梯度下降
b, k, b_history, k_history = gradient_descent(x, y, b, k, alpha, num_iters)

# 生成 b 和 k 的网格，扩大范围以展示完整曲面
b_grid = np.linspace(-10, 10, 100)
k_grid = np.linspace(-10, 10, 100)
B, K = np.meshgrid(b_grid, k_grid)
Z = np.zeros_like(B)
for i in range(B.shape[0]):
    for j in range(B.shape[1]):
        Z[i, j] = mse_loss(x, y, B[i, j], K[i, j])

# 计算梯度下降过程中的损失值
loss_history = [mse_loss(x, y, b, k) for b, k in zip(b_history, k_history)]

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 创建 3D 图形
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='3d')

# 绘制损失函数曲面
surf = ax.plot_surface(B, K, Z, cmap='viridis', alpha=0.8)
fig.colorbar(surf, shrink=0.5, aspect=5)

# 绘制梯度下降路径，增大点的大小
ax.plot(b_history, k_history, loss_history, 'r-o', markersize=5, label='Gradient Descent Path')

# 设置标题和轴标签
ax.set_title('Gradient Descent in 3D (MSE Loss)')
ax.set_xlabel('Intercept (b)')
ax.set_ylabel('Slope (k)')
ax.set_zlabel('Loss')
ax.legend()

# 显示图形
plt.show()