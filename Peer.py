import hashlib
import json
from argparse import ArgumentParser
import requests
from flask import Flask, jsonify,request

from Block import Block
from BlockChain import BlockChain
from Transaction import Transaction


class Peer:
    def __init__(self):
        #初始化这个节点的链
        self.blockchain=BlockChain()
        #初始化这个节点的邻居节点
        self.neighbours=[]
        self.address=0
    def setAddress(self,addr):
        self.address=addr
    def addNeighbour(self,neighbour):
        """
        给这个节点添加一个邻居
        :param neighbour: 这个邻居的地址信息：http:127.0.0.1:5001
        :return: 无
        """
        self.neighbours.append(neighbour)

    def validChain(self,chain)->bool:
        """
        确定链是不是有效的，只需要查看工作量证明是不是有问题就好
        :param chain: 一个区块链
        :return: 区块链有效的话返回true，否则返回False
        """
        index=1
        lastBlock=chain[0]
        length=len(chain)
        while index<length:
            block=chain[index]
            #检查哈希值是不是正确
            lastBlockHash=hashlib.sha256(json.dumps(lastBlock).encode()).hexdigest()
            if block['previous_Hash']!=lastBlockHash:
                return False
            #检查工作量证明是不是正确
            if not self.blockchain.validProof(lastBlock['proof'], block['proof']):
                return False
            lastBlock=block
            index+=1
        return True
    def resolveConflicts(self)->bool:
        """
        实现共识算法：
        使用网络中最长的链作为最终链
        :return:  如果节点的链被取代，则返回True，否则返回False
        """
        newChain=None
        #寻找比自己长的链，比自己短的链不去管它，这由共识算法决定
        maxLen=len(self.blockchain.chain)
        #遍历所有的邻居节点，判断邻居节点的链和自己的异同
        #如果邻居节点的链比自己的长，并且链是合法的，将这条链暂存起来作为最终
        #候选链，遍历结束后得到的候选链就是节点网络中 最长的一个链

        for node in self.neighbours:
            response=requests.get(
                f'http://localhost:{node}/chain')
            if response.status_code==200:
                length=response.json()['length']
                chain=response.json()['chain']
                if length>maxLen and self.validChain(chain):
                    maxLen=length
                    newChain=chain
        if newChain:
            self.blockchain.chain=[]
            for temp in newChain:
                transactions=[]
                transet=temp['transactions']
                for t in transet:
                    transactions.append(Transaction(t['sender'],t['receiver'],int(t['amount'])));
                self.blockchain.chain.append(
                    Block(temp['index'],temp['timestamp'],transactions,temp['proof'],temp['previous_Hash'])
                )
            return True
        return False
peer=Peer()
app=Flask(__name__)
@app.route("/chain",methods=['GET'])
def getChian():
    """
    获取该节点区块链上的所有区块的信息
    :return: 返回区块的信息和请求状态码
    """
    temp=peer.blockchain.chain
    json_chain=[]
    for block in temp:
        json_chain.append(block.toJson())
    response={
        'chain':json_chain,
        'length':len(temp)
    }
    return jsonify(response),200
@app.route('/transaction/new',methods=['POST'])
def addNewTransaction():
    """
    添加新的交易到当前节点的区块中
    :return: 返回提示信息
    """
    #检查提交的参数是不是完整，不完整返回错误:
    sender=request.values.get("sender")
    receiver = request.values.get("receiver")
    amount = request.values.get("amount")
    if sender==None or receiver==None or amount==None:
        return "您发送的请求参数不完整，无法操作",400
    index=peer.blockchain.addTransaction(sender,receiver,int(amount))
    response={
        "服务器消息":"添加成功",
        "所在区块索引":index
    }
    return jsonify(response),201

@app.route("/mine",methods=['GET'])
def mine():
    """
    挖矿产生新的区块：
    :return: 返回http response
    """
    last_block=peer.blockchain.lastBlock()
    last_proof=last_block.proof
    proof=peer.blockchain.proofWork(last_proof)

    #挖矿奖励：
    peer.blockchain.addTransaction(sender="区块链系统",receiver=f'http://127.0.0.1:{peer.address}',amount=1)

    block=peer.blockchain.createBlock(None,proof)

    response={
        "message":"新的区块形成了",
        "index":block.index,
        "transactions":[t.toJsonStr()
                        for t in block.transactions],
        "proof":block.proof,
        "previous_Hash":block.previous_Hash
    }
    return jsonify(response),200

@app.route("/neighbour/add",methods=['POST'])
def addNeighbour():
    """
    接受前端传过来的值，加入到自己的邻居节点中
    :return: 返回响应的消息
    """
    node=request.values.get("node")
    print(node)
    print("------------")
    if node==None:
        return "您的请求缺少参数，无法处理",400
    peer.addNeighbour(node)
    response={
        "服务器返回信息":"添加peer邻居成功！",
        "节点地址":peer.address,
        "邻居节点数量":len(peer.neighbours)
    }
    return jsonify(response),200
@app.route("/consensus")
def consensus():
    replaced=peer.resolveConflicts()
    if replaced:
        response={
            "message":"链条被更新",
            "length":len(peer.blockchain.chain)
        }
    else:
        response={
            "message":"保持链条不变",
            "length":len(peer.blockchain.chain)
        }
    return jsonify(response),200
if __name__ == '__main__':
    """
    实现区块链 p2p 网络，构造多个peer节点：
    """
    parser=ArgumentParser()
    parser.add_argument("-p","--port",default=5000,type=int,help="监听的端口")
    port=parser.parse_args().port
    peer.setAddress(port)
    app.run(host='127.0.0.1',port=port)
