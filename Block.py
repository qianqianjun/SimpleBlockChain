import json
from typing import List
class Block:
    def __init__(self,index1:int,timestamp1,
                 transactions1:List,proof1:int,
                 previousHash1:str):
        self.index=index1
        self.timestamp=timestamp1
        self.transactions=transactions1
        self.proof=proof1
        self.previous_Hash=previousHash1
    def toJson(self):
        temp={
            'index':self.index,
            'timestamp':self.timestamp,
            'transactions':[i.toJsonStr() for i in self.transactions],
            'proof':self.proof,
            'previous_Hash':self.previous_Hash
        }
        return temp