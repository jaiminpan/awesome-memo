第四部分：实时通道
================================

Pulsar实时分析系统主要有四个组件组成，包括收集组件（Collector）、Session化组件（Sessionizer）、分发组件（Distributor）、度量计算组件（Metric calculator）。每个组件都可以部署应用集群。

4.1 收集组件
----------------------

收集组件是一个可以在我们云环境跨多个数据中心部署的Jetstream CEP应用，这是我们实时管道的第一个组件，负责从事件生产者获取并把数据流向下一个组件Session化组件，这组件是无状态的，通过REST接口收集生产者的事件，事件到达后会做有效性验证，通过检验的数据才会由CEP引擎传递给下一个组件、CEP引擎会根据BOT缓存查找Bot签名(`signatures`)来过滤掉`BOT`事件。

### 4.1.1 地理和设备类别数据

被过滤的Bot事件由地理信息来填充，根据事件的IP地址在一个内存地理位置数据库里查找地里信息，像云城市，国家，洲，地区和网速。事件中的一个字段包括了一个IP地址，地理位置数据库由地理位置供应商周期性地维护，这些数据压缩成一个基于桶二进树（`buckedtized binary tree`）[注1]的结构，对于空间查询它是非常有效的，我们能够在150ms内就查询到地理信息。

收集组件还有一个设备分类标识来根据user-agent字符串来确定设备类型，操作系统版本和其他设备分类信息。

跟踪事件的Agent字符串会使用与设备关相联的user-agent信息来进行加工，事件增加Tags然后流向下游系统进一下分析。

4.2 Bot检测组件 
----------------------
在我们的系统环境，Bot特征会在我们的生产环境应用层之上发现，这些特征一般是自己声明和经过离线处理时发现然后更新到缓存里的。然而Bot不是这样做，通常都是直接流过实时管道。这些Bot需要在实时管道中尽早地检测出来，我们才能在消耗宝贵资源之前把这综合症过滤掉。

Bot表现出某种模式来访问我们的网站，我们最关心的是检测出消耗了我们大量网站资源、核心计算、网络和后端资源的Bot。这样的做法有，通过指定的特征来观察Bot访问网站的频率，我们的做法是在滚动窗口中使用随机频率的估算技术去检测，在我们主张的CEP，在这种像大海捞针的场景，用CEP引擎检测这些是最好的了。

当CEP引擎发现Bot特征，它会更新到Bot特征缓存，收集组件会查询这些特征并把Bot过滤掉。


4.3 Session化组件 
----------------------
Session化组件是实时管道的第二个组件，它主要功能是支持租户式的Session化。

Session化是一个由临时事件组所组成的处理单元，它包含一个称为Session持久时间的特定标识符。当具有指定标识符的事件第一次被检测的时候，窗口就开始，当在指定的Session持久时间内没有具有指定标识符的事件没有到达，这个窗口就会关闭。

### 4.3.1 会话元数据，计数器和状态
从事件收集的数据会流进Session，Session会存储在Session元数据形式的Session记录，Session元数据的一些例子有SessionId，PageId，地理位置（城市、地区、国家、州、经度、纬度和ISP、浏览器、OS和设备类型）。

当事件到达，我们会维护一个用户在事件里自定义的字段的计数或者事件的计数，这些计数器在我们的Session存储里维护。我们也需要维护每个Session的状态，当我们处理事件时，我们需要设置和重置状态，所有的处理逻辑都由SQL来编写。

### 4.3.2 会话存储
Session记录存储在本地的堆外（`off-heap`）缓存，该缓存备份于一个后备存储器。我们需要设置缓存条目（`cache entry`）的TTL，同时当这条目过期时能够精确作出通知。由于我们没有找到一个有这些功能的商用现成（`Commercial-off-the-shelf，COTS`）解决方案，我们开发了一个专用的堆外缓存和监听器，这样就能监控一个缓存条目过期然后发送通知。由于缓存条目会在节点宕机时数据丢失，所以我们存储在堆外缓存的同时还存储在一个外部的后备存储器。

