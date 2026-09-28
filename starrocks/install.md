# 手动安装 Starrocks/doris

# 修改配置文件。所有be的机器

```
cat >> /etc/sysctl.conf << EOF
vm.swappiness=0
EOF
// 使修改生效。
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


cat >> /etc/sysctl.conf << EOF
vm.max_map_count = 2000000
EOF

> vi /etc/profile
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```


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

存算分离配置
```
run_mode = shared_data
cloud_native_meta_port = <meta_port>
cloud_native_storage_type = S3

# 例如 testbucket/subpath
aws_s3_path = <s3_path>

# 例如 us-west-2
aws_s3_region = <region>

aws_s3_access_key = <access_key>
aws_s3_secret_key = <secret_key>
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


ALTER SYSTEM ADD COMPUTE NODE "172.31.37.145:9050";
SHOW COMPUTE NODES;


````
// 额外建立默认卷
CREATE STORAGE VOLUME def_volume
TYPE = S3
LOCATIONS = ("s3://dev-starrocks-data")
PROPERTIES
(
    "enabled" = "true",
    "aws.s3.region" = "ap-southeast-1",
    "aws.s3.endpoint" = "https://s3.ap-southeast-1.amazonaws.com",
    "aws.s3.use_aws_sdk_default_behavior" = "false",
    "aws.s3.use_instance_profile" = "false",
    "aws.s3.access_key" = "xxxxxxxxxx",
    "aws.s3.secret_key" = "yyyyyyyyyy",
    "aws.s3.enable_partitioned_prefix" = "true"
);

SET def_volume AS DEFAULT STORAGE VOLUME;

SHOW STORAGE VOLUMES;

DESC STORAGE VOLUME def_volume;


DROP STORAGE VOLUME IF EXISTS vol_test2;

````

````
CREATE DATABASE lakes; ## 创建数据库
use lakes; ## 选择数据库
CREATE TABLE lakes.t_record_stream_detail (
   event_time   DATETIME NOT NULL,
   uid          VARCHAR(64) NOT NULL,
   order_id     VARCHAR(64) NOT NULL DEFAULT '',
   once_id      VARCHAR(64) NOT NULL DEFAULT '' ,
   channel      VARCHAR(64) NOT NULL DEFAULT '',
   once_ts      BIGINT NOT NULL,
   once_type    INTEGER NOT NULL ,
   data         TEXT NOT NULL,
   ext_data     VARCHAR(65533)
)
PRIMARY KEY (event_time, uid, order_id, once_id)
PARTITION BY date_trunc('day', event_time)
DISTRIBUTED BY HASH(uid)
PROPERTIES (
    "storage_volume" = "def_volume",
    "bloom_filter_columns" = "uid, order_id, once_id",
    "replication_num" = "1",
    "datacache.enable" = "true",
    "datacache.partition_duration" = "7 DAY"
);

# 建立同步kafka任务 
CREATE ROUTINE LOAD load_detail
ON t_record_stream_detail
COLUMNS (
  uid,
  channel,
  once_ts,
  order_id,
  once_id,
  once_type,
  data,
  event_time = from_unixtime(once_ts / 1000),
  ext_data
)
PROPERTIES (
    "format" = "json",
    "max_batch_rows" = "200000",
    "max_batch_interval" = "30",
    "strip_outer_array" = "false",
    "strict_mode" = "false",
    "max_error_number" = "100"
)
FROM KAFKA (
    "kafka_broker_list" = "172.31.36.4:9092",
    "kafka_topic" = "detail",

    "property.group.id" = "doris_grp",
    "property.auto.offset.reset" = "latest"
);

SHOW ROUTINE LOAD;

PAUSE ROUTINE LOAD FOR load_transaction_record;
RESUME ROUTINE LOAD FOR [db_name.]<job_name>;


-- SHOW PARTITIONS FROM t_record_stream_detail;
-- ALTER TABLE t_record_stream_detail DROP PARTITION p20240101;
-- ALTER TABLE t_record_stream_detail_archive ADD PARTITION p20240101
-- VALUES [('2024-01-01'), ('2024-01-02')];


CREATE MATERIALIZED VIEW t_record_stream_hourly_mv
PARTITION BY date_trunc('day', event_time)
DISTRIBUTED BY HASH(uid) 
REFRESH ASYNC
AS
SELECT
    DATE_TRUNC('hour', event_time) AS hour_time,
    uid,
    channel,
    SUM(val_amount) AS total_val,
    SUM(agg_amount) AS total_agg,
FROM game_lakes.t_record_stream_player_game_detail
GROUP BY
    DATE_TRUNC('hour', event_time),
    uid,
    channel;


CREATE MATERIALIZED VIEW t_record_stream_5min_mv
PARTITION BY date_trunc('day', event_time)
DISTRIBUTED BY HASH(uid)
REFRESH ASYNC
AS
SELECT
    date_trunc('minute', event_time) - (extract(minute from event_time)::int % 5) * interval '1 minute'
        AS minute_5_time,
    uid,
    channel,
    SUM(val_amount) AS total_val,
    SUM(agg_amount) AS total_agg
FROM game_lakes.t_record_stream_player_game_detail
GROUP BY
    date_trunc('minute', event_time) - (extract(minute from event_time)::int % 5) * interval '1 minute',
    uid,
    channel;

````


