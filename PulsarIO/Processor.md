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

#### AbstractQueuedEventProcessor
真正实现sendEvent的抽象类



