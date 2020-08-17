# install


## 1.安装zookeeper


## 2.在任一个Pulsar节点，初始化集群元数据。

```sh
   # 进入 zookeepers 目录
  cd /opt/apache-pulsar-2.5.1

  # 执行命令初始化集群元数据

  bin/pulsar initialize-cluster-metadata \

  --cluster pulsar-cluster \

  --zookeeper 192.168.10.10:12181 \

  --configuration-store 192.168.10.10:12181 \

  --web-service-url http://192.168.10.10:8083/ \

  --web-service-url-tls https://192.168.10.10:8443/ \

  --broker-service-url pulsar://192.168.10.10:6650/ \

  --broker-service-url-tls pulsar+ssl://192.168.10.10:6651/

```

## 3.配置部署 BookKeeper 集群

#### 编辑 bookkeeper.conf 文件
　　# 进入bookie 配置文件目录

　　cd /opt/apache-pulsar-2.5.1/conf

```sh
    vim bookkeeper.conf

    # advertisedAddress 修改为服务器对应的ip,在另外两台服务器也做对应的修改
    advertisedAddress=192.168.10.10

    # 修改以下两个文件目录地址
    journalDirectories=/data/appdatas/bookkeeper/journal
    ledgerDirectories=/data/appdatas/bookkeeper/ledgers

    # 修改zk地址和端口信息
    zkServers=192.168.10.10:12181,192.168.10.11:12181,192.168.10.12:12181

    # 修改Prometheus指标采集端口，该端口不修改会冲突
    prometheusStatsHttpPort=8100

    # 修改 httpServerEnabled
    httpServerEnabled=true

    # 修改httpServerPort
    httpServerPort=8100
```

#### 初始化元数据，并启动 bookie 集群
```sh
    # 先执行初始化元数据命令；再执行启动命令

    # 进入 bookies 目录

    cd /opt/apache-pulsar-2.5.1

    # 执行初始化元数据命令；若出现提示，输入 Y，继续（只需在一个bookie节点执行一次）

    bin/bookkeeper shell metaformat

    # 以后台进程启动 bookie

    bin/pulsar-daemon start bookie
```

#### 按照以上步骤，启动另外两个 bookie 节点
#### 验证 bookie 是否启动成功
```sh
    # 进入 bookies 目录

    cd /opt/apache-pulsar-2.5.1

    # 验证是否启动成功

    bin/bookkeeper shell bookiesanity

    # 出现如下显示，表示启动成功Bookie 

    sanity test succeeded.
```

## 4.部署配置 Broker 集群

#### 1. 修改配置文件 broker.conf
```sh
    # 进入配置文件目录
    cd /opt/apache-pulsar-2.5.1/conf

    # 编辑 broker.conf 文件

    # 修改集群名，和ZooKeeper里初始化元数据时指定的集群名(--cluster pulsar-cluster)相同
    clusterName=pulsar-cluster

    # 修改如下两个配置，指定的都是ZooKeeper集群地址和端口号
    zookeeperServers=192.168.10.10:12181,192.168.10.11:12181,192.168.10.12:12181

    configurationStoreServers=192.168.10.10:12181,192.168.10.11:12181,192.168.10.12:12181

    # 修改如下参数为本服务器ip地址，另外两个broker节点配置文件也做对应修改
    advertisedAddress=192.168.10.10

    # 修改brokerServicePortTls端口
    brokerServicePortTls=6651

    # 修改webServicePortTls端口
    webServicePortTls=8443

    # 修改brokerDeleteInactiveTopicsEnabled，默认非活动的topic会被删除
    brokerDeleteInactiveTopicsEnabled=false
```

#### 2. 启动 broker 节点
```sh
    # 进入 brokers 目录
    cd /opt/apache-pulsar-2.5.1

    # 以后台进程启动 broker
    bin/pulsar-daemon start broker
```


#### 3. 按照以上步骤，对另外两个 broker 节点做对应配置，并启动 broker 节点
#### 4. 查看集群中 brokers 节点信息，验证 broker 是否都启动成功
```sh
    # 进入任一个 broker 目录
    cd /opt/apache-pulsar-2.5.1

    # 查看集群 brokers 节点情况
    bin/pulsar-admin brokers list pulsar-cluster
```

    至此，集群 ZooKeeper，Broker，Bookie 节点启动完毕，集群部署成功！接下来可以进行 HelloWorld 测试！
