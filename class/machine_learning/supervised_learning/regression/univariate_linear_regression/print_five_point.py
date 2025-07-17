import numpy as np
import matplotlib.pyplot as plt

# 定义x和y的值
x = np.array([1, 2, 3, 4, 5])
y = np.array([4, 6, 7, 10, 18])

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 绘制散点图
plt.scatter(x, y)

# 添加标题和轴标签
plt.title('Five Points Plot')
plt.xlabel('x')
plt.xticks(rotation=45)
plt.ylabel('y')

# 显示图形
plt.show()