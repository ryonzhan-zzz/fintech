### 美式看跌 
这段Python代码实现了使用二叉树模型对美式看跌期权进行定价，并绘制了期权的最优行权边界。以下将详细描述代码的各个部分，包括参数初始化、二叉树参数计算、资产价格树构建、期权价值计算以及可视化。 
### 1. 参数初始化 

```
def initialize_parameters():
    params = {
        'r': 0.03,  # 无风险利率
        'q': 0,  # 股息率
        'X': 1,  # 执行价格
        'sigma': 0.3,  # 波动率
        'N': 100,  # 时间步数
        'T': 1,  # 到期时间
        'S0': 1  # 初始资产价格
    }
    params['dt'] = params['T'] / params['N']  # 时间间隔
    return params
```

该函数用于初始化期权定价所需的参数，包括无风险利率 $r$、股息率 $q$、执行价格 $X$、波动率 $\sigma$、时间步数 $N$、到期时间 $T$ 和初始资产价格 $S_0$。同时，计算时间间隔 $\Delta t$，其值为到期时间 $T$ 除以时间步数 $N$。  $\Delta t = \frac{T}{N}$

### 2. 计算二叉树模型所需的参数

```
def calculate_binomial_parameters(params):
    u = np.exp(params['sigma'] * np.sqrt(params['dt']))  # 上涨因子
    d = 1 / u  # 下跌因子
    p = (np.exp((params['r'] - params['q']) * params['dt']) - d) / (u - d)  # 风险中性概率
    disc = np.exp(-params['r'] * params['dt'])  # 贴现因子
    return u, d, p, disc
```

该函数根据初始化的参数计算二叉树模型所需的参数，包括上涨因子 $u$、下跌因子 $d$、风险中性概率 $p$ 和贴现因子 $\text{disc}$。上涨因子 $u$ 由波动率 $\sigma$ 和时间间隔 $\Delta t$ 计算得出；下跌因子 $d$ 是上涨因子 $u$ 的倒数；风险中性概率 $p$ 基于无风险利率 $r$、股息率 $q$、上涨因子 $u$ 和下跌因子 $d$ 计算；贴现因子 $\text{disc}$ 由无风险利率 $r$ 和时间间隔 $\Delta t$ 计算。 
- 上涨因子： $$u = e^{\sigma\sqrt{\Delta t}}$$
- 下跌因子： $$d = \frac{1}{u}$$
- 风险中性概率： $$p = \frac{e^{(r - q)\Delta t}-d}{u - d}$$
- 贴现因子： $$\text{disc} = e^{-r\Delta t}$$ 
### 3. 构建资产价格二叉树

```
def build_price_tree(params, u, d):
    S = np.full((params['N'] + 1, params['N'] + 1), np.nan)
    S[0, 0] = params['S0']
    for i in range(1, params['N'] + 1):
        for j in range(i + 1):
            S[i, j] = params['S0'] * (u ** j) * (d ** (i - j))
    return S
```

该函数构建资产价格二叉树。首先创建一个大小为 $(N + 1) \times (N + 1)$ 的矩阵 $S$，并将初始资产价格 $S_0$ 赋值给矩阵的第一个元素 $S[0, 0]$。然后，通过双重循环计算每个节点的资产价格，节点 $(i, j)$ 的资产价格由初始资产价格 $S_0$、上涨因子 $u$ 和下跌因子 $d$ 计算得出。这里我们不用考虑会不会提前行权，只需要算出所有的s先。 
节点 $(i, j)$ 的资产价格计算公式为： $$S_{i,j} = S_0 \times u^j \times d^{i - j}$$ 其中，$i$ 表示时间步，$j$ 表示上涨的次数。 
以4步为例：
![[image-11.png]]
### 4. 计算美式看跌期权的价值

```
def calculate_option_values_put(params, S, p, disc):
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
```

该函数计算美式看跌期权的价值。和上面类似，首先创建一个大小为 $(N + 1) \times (N + 1)$ 的矩阵 $V$，这就是真实的美式期权下的数据，需要和上面没有提前行权的价格进行比较之后逐步填补即 $V_{N,j} = \max(X - S_{N,j}, 0)$。然后，从到期时间开始反向递归计算每个节点的期权价值。对于每个节点 $(i, j)$，计算继续持有价值 $\text{continuation}$ 和立即行权价值 $\text{immediate exercise}$，美式期权的价值取两者的最大值。同时，记录最优行权节点，并计算行权边界。 
到期日期权价值，此时根据题目可得$X=1$： $$V_{N,j} = \max(X - S_{N,j}, 0)$$ 继续持有价值： $$\text{continuation} = \text{disc} \times (p \times V_{i + 1, j + 1} + (1 - p) \times V_{i + 1, j})$$ 因为题目要的是算put，所以立即行权价值： $$\text{immediate exercise} = max(X - S_{i,j}, 0)$$ 美式期权价值： $$V_{i,j} = max(\text{continuation}, \text{immediate exercise})$$ 
### 5. 绘制最优行权边界的图像

```
def plot_exercise_boundary(exercise_boundary, params):
    time_steps = np.arange(0, params['N'])
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, exercise_boundary)
    plt.xlabel('Time Step')
    plt.ylabel('Optimal Exercise Boundary')
    plt.title('Optimal Exercise Boundary for American Put Option')
    plt.grid(True)
    plt.show()
```

该函数用于绘制美式看跌期权的最优行权边界图像。以时间步为横轴，行权边界为纵轴，绘制行权边界随时间的变化曲线。 

## 美式看涨
与上面唯一不同的地方在于下面这个函数，计算的逻辑会不太一样，是相反的
  
``` 
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
```  
  
该函数计算美式看涨期权的价值。首先创建一个大小为 $(N + 1) \times (N + 1)$ 的矩阵 $V$。然后，设置到期日期权价值为 $V_{N,j} = \max(S_{N,j} - X, 0)$。接着，从到期时间开始反向递归计算每个节点的期权价值。对于每个节点 $(i, j)$，计算继续持有价值 $\text{continuation}$ 和立即行权价值 $\text{immediate exercise}$，美式期权的价值取两者的最大值。同时，记录最优行权节点，并计算行权边界。 到期日期权价值： $$V_{N,j} = \max(S_{N,j} - X, 0)$$   
继续持有价值： $$\text{continuation} = \text{disc} \times (p \times V_{i + 1, j + 1} + (1 - p) \times V_{i + 1, j})$$   
立即行权价值： $$\text{immediate exercise} = \max(S_{i,j} - X, 0)$$   
美式期权价值： $$V_{i,j} = \max(\text{continuation}, \text{immediate exercise})$$