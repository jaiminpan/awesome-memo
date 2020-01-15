# Elastic Search

## 一.下载安装包
1.官网下载地址
https://www.elastic.co/downloads/elasticsearch （当然也可以直接在linux中使用命令下载，但是可能比较慢，我们选择在官网进行下载）
选择对应的系统版本即可

2.历史版本下载
这个地址默认是最新的版本，如果想要历史版本，在此页面上找到past releases

点击进去找到想要的版本即可。
本文下载的是6.8.2版本（Elasticsearch和Kibana）
Elasticsearch 6.8.2
Kibana 6.8.2

注意：ES启动需要jdk，我本地已经配置了java8环境变量，不想改动，就用6.X的版本。
如果还没有配置jdk环境变量，则需要先安装jdk，因为ES是基于java以言编写，需要jdk环境。
7.0及以上版本虽然内置了jdk，但是需要java11及以上，我们不适用此版本。

## 二.elasticsearch-6.8.2安装
1.上传安装包至linux
下载好elasticsearch-6.8.2.tar.gz安装包后，上传至linux中，
我放在了/home/zjq中，在此目录下使用命令 rz 选择安装包上传即可；

2.解压
上传完成后，使用如下命令解压：
tar -zxvf elasticsearch-6.8.2.tar.gz

3.修改配置文件
进入解压后的config目录，
cd ./elasticsearch-6.8.2/config
修改elasticsearch.yml配置文件，
找到下面两项配置，开放出来（删除前面的#符号）
network.host: 192.168.212.151
http.port: 9200
bootstrap.memory_lock: true

vi config/jvm.options
```
# 替换为总内存的一半:例如内存为16g
-Xms8g
-Xmx8g
```

c. 这时候需要修改系统配置文件：
```
#> vi /etc/sysctl.conf
##生产上一定要打开文件描述符。
vm.max_map_count=262144

#> sudo sysctl -p

# when bootstrap.memory_lock: true
vm.swappiness=0
```

d. 这时候还需要修改系统配置文件：
```
vi /etc/security/limits.conf
添加如下4行：
* soft nofile 65536
* hard nofile 131072
* soft nproc 2048
* hard nproc 4096

# when bootstrap.memory_lock: true
# * soft memlock unlimited
# * hard memlock unlimited
```

4.启动ES
注意，es启动过程中会多次失败，需要修改多处配置文件，注意下文步骤：

修改完成后，重启linux系统。然后启动ES即可。

5.访问ES
注意没关闭防火墙的，需要关闭防火墙：
关闭防火墙 systemctl stop firewalld.service

启动完成后，访问地址，显示如下内容表示启动成功。

#### Misc
