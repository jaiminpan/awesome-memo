Docker
=================

Usage
-----------------
Install the most recent version of the Docker Engine for your platform using the official Docker releases, which can also be installed using:
```
# This script is meant for quick & easy install via:
  'curl -sSL https://get.docker.com/ | sh'
# or:
  'wget -qO- https://get.docker.com/ | sh'
```


Reference
--------------
https://github.com/widuu/chinese_docker/tree/master/userguide

Books
------------
[Docker —— 从入门到实践](https://www.gitbook.com/book/yeasy/docker_practice)


### docker
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

### docker-compose
```sh
curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod a+x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin
```

```sh
# 创建网络
docker network create app-network
```