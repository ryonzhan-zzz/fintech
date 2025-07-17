import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import sklearn.preprocessing
import torch
import torch.nn as nn

df = pd.read_csv('prices-split-adjusted.csv')
valid_set_size_percentage = 10
test_set_size_percentage = 10


def normalize_data(df):
    min_max_scaler = sklearn.preprocessing.MinMaxScaler()
    # YOUR TASK: Try your best to fill this part!
    # hint: MinMaxScaler.fit_transform() expects 2D array-like input, but pandas Series/numpy arrays are 1D by default, so reshaping is needed
    df['open'] = min_max_scaler.fit_transform(df['open'].values.reshape(-1, 1))
    df['close'] = min_max_scaler.fit_transform(df['close'].values.reshape(-1, 1))
    df['low'] = min_max_scaler.fit_transform(df['low'].values.reshape(-1, 1))
    df['high'] = min_max_scaler.fit_transform(df['high'].values.reshape(-1, 1))
    return df


# function to create train, validation, test data given stock data and sequence length
def load_data(stock, seq_len):
    data_raw = np.array(stock)  # convert to numpy array
    data_sequences = []
    for i in range(len(data_raw) - seq_len + 1):
        data_sequences.append(data_raw[i:i + seq_len])
    data_sequences = np.array(data_sequences)

    x_data_list = []
    y_data_list = []
    for seq in data_sequences:
        x_data_list.append(seq[:-1])
        y_data_list.append(seq[-1])
    x_data = np.array(x_data_list)
    y_data = np.array(y_data_list)

    # 计算验证集和测试集的大小
    valid_set_size = int(len(x_data) * (valid_set_size_percentage / 100))
    test_set_size = int(len(x_data) * (test_set_size_percentage / 100))
    train_set_size = len(x_data) - valid_set_size - test_set_size

    # 划分训练集、验证集和测试集
    x_train = x_data[:train_set_size]
    y_train = y_data[:train_set_size]
    x_valid = x_data[train_set_size:train_set_size + valid_set_size]
    y_valid = y_data[train_set_size:train_set_size + valid_set_size]
    x_test = x_data[train_set_size + valid_set_size:]
    y_test = y_data[train_set_size + valid_set_size:]

    # YOUR TASK: Try your best to fill this part!
    # hint: first create all possible continuous sequences of length seq_len

    return [x_train, y_train, x_valid, y_valid, x_test, y_test]


df_stock = df[df.symbol == 'EQIX'].copy()
df_stock.drop(columns=['symbol'], inplace=True)
df_stock.drop(columns=['volume'], inplace=True)
df_stock.drop(columns=['date'], inplace=True)

# normalize stock
df_stock_norm = df_stock.copy()
df_stock_norm = normalize_data(df_stock_norm)

# create train, test data
seq_len = 20  # choose sequence length
x_train, y_train, x_valid, y_valid, x_test, y_test = load_data(df_stock_norm, seq_len)
print('x_train.shape = ', x_train.shape)
print('y_train.shape = ', y_train.shape)
print('x_valid.shape = ', x_valid.shape)
print('y_valid.shape = ', y_valid.shape)
print('x_test.shape = ', x_test.shape)
print('y_test.shape = ', y_test.shape)

# draw a figure
plt.figure(figsize=(15, 5))
plt.plot(df_stock_norm.open.values, color='red', label='open')
plt.plot(df_stock_norm.close.values, color='green', label='low')
plt.plot(df_stock_norm.low.values, color='blue', label='low')
plt.plot(df_stock_norm.high.values, color='black', label='high')
plt.title('stock')
plt.xlabel('time [days]')
plt.ylabel('normalized price/volume')
plt.legend(loc='best')
plt.show()