### 会话后备存储器
我们使用以下标准去选择后备存储器：  
a. 支持本地读、写和删除   
b. 支持本地和跨数据中心复制    
c. 支持最终一致性   
d. 存储条目的生命周期管理（支持TTL）   
e. 支持写和读比例为10:4的场景   
f. 提供至少1M每秒读写能力   
g. 很好地支持200到50000字节的数据   
h. 能部署在云环境优先   
i. 创建二级索引用于查找内嵌已知客户端的Key

Session数据存储在堆外内存和后备存储器，我们提供一个存储抽象接口来支持不同的后备存储器。

我们的场景有很大量的写和删除负载。任何基于硬盘的解决方案都要求在删除的时候做压缩。这会要求很大的群集和非常昂贵的存储。对我我们的工作负载，一个具有副本的完全in-memory存储器将是最好的。我们评估过Cassandra, Couch base和本地存储。我们发现Cassandra和Couch Base都是基于硬盘的解决方案，压缩就变成一个瓶颈，我们的选择是使用一个本地存储的方案，这个方案操作全部在内存和可以跨多个数据中心的副本最大限度地保存数据一致性。

### 4.3.4 SQL扩展
Jetstream提供了一个注解插件框架，通过这框架用户可编写他们自己的注解来扩展Esper的类SQL语言，我们利用Jetstream这特性开发了这个特别的注解来增加SQL，下面是我们编写SQL语句来完成以下操作:  
   
a. 为租户指定会话持久时间和会话标识符   
b. 在会话存储元数据   
c. 在会话维护Counter   
d. 在会话中存储和操纵状态

例如，下面SQL用于创建一个会话并定义标识符和会话持久时间：   
@Session("WebSession")     
select si as _pk_,_ct as _timestamp_, 30 as _duration_   
from RawEvent(si is not null and _ct is not null);

我们可以使用下面的SQL来更新在会话名为『Pageviews』的计数器：   
@UpdateCounter("pageviews")   
select * from RawEvent(pageGroup = 'HomePage');

4.4 事件分发组件  
----------------------
这是管道中的第三组件，它主要的功能是为管道订阅者创建自定义的视图。这个视图通过转换、过滤和路由Session化的流。管道订阅者使用一个发布-订阅接口来订阅分发组件的事件源，这个订阅通过一个授权系统来执行授权订阅者的视图。订阅者能够随意加入或离开管道，当订阅者加入管道它们的视图就变成活动。它们开始从活动的视图接收事件。

### 4.1.1 事件过滤，转换和路由
转换、过滤和路由的规则都是由SQL编写并且它在运行时改变，下面展示了一个转换、过滤和路由的SQL例子：   
insert into PSTREAM select D1, D2, D3, D4 from RawEvent   
where D1 = 2045573 or D2 = 2047936 or D3 = 2051457 or D4 = 2053742

@PublishOn(topic="Trkng.Aconsumer/pEvent")   
@OutputTo("OutboundMessageCHannel")  
@ClusterAffinityTag(column = D1)   
select * FROM PSTREAM;

所有转换和过滤都在SQL语法里完成，Jetstream提供给我们一个注解扩展SQL，这个注解我们能在管道中使用。我们在Select语句执行过程中，在指定数据的管道使用这些注解来做事件路由。

4.5 多维度OLAP的指标计算组件  
----------------------
指标数据计算是一个实时指标计算引擎，主要用于计算各种自定义维度的指标和生成时序数据，它提供一个SQL接口来给用户提交SQl查询，这个SQl可通过基于时间窗口实现多维指标数据。指标事件，由CEP引擎产生，可以路由到一个或多个目的地-所有都由SQL控制。目的地可能是时序数据库，或者通过一个Webstocket连接的可视化挂件，或者用户需要通过一个指标数据阀值来确定是否需要警告。

