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


Docker In Github
---------------
* Gitlab, PostgreSQL, MySQL, MongoDB and etc  
  https://github.com/sameersbn/  

Gitlab Docker Sample:
---------------
According to [Guilding](https://github.com/sameersbn/docker-gitlab)  
Note: 
* The alias of the postgresql server container should be set to **postgresql** while linking with the gitlab image.
* The alias of the redis server container should be set to **redisio** while linking with the gitlab image.
* If host (pg or redis server) is not reachable inside Gitlab docker, use **`iptables -t filter -A DOCKER -d 172.17.0.0/16 -i docker0 -o docker0 -j ACCEPT`**


Reference
--------------
https://github.com/widuu/chinese_docker/tree/master/userguide

Books
------------
[Docker —— 从入门到实践](https://www.gitbook.com/book/yeasy/docker_practice)
