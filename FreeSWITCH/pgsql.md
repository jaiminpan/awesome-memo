# Pgsql

## Enable Pgsql

```sh
./configure --enable-core-pgsql-support
```

安装后需要修改的配置文件

freeswitch默认每个程序都有一个数据库。根据自己需要，将不通程序对于的配置文件修改即可。 
大概有以下文件需要修改 
* switch.conf.xml //核心表 
* db.conf.xml //核心表 
* voicemail.conf.xml //留言相关的表 
* internal.xml // 
* external.xml // 
* cdr_pg_csv.conf.xml //通话记录 
* fifo.conf.xml //fifo相关的表 
* callcenter.conf.xml //callcenter程序相关的表。

```xml
<param name="odbc-dsn" value="pgsql://hostaddr=0.0.0.0 port=5432 dbname=fs_db user=fs_dba password='123456'"/>
```


#### cdr

在 modules.conf 中开启 mod_cdr_pg_csv
```sh
  # vi modules.conf
  event_handlers/mod_cdr_pg_csv
```

修改 cdr_pg_csv.conf.xml
```xml
<param name="db-info" value="host=0.0.0.0 port=5432 user=fs_dba password=*dbname=fs_db connect_timeout=10" />
```

手动创建
```sql
create table cdr (
    id                        serial primary key,
    local_ip_v4               inet not null,
    caller_id_name            varchar,
    caller_id_number          varchar,
    destination_number        varchar not null,
    context                   varchar not null,
    start_stamp               timestamp with time zone not null,
    answer_stamp              timestamp with time zone,
    end_stamp                 timestamp with time zone not null,
    duration                  int not null,
    billsec                   int not null,
    hangup_cause              varchar not null,
    uuid                      uuid not null,
    bleg_uuid                 uuid,
    accountcode               varchar,
    read_codec                varchar,
    write_codec               varchar,
    sip_hangup_disposition    varchar,
    ani                       varchar
);
```
