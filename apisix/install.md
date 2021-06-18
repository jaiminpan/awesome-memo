# apisix install
api网管系统。

https://github.com/apache/apisix/

#### 安装准备

打开github官网
https://github.com/apache/apisix/ 下找到 Get Started (官网一直在变动)

#### 源码安装
参考 https://github.com/apache/apisix/

#### 1 安装依赖
https://github.com/apache/apisix/blob/master/docs/en/latest/install-dependencies.md

```sh
# install etcd
wget https://github.com/etcd-io/etcd/releases/download/v3.4.13/etcd-v3.4.13-linux-amd64.tar.gz
tar -xvf etcd-v3.4.13-linux-amd64.tar.gz && \
    cd etcd-v3.4.13-linux-amd64 && \
    sudo cp -a etcd etcdctl /usr/bin/

# add OpenResty source
sudo yum install yum-utils
sudo yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo

# install OpenResty and some compilation tools
sudo yum install -y openresty curl git gcc openresty-openssl111-devel unzip

# install LuaRocks
curl https://raw.githubusercontent.com/apache/apisix/master/utils/linux-install-luarocks.sh -sL | bash -

# start etcd server
nohup etcd &
```

#### 2 安装apisix
https://github.com/apache/apisix/

```sh
# 下载源码
$ mkdir apisix-2.3
$ wget https://downloads.apache.org/apisix/2.3/apache-apisix-2.3-src.tgz
$ tar zxvf apache-apisix-2.3-src.tgz -C apisix-2.3

# 安装依赖包
$ make deps

# 检查版本
$ ./bin/apisix version

# 启动服务
$ ./bin/apisix start
```

#### 3 安装dashboard
https://github.com/apache/apisix-dashboard

https://github.com/apache/apisix-dashboard/blob/master/docs/en/latest/deploy.md
```sh
# web依赖安装
# node安装
https://nodejs.org/en/download/

# yarn 安装
https://yarnpkg.com/getting-started/install

# 克隆工程
git clone -b v2.4 https://github.com/apache/apisix-dashboard.git

# 编译
cd apisix-dashboard
make build

# 启动服务
cd output
./manager-api
nohup ./manager-api &
```

#### 4 测试
配置端口为9000
http://127.0.0.1:9000/

如果要让外网访问的话

修改conf/config.yaml文件

修改listen 端口为 0.0.0.0:9000

修改allow ip 加上你自己的IP地址

* dashboard 的操作流程说明 *
https://blog.csdn.net/weixin_44096325/article/details/110230011
修改


配置参考
```sh 
apisix:
      allow_admin:                  # 参考
        - 10.4.0.0/24              # 设置你可以访问的ip段
        - 127.0.0.0/16
      admin_key:
        -
          name: "admin"
          key: admin 
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