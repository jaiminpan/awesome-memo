# Install

Reference: http://www.rstudio.com/products/rstudio/download-server/

## Step On CentOS 7

#### Install
```sh
$ sudo yum -y install R

$ wget https://download2.rstudio.org/rstudio-server-rhel-1.0.143-x86_64.rpm
$ sudo yum install --nogpgcheck rstudio-server-rhel-1.0.143-x86_64.rpm
```

Now visit http://<machine_ip>:8787

#### Post config Firewall (option)
```
vi /etc/sysconfig/iptables
-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
+ -A INPUT-m state --state NEW -m tcp -p tcp --dport 8787 -j ACCEPT
```

## Login

change config
```
vi /etc/rstudio/rserver.conf
auth-required-user-group=rstudio_users
```

Add user
```
useradd ruser
passwd ruser

usermod -a -G rstudio_users ruser
```

Now you can login using the user in groups rstudio_users by http://<machine_ip>:8787



