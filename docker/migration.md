# gitlab迁移docker部署并版本升级

## Specific by Example

机器名 |	业务 |	系统 |	IP地址 |	配置
---- | ---- |---- |---- | ----
O |	旧gitlab(8.10.5) |	CentOS 6.5 |	172.16.17.91 |	4c/8G/1.2T
A |	新gitlab(9.2.2) |	CentOS 7.2 |	172.16.16.147 |	4c/8G/1T
B |	nginx(1.10.3) postgresql(9.6) redis(2.8.4)  haproxy(1.7.6) |	CentOS 7.2 |	172.16.16.148 |	4c/8G/200G

基本目录约束：
```sh
总目录：/home/data
docker-compose配置文件：/home/data/docker-compose.yml
docker数据：/home/data/gitlab/data
nginx：
    配置：/home/data/nginx/etc/sites
    ssl证书：/home/data/nginx/etc/ssl
    logs日志：/home/data/nginx/logs
haproxy配置文件：/home/data/haproxy/etc/haproxy.cfg
postgresql数据：/home/data/postgresql/data
redis数据：/home/data/redis/data
```

#### 1.基本环境准备
1.关闭SELinux和防火墙

机器A、B：
```sh
#防火墙
#关闭防火墙
systemctl stop firewalld
#禁止开机启动
systemctl disable firewalld
#SELinux
#关闭即时生效
setenforce 0
#永久有效
#修改/etc/selinux/config，“SELINUX=enforcing”修改为“SELINUX=disabled”，然后重启。
sed -i 's#SELINUX=enforcing#SELINUX=disabled#g' /etc/selinux/config
#重启生效修改
reboot
```

2.修改ssh登录端口

机器A、B：
```sh
#编辑配置文件
vi /etc/ssh/sshd_config
#改成8822端口
Port 8822
#重启ssh服务
systemctl restart sshd
```

#### 2.安装
1.docker安装
```sh
#安装
curl -sSL https://get.daocloud.io/docker | sh
#配置 Docker 加速器
curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://26109e56.m.daocloud.io
#启动docker
systemctl start docker
#加入开机启动docker
systemctl enable docker
```
2.docker-compose安装
```sh
curl -L https://get.daocloud.io/docker/compose/releases/download/1.13.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod a+x /usr/local/bin/docker-compose
```

3.docker镜像pull

机器A：
```sh
#因为迁移和升级是两个部分，所有需要pull两个版本，gitlab（https://github.com/sameersbn/docker-gitlab）
docker pull sameersbn/gitlab:8.10.5
docker pull sameersbn/gitlab:9.2.2
```
机器B：
```sh
#redis（https://github.com/sameersbn/docker-redis）
docker pull sameersbn/redis
#nginx（https://github.com/sameersbn/docker-nginx）
docker pull sameersbn/nginx
#postgresql（https://github.com/sameersbn/docker-postgresql）
docker pull sameersbn/postgresql:9.6-2
#haproxy（for gitlab ssh mode）
docker pull haproxy:1.7.6
```

#### 3.配置
1.机器B

docker-compose配置文件
```sh
nginx:
  restart: always
  image: sameersbn/nginx:latest
  volumes:
    - /home/data/nginx/etc/sites:/etc/nginx/conf.d:Z
    - /home/data/nginx/etc/ssl:/etc/nginx/ssl:Z
    - /home/data/nginx/logs:/var/log/nginx:Z
  ports:
    - "80:80"
    - "443:443"
postgresql:
  restart: always
  image: sameersbn/postgresql:9.6-2
  environment:
    - DB_USER=gitlab
    - DB_PASS=hamgua!@#gitlab
    - DB_NAME=gitlabhq_production
    - DB_EXTENSION=pg_trgm
  volumes:
    - /home/data/postgresql/data:/var/lib/postgresql:Z
  ports:
    - "5432:5432"
redis:
  restart: always
  image: sameersbn/redis:latest
  volumes:
    - /home/data/redis/data:/var/lib/redis:Z
  ports:
    - "6379:6379"
haproxy:
  restart: always
  image: haproxy:1.7.6
  volumes:
    - /home/data/haproxy/etc:/usr/local/etc/haproxy:Z
  ports:
    - "22:80"  
```