### 4.5.1 聚集指标
事件可以使用随机或基于关联模式在指标计算应用集群里调度。对于基于关联调度，一个关联 会在事件流和其中一个处理节点之间创建，关联键是使用事件的一个或多个维度组合而成。关联键把事件流绑定到集群中的处理节点，这就保证事件在集群中相同关联键的事件都落到同一个处理节点，使我们能在内存中维护结果集。
 
指标数据通过很小的时间窗口（10秒）从流中聚集，当时间窗口滚动,它会给每个唯一维度组发送一个指标事件。下面是一个SQL查询来获取指标数据的例子：

create context MCContext start @now end pattern   
[timer:interval(10) or EsperEndEvent];   

context MCContext    
insert into aggregate1     
select count(*) as count, D1, D2, D3, _timestamp as tag_time, 'M1' as metricName    
from RawEvent(D1 is not null and D2 is not null and D3 is not null)   
group by D1, D2, D3 output snapshot when terminated;

### 4.5.2 聚合在指标计算集群
指标计算在4.5.1章节中只要指标增加一个由关联键就可以完成，这个关联键由维度组中的其中一个维度生成。然而这个计算在以下情况不会完成，当事件使用随机模式来调度，或者使用关联键模式来做关联调度，但这个关联键不是由维度组的一部分生成。

预期计算结果是CEP引擎只会对一个独立维度组产生一条指标数据，上面讨论的场景为集群中生成单个指标数据，所有单个指标事件必需直接发送到维度组群集内同一个节点，流的关联需要通过一个关联键来建立。下面将展示这个完整的Jetstream SQL 注解：

@OutputTo("outboundMessageChannel")   
@ClusterAffinityTag(dimension=@CreateDimension(name="groupimen",dimensionspan="D1, metricName, D2, D3, tag_time"))
@PublishOn(topic="Trkng,MC/clusterLevelAggregate")   
select * from aggregate1;


### 4.5.3 生成汇总数据，写入时序数据库
我们通过其他30秒的时间窗口来计算群集级的聚合指标数据，当时间窗口滚动，聚合指标数据就会输出一个指数事件。CEP引擎就会马上生成时序数据，下面将展示生成群集级别结果集，然后指标事件上直接写入时序数据库的例子：

create context CAContext start @now end pattern [timer:interval(30) or EsperEndEvent]  

context CAContext  
insert into clusteraggregate select SUM(count) as count, D1, D2, D3, tag_time, metricName from aggregate1 
group by D1, D2, D3, tag_time, metricName;   

@OutputTo("timeseriesdatabase,visualizer")   
select * from   
clusteraggregate output snapshot when terminated;

时序数据会被生成并写入时序数据库，或者在实时仪表盘驱动可视化挂件。

### 4.5.4 Metric存储
我们的时序数据存储要求很高写入速度（差不多十万事件每秒）、根据不同的时间窗口（分钟、小时、天）来生成rollup汇总数据、可以根据任何维度组合来提交特定创建聚合查询、查询范围可以是几年、大多数场景下查询延迟都在几秒内、支持超过一百并发查询时不会影响写入速率和查询延迟、高可用和支持以下的聚合功能像SUM、AVG、COUNT、TOP N、DISTINCT COUNT、PERCENTILES。

我们评估了Open TSDB、Cassandra和DRUID。Open TSDB支持高性能写入和支持我们想要的一些聚合函数，但是它不支持生成rollup汇总数据，同时也不支持从存在的结果集中生成新的结果集。Cassandra同样支持高性能写入。我们可以使用Cassandra计数器列族来对不同时间窗口中生成rollup汇总数据，但是Cassandra不支持GROUP BY和我们想要的聚合函数。我们选择都支持我们所有需求的DRUID。

-----------------------------------
1. [binary tree](https://en.wikipedia.org/wiki/Binary_tree)
2. ROLLUP是数据汇总的一种形式，这详见：https://technet.microsoft.com/zh-cn/library/ms189305(v=sql.90).aspx

-----------------

[« 第四部分: 实时通道](part4-pipeline.md)　　　　[总结 »](concluding.md)
