# Getting Start

---

## 开发环境配置

- 配置Python 3  环境

- 使用pip安装flask 框架（用于构建一个网络节点服务器）

- 安装requests库用于网络请求

- 下载postman 用于验证 api 程序和查看返回值

## 运行

- ### 启动节点（cmd或者终端）
  - 命令：python Peer.py -p 端口号

  - 注意，打开多个终端用于模拟多个节点，注意端口号要不同

  - 下面例子只启动两个节点，端口号分别为5000端口和5001端口，程序运行成功后会在下面显示如下信息：

    终端一

    ```bash
     * Serving Flask app "Peer" (lazy loading)
     * Environment: production
       WARNING: Do not use the development server in a production environment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```

    终端二

    ```bash
     * Serving Flask app "Peer" (lazy loading)
     * Environment: production
       WARNING: Do not use the development server in a production environment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
    ```

- ### 构建p2p网络，将两个节点互相设置为邻居节点：

  使用postman 发送两个post请求，网址为 http://127.0.0.1:port/neighbour/add

  请求参数名称是node，给5000添加邻居时node值为5001，给5001添加邻居时node值为5000

  正确添加后会返回如下消息：

  ```json
  {
   "服务器返回信息": "添加peer邻居成功！",
   "节点地址": 5000,
   "邻居节点数量": 1
  }
  ```

  ```json
  {
   "服务器返回信息": "添加peer邻居成功！",
   "节点地址": 5001,
   "邻居节点数量": 1
  }
  ```

- ### 查看节点的区块链信息

  使用 postman 发送一个get请求来查看，网址为：http://127.0.0.1:port/chain

  正确后两个终端返回的信息应该一样：

  ```json
  {
      "chain": [
          {
              "index": 0,
              "previous_Hash": "创世区块无前面的哈希",
              "proof": 520,
              "timestamp": 100000000.00000001,
              "transactions": []
          }
      ],
      "length": 1
  }
  ```

- ### 添加一个交易并挖矿

  使用postman 发送一个post请求，网址为：http://127.0.0.1:5000/transaction/new

  参数为：

  sender：发送者地址，例子是http://127.0.0.1:5000

  receiver：接收着地址，这里是http://127.0.0.1:5001

  amount：交易金额，任意一个整数就好

  这里只给端口为5000的节点发送这个添加交易的请求，有人可能有疑问，这样的话两个节点的链不就不一样了么？ 不用担心，后面会使用共识机制来解决冲突

  添加交易成功后会返回下面信息：

  ```json
  {
      "所在区块索引": 1,
      "服务器消息": "添加成功"
  }
  ```

  随后进行挖矿，实现这个节点链的增长：

  使用postman 发送一个get请求到 http://127.0.0.1:5000/mine

  返回如下信息

  ```json
  {
      "index": 2,
      "message": "新的区块形成了",
      "previous_Hash": "f0efaa7f6a60f1707d8d446b891ef948abf98b7aaf2e7ed44e56e5914a95de8a",
      "proof": 287,
      "transactions": [
          {
              "amount": 520,
              "receiver": "http://127.0.0.1:5001",
              "sender": "http://127.0.0.1:5000"
          },
          {
              "amount": 520,
              "receiver": "http://127.0.0.1:5001",
              "sender": "http://127.0.0.1:5000"
          },
          {
              "amount": 1,
              "receiver": "http://127.0.0.1:5000",
              "sender": "区块链系统"
          }
      ]
  }
  ```

  可以看到生成了一个新的区块，再次查看5000端口节点的链条，返回信息如下：

  ```json
  {
      "chain": [
          {
              "index": 0,
              "previous_Hash": "创世区块无前面的哈希",
              "proof": 520,
              "timestamp": 100000000.00000001,
              "transactions": []
          },
          {
              "index": 2,
              "previous_Hash": "f0efaa7f6a60f1707d8d446b891ef948abf98b7aaf2e7ed44e56e5914a95de8a",
              "proof": 287,
              "timestamp": 1550998947.9427276,
              "transactions": [
                  {
                      "amount": 520,
                      "receiver": "http://127.0.0.1:5001",
                      "sender": "http://127.0.0.1:5000"
                  },
                  {
                      "amount": 1,
                      "receiver": "http://127.0.0.1:5000",
                      "sender": "区块链系统"
                  }
              ]
          }
      ],
      "length": 2
  }
  ```

  可见链条信息增长了，并且交易信息被保存在了第二个块中，而且还多个一个交易：矿工挖矿得到的收益，由系统发放，我们查看5001节点的链，信息如下，可见，数据不一致产生了：

  ```json
  {
      "chain": [
          {
              "index": 0,
              "previous_Hash": "创世区块无前面的哈希",
              "proof": 520,
              "timestamp": 100000000.00000001,
              "transactions": []
          }
      ],
      "length": 1
  }
  ```

- ### 解决冲突

  当两个邻居节点发现彼此之间数据不一致的情况下，会依据共识机制来解决冲突，根据共识机制的规则，可知当5000节点解决冲突的时候会保留自己的链，5001解决冲突的时候会用长链（5000）的链来替换自己的链（当然替换之前也要对5000的链进行合法性判断）

  使用 postman 发送一个get请求到http://127.0.0.1:5000/consensus  调用5000节点的解决冲突功能

  返回信息如下：

  ```json
  {
      "length": 2,
      "message": "保持链条不变"
  }
  ```

  返回了链条的长度为2，并且说明了在解决冲突的过程中保持了自己的链

  使用postman 发送get请求到 http://127.0.0.1:5000/consensus 调用5001节点的解决冲突功能，预期返回应该是5001节点的链被替换，结果如下，正是这样：

  ```json
  {
      "length": 2,
      "message": "链条被更新"
  }
  ```

  再次查看两个节点的链条信息，发现结果一致，冲突解决：

  ```json
  {
      "chain": [
          {
              "index": 0,
              "previous_Hash": "创世区块无前面的哈希",
              "proof": 520,
              "timestamp": 100000000.00000001,
              "transactions": []
          },
          {
              "index": 2,
              "previous_Hash": "f0efaa7f6a60f1707d8d446b891ef948abf98b7aaf2e7ed44e56e5914a95de8a",
              "proof": 287,
              "timestamp": 1550998947.9427276,
              "transactions": [
                  {
                      "amount": 520,
                      "receiver": "http://127.0.0.1:5001",
                      "sender": "http://127.0.0.1:5000"
                  },
                  {
                      "amount": 520,
                      "receiver": "http://127.0.0.1:5001",
                      "sender": "http://127.0.0.1:5000"
                  },
                  {
                      "amount": 1,
                      "receiver": "http://127.0.0.1:5000",
                      "sender": "区块链系统"
                  }
              ]
          }
      ],
      "length": 2
  }
  ```

- ### 总结

  程序实现了区块链的核心功能，模拟了区块链的运行原理，对理解区块链的运行有很大的帮助。

  疑难解答：1905946527@qq.com


































