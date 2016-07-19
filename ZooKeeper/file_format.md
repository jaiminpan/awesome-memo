
## 简介
zoo.cfg配置文件中:
* `dataDir`: 用于存储Snapshot（快照）数据，
* `dataLogDir`: 用于存储Log（事务日志），如果没有设置，则默认使用dataDir的配置。
* 在Log文件写入频率非常高的情况下，可以为Log与Snapshot分别配置不同的目录存储。


本文主要是结合源码分析Zookeeper的Log与Snapshot文件。


事务日志与Snapshot的操作是在org.apache.zookeeper.server.persistence包中，
这里也主要是分析该包下的各个类；
* FileTxnSnapLog类：为Log日志与Snapshot配置的目录下又创建了子目录`version-2`，同时又指定为该两种文件的存储路径，
* FileTxnLog、FileSnap类：分别为处理事务日志和Snapshot的

## LOG 事务日志文件

在Zab协议中我们知道每当有接收到客户端的事务请求后Leader与Follower都会将把该事务日志存入磁盘日志文件中，
该日志文件就是这里所说的事务日志，下面将详细分析该日志文件；
FileTxnLog类用于处理事务日志文件这里就从此类开始，
在该类中看到了preAllocSize、TXNLOG_MAGIC、VERSION、lastZxidSeen、dbId等这样的属性：
 1. preAllocSize: 默认预分配的日志文件的大小65536*1024字节
 2. TXNLOG_MAGIC：日志文件魔数为ZKLG
 3. VERSION：日志文件版本号2
 4. lastZxidSeen：最后的ZXID

类中还有一个静态代码块用于读取配置项中的preAllocSize，
也就是说预分配的日志文件大小是可配置的，接下来看看该类中最重要的一个方法append，
该方法主要功能是创建新的日志文件与往日志文件中追加新的事务日志记录；从中可以看到日志文件的相关信息：

 1. 文件名为log，后缀为十六进制的ZXID
 2. 日志文件头有：magic、version、dbid
 3. 创建文件后分配的文件大小为：67108864字节+16字节，其中16字节为文件头
 4. 使用Adler32作为日志文件的校验码
 5. 当日志文件写满预分配大大小后就扩充日志文件一倍大小

#### 知识点
 * 如代码一样，`version-2`目录中存储着Zookeeper的事务日志文件，有看到如`log.xx`文件(大小为64MB文件)，这些都是事务日志文件；
**时间越早的文件，其后缀xx数字越小，反之越晚生成的，xx数字越大。**

 * 如果有了解过Zookeeper的ZAB协议，可以知道zookeeper为每一个事务请求都分配了一个事务ID也就是ZXID
 * 文件后缀的xx其实就是Zookeeper处理请求的ZXID，该ZXID为log文件中第一条事务的ZXID
 * ZXID规则为前32字节为Leader周期，后32字节为事务请求序列
 * 通过事务日志就可以轻松的知道当前的Leader周期与每个文件所属的Leader周期

## SNAPSHOT 快照文件

在FileSnap类中处理，与事务日志文件一样快照文件也一样有SNAP_MAGIC、VERSION、dbId这些，这作用也只是用来标识这是一个快照文件；
Zookeeper的数据在内存中是以DataTree为数据结构存储的，快照就是每间隔一段时间Zookeeper就会把整个DataTree的数据序列化然后把它存储在磁盘中，这就是Zookeeper的快照文件，
快照文件是指定时间间隔对数据的备份，所以快照文件中数据通常都不是最新的，

多久抓一个快照这也是可以配置的snapCount配置项用于配置处理几个事务请求后生成一个快照文件；
与事务日志文件一样快照文件也是使用ZXID作为快照文件的后缀，
在FileTxnSnapLog类中的save方法中生成文件并调用FileSnap类序列化DataTree数据并且写入快照文件中；

