# Process

## EventSource接口
定义了添加删除sink的接口
* addEventSink
* getEventSinks
* removeEventSink
* setEventSinks

## EventSink接口
* sendEvent

## AbstractEventSource

简单实现EventSource 接口
* 对sink进行pause/resume 
* fireSendEvent(): 实现了把消息发送给子sink对象
* 实现 error接口，注册erro，取error等

**主要是对子sink的控制**

## AbstractEventProcessor

继承抽象类AbstractEventSource，并实现EventProcessor接口，
EventProcessor接口主要是组合EventSource，EventSink，Monitorable, MonitorableStatCollector四个接口

Monitorable, MonitorableStatCollector两个接口主要和监控统计相关
此类大部分代码是和监控有关，还有用PipelineFlowControl控制process的能力，包括此process的pause/resume状态变更

**主要是对process本身的控制和信息统计**

## AbstractQueuedEventProcessor
真正实现 sendEvent 的抽象类，在sendEvent中调用queueEvent方法， 默认实现queueEvent方法为：把事件放入RequestQueueProcessor(一个util类，此类实现了一个ringbuffer的工作线程池)线程池并配置真正处理的EventProcessRequest工作类，在工作线程处理

子类可以重载 queueEvent方法，并必须实现 getProcessEventRequest，来决定真正的处理工作方式。在EventProcessRequest 中留有接口processEvent方法来处理，如在EsperProcessor的实现中，新增了ProcessEventRequest来让epl处理真正的工作。