# Definition of RNN
class RNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, num_class, dropout_rate):
        super(RNN, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout_rate = dropout_rate

        self.rnn = nn.LSTM(self.input_dim,
                           self.hidden_dim,
                           num_layers=self.num_layers,
                           batch_first=True,
                           dropout=self.dropout_rate)
        self.fc = nn.Linear(hidden_dim, num_class)

    def forward(self, x):
        stacked_outputs, _ = self.rnn(x)  # 50 * 19 * 200
        # YOUR TASK: finish the forward pass so the outputs are passed through the final linear layer.
        # Hint: stacked_outputs is likely shaped as 50 * 19 * 200
        last_output = stacked_outputs[:, -1, :]
        output = self.fc(last_output)
        return output


# function to get the next batch
index_in_epoch = 0
perm_array = np.arange(x_train.shape[0])
np.random.shuffle(perm_array)


def get_next_batch(batch_size):
    global index_in_epoch, x_train, perm_array
    start = index_in_epoch
    index_in_epoch += batch_size

    if index_in_epoch > x_train.shape[0]:
        np.random.shuffle(perm_array)  # shuffle permutation array
        start = 0  # start next epoch
        index_in_epoch = batch_size

    end = index_in_epoch
    return x_train[perm_array[start:end]], y_train[perm_array[start:end]]


# parameters
n_steps = seq_len - 1
n_inputs = 4
hidden_dim = 100
n_outputs = 4
n_layers = 2
learning_rate = 0.001
batch_size = 50
n_epochs = 100
dropout_rate = 0.5
train_set_size = x_train.shape[0]
test_set_size = x_test.shape[0]

rnn = RNN(input_dim=n_inputs, hidden_dim=hidden_dim, num_layers=n_layers, num_class=n_outputs,
          dropout_rate=dropout_rate)
# Optimizer
optimizer = torch.optim.Adam(rnn.parameters(), lr=learning_rate)  # optimize all cnn parameters
# Loss function
criterion = nn.MSELoss()


# Validation function
def model_valid(cur_epochs, train_loss):
    rnn.eval()  # 将模型设置为评估模式，关闭 dropout 等训练时使用的特殊层
    with torch.no_grad():
        x_valid_tensor = torch.tensor(x_valid, dtype=torch.float32)
        y_valid_tensor = torch.tensor(y_valid, dtype=torch.float32)
        output = rnn(x_valid_tensor)
        eval_loss = criterion(output, y_valid_tensor)
        print(f'Epoch {cur_epochs}: Train/Valid Loss = {train_loss:.6f}/{eval_loss:.6f}')
    return eval_loss


# # Training
# total_loss = 0.
# last_eval_loss = float('inf')
#
# for iteration in range(int(n_epochs * train_set_size / batch_size)):
#     x_batch, y_batch = get_next_batch(batch_size)  # fetch the next training batch
#
#     # YOUR TASK: Try your best to fill this part!
#     # Make sure to call model_valid and print training and validation loss after every 5 epoches.
#     rnn.train()
#     optimizer.zero_grad()
#     inputs = torch.tensor(x_batch, dtype=torch.float32)
#     labels = torch.tensor(y_batch, dtype=torch.float32)
#
#     outputs = rnn(inputs)
#     loss = criterion(outputs, labels)
#
#     loss.backward()  # 反向传播
#     optimizer.step()  # 更新参数
#
#     total_loss += loss.item()
#
#     # 每 5 个 epoch 进行一次验证
#     if (iteration + 1) % (train_set_size // batch_size * 5) == 0:
#         cur_epoch = (iteration + 1) // (train_set_size // batch_size)
#         avg_train_loss = total_loss / (train_set_size // batch_size * 5)
#         eval_loss = model_valid(cur_epoch, avg_train_loss)
#         total_loss = 0.
# torch.save(rnn.state_dict(), './LSTM.pt')
# print("Model Training Finished !")



rnn.load_state_dict(torch.load('LSTM.pt'))
rnn.eval()
with torch.no_grad():
    x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    y_train_pred = rnn(x_train_tensor)

    x_valid_tensor = torch.tensor(x_valid, dtype=torch.float32)
    y_valid_tensor = torch.tensor(y_valid, dtype=torch.float32)
    y_valid_pred = rnn(x_valid_tensor)

    x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)
    y_test_pred = rnn(x_test_tensor)

ft = 1  # 0 = open, 1 = close, 2 = highest, 3 = lowest
## show predictions
plt.figure(figsize=(15, 5));
plt.subplot(1, 2, 1);

plt.plot(np.arange(y_train.shape[0]), y_train[:, ft], color='blue', label='train target')

plt.plot(np.arange(y_train.shape[0], y_train.shape[0] + y_valid.shape[0]), y_valid[:, ft],
         color='gray', label='valid target')

plt.plot(np.arange(y_train.shape[0] + y_valid.shape[0],
                   y_train.shape[0] + y_test.shape[0] + y_test.shape[0]),
         y_test[:, ft], color='black', label='test target')

plt.plot(np.arange(y_train_pred.shape[0]), y_train_pred[:, ft], color='red',
         label='train prediction')

plt.plot(np.arange(y_train_pred.shape[0], y_train_pred.shape[0] + y_valid_pred.shape[0]),
         y_valid_pred[:, ft], color='orange', label='valid prediction')

plt.plot(np.arange(y_train_pred.shape[0] + y_valid_pred.shape[0],
                   y_train_pred.shape[0] + y_valid_pred.shape[0] + y_test_pred.shape[0]),
         y_test_pred[:, ft], color='green', label='test prediction')

plt.title('past and future stock prices')
plt.xlabel('time [days]')
plt.ylabel('normalized price')
plt.legend(loc='best');

plt.subplot(1, 2, 2);

plt.plot(np.arange(y_train.shape[0], y_train.shape[0] + y_test.shape[0]),
         y_test[:, ft], color='black', label='test target')

plt.plot(np.arange(y_train_pred.shape[0], y_train_pred.shape[0] + y_test_pred.shape[0]),
         y_test_pred[:, ft], color='green', label='test prediction')

plt.title('future stock prices')
plt.xlabel('time [days]')
plt.ylabel('normalized price')
plt.legend(loc='best')
corr_price_development_train = np.sum(np.equal(np.sign(y_train[:, 1] - y_train[:, 0]),np.sign(y_train_pred[:, 1] - y_train_pred[:, 0])).numpy()) / y_train.shape[0]
corr_price_development_valid = np.sum(np.equal(np.sign(y_valid[:, 1] - y_valid[:, 0]),np.sign(y_valid_pred[:, 1] - y_valid_pred[:, 0])).numpy()) /y_valid.shape[0]
corr_price_development_test = np.sum(np.equal(np.sign(y_test[:, 1] - y_test[:, 0]),np.sign(y_test_pred[:, 1] - y_test_pred[:, 0])).numpy()) / y_test.shape[0]

print('correct sign prediction for close - open price for train/valid/test: %.2f/%.2f/%.2f' % (
    corr_price_development_train, corr_price_development_valid, corr_price_development_test))
plt.show()