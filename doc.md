# 使用Python构建一个简单的区块链系统

---

基于区块链核心原理编写的简单实现。[原理讲解](https://github.com/qianqianjun/SimpleBlockChain/blob/master/README.md)

## 确定区块结构

```json
{
     "index": 区块索引,

     "previous_Hash": 前一个区块的哈希,

     "proof": 用于工作量证明的随机数,

     "timestamp": 时间戳,

     "transactions": [区块中包含的所有交易]

}
```

## 确定交易的结构

```json
{
    "sender":交易发送方,
    "receiver":交易接受方,
    "amount":交易的数量
}
```

## 编写交易和区块类

- 交易类：Transaction.py

  ```python
  import json
  from typing import *
  class Transaction:
      """
      存储交易信息的类
      包括交易发送人，交易接受人，交易数量信息
      """
      def __init__(self,sender1:str,receive1:str,amount1:int):
          self.sender=sender1
          self.receiver=receive1
          self.amount=amount1
      def toJsonStr(self):
          return {
              'sender':self.sender,
              'receiver':self.receiver,
              'amount':self.amount
          }
  ```

- 区块类：Block.py

  ```python
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
  ```

## 编写区块链类：BlockChain.py

区块链核心功能应该添加交易到待挖区块中，生成新的区块，进行工作量证明，此外，为了方便操作，还定义了一个hash函数用于打包区块生成摘要。(注意：下面的函数都是类成员函数)

- ### 添加交易

  ```python
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
  ```

- ### 工作量证明

  ```python
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
  ```

- ### 生成新区快

  ```python
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
  ```

- ### 构造函数
  - 因为所有的节点都是一个创世区块，所以用类的静态成员来构造，并在每个节点产生时，将创世区块加入到节点的区块链中

  ```python
  publicBlock=Block(0,100000000.00000001,[],520,"创世区块无前面的哈希")
      def __init__(self):
          self.transactions=[]
          self.chain=[]
          self.chain.append(BlockChain.publicBlock)
  ```

- ### 其它函数

  ```python
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
              
      def hash(self,block)->str:
          """
          生成区块的哈希
          :param block: 区块
          :return: 返回的是区块的哈希摘要字符串
          """
          blockInfo=json.dumps(block.toJson(),sort_keys=True).encode()
          return hashlib.sha256(blockInfo).hexdigest()
  ```

## 编写点对点网络模拟程序 Peer.py

使用flask 框架来生成服务器，使用requests库来进行节点间的通信，通过开启多个终端来模拟p2p网络节点

点对点的网络要求可以发现邻居节点（这里手动发现），添加邻居节点。解决节点之间数据不一致的冲突，另外还要提供api供其他节点访问

- ### 构造函数

  ```python
      def __init__(self):
          #初始化这个节点的链
          self.blockchain=BlockChain()
          #初始化这个节点的邻居节点
          self.neighbours=[]
          self.address=0
          
      def setAddress(self,addr):
          self.address=addr
  ```

- ### 添加邻居节点

  ```python
      def addNeighbour(self,neighbour):
          """
          给这个节点添加一个邻居
          :param neighbour: 这个邻居的地址信息：http:127.0.0.1:5001
          :return: 无
          """
          self.neighbours.append(neighbour)
  ```

- ### 解决冲突

  ```python
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
  ```

- ### 节点API路由

  ```python
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
  ```

### 完整代码地址：[Github](https://github.com/qianqianjun/SimpleBlockChain)

### 使用方法：[Geting start](https://github.com/qianqianjun/SimpleBlockChain/blob/master/getting%20start.md)
