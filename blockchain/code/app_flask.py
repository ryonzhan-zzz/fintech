import uuid

from flask import Flask, jsonify, request, render_template

from blockchain.code.Blockchain import Blockchain

app = Flask(__name__)
node_identifier = str(uuid.uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/blockchain', methods=['GET'])
def full_chain():
    # 构建响应体
    response = {
        'chain': blockchain.chain,  # 链信息
        'length': len(blockchain.chain)  # 链长度
    }
    # 返回JSON格式的响应体，状态码为200
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine_block():
    # 添加一笔交易，发送者为"0"，接收者为节点标识符，金额为1
    blockchain.add_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    # 获取最后一个区块
    last_block = blockchain.last_block
    # 计算最后一个区块的哈希值，如果链为空则返回None
    last_block_hash = blockchain.hash_block(last_block) if last_block else None

    # 计算新区块的随机数
    nonce = blockchain.proof_of_work(
        len(blockchain.chain),  # 链的长度
        last_block_hash,  # 上一个区块的哈希值
        blockchain.current_transactions  # 当前交易列表
    )

    # 创建新区块并添加到链中
    block = blockchain.append_block(
        nonce, last_block_hash
    )

    # 构建响应体
    response = {
        'message': 'New Block Forged',  # 消息内容
        'index': block['index'],  # 区块索引
        'transactions': block['transactions'],  # 交易列表
        'nonce': block['nonce'],  # 随机数
        'hash_of_previous_block': block['hash_of_previous_block']  # 上一个区块的哈希值
    }

    # 返回JSON格式的响应体，状态码为200
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # 提取交易数据
    values = request.get_json()

    # 验证必需字段
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing required fields', 400

    # 处理新交易
    index = blockchain.add_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )

    response = {
        'message': f'Transaction scheduled for Block {index}'
    }
    return jsonify(response), 201



@app.route('/nodes/add_nodes', methods=['POST'])
def add_nodes():
    # 获取POST请求中的JSON数据
    values = request.get_json()
    # 从JSON数据中获取节点列表
    nodes = values.get('nodes')

    # 检查节点列表是否为空
    if nodes is None:
        # 如果节点列表为空，则返回错误信息
        return "Error: Invalid node list", 400

    # 遍历节点列表，将每个节点添加到区块链网络中
    for node in nodes:
        blockchain.add_node(node)

    # 构建响应体，包含注册成功的消息和当前节点总数
    response = {
        'message': 'New nodes registered',
        'total_nodes': list(blockchain.nodes)
    }
    # 返回JSON格式的响应体，状态码为201
    return jsonify(response), 201



@app.route('/nodes/sync', methods=['GET'])
def sync():
    # 更新区块链
    updated = blockchain.update_blockchain()

    # 判断是否成功更新区块链
    if updated:
        # 如果成功更新，则构建响应体，包含更新成功的消息和最新的链信息
        response = {
            'message': 'Chain updated to latest version',
            'new_chain': blockchain.chain
        }
    else:
        # 如果未成功更新，则构建响应体，包含更新失败的消息和当前的链信息
        response = {
            'message': 'Chain is already up to date',
            'current_chain': blockchain.chain
        }

    # 返回JSON格式的响应体，状态码为200
    return jsonify(response), 200



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
