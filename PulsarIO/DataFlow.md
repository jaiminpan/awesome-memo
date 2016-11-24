# DataFlow

位于com.ebay.jetstream.application.dataflows包下

## 介绍
这个部分，主要是用来显示相关bean所处理的数据流。

* DataFlows: 继承了Spring的BeanFactoryAware, 从源头类InboundChannel开始，获取相关的EventSource，形成数据流数据，保存起来
* VisualDataFlow: 通过DataFlows得到数据流，然后使用外部接口 http://yuml.me/ 生成对应的图片。
* VisualServlet: 把VisualDataFlow用servlet暴露出去。
* DirectedGraph: 辅助类，保存图数据

