# Kafka Consumer

[原文](http://m.blog.csdn.net/article/details?id=69554569)

Kafka从0.7版本到现在的0.10版本, 经历了巨大的变化; 而其中, 首当其冲的是Consumer的机制.

Kafka最早设计Consumer的时候, 大方向比较明确, 就是同时支持Subscribe功能和Message Queue功能. 语义设计上很清晰，但是实现之后, 发现有一些问题. 主要问题集中在:
* 用户希望自己能够控制Offset的保存和读取; 
0.8.0 SimpleConsumer Example
* Offset保存在Zookeeper中对Zookeeper带来压力较大, 需要脱离的ZK的依赖;
    * Committing and fetching consumer offsets in Kafka
    * Offset Management
    * https://issues.apache.org/jira/browse/KAFKA-657
* 用户希望能获得Offset并且自行决定保存的位置;
* 用户自己控制Offset时, 却会陷入复杂的异常处理逻辑;
* 老的Consumer会有惊群效应和脑裂问题;

#### Consumer Client Re-Design
Consumer的改进直到0.9版本, 终于有了一个接近完美的版本; 但是由于向前兼容的需要, 以前的Consumer方式正在被使用, 并没有彻底移除. 由于Consumer的多版本存在, 并且个版本的Consumer变化很大, 这些影响又是对上层可见的, 所以对使用者造成了很大的混淆和困惑.
所以我想在这篇Blog中整理分析一下各Consumer的特点和区别, 让大家有一个纵观历史的认识.

![image](https://github.com/jaiminpan/misc-image/blob/master/kafka_consumer.jpeg)
