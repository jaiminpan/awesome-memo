# jumpserver
Sample for 2.6.1


```sh
# 升级系统
$ yum upgrade -y

# 安装依赖包
$ yum -y install gcc epel-release git

# (选配可跳过) 设置防火墙, 开放 80 端口给 nginx 访问, 开放 8080 端口给 coco 和 guacamole 访问
$ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.100" port protocol="tcp" port="80" accept"
$ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.40" port protocol="tcp" port="8080" accept"
$ firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.100.50" port protocol="tcp" port="8080" accept"
$ firewall-cmd --reload

# (选配可跳过) 安装 nginx
$ yum -y install nginx
$ systemctl enable nginx

# 安装 Python3.6
$ yum -y install python36 python36-devel

# 配置 py3 虚拟环境
$ python3.6 -m venv /opt/py3
$ source /opt/py3/bin/activate

# 下载 Jumpserver tag v2.6.1 到 /opt/jumpserver
$ cd /opt && git clone --depth=1 -b v2.6.1 https://github.com/jumpserver/jumpserver.git

# 安装依赖 RPM 包
$ yum -y install $(cat /opt/jumpserver/requirements/rpm_requirements.txt)

# 安装 Python 库依赖
$ pip install --upgrade pip setuptools
$ pip install -r /opt/jumpserver/requirements/requirements.txt

# 需要外部 redis 和 mysql 需要提前安装 mysql >= 5.7

# 修改 jumpserver 配置文件
$ cd /opt/jumpserver
$ cp config_example.yml config.yml

$ echo "# jumpserver config" >> ~/.bashrc
$ SECRET_KEY=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 50`  # 生成随机SECRET_KEY
$ echo "SECRET_KEY=$SECRET_KEY" >> ~/.bashrc
$ BOOTSTRAP_TOKEN=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 16`  # 生成随机BOOTSTRAP_TOKEN
$ echo "BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN" >> ~/.bashrc

$ sed -i "s/SECRET_KEY:/SECRET_KEY: $SECRET_KEY/g" /opt/jumpserver/config.yml
$ sed -i "s/BOOTSTRAP_TOKEN:/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/jumpserver/config.yml
$ sed -i "s/# DEBUG: true/DEBUG: false/g" /opt/jumpserver/config.yml
$ sed -i "s/# LOG_LEVEL: DEBUG/LOG_LEVEL: ERROR/g" /opt/jumpserver/config.yml
$ sed -i "s/# SESSION_EXPIRE_AT_BROWSER_CLOSE: false/SESSION_EXPIRE_AT_BROWSER_CLOSE: true/g" /opt/jumpserver/config.yml

$ echo -e "\033[31m 你的SECRET_KEY是 $SECRET_KEY \033[0m"
$ echo -e "\033[31m 你的BOOTSTRAP_TOKEN是 $BOOTSTRAP_TOKEN \033[0m"

```


```
$ vi config.yml

# 默认使用 sqlite3 

# mysql 样式
DB_ENGINE: mysql
DB_HOST: 192.168.100.100
DB_PORT: 3306
DB_USER: jumpserver
DB_PASSWORD: 你的数据库密码
DB_NAME: jumpserver

# postgres 样式
DB_ENGINE: postgresql
DB_HOST: 192.168.100.100
DB_PORT: 5432
DB_USER: jumpserver
DB_PASSWORD: 你的数据库密码
DB_NAME: jumpserver
```

使用 postgresql
需要
yum install postgresql-devel
pip install psycopg2

## Q:ImportError: cannot import name 'byte_string'
```
pip uninstall pycrypto
pip uninstall pycryptodome
pip install pycryptodome
```

```

# 修改 nginx 配置文件(如果无法正常访问, 请注释掉 nginx.conf 的 server 所有字段)
$ vi /etc/nginx/conf.d/jumpserver.conf

server {
    listen 80;

    client_max_body_size 100m;  # 录像上传大小限制

    location /media/ {
        add_header Content-Encoding gzip;
        root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
    }

    location /static/ {
        root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
    }

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```
# nginx 测试并启动, 如果报错请按报错提示自行解决
$ nginx -t
$ systemctl start nginx
```

## 启动运行 Jumpserver
```
$ cd /opt/jumpserver
$ ./jms start all  # ./jms start|stop|status all 后台运行请添加 -d 参数
# 访问 http://192.168.100.30 默认账号: admin 密码: admin

# 多节点部署, 请参考此文档, 设置数据库时请选择从库, 其他的一样

## 或者配置成服务
wget -O /usr/lib/systemd/system/jms.service https://demo.jumpserver.org/download/shell/centos/jms.service
chmod 755 /usr/lib/systemd/system/jms.service
systemctl enable jms
systemctl enable start
```

## koko
支持终端管理，默认port为2222
```
wget https://github.com/jumpserver/koko/releases/download/v2.6.1/koko-v2.6.1-linux-amd64.tar.gz

cp config_example.yml config.yml
vim config.yml  # BOOTSTRAP_TOKEN 需要从 jumpserver/config.yml 里面获取, 保证一致
./koko
```

## guacamole
```
$ cd /opt
$ git clone --depth=1 -b v2.1.0  https://github.com/jumpserver/docker-guacamole-v1
$ cd /opt/docker-guacamole
$ tar xf guacamole-server-1.0.0.tar.gz
$ cd /opt/docker-guacamole/guacamole-server-1.0.0

