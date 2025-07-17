import hashlib
import json
import time
from urllib.parse import urlparse

import requests


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


    def hash_block(self, block):
        # 将区块信息编码为JSON格式
        block_encoded = json.dumps(block, sort_keys=True).encode()
        # 使用SHA-256算法对编码后的区块信息进行哈希计算
        return hashlib.sha256(block_encoded).hexdigest()


    def proof_of_work(self, index, hash_of_previous_block, transactions):
        # 初始化随机数
        nonce = 0
        # 循环寻找合适的随机数
        while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:
            # 如果当前随机数不满足条件，则增加随机数
            nonce += 1
        # 返回找到的随机数
        return nonce


    def valid_proof(self, index, hash_of_previous_block, transactions, nonce):
        # 将索引、前一个区块的哈希值、交易信息和非随机数编码为字节串
        content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()
        # 对编码后的内容进行SHA-256哈希计算
        content_hash = hashlib.sha256(content).hexdigest()
        # 判断哈希值的前缀是否与难度目标匹配
        return content_hash[:len(self.difficulty_target)] == self.difficulty_target


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


    def add_node(self, address):
        # 解析传入的地址
        parsed_url = urlparse(address)
        # 将解析出的网络位置添加到节点集合中
        self.nodes.add(parsed_url.netloc)
        # 打印添加成功的节点信息
        print(f"Added node: {parsed_url.netloc}")


    @property
    def last_block(self):
        # 如果链不为空
        if self.chain:
            # 返回链中的最后一个区块
            return self.chain[-1]
        # 如果链为空，则返回None
        return None


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
