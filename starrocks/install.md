# 手动安装 Starrocks/doris

# 修改配置文件。所有be的机器
cat >> /etc/sysctl.conf << EOF
vm.swappiness=0
EOF
# 使修改生效。
sysctl -p


cat >> /etc/security/limits.conf << EOF
* soft nproc 65535
* hard nproc 65535
* soft nofile 655350
* hard nofile 655350
* soft stack unlimited
* hard stack unlimited
* hard memlock unlimited
* soft memlock unlimited
EOF

cat >> /etc/security/limits.d/20-nproc.conf << EOF 
*          soft    nproc     65535
root       soft    nproc     65535
EOF


>$ cat >> /etc/sysctl.conf << EOF
vm.max_map_count = 2000000
EOF

>$ vi /etc/profile
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64



wget https://downloads.apache.org/doris/3.1/3.1.1/apache-doris-3.1.1-bin-x64.tar.gz
tar -zxvf apache-doris-3.1.1-bin-x64.tar.gz -C /opt/doris
OR
wget https://releases.starrocks.io/starrocks/StarRocks-3.5.8-ubuntu-amd64.tar.gz
tar -zxvf StarRocks-3.5.8-ubuntu-amd64.tar.gz -C /opt/starrocks


cd /opt/starrocks

> vi ./fe/conf/fe.conf
```
# 每台机器都要改
priority_networks = 172.31.0.0/16 # 根据你内网网段填写
meta_dir = /data/fe/meta # 文件地址
log_dir = /data/fe/log # 日志地址
```

## 启动
```
./fe/bin/start_fe.sh --daemon
```

检查
```
http://172.31.37.145:8030

```

-- 注册 Follower FE
ALTER SYSTEM ADD FOLLOWER "172.31.39.114:9010";
ALTER SYSTEM ADD FOLLOWER "172.31.44.59:9010";


-- 注册 Observer FE（可选/只读）
ALTER SYSTEM ADD OBSERVER "172.31.44.59:9010";

启动其他 FE
```
./fe/bin/start_fe.sh --daemon --helper "172.31.37.145:9010"
```

mysql -h172.31.37.145 -P9030 -uroot

SHOW FRONTENDS\G;


六、配置 BE

> vi ./be/conf/be.conf：
```
priority_networks = 172.31.0.0/16
storage_root_path = /data/be/storage
sys_log_dir = /data/be/log
```

🧱 七、启动 BE

在每台机器上执行：
```
./be/bin/start_be.sh --daemon
```

注册 BE 到 FE

在 FE 主节点的 SQL 控制台执行：

ALTER SYSTEM ADD BACKEND "172.31.37.145:9050";
ALTER SYSTEM ADD BACKEND "172.31.39.114:9050";
ALTER SYSTEM ADD BACKEND "172.31.44.59:9050";

SHOW BACKENDS;


出现三条 Alive = true，说明集群成功。









