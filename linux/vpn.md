# VPN on Linux
隧道协议PPTP、L2TP、IPSec和SSLVPN

# PPTP协议
## Client

### Prepare
pppd 一般系统自带。
pptp
pptp-setup

```
yum install ppp
yum install pptp
yum install pptp-setup

# turn on: pon -> /usr/shared/doc/ppp-2.4.5/scripts/pon
# turn off: poff -> /usr/shared/doc/ppp-2.4.5/scripts/poff 
ln -s /usr/shared/doc/ppp-2.4.5/scripts/pon /usr/sbin/
ln -s /usr/shared/doc/ppp-2.4.5/scripts/poff /usr/sbin/
chmod a+x /usr/sbin/pon
chmod a+x /usr/sbin/poff
```

### Configure
```
# pptpsetup –help
pptpsetup –create <TUNNEL> –server <SERVER> [--domain <DOMAIN>]
          –username <USERNAME> [--password <PASSWORD>]
          [--encrypt] [--start]
Options:
* <TUNNEL>  配置文件的名称，可以根据不同的连接用不同的名字，自已指定，我这里有vpn.
* <SERVER>  PPTP SERVER的IP。
* <DOMAIN> 所在的域，可以省略，一般不用。
* <USERNAME>  VPN 上认证用的用户名，VPN用户
* <PASSWORD>  VPN上用户认证用的密码
* –encrypt 启用加密
*           当没使用–encrypt 连接时出现下面的错误时，表示使用了加密，这点也可以和VPN的管理员联系确认一下，遇到下面的
*           情况可以加上该参数。
*                    CHAP authentication succeeded
*                          LCP terminated by peer (ZM-76-^@<M-Mt^@^@^BM-f ) 
*                            
* –start  直接连接，第一次使用。
```
#### Sample 
假设VPN的用户名: tuser 密码: ptest, IP是：xxx.xxx.xxx.xx, vpn命名为myvpn
```
# option 1: 创建vpn并直接连接
> pptpsetup –create myvpn –server XXX.XXX.XXX.XX  –username utest –password ptest –encrypt –start

# option 2: 创建vpn，之后在连接
> pptpsetup –create myvpn –server XXX.XXX.XXX.XX  –username utest –password ptest –encrypt
> pon myvpn
```

在正常连接后，ifconfig 会发现多了一个网卡的device，如ppp0, 说明vpn已经建立。  
如果不能访问vpn内的机器，请参考 route 配置转发。  
```
ppp0      Link encap:Point-to-Point Protocol  
          inet addr:192.168.0.151  P-t-P:192.168.0.150  Mask:255.255.255.255
          UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1496  Metric:1
          RX packets:17 errors:0 dropped:0 overruns:0 frame:0
          TX packets:17 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:3 
          RX bytes:996 (996.0 b)  TX bytes:1002 (1002.0 b)
```

#### route
如果VPN的机器所在网段是192.168.0.0/24，用下面命令配置转发：
```
> route add -net 192.168.0.0 netmask 255.255.255.0 gw 192.168.0.150	device ppp0

> rount -nNvee
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface    MSS   Window irtt
...
192.168.0.150   0.0.0.0         255.255.255.255 UH    0      0        0 ppp0     0     0      0
192.168.0.0     192.168.0.150   255.255.255.0   UG    0      0        0 ppp0     0     0      0
...
```

#### Detail

执行pptpsetup后，会在 `/etc/ppp/chap_secrets` 中保存vpn的相关信息，在 `/etc/ppp/peers/<TUNNEL>` 保存具体的vpn连接配置信息。
```
# written by pptpsetup
pty "pptp xxx.xxx.xxx.xx --nolaunchpppd"
lock
noauth
nobsdcomp
nodeflate
name xxxx
remotename xxxx
ipparam xxxx
require-mppe-128
file /etcp/options.pptp
```
实际上的启动命令是 `pppd call <TUNNEL>`, `pon <TUNNEL>`只是一段封装后的脚本，同理适用于 `poff` 脚本


#### log
vpn连接的相关日志在 `/var/log/message` 中查看
```
> tail -f /var/log/message
Using interface ppp0
Connect: ppp0 <–> /dev/pts/2
CHAP authentication succeeded
MPPE 128-bit stateless compression enabled
local  IP address 192.168.0.150
remote IP address 192.168.0.151
```
