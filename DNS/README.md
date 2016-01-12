DNS
============
域名系统（英文：Domain Name System，缩写：DNS）是因特网的一项服务。  
它作为将域名和IP地址相互映射的一个分布式数据库，能够使人更方便地访问互联网。DNS使用TCP和UDP端口53。
当前，对于每一级域名长度的限制是63个字符，域名总长度则不能超过253个字符。

简介
------------
[维基百科 英文](https://en.wikipedia.org/wiki/Domain_Name_System)  
[维基百科 中文](https://zh.wikipedia.org/wiki/域名系统)  

DNS系统中，常见的资源记录类型有：

* `主机记录（A记录）:` RFC 1035定义，A记录是用于名称解析的重要记录，它将特定的主机名映射到对应主机的IP地址上。
* `别名记录（CNAME记录）:` RFC 1035定义，CNAME记录用于将某个别名指向到某个A记录上，这样就不需要再为某个新名字另外创建一条新的A记录。
* `IPv6主机记录（AAAA记录）:` RFC 3596定义，与A记录对应，用于将特定的主机名映射到一个主机的IPv6地址。
* `服务位置记录（SRV记录）:` RFC 2782定义，用于定义提供特定服务的服务器的位置，如主机（hostname），端口（port number）等。
* `NAPTR记录:` RFC 3403定义，它提供了正则表达式方式去映射一个域名。NAPTR记录非常著名的一个应用是用于ENUM查询。

调试查看命令
----------------
Linux: dig www.google.com @127.0.0.1
```
; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.17.rc1.el6_4.6 <<>> www.google.com @223.5.5.5
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25396
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;www.google.com.			IN	A

;; ANSWER SECTION:
www.google.com.		232	IN	A	216.58.221.132

;; Query time: 7 msec
;; SERVER: 223.5.5.5#53(223.5.5.5)
;; WHEN: Tue Jan 12 14:29:21 2016
;; MSG SIZE  rcvd: 48
```

开源实现 (Linux)
-------------
### dnspod-sr
dnspod-sr 是一个运行在 Linux 平台上的高性能的递归 DNS 服务器软件，强烈公司内网或者服务器内网使用dnspod-sr。  
具备高性能、高负载、易扩展的优势，非 BIND、powerdns 等软件可以比拟。
但是dnspod-sr不具备授权功能。也只能用在内部。

Code: https://github.com/DNSPod/dnspod-sr  
Wiki: https://github.com/DNSPod/dnspod-sr/wiki  
FAQ: https://github.com/DNSPod/dnspod-sr/wiki/FAQ  

参考：  
http://skypegnu1.blog.51cto.com/8991766/1635563  
http://blog.dnspod.cn/2014/07/kaiyuan/  
http://www.ttlsa.com/linux/dnspod-sr-little-dns/  
http://blog.chinaunix.net/uid-29762534-id-4536608.html  


### Bind
Bind-DLZ主页：http://bind-dlz.sourceforge.net/  
DLZ(Dynamically Loadable Zones)与传统的BIND9不同，BIND的不足之处：

* BIND从文本文件中获取数据，这样容易因为编辑错误出现问题。
* BIND需要将数据加载到内存中，如果域或者记录较多，会消耗大量的内存。
* BIND启动时解析Zone文件，对于一个记录较多的DNS来说，会耽误更多的时间。
* 如果近修改一条记录，那么要重新加载或者重启BIND才能生效，那么需要时间，可能会影响客户端查询。

而Bind-dlz 即将帮你解决这些问题, 对Zone文件操作也更方便了，直接对数据库操作,可以很方便扩充及开发管理程序。

参考:  
http://bbs.linuxtone.org/thread-2081-1-1.html  
http://blog.csdn.net/liangyuannao/article/details/41076521  
http://sweetpotato.blog.51cto.com/533893/1598225 
http://blog.csdn.net/zhu_tianwei/article/details/45045431  
