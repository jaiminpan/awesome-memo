# Zabbix install

## Install on CentOS with PostgreSQL
software | version
---- | ----
centos | 6.8
zabbix | 3.4.1
postgres | 9.6

### Install PostgreSQL 
Reference [Install Guide](https://github.com/jaiminpan/fast-memo/blob/master/PostgreSQL/install.md)

### Install Zabbix
Download From https://www.zabbix.com/download

#### Install package
```
zabbix-server-pgsql
```

#### Prepared DB
```
CREATE USER zabbix;
CREATE DATABASE zabbix OWNER zabbix;
```
Import data to postgresql
```
cd /usr/share/doc/zabbix-server-pgsql-3.0.4/
zcat create.sql.gz | psql -U zabbix -d zabbix
```

Adjust the /etc/zabbix/zabbix_server.conf, adding:
```
DBUser=zabbix
DBPort=5432
DBHost=localhost
```
