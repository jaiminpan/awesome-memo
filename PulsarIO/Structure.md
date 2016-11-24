# Code Structure

核心项目 jetstream的代码结构
* -- PATH
* |- jetstreamcore
* |- jetstreamframework
* |- jetstreamspring
* |- jetstream-messaging
* |- jetstream-channels-processors
* |- jetstream-hdfs
* |- configurationmanagement
* |- jetstreamdemo

## jetstreamcore
* 核心类库，主要实现Messaging(核心的消息传递框架，包括zookeeper交互[ZooKeeperTransport类]、netty的交互[NettyTransport类])
* Configure(Spring的ApplicationContext)
* Management
* netty服务器和客户端
* jettyserver (已废弃，直接用)

## jetstreamframework
* Application启动入口和参数解析
* 事件(event)流的处理框架(核心抽象类 AbstractEventSource、AbstractEventProcessor)
* AbstractEventSource子类(补充统计相关信息，AbstractInboundChannel、AbstractOutboundChannel)
* 数据流画像 dataflow
* 默认spring xml配置

## jetstream-messaging
* 连接流处理框架、 Messaging (InboundMessagingChannel、OutboundMessagingChannel)
* 连接流处理框架、 REST(http) (InboundRESTChannel、OutboundRESTChannel)
* 连接流处理框架、 kafka (InboundKafkaChannel、OutboundKafkaChannel)

## jetstreamspring
主要是Configure用到，和Spring的 ListableBeanFactory、 ApplicationEvent、BeanChangeAware 相关的代码。

## jetstream-channels-processors

## jetstream-hdfs

## configurationmanagement

## jetstreamdemo
例子
