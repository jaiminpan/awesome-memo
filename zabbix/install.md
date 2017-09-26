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
#### Install Web
Zabbix Web is written by php.
To install web just by copy `zabbix/frontends/php` directory from source code and config nginx  
** Upgrade php to 5.6 **  
Reference [php5.6 Install Guide](https://github.com/jaiminpan/fast-memo/blob/master/php/install.md)


## Source Code Install
Reference [Official Webpage](https://www.zabbix.com/documentation/3.4/manual/installation/install)
### Download Source Code
Go to the [Zabbix Download Page](https://www.zabbix.com/download)
```
tar xvfz zabbix-3.4.0.tar.gz
```
### Create user account
```
useradd zabbix
```

### Compile & install
```
./configure --prefix=/usr/local/zabbix/3.4 \
  --enable-server \
  --enable-agent \
  --with-postgresql \
  --enable-ipv6 \
  --with-net-snmp \
  --with-libcurl \
  --with-libxml2
```


## Other Installation Guide
https://yq.aliyun.com/articles/9091




