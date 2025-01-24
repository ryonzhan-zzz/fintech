## init解析
```python
class Blockchain(object):
    # 难度目标，即哈希值前几位为0
    difficulty_target = "0000"

    def __init__(self):
        # 初始化节点集合
        self.nodes = set()
        # 初始化链结构
        self.chain = []
        # 初始化当前交易列表
        self.current_transactions = []
        # 计算创世区块的哈希值
        genesis_hash = self.hash_block("genesis_block")
        # 将创世区块添加到链中
        self.append_block(
            # 设置前一个区块的哈希值为创世区块的哈希值
            hash_of_previous_block=genesis_hash,
            # 设置创世区块的随机数为通过工作量证明算法计算得到的值
            nonce=self.proof_of_work(0, genesis_hash, [])
        )
```
### 1. 初始化节点集合
```python
self.nodes = set()
```
- **解释**：创建一个空的集合 `nodes`，用于存储区块链网络中其他节点的地址，集合能保证节点地址的唯一性。

### 2. 初始化链结构
```python
self.chain = []
```
- **解释**：创建一个空的列表 `chain`，这个列表将用来存放区块链中的所有区块。

### 3. 初始化当前交易列表
```python
self.current_transactions = []
```
- **解释**：创建一个空的列表 `current_transactions`，用于临时存储还未被打包进区块的交易信息。

### 4. 计算创世区块的哈希值
```python
genesis_hash = self.hash_block("genesis_block")
```
- **解释**：调用 `hash_block` 方法，对字符串 `"genesis_block"` 进行哈希计算，得到创世区块的哈希值并存储在 `genesis_hash` 中。

### 5. 计算创世区块的随机数
```python
nonce = self.proof_of_work(0, genesis_hash, [])
```
- **解释**：调用 `proof_of_work` 方法，传入索引 `0`、创世区块的哈希值 `genesis_hash` 和空的交易列表 `[]`，通过工作量证明算法计算出符合难度目标的随机数 `nonce`。

### 6. 添加创世区块到链中
```python
self.append_block(
    hash_of_previous_block=genesis_hash,
    nonce=nonce
)
```
- **解释**：调用 `append_block` 方法，将创世区块添加到区块链中。传入前一个区块的哈希值（这里就是创世区块自身的哈希值 `genesis_hash`）和计算得到的随机数 `nonce`，该方法会创建创世区块并将其添加到 `chain` 列表中。 


## 各部分代码详细解析
### 1.`hash_block`方法
```python
def hash_block(self, block):
    # 将区块信息编码为JSON格式
    block_encoded = json.dumps(block, sort_keys=True).encode()
    # 使用SHA-256算法对编码后的区块信息进行哈希计算
    return hashlib.sha256(block_encoded).hexdigest()
```
- 该方法接受一个区块信息`block`作为参数。
- `json.dumps(block, sort_keys=True).encode()`：将区块信息转换为JSON格式的字符串，并按键排序，然后将字符串编码为字节串。
- `hashlib.sha256(block_encoded).hexdigest()`：使用SHA - 256算法对编码后的字节串进行哈希计算，并将结果转换为十六进制字符串返回。

### 2.`proof_of_work`方法
```python
def proof_of_work(self, index, hash_of_previous_block, transactions):
    # 初始化随机数
    nonce = 0
    # 循环寻找合适的随机数
    while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:
        # 如果当前随机数不满足条件，则增加随机数
        nonce += 1
    # 返回找到的随机数
    return nonce
```
- 该方法实现了工作量证明算法，用于找到一个合适的随机数`nonce`。
- 初始化随机数`nonce`为0。
- 使用`while`循环不断尝试不同的随机数，直到`valid_proof`方法返回`True`，表示找到了符合难度目标的随机数。
- 每次循环将随机数加1。
- 最后返回找到的随机数。

### 3.`valid_proof`方法
```python
def valid_proof(self, index, hash_of_previous_block, transactions, nonce):
    # 将索引、前一个区块的哈希值、交易信息和非随机数编码为字节串
    content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()
    # 对编码后的内容进行SHA-256哈希计算
    content_hash = hashlib.sha256(content).hexdigest()
    # 判断哈希值的前缀是否与难度目标匹配
    return content_hash[:len(self.difficulty_target)] == self.difficulty_target
```
- 该方法用于验证给定的随机数`nonce`是否满足难度目标。
- 将索引、前一个区块的哈希值、交易信息和随机数拼接成一个字符串，并编码为字节串。
- 使用SHA - 256算法对字节串进行哈希计算，得到哈希值。
- 检查哈希值的前缀是否与难度目标`difficulty_target`（即`"0000"`）匹配，如果匹配则返回`True`，否则返回`False`。

