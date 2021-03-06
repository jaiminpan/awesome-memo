第三部分：架构
================================
我们的实时分析数据管道由一些松耦合的组件组成，每个组件都独立于相邻的组件，它们通过异步通信进行交互，这就提供了一个具有较高的可靠性和可伸缩性的扩展模型。每个组件可以独立构建和运行,而且可以采取自己的部署和发布周期，改变拓扑结构过程中无需停止服务。


在我们的后台实时分析架构中管道是可以在生产环境服务和应用中随时扩展。

事件流在源中收集用户操作然后作为事件发送到管道里，事件包含丰富的上下文信息，然后在管道上的各种各样的组件进行分析。

事件可以在in-flight和rest里分析。对于在线分析，我们把事件流放到具有复杂事件处理（CEP）能力的流处理架构，这个架构的目标就是要求最大2秒廷迟处理各种计算的实时计算场景。

我们的做法是把事件流作为一个数据库表，我们在实时流上使用类SQL查询，像事件流动那样汇总数据。与这个技术相反的其中之一就是原始数据先收集存储然后通过Map-Reduce job来汇总数据。我们这技术能够得到指标数据更加快速需要更小的资源，它还为我们提供了运行时部署代码查询的灵活性。



3.1 复杂事件处理(`CEP`)框架
----------------------

我们打算在很我的处理计算上使用复杂事件处理（`CEP`）引擎，当CEP某些不适合我们处理计算或者太重的时候，我们会通过自定Processors来增强CEP引擎。

我们数据是由处理节点组成的直接非循环国谱（`DAG`），如图2

每个处理节点都是CEP程序的一个具有自己一个DAG组件的实例，一系列的处理节点在图谱中执行从通道组件的相同操作，管道消费者的处理节点来自于DAG的子节点，DAG可以通过不断增加而扩展，更多的消费者在Process会改变拓朴结构。我们想要一个声明式的管道拼接以做到在运行时能够自动适应动态拓扑改变。

我们处理逻辑包括在翻滚（`tumbling windows`）和滚动窗口（`rolling windows`）处理事件流计算指标，拼接流，过滤，增加和转换流，通过DAG来控制事件的流程，拼接多个流和状态管理。

这系统希望不用专家级的程序员就能做到非常敏捷编写和发布处理逻辑，我们公司很多技术人员通常都很熟悉SQL，因此我们决定支持类SQL的语言，就像声明式语言那样去编写处理规则。类SQL语句被编译成运行时的Java字节代码，因此能很高性能地进行实时查询处理，我们同样需要扩展SQL使得通道能够访问SQL，还有能够在通道里编写逻辑来控制数据的流转。

我们希望我们程序可以发布在云上，通道的拓朴横跨多个数据中心，因此我有完整的灾难恢复。

鉴于我们独特的复杂事件处理需求，我们决定开发基于Spring和分布式复杂事件处理基础框架，并称为Jetstream，它给我们提供了一个基于Java的CEP框架和用来在云环境中构建、部署和管理CEP应用的工具。这工具同时提供发布在Docker容器的EC2环境。


Jetstream 具有以下功能：
1. SQL的声明式定义的处理逻辑
2. 不用重启的热部署SQL
3. 用于扩展SQL函数的注解插件框架
4. 使用SQL进行管道流量路由
5. 使用SQL动态创建流关系
6. 使用Spring IOC 声明式通道绑定，运行时动态改变拓朴
7. 弹性扩展集群
8. 云主机部署
9. 支持Push和Pull模式的订阅发布消息处理

所我们的实时通道应用都是使用Jetstream来构建。


3.2 消息传递
----------------------
### 3.2.1 收集消息
平常的一天我们每秒从100,000个服务器节点里收集成千上万事件，事件平均的大小在1000到3000字节。消息的生产者分布在多语言环境里，事件数据通常都是不可预知模式的非结构化数据，针对某些场景，我们还需要保持系统的端到端的延迟在2秒内。

我们的首要选择是通过REST接口收集所有入口事件，事件内容以JSON或AVRO的序列化形式，在源里作批量提交而且批量大小不超过40事件。事件流会定期回收持久的http连接，数据通过动态压缩来优化网络带宽，REST API提供给我们事务语义来保证数据收集组件数据的完整性，同时也很好地解决我们整合多语言环境的消息生产者的问题。
### 3.2.2 Push Vs. Pull 消息传递
对于实时管道中的分发组件进行消息传递，我需要决定推与拉模型。

Push消息传递模型提供了低延迟，而且因为不需要在分发组件中持久队列所以成本非常小。然而，它的缺点是处理慢消费者，而已如果消费者宕机时消息可能丢失。

另一方面，Pull模型存在高延迟，因为要持久队列所以成高更大。然后这种模型非常合适慢消费者和非常可靠。


3.2 消息传递选择
----------------------
我们正在处理的许多类问题在管道要求非常低的延迟(少于100毫秒),但同时也要求非常低的传输损失(少于0.01%)。在云部署可以分布在多个处理节点数据中心，由于我们许多计算的聚合都在内存里维护，为了扩展，我们要求我们消息层提供集群能力，除此之外，我们想消息传递层能与消费者应用集群中的节点建立联系。因为我们的消费者在发布-订阅消息传递模型时可以加入和离开管道，所以我们分发集群必须是低耦合。

Jetstream 提供了一个代理集群in-memory和低延迟的发布-订阅消息传递解决方案，它支持流关联通过支持一致的哈希事件调度器，它同样支持一个随机调度在集群节点中做负载均衡，它提供一个跨数据中心发布应用的能力，它有流控制语义-消费者可以信号生产者停止发送事件由于繁忙的集群实现再平衡，它有能力检测缓慢的消费者和发送报告包含未提交的事件。侦听器将没有提交的事件放到持久队列时以便后续夺回放。

Jetstream使用Kafka提供的至少一次的传递语义来支持发布-订阅消费传递，
我们结合我们的代理存储少量消息和回放出现处理异常的慢消息者没有被提交的事件。对于低延迟的可靠的消息传递，我们可以选择把这个消息将事件转发给管道消费者。


我们选择了一个in-memory集群消息传递与异常时使用持久队列的混合的方式，这个决定主要是由成本和延迟方面的考虑。持久队列方法导致网络上的事件流经我们的分布式多级管道和添加一个在各个分布的组件这间至少300毫秒的延迟。4个组件接合，就会产生1.2秒的延迟。如果我们跨数据中心部署还会产生更高延迟，在这个在我们的主要场景里是不能接近的。

结合的in-memory消息传递和异常时传递到持久化队列，这个方法对于我们来说非常合适。我们能够实现少于100毫秒实时数据所端到端延迟和管道损失小于0.01%。

-----------------

[« 第二部分: 数据和处理模型](part2-data-model.md)　　　　[第四部分: 实时管道 »](part4-pipeline.md)
