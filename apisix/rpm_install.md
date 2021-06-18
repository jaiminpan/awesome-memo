# rpm_install

APISIX 是基于 OpenResty + etcd 实现的云原生、高性能、可扩展的微服务 API 网关

* OpenResty：通过 Lua 扩展 NGINX 实现的可伸缩的 Web 平台。
* etcd：Key/Value 存储系统。

## 快速安装

#### 1.1 安装 OpenResty
```sh
# 安装 OpenResty 的 YUM 软件源
$ yum install yum-utils
$ yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo

# 安装 OpenResty 软件
$ yum install -y openresty 
```

#### 1.2 安装 etcd
安装 etcd，使用如下命令：
```sh
# 安装 etcd
$ yum install -y etcd

# 启动 etcd
$ service etcd start
```

#### 1.3 安装 APISIX
安装 APISIX，使用如下命令：

友情提示：这里我们安装的 APISIX 的版本是 1.2 版本。
最新版本的，可以从《APISIX 官方文档 —— 构建 Apache APISIX》获取。
```sh
# 安装 APISIX
$ yum install -y https://github.com/apache/incubator-apisix/releases/download/1.2/apisix-1.2-0.el7.noarch.rpm

# 启动 APISIX
$ apisix start
```

此时，APISIX 安装在 /usr/local/apisix/ 目录，使用如下命令：
```sh
$ cd /usr/local/apisix/
$ ls -ls
total 40
4 drwxr-xr-x 8 root   root 4096 May  1 20:40 apisix # APISIX 程序
4 drwx------ 2 nobody root 4096 May  1 20:44 client_body_temp
4 drwxr-xr-x 3 root   root 4096 May  1 20:50 conf # 配置文件
4 drwxr-xr-x 6 root   root 4096 May  1 20:40 dashboard # APISIX 控制台
4 drwxr-xr-x 5 root   root 4096 May  1 20:40 deps
4 drwx------ 2 nobody root 4096 May  1 20:44 fastcgi_temp
4 drwxrwxr-x 2 root   root 4096 May  1 20:44 logs # 日志文件
4 drwx------ 2 nobody root 4096 May  1 20:44 proxy_temp
4 drwx------ 2 nobody root 4096 May  1 20:44 scgi_temp
4 drwx------ 2 nobody root 4096 May  1 20:44 uwsgi_temp
```
默认情况下，APISIX 启动在 9080 端口，使用如下命令：
```sh
$ curl http://127.0.0.1:9080/
{"error_msg":"failed to match any routes"}
```

## 2. APISIX 控制台
APISIX 内置控制台功能，方便我们进行 APISIX 的 Route、Consumer、Service、SSL、Upstream 的查看与维护。如下图所示

APISIX 控制台

在 /usr/local/apisix/conf/nginx.conf 配置文件中，设置了 APISIX 控制台的访问路径为 /apisix/dashboard。如下图所示：
```sh
location /apisix/dashboard {
  allow 127.0.0.0/24;
  deny all;

  alias dashboard/;
  try_files $uri $uri/index.html /index.html;
}
```


APISIX 控制台 - 配置

友情提示：如果胖友是安装 APISIX 在本机上，可以不执行如下步骤。

考虑到安全性，APISIX 控制台只允许本机访问，因此我们需要修改 /usr/local/apisix/conf/config.yaml 配置文件，增加允许访问的远程 IP 地址。

配置参考
```sh 
apisix:
      allow_admin:                  # 参考
        - 10.4.0.0/24              # 设置你可以访问的ip段
        - 127.0.0.0/16
        - 127.16.48.0/24
      admin_key:
        -
          name: "admin"
          key: edd1c9ff63512fc8f1 
          role: admin
        -
          name: "viewer"
          key: 40334cf04fe33476a2 
          role: admin

    conf:
      listen:
        host: 10.4.6.211 # 把127.0.0.1改成当前安装apisix-dashboar的主机的ip
        port: 8081 # 端口
      etcd:
        endpoints: # supports defining multiple etcd host addresses for an etcd cluster
          - 127.0.0.1:2379
      log:
        error_log:
          level: warn # supports levels, lower to higher: debug, info, warn, error, panic, fatal
          file_path:
            logs/error.log # supports relative path, absolute path, standard output
            # such as: logs/error.log, /tmp/logs/error.log, /dev/stdout, /dev/stderr
    authentication:
      secret:
       secret # secret for jwt token generation.
        # NOTE: Highly recommended to modify this value to protect `manager api`.
        # if it's default value, when `manager api` start , it will generate a random string to replace it.
      expire_time: 3600 # jwt token expire time, in second
      users:
        - username: admin # username and password for login `manager api`
          password: admin
        - username: user
          password: user
```
APISIX 控制台 - 修改配置

修改完配置后，使用 `apisix restart` 命令，重启 APISIX 来生效配置。然后，使用浏览器访问 http://172.16.48.185:9080/apisix/dashboard 地址，进入 APISIX 控制台。

APISIX 控制台 - 登陆

使用默认的**「admin/123456」**账号，登陆 APISIX 控制台。

APISIX 控制台 - 首页

友情提示：APISIX 控制台是通过调用 APISIX 提供的管理 API 来实现的，所以可以看看《APISIX 官方文档 —— 管理 API》


