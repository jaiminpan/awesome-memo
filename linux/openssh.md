

## 背景介绍
很多公司都使用静态密码+动态密码的方式登陆跳板机，某些还会强制一个动态密码只能登陆一次，于是我们面临着等一分钟才能登陆一次跳板机，很不方便。本文介绍一种在本机的设置，免除每次输入密码的方法。

## 实现方法
此功能是利用SSH的ControlPersist特性，SSH版本必须是5.6或以上版本才可使用ControlPersist特性。升级SSH可参考CentOS6下升级OpenSSH至7.1一文。


```sh
# vi ~/.ssh/config

Host *
    ControlMaster auto
    ControlPersist 4h
    # ControlPersist yes
    ControlPath   ~/.ssh/sessions/ctrl:%h:%p:%r
    # Compression yes


```

```
# Check
ssh -O check HostName

# Exit
ssh -O exit HostName
```


### Other Config

```sh
# vi ~/.ssh/config, mod 600

Host jpserver
User testa
Hostname 10.100.3.80
PreferredAuthentications publickey
IdentityFile /Users/xxx/.ssh/abc.pem

Host fileserver
User centos
Port 22
Hostname 10.81.23.81
#ProxyCommand  ssh nixcraft@gateway.uk.cyberciti.biz nc %h %p 2> /dev/null
```