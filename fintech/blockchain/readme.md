# 理论
## 代码解析
[代码解析文档](code.md)

tips：看看就好，真了解还得看实操

# 实操
## 环境安装
### 下载相应的环境
![img_31.png](../../.README_images/img_31.png)
找到上图的地方，打开命令行，输入并执行：`conda create -n blockchain python=3.10`

### 确认
![img_32.png](../../.README_images/img_32.png)
输入`y`以确认创建环境

### 激活环境
环境创建完成后，需要对环境进行激活，继续在命令行执行：`conda activate blockchain`
![img_33.png](../../.README_images/img_33.png)

### 配置使用的包
![img_23.png](../../.README_images/img_23.png)
![img_28.png](../../.README_images/img_28.png)
![img_37.png](../../.README_images/img_37.png)

### 安装需要的依赖包
1. 在命令行执行：`pip install flask`
2. 下图就是安装成功的显示
![img_35.png](../../.README_images/img_35.png)
3. 在命令行执行：`pip install requests`
4. 下图就是安装成功的显示
![img_38.png](../../.README_images/img_38.png)

## 运行
1. 执行
- 在命令行执行：`python ./code/app_flask.py`
- 或者找到app_flask文件后点击右上角的执行按钮进行执行![img.png](../../.README_images/img42.png)
看到下面这个就证明运行成功了，服务已经启动
![img_39.png](../../.README_images/img_39.png)

2. 访问`http://localhost:5000/`
，进行相关操作
![img_40.png](../../.README_images/img_40.png)

3. 如果想要退出
![img_41.png](../../.README_images/img_41.png)