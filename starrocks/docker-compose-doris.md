#### case 1
version: "3"
services:
  fe:
    image: apache/doris:fe-3.1.1     # 替换为实际 tag
    hostname: fe1
    environment:
      - FE_SERVERS=fe1:${INTERNAL_IP}:9010   # INTERNAL_IP 替换为宿主机内网 IP
      - FE_ID=1
    volumes:
      - /data/doris/fe/doris-meta/:/opt/apache-doris/fe/doris-meta/
      - /data/doris/fe/log/:/opt/apache-doris/fe/log/
    network_mode: host

  be:
    image: apache/doris:be-3.1.1     # 替换为实际 tag
    hostname: be1
    environment:
      - FE_SERVERS=fe1:${INTERNAL_IP}:9010
      - BE_ADDR=${INTERNAL_IP}:9050
    volumes:
      - /data/doris/be/storage/:/opt/apache-doris/be/storage/
      - /data/doris/be/script/:/docker-entrypoint-initdb.d/
    network_mode: host
    depends_on:
      - fe

#### case 2
version: "3"
services:
  fe:
    image: apache/doris:fe-3.1.1     # 替换为实际 tag
    hostname: fe1
    environment:
      - FE_SERVERS=fe1:172.31.37.145:9010   # INTERNAL_IP 替换为宿主机内网 IP
      - FE_ID=1
    volumes:
      - /data/doris/fe/doris-meta/:/opt/apache-doris/fe/doris-meta/
      - /data/doris/fe/log/:/opt/apache-doris/fe/log/
    network_mode: host

  be:
    image: apache/doris:be-3.1.1     # 替换为实际 tag
    hostname: be1
    environment:
      - FE_SERVERS=fe1:172.31.37.145:9010
      - BE_ADDR=172.31.37.145:9050
    volumes:
      - /data/doris/be/storage/:/opt/apache-doris/be/storage/
      - /data/doris/be/script/:/docker-entrypoint-initdb.d/
    network_mode: host
    depends_on:
      - fe

#### case 
version: "3"
services:
  fe:
    image: apache/doris:fe-3.1.1
    container_name: doris-fe
    hostname: fe1
    environment:
      - FE_SERVERS=fe1:172.31.37.145:9010,fe2:172.31.39.114:9010,fe3:172.31.44.59:9010
      - FE_ID=1
    ports:
      - "8030:8030"  # HTTP
      - "9030:9030"  # MySQL
      - "9010:9010"  # heartbeat
    volumes:
      - /data/doris/fe/meta:/opt/apache-doris/fe/doris-meta
      - /data/doris/fe/log:/opt/apache-doris/fe/log
    network_mode: host

mysql -uroot -P9030 -h127.0.0.1

-- 注册 Follower FE
ALTER SYSTEM ADD FOLLOWER "fe2:172.31.39.114:9010";

-- 注册 Observer FE（可选）
ALTER SYSTEM ADD OBSERVER "fe3:172.31.44.59:9010";


version: "3"
services:
  fe:
    image: apache/doris:fe-3.1.1
    container_name: doris-fe
    hostname: fe2
    environment:
      - FE_SERVERS=fe1:172.31.37.145:9010,fe2:172.31.39.114:9010,fe3:172.31.44.59:9010
      - FE_ID=2
    ports:
      - "8030:8030"
      - "9030:9030"
    volumes:
      - /data/doris/fe/meta:/opt/apache-doris/fe/doris-meta
      - /data/doris/fe/log:/opt/apache-doris/fe/log
    network_mode: host


在三台机器都添加 BE 服务（同样用 docker-compose）：
```
version: "3"
services:
  be:
    image: apache/doris:be-3.1.1
    container_name: doris-be
    hostname: be
    environment:
      - FE_SERVERS=fe1:172.31.37.145:9010
      - BE_ADDR={HOST_IP}:9050
    ports:
      - "8040:8040"
      - "9050:9050"
    volumes:
      - /data/doris/be/storage:/opt/apache-doris/be/storage
      - /data/doris/be/log:/opt/apache-doris/be/log
    network_mode: host
```

其中 {HOST_IP} 分别替换为：
172.31.37.145
172.31.39.114
172.31.44.59


ALTER SYSTEM ADD BACKEND "172.31.37.145:9050";
ALTER SYSTEM ADD BACKEND "172.31.39.114:9050";
ALTER SYSTEM ADD BACKEND "172.31.44.59:9050";


SHOW FRONTENDS;
SHOW BACKENDS;

Web UI（FE HTTP 端口）：
浏览器访问
👉 http://172.31.37.145:8030
默认用户：root，无密码。

