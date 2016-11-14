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


### Log rotate

vi /etc/logrotate.d/zookeeper
```
/PATH/TO/zookeeper/zookeeper.out
{
    missingok
    notifempty
    size 200M
    compress
    dateext
    weekly
    rotate 4
    copytruncate
}
```

#### 手动触发
/usr/sbin/logrotate /etc/logrotate.conf
或者
/usr/sbin/logrotate /etc/logrotate.d/zookeeper

#### 自动触发 
Logrotate是基于CRON运行的，其脚本是`/etc/cron.daily/logrotate`
```
#!/bin/sh

/usr/sbin/logrotate /etc/logrotate.conf
EXITVALUE=$?
if [ $EXITVALUE != 0 ]; then
    /usr/bin/logger -t logrotate "ALERT exited abnormally with [$EXITVALUE]"
fi
exit 0
```

vi /etc/crontab
```bash
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
HOME=/

# run-parts
01 * * * * root run-parts /etc/cron.hourly
59 23 * * * root run-parts /etc/cron.daily
22 4 * * 0 root run-parts /etc/cron.weekly
42 4 1 * * root run-parts /etc/cron.monthly
```
