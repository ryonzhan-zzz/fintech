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
    blockchain.add_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )
    last_block = blockchain.last_block
    last_block_hash = blockchain.hash_block(last_block) if last_block else None
    nonce = blockchain.proof_of_work(
        len(blockchain.chain),
        last_block_hash,
        blockchain.current_transactions
    )
    block = blockchain.append_block(
        nonce, last_block_hash
    )
    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'hash_of_previous_block': block['hash_of_previous_block']
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # Extract transaction data
    values = request.get_json()

    # Validate required fields
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing required fields', 400

    # Process new transaction
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
    # Get node list from request
    values = request.get_json()
    nodes = values.get('nodes')

    # Validate input
    if nodes is None:
        return "Error: Invalid node list", 400

    # Register each node
    for node in nodes:
        blockchain.add_node(node)

    response = {
        'message': 'New nodes registered',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/sync', methods=['GET'])
def sync():
    updated = blockchain.update_blockchain()
    if updated:
        response = {
            'message': 'Chain updated to latest version',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Chain is already up to date',
            'current_chain': blockchain.chain
        }
    return jsonify(response), 200

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