### 4.`append_block`方法
```python
def append_block(self, nonce, hash_of_previous_block):
    # 创建一个新的区块
    block = {
        'index': len(self.chain),
        'timestamp': time.time(),
        'transactions': self.current_transactions,
        'nonce': nonce,
        'hash_of_previous_block': hash_of_previous_block
    }
    # 重置待处理的交易列表
    # Reset pending transactions
    self.current_transactions = []
    # 将新区块添加到链中
    # Add new block to chain
    self.chain.append(block)
    return block
```
- 该方法用于创建一个新的区块并添加到区块链中。
- 创建一个字典`block`，包含区块的索引（即区块链的长度）、时间戳、当前待处理的交易列表、随机数和前一个区块的哈希值。
- 重置`current_transactions`列表为空，因为这些交易已经被打包到新区块中。
- 将新区块添加到`chain`列表中，并返回该区块。

### 5.`add_transaction`方法
```python
def add_transaction(self, sender, recipient, amount):
    # 将交易添加到当前交易列表中
    self.current_transactions.append({
        'amount': amount,
        'recipient': recipient,
        'sender': sender
    })

    # 返回包含此交易的区块的索引
    # 如果链中存在区块，则返回最后一个区块的索引加1
    # 否则，返回1，表示交易将被添加到第一个区块中
    return self.last_block['index'] + 1 if self.last_block else 1
```
- 该方法用于添加一笔新的交易到当前待处理的交易列表中。
- 创建一个包含交易信息（发送方、接收方和交易金额）的字典，并添加到`current_transactions`列表中。
- 返回包含此交易的区块的索引。如果区块链中已经有区块，则返回最后一个区块的索引加1；否则返回1。

### 6.`add_node`方法
```python
def add_node(self, address):
    # 解析传入的地址
    parsed_url = urlparse(address)
    # 将解析出的网络位置添加到节点集合中
    self.nodes.add(parsed_url.netloc)
    # 打印添加成功的节点信息
    print(f"Added node: {parsed_url.netloc}")
```
- 该方法用于添加一个新的节点到区块链网络中。
- 使用`urlparse`方法解析传入的节点地址，提取出网络位置（如`localhost:5000`）。
- 将网络位置添加到`nodes`集合中。
- 打印添加成功的节点信息。

### 7.`last_block`属性
```python
@property
def last_block(self):
    # 如果链不为空
    if self.chain:
        # 返回链中的最后一个区块
        return self.chain[-1]
    # 如果链为空，则返回None
    return None
```
- 这是一个属性方法，用于获取区块链中的最后一个区块。
- 如果区块链不为空，则返回`chain`列表中的最后一个元素；否则返回`None`。

### 8.`valid_chain`方法
```python
def valid_chain(self, chain):
    last_block = chain[0]
    current_index = 1

    while current_index < len(chain):
        # 获取当前区块
        block = chain[current_index]
        # 检查当前区块的前一个区块哈希值是否与上一个区块的哈希值一致
        if block['hash_of_previous_block'] != self.hash_block(last_block):
            return False

        # 检查当前区块的哈希值是否符合工作量证明条件
        if not self.valid_proof(
                current_index,
                block['hash_of_previous_block'],
                block['transactions'],
                block['nonce']
        ):
            return False

        # 更新上一个区块为当前区块
        last_block = block
        current_index += 1
    return True
```
- 该方法用于验证给定的区块链是否有效。
- 从区块链的第二个区块开始遍历，检查每个区块的前一个区块哈希值是否与上一个区块的实际哈希值一致，以及每个区块的哈希值是否符合工作量证明条件。
- 如果发现任何不一致或不符合条件的情况，则返回`False`；否则返回`True`。

### 9.`update_blockchain`方法
```python
def update_blockchain(self):
    # 获取节点列表
    neighbours = self.nodes
    # 初始化新的链为空
    new_chain = None
    # 初始化当前链的长度为本地链的长度
    max_length = len(self.chain)

    # 遍历节点列表
    for node in neighbours:
        # 向节点发送GET请求获取区块链信息
        response = requests.get(
            f'http://{node}/blockchain'
        )

        # 如果请求成功
        if response.status_code == 200:
            # 获取响应中的链长度
            length = response.json()['length']
            # 获取响应中的链
            chain = response.json()['chain']

            # 如果响应中的链长度大于当前链长度且链有效
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain

    # 如果找到了更长的有效链
    if new_chain:
        # 更新本地链为新的链
        self.chain = new_chain
        return True
    return False
```
- 该方法用于更新本地区块链，使其与网络中最长的有效链保持一致。
- 遍历`nodes`集合中的所有节点，向每个节点发送GET请求获取其区块链信息。
- 如果请求成功，检查响应中的链长度是否大于本地链长度，并且该链是否有效。如果满足条件，则更新`max_length`和`new_chain`。
- 如果找到了更长的有效链，则将本地链更新为新的链，并返回`True`；否则返回`False`。

