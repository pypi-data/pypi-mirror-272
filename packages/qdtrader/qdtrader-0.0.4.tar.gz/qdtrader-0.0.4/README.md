# qdtrader量化交易工具包

## 一. 简介
qdtrader量化交易工具包可以通过pip直接安装在用户本地，实现在任意python环境下进行策略开发、回测、模拟交易和实盘交易。

如需更详细的使用说明，请参见如下链接：https://doc.quantdo.com.cn/helpbook/index.html#/cn/qdsdk/0.0.1/README

<br>

## 二. 安装说明
量化交易工具包qdtrader的运行依赖如下几部分内容，所以，在安装qdtrader包之前，请先保证这几部分安装完成。
- python环境（版本3.7或以上）
- redis缓存数据库
- Microsoft C++ Build Tools

> ### 1. 安装python和创建环境
可以直接在电脑上安装python环境，也可以采用miniconda这样的Python集成和管理工具，对本机python环境进行管理。为了保证多个python环境相互独立，互不影响，以及管理方便，在这里，我们使用miniconda。
安装步骤如下：
- 下载安装包。在miniconda官方下载与操作系统对应的安装包，比如windows操作系统就下载Miniconda3 Windows 64-bit。官方地址：[Miniconda — Anaconda documentation](https://docs.anaconda.com/free/miniconda/index.html)
- 下载完成后，根据提示进行安装。安装完毕，需要进行如下配置：

    **Windows操作系统**
    ```
    在“系统环境变量PATH”下，添加如下3个路径（假设安装路径为c:/dev/miniconda3）：
    miniconda安装路径：c:/dev/miniconda3
    scripts路径：C:/Dev/miniconda3/Scripts
    Library路径：C:/Dev/miniconda3/Library/bin
    ```
    
    **Linux操作系统**
    
    ```shell
    # 根据如下命令，将miniconda安装路径添加到环境变量path（假设安装路径为/opt/miniconda3）：
    
    $ vim /etc/profile
    export PATH="/opt/miniconda3/bin:$PATH"
    
    # 确认是否安装成功
    $ conda --version
    conda 22.11.1
    ```

    <br>

- 创建python环境
    ```
    # 如下命令中的"py310_qdtrader"为python环境名字，可自定义
    # 如下命令中的"python==3.10"是指明python的版本，版本必须大于3.7
    
    $ conda create -n py310_qdtrader python==3.10
    ```
        
    **conda相关命令**
    ```
    # 查看当前系统有哪些python环境
    $ conda env list
     
    # 激活特定python环境，激活后，所有安装的包和文件都只存在激活的这个python环境
    $ conda activate python环境名
     
    # 退出python环境
    $ deactivate
     
    # 查看当前python环境下有哪些安装包
    $ conda list
    ```


<br>

> ### 2. 安装Redis
- Windows操作系统

    可以使用我们提供的安装配套的redis-server服务，下载后运行该工具即可。下载链接：https://quantease.cn/downloads/qeserver/installRedis.exe

    注：
    - qdtrader使用的Redis端口号是6379。若需要修改为其他端口号，需要在qdtrader安装完毕后修改qdtrader的配置
    - 若要加快安装速度，可以使用国内镜像站点
<br>
- Linux操作系统

    linux下安装Redis最简单快捷的方式是使用Docker安装
    ```
    # 下载redis最新镜像版本
    $ docker pull redis
    
    # 启动redis容器
    # 命令中的"redis-server"为容器的名字，可以自定义
    # 命令中"-p 6379:6379"是将容器和主机的端口映射，格式为"主机端口:容器端口"。如果启动容器的主机上的6379端口被占用，可以修改为其它端口
    $ docker run -itd --name redis-server -p 6379:6379 redis
    ```

<br>

> ### 3. 安装Microsoft C++ Build Tools

通过如下链接下载vs_BuildTools.exe，并进行安装。
```HTML
https://visualstudio.microsoft.com/visual-cpp-build-tools

注：该工具版本号需要在14以上
```

<br>

## 三. 安装qdtrader

```bash
$ pip install -U qdtrader --timeout=60

# 若要加快安装速度，可以使用国内镜像站点
```

<br>

## 四. 启动网页服务

- 写一个python文件命名为runWeb.py
  ```python
  from qdtrader.qeweb import runWebpage
  runWebpage()
  ```

- 在之前创建的python环境"py310_qdtrader"下，执行此py文件。
  - 命令行环境下进入runWeb.py所在目录，并运行如下命令
    ```bash
    python runWeb.py
    ```
  - 运行后web网页服务将启动，用户可以实时查看订单委托，成交，持仓，权益和日志信息，并可以观察行情图。
  - 按键Ctrl+C或者关闭窗口可以终止该服务，网页将无法查看，重新运行上述命令后可恢复。
    
  
<br>

## 五. 编写策略文件并运行

- 如下是一个python策略文件范例

  ```python
  import qdsdk
  from datetime import datetime,timedelta
  from qdtrader import *
  qdsdk.auth('Your username','Your authcode')
  user_setting = {'investorid':'000000', 'password':'XXXXXXXXXXXXXX','broker':'simnow'}
  user = 'myname'
    
  def getLastToken(user):
      acclist = listSimuAccounts(user)
      if len(acclist)>0:
          return acclist[-1]
      else:
          return  createSimuAccount(user, initCap=10000000)
    
  class mystrat(qeStratBase):
        
      def __init__(self):
          self.instid=['AG2306.SFE']
          self.datamode='minute'
          self.freq = 1
            
      def crossDay(self,context):
          pass
      def onBar(self,context):
          print(get_bar(context,1))
            
      def handleData(self,context):
          pass
    
    
  if __name__=='__main__':
      strat1 = mystrat()
      token_code = getLastToken(user)
      runStrat(user,'real', [strat1], simu_token=token_code, real_account=user_setting)
    
  ```

    > 注：
    >
    > 1.auth语句中授权码需要联系官方获取。
    >
    > 2.user_setting中账户信息需要换成您自己的账户信息
    >
    > 3.运行后复制给出的网页链接在浏览器中查看运行结果即可

  
<br>

## 六. 修改系统配置

- 获取系统配置
  ```python
  from qdtrader import read_sysconfig
  read_sysconfig()
  ```
  获取结果为
  ```
  {'redis': {'host': '127.0.0.1', 'port': 6379, 'password': ''}, 'webpage': {'host': '127.0.0.1', 'port': 5814}}
  ```

- 修改Redis配置

  接口函数为
  ```python
  setRedisConfig(host='127.0.0.1', port=6379, password='')
  ```
  根据您本地Redis-server配置修改该接口，使得qdtrader可以访问您的本地数据库。
  比如您本地Redis端口号为6380， 那么可以这么运行

  ```python
  from qdtrader import setRedisConfig
  setRedisConfig(port=6380)
  ```
  恢复默认出厂设置,仅需要调用不带参数的setRedisConfig即可
  ```python
  from qdtrader import setRedisConfig
  setRedisConfig()
  ```

- 修改网页配置

  接口函数为
  ```python
  setWebConfig(host='127.0.0.1',port=5814)
  ```
  如果qdtrader网页服务默认端口号5814和您本地端口冲突，您可以修改为其他端口号，比如修改为5008。
  ```python
  from qdtrader import setWebConfig
  setWebConfig(port=5008)
  ```
  恢复默认出厂，设置仅需要调用不带参数的setWebConfig即可
  ```
  from qdtrader import setWebConfig
  setWebConfig()
  ```
  在浏览器测试一下输入网址http://127.0.0.1:5814, 出现如下文字代表启动成功
    ```
    qdtrader网页展示服务已经成功启动
    ```

<br>

## 如何编写策略

参照[官方文档](http://doc.quantdo.com.cn/helpbook?authcode=8%2B4wHJbzPBV0Ad%2F9N0iDlZwJQTo%3D)文档说明



<br>

## 插件使用说明

### 安装

以“algoex“插件为例，下载插件代码如下：

```python
from qdsdk import auth
auth('your username','your authcode')

from qdtrader.qeplugins import installPlugin
installPlugin('algoex')
```

运行代码后，出现如下提示代表安装成功：

```
插件algoex下载成功
在策略文件中按如下格式import该插件:
from qdtrader.plugins.qealgoex import plugin_algoex
```

> 注;下载插件需要成为VIP付费客户，否则会下载失败。注册VIP请联系客服

### 引用插件

以'algoex'为例，根据按照的说明，在code中使用：

```python
from qdsdk import auth
##授权码
auth('your username','your authcode')
from qdtrader import listSimuAccounts, createSimuAccount,runStrat
from qdtrader.plugins.qealgoex import plugin_algoex 

##实盘账户信息
user_setting = {'investorid':'xxxxxx', 'password':'xxxxxxxx','broker':'xxxxxx'}

if __name__=='__main__':
    ##换成自己的用户名
    user='myname'
    ##如果有模拟账户，用第一个账户，没有新建一个
    tokenlist = listSimuAccounts(user)
    if len(tokenlist) > 0:
        token = tokenlist[0]
    else:
        token = createSimuAccount(user)
    ##运行策略，algoex插件本身就是个策略实例，可以直接使用
    runStrat(user,'real',[plugin_algoex], simu_token=token,real_account=user_setting)

```

