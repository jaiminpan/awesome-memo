
原文链接： [Pulsar-Real-time Analytics at Scale](https://github.com/pulsarIO/realtime-analytics/wiki/documents/Whitepaper_Pulsar_Real-timeAnalyticsatScale.pdf) 

关PPT：[Pulsar_Presentation](http://gopulsar.io/docs/Pulsar_Presentation.pdf)


Pulsar-可扩展的实时分析系统
=======================================
随着移动设备的快速增长，每天有数以百万计消费者在选购十多亿的商品，数千万的机器在提供服务，为了更好的购物体验，实时地响应他们的操作至关重要，并在购买的过程中提供有关下一步的服务。

用户体验在过去几年里越来越好，现在他们希望在多屏中更加个性化，包括运营人员--能根据消费选择意向来提供丰富且而贴切的广告。
   
欺诈检测，购物行为监控等都需要实时地处理数据，在秒级收集可疑点，还要快速地产生信号然后处理。像Hadoop这种廷时的存储-处理的面向批处理系统不太合适。 
 
海量的数据和低廷时场景要求源源不断地数据处理，而不是存储-处理，流式处理架构需要分布在每个数据中心上，同样这个程序模型不需要专业人才能明白。这个系统还能支持高可用（例如. 允许应用不停机重新发布）  

这篇论文主要讨论Puslar的设计，一个解决了上述问题的实时分析平台。我们将讨论关键的子系统和组件的设计和选择理由。


目录
-----------------

- [译序](#译序)
- [概述](#Pulsar-可扩展的实时分析系统)
- [第一部分：简介](part1-introduction.md)
- [第二部分：数据和处理模型](part2-data-model.md)
    1. [用户行为数据](part2-data-model.md#用户行为数据])
    2. [非结构化数据](part2-data-model.md#混合数据)
    3. [会话数据](part2-data-model.md#会话数据)
    4. [用户自定义流](part2-data-model.md#用户自定义流)
    5. [多维度实时聚合计算](part2-data-model.md#多维度实时聚合计算)
    6. [实时计算TopN,百分比和Disctinct指标](part2-data-model.md#实时计算TopN,百分比和Disctinct指标)
    7. [处理无序和廷迟件](part2-data-model.md#处理无序和廷迟事件)
- [第三部分：架构](part3-architecture.md)
    1. [复杂事件（`CEP`）处理框架](part3-architecture.md)
    2. [消息传递](part3-architecture.md)
       - [收集消息](part3-architecture.md)
       - [Push vs. Pull消息传递](part3-architecture.md)
    3. [消息传递选择](part3-architecture.md)
- [第四部分：实时通道](part4-pipeline.md)
    1. [收集组件](part4-pipeline.md)
    	- [地理和设备类别数据](part4-pipeline.md)
    2. [Bot检测组件](part4-pipeline.md) 
    3. [Session化组件](part4-pipeline.md)
       - [会话元数据，计数器和状态](part4-pipeline.md)
       - [会话存储](part4-pipeline.md)
       - [会话回退存储](part4-pipeline.md)
       - [SQL扩展](part4-pipeline.md)
    4. [事件分发组件](part4-pipeline.md)
       - [事件过滤，转换和路由](part4-pipeline.md)
    5. [多维度OLAP的Metrics计算组件](part4-pipeline.md)
       - [收集Metrics](part4-pipeline.md)
       - [聚合](part4-pipeline.md)
       - [用时序数据库汇总](part4-pipeline.md)
       - [Metrics存储](part4-pipeline.md) 
- [总结](concluding.md)
