import os
import subprocess

from flask import Flask, jsonify, request, render_template

from fintech.blockchain.code.Blockchain import Blockchain

# 创建区块链实例
blockchain = Blockchain()

# 创建 Flask 应用
app = Flask(__name__)


# 获取整个区块链
@app.route('/blockchain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


# 添加新交易
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


# 挖掘新块
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_hash = blockchain.hash_block(last_block)
    nonce = blockchain.proof_of_work(len(blockchain.chain), last_hash, blockchain.current_transactions)

    block = blockchain.append_block(nonce, last_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'hash_of_previous_block': block['hash_of_previous_block']
    }
    return jsonify(response), 200


# 注册新节点
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.add_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


# 同步区块链
@app.route('/nodes/sync', methods=['GET'])
def consensus():
    replaced = blockchain.update_blockchain()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # 定义三个节点的端口
    ports = [5000, 5001, 5002]
    processes = []
    for port in ports:
        # 设置 FLASK_APP 环境变量
        env = os.environ.copy()
        env['FLASK_APP'] = __file__
        # 启动每个节点
        p = subprocess.Popen(['python', '-m', 'flask', 'run', '--port', str(port)], env=env)
        processes.append(p)
    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
