import hashlib
import json
from Block import Block
from time import time

from Transaction import Transaction

"""
区块链的简单实现类
完成了区块链的简单操作
"""
class BlockChain:
    publicBlock=Block(0,100000000.00000001,[],520,"创世区块无前面的哈希")
    def __init__(self):
        self.transactions=[]
        self.chain=[]
        self.chain.append(BlockChain.publicBlock)
        #self.createBlock(previusHash="111",proof=100)
    def createBlock(self,previusHash:str,proof:int):
        """
        创造新的区块
        :param previusHash:上一个区块的哈希值
        :param proof: 工作量证明
        :return: 返回新的区块
        """
        index=len(self.chain)+1
        hashValue=previusHash or self.hash(self.chain[-1])
        block=Block(index,time(),
                    self.transactions,
                    proof,hashValue
                    )
        #生成新块之后要新建一个存放交易的列表用于存放新交易
        self.transactions=[]
        #将新生成的区块加入到区块链中
        self.chain.append(block)
        return block

    def addTransaction(self,sender:str,receiver:str,amount:int)->int:
        """
        生成新的交易信息，将信息加入到待挖区块中
        :param sender: 交易的发送方
        :param receiver: 交易的接受方
        :param amount: 交易数量
        :return: 返回的是交易要插入的区块的index
        """
        newTransaction=Transaction(sender,receiver,amount)
        self.transactions.append(newTransaction)
        return self.lastBlock().index+1
    def hash(self,block)->str:
        """
        生成区块的哈希
        :param block: 区块
        :return: 返回的是区块的哈希摘要字符串
        """
        blockInfo=json.dumps(block.toJson(),sort_keys=True).encode()
        return hashlib.sha256(blockInfo).hexdigest()

    def proofWork(self,lastProof:int)->int:
        """
        工作量证明函数：
        :param lastProof:上一个区块的工作量证明。
        :return: 返回工作量证明的值
        备注：工作量证明是一个非常无聊的事情，要求一个数字，这个数字
        和上一个区块的工作量证明拼在一起得到的哈希值前面有若干个0,
        0越多，这个数字就越难算，计算这个数字的唯一方法就是从0开始
        遍历每一个数字计算。
        """
        proof=0
        while not self.validProof(lastProof,proof):
            proof+=1
        return proof
    @staticmethod
    def validProof(lastproof:int,proof:int)->bool:
        """
        验证哈希值是不是满足要求，作为演示需要，这里认为哈希值前面
        有4个0就合格
        :param lastproof:上一个区块的工作量证明
        :param proof: 测试的工作量证明
        :return: 测试的工作量证明是不是满足要求
        """
        test=f'{lastproof}{proof}'.encode()
        hashStr=hashlib.sha256(test).hexdigest()
        return hashStr[0:4]=="0000"

    def lastBlock(self):
        """
        得到节点区块链的最后一个区块
        :return: 如果当前节点没有区块，返回None
        如果有则返回最后一个区块
        """
        try:
            obj=self.chain[-1]
            return obj
        except:
            return None