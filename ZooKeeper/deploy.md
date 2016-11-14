# Deploy

# Deploy
下载zookeeper安装包,解压

* 修改日志位置 
  `bin/zkEnv.sh`中, 设置 `ZOO_LOG_DIR="日志目录"`
* 配置 
```bash
cp zoo_sample.cfg zoo.cfg
vi zoo.cfg
# 设置 
dataDir=/tmp/test   # 设置data目录
dataLogDir=/tmp/test_wal 设置wal目录 #

# 集群ip，只有配置集群才需要
server.1= 10.2.27.72:2888:3888
server.2= 10.2.27.73:2888:3888
server.3= 10.2.27.75:2888:3888
 ```
 
* 设置本机的集群id，只有配置集群才需要
touch /tmp/test/myid # 新建文件
echo 1 > /tmp/test/myid  #假设本机ip对应了server.1，则把 1放入myid中

* 启动 bin/zkServer.sh start
