# Install

## Install 5.6 On CentOS

#### List what already installed
```
yum list installed | grep php  
```
#### Remove them
```
yum remove php.x86_64 php-cli.x86_64 php-common.x86_64 \
    php-gd.x86_64 php-ldap.x86_64 \
    php-mbstring.x86_64 php-mcrypt.x86_64 \
    php-mysql.x86_64 php-pdo.x86_64  
```

#### Config new `yum` source

追加CentOS 6.5的epel及remi源。
```
# rpm -Uvh http://ftp.iij.ad.jp/pub/linux/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm

# rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
```

以下是CentOS 7.0的源。
```
# yum install epel-release

# rpm -ivh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
```
使用yum list命令查看可安装的包(Packege)。
```
# yum list --enablerepo=remi --enablerepo=remi-php56 | grep php
```

### Install PHP5.6.x
```
# yum install --enablerepo=remi --enablerepo=remi-php56 \
    php php-opcache \
    php-devel php-mbstring \
    php-gd php-bcmath php-ldap \
    php-mcrypt \
    php-mysqlnd php-phpunit-PHPUnit \
    php-pecl-xdebug php-pecl-xhprof
# php --version
```

```
# for postgresql connection
yum install --enablerepo=remi --enablerepo=remi-php56 php-pgsql
```

#### Install PHP-fpm
```
yum install --enablerepo=remi --enablerepo=remi-php56 php-fpm  
```

