# Replication

(version > pg10)

## Step 0
#### 主库检查 postgres.conf
```
wal_level = replica
```

## Step 1
##### CREATE USER
> CREATE ROLE repadmin login replication encrypted password 'pwd'

##### MODIFY `pg_hba.conf`
```
host    replication     repadmin        10.0.0.0/16      md5
```
reload conf
> systemctl reload xxx.service

```
cp /usr/pgsql-11/share/recovery.conf.sample   /PATH/TO/PGDATA/recovery.done
chown postgres:postgres recovery.done
chmod 600 recovery.done
```

vi recovery.done
```
standby_mode = on
primary_conninfo = 'host=10.0.xx.xx port=xxx user=repadmin password=pwd'
```

## Step 2
####  生成备库
```
mkdir /data/appdatas/pgsql/data_xx
chown postgres /data/appdatas/pgsql/data_xx
chmod 700 /data/appdatas/pgsql/data_xx
  
export PGPASSWORD="pwd"
pg_basebackup -D /data/appdatas/pgsql/11/dataxx -Fp -P -X stream -v -h 10.0.x.x -p xxx -U repadmin
```

## Step 3
#### 主库操作
> select * from pg_create_physical_replication_slot('rep_slot_1');


## 备库操作  
mv recovery.done recovery.conf
vi recovery.conf
```
primary_slot_name = 'rep_slot_1'
```

option 修改 postgresql.conf
```
hot_standby_feedback = on
```

## Step 4
#### 启动备库
> /usr/pgsql-11/bin/pg_ctl start -D dataxx







