# Druid

官网: http://druid.io/  
github: https://github.com/druid-io  
文档: http://druid.io/docs/0.9.2/design/index.html  
quickstart: http://druid.io/docs/0.9.2/tutorials/quickstart.html  

## 简单安装

#### 依赖
* Zookeeper: https://github.com/jaiminpan/fast-memo/blob/master/ZooKeeper/deploy.md
* Mysql OR Postgres(可选)
* hdfs(可选)

#### 准备
```
curl -O http://static.druid.io/artifacts/releases/druid-0.9.2-bin.tar.gz
tar -xzf druid-0.9.2-bin.tar.gz
cd druid-0.9.2
```

目录结构:
* LICENSE - 软件许可证
* bin/ - 启动脚本
* conf/* - 配置文件模版
* conf-quickstart/* - quickstart例子的配置文件
* extensions/* - 插件
* hadoop-dependencies/* - Druid Hadoop 依赖包.
* lib/* - 依赖包.
* quickstart/* - quickstart例子的测试数据和脚本.

#### 配置环境脚本
bin目录中有
```
broker.sh coordinator.sh historical.sh middleManager.sh overlord.sh node.sh
generate-example-metrics jconsole.sh init
```
`node.sh` 是核心的启动脚本，其他一些如broker.sh都是基于之上的分装。

在使用这些命令前，需要配置环境变量，考虑创建环境脚本[env.sh][env]  
source以后就可以直接调用broker.sh。
```
cat env.sh
# 配置文件目录
export DRUID_CONF_DIR=/opt/appsoft/druid-0.9.2/conf-quickstart/druid

# log目录
export DRUID_LOG_DIR=/data/var/log/druid

# pid目录
export DRUID_PID_DIR=/data/var/druid/pids

# lib目录
# export LIB_DIR=
```

#### init
创建需要的文件目录，可以参考 `bin/init` 文件内容
```
LOG_DIR=var

mkdir -p log
mkdir -p $LOG_DIR/tmp;
mkdir -p $LOG_DIR/druid/indexing-logs;
mkdir -p $LOG_DIR/druid/segments;
mkdir -p $LOG_DIR/druid/segment-cache;
mkdir -p $LOG_DIR/druid/task;
mkdir -p $LOG_DIR/druid/hadoop-tmp;
mkdir -p $LOG_DIR/druid/pids;

# OR
mkdir -p $LOG_DIR/{tmp,druid/{indexing-logs,segments,segment-cache,task,hadoop-tmp,pids}}
```


#### 配置文件修改
* 主要是 Zookeeper 地址，Metadata的db位置，还有deep storage和 indexing log的位置  
* 配置文件中已经存在，开启关闭注释即可，例
``` bash
# {CONF_PATH}/druid/_common/common.runtime.properties

# Zookeeper
#

druid.zk.service.host=localhost
druid.zk.paths.base=/druid

# For Derby server on your Druid Coordinator (only viable in a cluster with a single Coordinator, no fail-over):
druid.metadata.storage.type=derby
druid.metadata.storage.connector.connectURI=jdbc:derby://localhost:1527/var/druid/metadata.db;create=true
druid.metadata.storage.connector.host=localhost
druid.metadata.storage.connector.port=1527

# For MySQL:
....

#
# Deep storage
#

# For local disk (only viable in a cluster if this is a network mount):
# druid.storage.type=local
# druid.storage.storageDirectory=/data/var/druid/segments

# For HDFS:
druid.storage.type=hdfs
druid.storage.storageDirectory=hdfs://namenode_ip:port/mw/data/druid/segments
```
更多配置方法可参考，
* http://druid.io/docs/0.9.2/dependencies/metadata-storage.html
* http://druid.io/docs/0.9.2/dependencies/deep-storage.html
* http://druid.io/docs/0.9.2/dependencies/zookeeper.html


## 嵌套json的解析配置

参考 http://druid.io/docs/latest/ingestion/flatten-json.html  
flattenSpec 中的 fields的 type： "path" 表示嵌套的json子内容


代码: https://github.com/druid-io/druid-api/blob/master/src/main/java/io/druid/data/input/impl/JSONPathFieldType.java


## 数据导入

参考: 
* http://druid.io/docs/latest/tutorials/quickstart.html
* http://druid.io/docs/latest/tutorials/ingestion.html


## Misc

#### 启动文件 druid.sh
由于有时候需要全部重起节点，创建了快速启动的脚本 [druid.sh][druid_script]


[env]: https://github.com/jaiminpan/fast-memo/blob/master/druidio/script/env.sh
[druid_script]: https://github.com/jaiminpan/fast-memo/blob/master/druidio/script/druid.sh