# 根据 http://guacamole.apache.org/doc/gug/installing-guacamole.html 文档安装对应的依赖包
$ ./configure --with-init-dir=/etc/init.d
$ make
$ make install
```

#### 访问 https://mirror.bit.edu.cn/apache/tomcat/tomcat-9/v9.0.35/bin/apache-tomcat-9.0.35-fulldocs.tar.gz 下载最新的 tomcat9（tomcat随时有更新，下面命令中请自行更改）


```
$ mkdir -p /opt/guacamole /opt/guacamole/lib /opt/guacamole/extensions /opt/guacamole/data/log/
$ cd /opt

$ wget http://mirrors.tuna.tsinghua.edu.cn/apache/tomcat/tomcat-9/v9.0.22/bin/apache-tomcat-9.0.22.tar.gz
$ tar xf apache-tomcat-9.0.22.tar.gz
$ mv apache-tomcat-9.0.22 tomcat9
$ rm -rf /opt/tomcat9/webapps/*

$ sed -i 's/Connector port="8080"/Connector port="8081"/g' /opt/tomcat9/conf/server.xml
$ echo "java.util.logging.ConsoleHandler.encoding = UTF-8" >> /opt/tomcat9/conf/logging.properties
$ ln -sf /opt/docker-guacamole/guacamole-1.0.0.war /opt/tomcat9/webapps/ROOT.war
$ ln -sf /opt/docker-guacamole/guacamole-auth-jumpserver-1.0.0.jar /opt/guacamole/extensions/guacamole-auth-jumpserver-1.0.0.jar
$ ln -sf /opt/docker-guacamole/root/app/guacamole/guacamole.properties /opt/guacamole/guacamole.properties
$ wget https://github.com/ibuler/ssh-forward/releases/download/v0.0.5/linux-amd64.tar.gz
$ tar xf linux-amd64.tar.gz -C /bin/
$ chmod +x /bin/ssh-forward


# 设置 guacamole 环境
$ export JUMPSERVER_SERVER=http://127.0.0.1:8080  # http://127.0.0.1:8080 指 jumpserver 访问地址
$ echo "export JUMPSERVER_SERVER=http://127.0.0.1:8080" >> ~/.bashrc

# BOOTSTRAP_TOKEN 为 Jumpserver/config.yml 里面的 BOOTSTRAP_TOKEN 值
$ export BOOTSTRAP_TOKEN=******
$ echo "export BOOTSTRAP_TOKEN=******" >> ~/.bashrc
$ export JUMPSERVER_KEY_DIR=/opt/guacamole/keys
$ echo "export JUMPSERVER_KEY_DIR=/opt/guacamole/keys" >> ~/.bashrc
$ export GUACAMOLE_HOME=/opt/guacamole
$ echo "export GUACAMOLE_HOME=/opt/guacamole" >> ~/.bashrc

$ /etc/init.d/guacd start
$ sh /opt/tomcat9/bin/startup.sh
```

## luna 终端控制台
wget  https://github.com/jumpserver/luna/releases/download/v2.6.1/luna-v2.6.1.tar.gz

## lina 管理后台
wget https://github.com/jumpserver/lina/releases/download/v2.6.1/lina-v2.6.1.tar.gz

## nginx
```
[root@xyw-dev opt]# cd /usr/local/nginx/conf/
[root@xyw-dev conf]# ls
fastcgi.conf            koi-utf             nginx.conf           uwsgi_params
fastcgi.conf.default    koi-win             nginx.conf.default   uwsgi_params.default
fastcgi_params          mime.types          scgi_params          win-utf
fastcgi_params.default  mime.types.default  scgi_params.default
[root@xyw-dev conf]# mkdir conf.d
[root@xyw-dev conf]# cd conf.d/
[root@xyw-dev conf.d]# vim jumpserver.conf
[root@xyw-dev conf.d]# ls
jumpserver.conf
[root@xyw-dev conf.d]# cat jumpserver.conf
server {
    listen 80;
    # server_name _;
    server_name bastion.qf.com;

    client_max_body_size 100m;  # 录像及文件上传大小限制

    location /ui/ {
        try_files $uri / /index.html;
        alias /opt/lina/;  # lina 路径 管理后台
        expires 24h;
    }

    location /luna/ {
        try_files $uri / /index.html;
        alias /opt/luna/;  # luna 路径 控制台
        expires 24h;
    }

    location /media/ {
        add_header Content-Encoding gzip;
        root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
    }

    location /static/ {
        root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
        expires 24h;
    }

    location /koko/ {
        proxy_pass       http://localhost:5000;
        proxy_buffering off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        access_log off;
    }

    location /guacamole/ {
        proxy_pass       http://localhost:8081/;
        proxy_buffering off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $http_connection;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        access_log off;
    }

    location /ws/ {
        proxy_pass http://localhost:8070;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        access_log off;
    }

    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /core/ {
        proxy_pass http://localhost:8080;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        rewrite ^/(.*)$ /ui/$1 last;
    }
}

```
