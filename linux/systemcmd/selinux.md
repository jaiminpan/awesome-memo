SELinux
==========

关于linux权限控制目前碰到有三种：
 * 文件系统权限 lsattr chattr
 * 用户组 user:group:other
 * SELiunx

一般情况下我们只会和用户组权限打交道，一般用chmod chown这两个命令做权限控制，这个也叫 DAC （Discretionary Access Control）”任意式读取控制”。
（DAC权限方式，我的理解就是静态的权限控制，对比于SELinux 我看作动态的权限控制）。

如果你已经获取root权限，也无法修改删除响应的文件时，考虑用lsattr查看对应的文件，并用chattr修改。
这种方式是文件系统对权限进行了限制，只有一部分文件系统支持，如ext3，ext4等。系统被黑了以后才知道的，说多了都是泪。

SELinux是后期的Linux系统才有的权限控制方式，在同一个用户下面，通过不同的进程拥有不同标签组，才有权限访问对应的标签组的文件。
也叫 MAC （Mandatory Access Control）“强制性读取控制”。   
通过ps –Z 和 ls –Z查看对应的标签组，用chcon -u|-r|-t 修改对应的用户、角色、类型。

简单用法   
```
  setenforce 0/1     0 表示允许；1 表示强制
  getenforce        查看当前SElinux的状态
```

详见下面链接   
http://blog.chinaunix.net/uid-21266384-id-186394.html   
http://vbird.dic.ksu.edu.tw/linux_basic/0440processcontrol_5.php   
https://wiki.centos.org/zh/HowTos/SELinux   
