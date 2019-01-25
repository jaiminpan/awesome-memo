# Consul install

## Install Sample
Example As `consul_1.4.1_linux_amd64.zip`

### Download 
Download From [Office Website](https://www.consul.io/downloads.html)  
#### OR  
Compile with [Github](https://github.com/hashicorp/consul)  

### Install Binary
```sh

unzip consul_1.4.1_linux_amd64.zip # Extract to consul

mv consul /usr/local/bin

```

### Config Dir
config Location is `/etc/consul.d/config.json` OR `/data/etc/consul.d/config.json`  
Reference file `consul.d/config.json`

## Start
consul agent -config-dir=/data/etc/consul.d

## Web Visit
http://ip:port/  
http://127.0.0.1:8500/  


## Other Config Guide
https://www.consul.io/docs/agent/options.html#command-line-options
https://my.oschina.net/guol/blog/353391
https://www.cnblogs.com/sunsky303/p/9209024.html
