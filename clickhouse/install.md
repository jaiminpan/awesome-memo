# Install

## Download

[Location](https://packagecloud.io/altinity/clickhouse)

Sample as version 1.1.54318-3 on CentOS7
  * clickhouse-server-common-1.1.54318-3.el7.x86_64.rpm	
  * clickhouse-server-1.1.54318-3.el7.x86_64.rpm
  * clickhouse-debuginfo-1.1.54318-3.el7.x86_64.rpm
  * clickhouse-compressor-1.1.54318-3.el7.x86_64.rpm
  * clickhouse-client-1.1.54318-3.el7.x86_64.rpm

## RPM install
  * rpm -ivh clickhouse-server-common-1.1.54318-3.el7.x86_64.rpm	
  * rpm -ivh clickhouse-server-1.1.54318-3.el7.x86_64.rpm
  * rpm -ivh clickhouse-client-1.1.54318-3.el7.x86_64.rpm
  * rpm -ivh clickhouse-compressor-1.1.54318-3.el7.x86_64.rpm

## Config Dir
/etc/clickhouse-server/

## Start
1. service clickhouse-server start
2. clickhouse-server --daemon --config-file=/etc/clickhouse-server/config.xml

## Client
```sh
clickhouse-client --host=xx.xx.xx.xx  --port=9001
:) show tables;
:) select now();
:) select 1;

```