nginx配置：
```sh
upstream git-hamgua {
  server 172.16.16.147:10080 max_fails=3 fail_timeout=30s weight=1;
}
server {
  listen   80;
  listen   443 ssl;
  server_name git.hamgua.com;
  ssl_certificate       /etc/nginx/ssl/git.hamgua.cn.crt;
  ssl_certificate_key   /etc/nginx/ssl/git.hamgua.cn.key;
  ssl_protocols         TLSv1 TLSv1.1 TLSv1.2;
  ssl_prefer_server_ciphers on;
  ssl_ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AES:RSA+3DES:!ADH:!AECDH:!MD5:!DSS;
  ssl_session_cache     shared:SSL:10m;
  ssl_session_timeout   10m;
  location / {
    proxy_pass http://git-hamgua;
    proxy_redirect          off;
    #proxy_next_upstream  error timeout invalid_header http_500 http_502 http_503 http_504;
    proxy_next_upstream off;
    proxy_set_header        Host $host;
    proxy_set_header        X-Real-IP $remote_addr;
    proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    #proxy_set_header       Accept-Encoding  "";
    proxy_connect_timeout   300;
    proxy_send_timeout      300;
    proxy_read_timeout      300;
    proxy_buffer_size       64k;
    proxy_buffers           16 64k;
    proxy_busy_buffers_size 128k;
    proxy_temp_file_write_size 128k;
    proxy_redirect          default;
    proxy_ignore_client_abort on;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
  }
}
```

haproxy配置：
```sh
global
    pidfile /var/run/haproxy.pid
    maxconn 81920
    nbproc 10
    daemon
    quiet
defaults
    log global
    mode http
    option httplog
    option dontlognull
    retries 3
    option redispatch
    maxconn 10240
    timeout connect 5000ms
    timeout client 60000ms
    timeout server 60000ms
frontend git
    bind 0.0.0.0:80
    mode tcp
    default_backend gitlab-ssh
backend gitlab-ssh
    option tcpka
    balance roundrobin
    mode tcp
    server gitlab-ssh1 172.16.16.147:10022 weight 1 check port 10022 inter 1s rise 2 fall 2
```

2.机器A

docker-compose配置文件（8.10.5版本）
```sh
gitlab:
  restart: always
  image: sameersbn/gitlab:8.10.5
  ports:
    - "10080:80"
    - "10022:22"
  environment:
    #postgresql
    - DB_ADAPTER=postgresql
    - DB_HOST=172.16.16.148
    - DB_PORT=5432
    - DB_USER=gitlab
    - DB_PASS=hamgua!@#gitlab
    - DB_NAME=gitlabhq_production
    #redis
    - REDIS_HOST=172.16.16.148
    - REDIS_PORT=6379
    #global config
    - DEBUG=false
    - TZ=Asia/Beijing
    - GITLAB_TIMEZONE=Beijing
    - GITLAB_ROOT_EMAIL=hamgua@hamgua.com
    - GITLAB_SECRETS_DB_KEY_BASE=mjztzlfksTvRz5wNXjVDstTJZklGKDWsHX6Q9s55ZVc9v7TdGvDs3DHzFLxsKWsT
    - GITLAB_HOST=git.hamgua.com
    #ssl port
    - GITLAB_PORT=443
    #ssh port
    - GITLAB_SSH_PORT=22
    - GITLAB_HTTPS=true
    - GITLAB_NOTIFY_ON_BROKEN_BUILDS=true
    - GITLAB_NOTIFY_PUSHER=false
    - GITLAB_PAGES_ENABLED=true
    - GITLAB_PAGES_DOMAIN=git.hamgua.com
    - GITLAB_EMAIL=hamgua@hamgua.com
    - GITLAB_EMAIL_REPLY_TO=hamgua@hamgua.com
    - GITLAB_INCOMING_EMAIL_ADDRESS=hamgua@hamgua.com
    #backup
    - GITLAB_BACKUP_SCHEDULE=daily
    - GITLAB_BACKUP_TIME=01:00
    #smtp
    - SMTP_ENABLED=true
    - SMTP_DOMAIN=hamgua.com
    - SMTP_HOST=smtp.exmail.qq.com
    - SMTP_PORT=587
    - SMTP_USER=hamgua@hamgua.com
    - SMTP_PASS=hamgua
    - SMTP_STARTTLS=true
    - SMTP_AUTHENTICATION=plain
    - IMAP_ENABLED=false
  volumes:
    - /home/data/gitlab/data:/home/git/data:Z
```

#### 4.初始化和启动
1.docker初始化

机器B：
```sh
cd /home/data
docker-compose create nginx redis postgresql
```
机器A：
```sh
cd /home/data
docker-compose create gitlab
```
2.docker启动

(注意必须先启动机器B的redis、postgresql服务) 
机器B：
```sh
cd /home/data
docker-compose start nginx redis postgresql
```
机器A：
```sh
cd /home/data
docker-compose start gitlab
```




