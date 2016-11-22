# ApplicationContext

[源码位置][code]


## 图示
ClassPathXmlAppliationContext的类继承层次图  
<img src="https://github.com/jaiminpan/misc-image/blob/master/memo/ClassPathXmlAppliationContext.png" width="500">

FileSystemXmlApplicationContext的类继承层次图  
<img src="https://github.com/jaiminpan/misc-image/blob/master/memo/FileSystemXmlAppliationContext.png" width="500">


#### 结构图
<img src="https://github.com/jaiminpan/misc-image/blob/master/memo/Class%20Diagram.png" width="600">

## 简单分析
* __DefaultResourceLoader__: 
  * 资源定位类，可以通过一个String类型的path获取一个Resource，从而指向一个具体的文件。
此类中最重要的方法是Resource getResource(String location)，该方法间接调用getResourceByPath来获取Resource.

* __AbstractApplicationContext__: 
  * refresh: refresh方法是入口方法也是核心方法，定义了生成ApplicationContext的实现步骤，使用了典型的模板方法模式，一些子步骤交给子类来实现。
obtainFreshBeanFactory方法可以获取一个真正的底层beanFactory，其中的refreshBeanFactory() 和 getBeanFactory()都是抽象方法

* __AbstractRefreshableApplicationContext__: 
  * 实现了 refreshBeanFactory() 和 getBeanFactory()，都是对父类AbstractApplicationContext的接口实现
createBeanFactory()在refreshBeanFactory被调用，是真正的创建工厂的方法，在此方法中创建了一个DefaultListableBeanFactory类型的工厂。
此类的中的beanFactory属性保存了此前创建的工厂实例。
  * 提供接口 loadBeanDefinitions 在refreshBeanFactory中被调用
  * createBeanFactory()可以被继承重载。

* __AbstractRefreshableConfigApplicationContext__:
  * 这个类的最主要的作用的保存配置文件的信息，主要存储在configLocations数组中。此类提供了如下方法
  * setConfigLocations()
  * getConfigLocations()

* __AbstractXmlApplicationContext__: 
  * 最核心的是实现了父类AbstractRefreshableApplicationContext中的`loadBeanDefinitions()`方法，
此方法拉开了解析XML配置文件的序幕。

* __FileSystemXmlApplicationContext__: 
  *  FileSystemXmlApplicationContext(String configLocations[], boolean refresh, ApplicationContext parent)
getResourceByPath方法是对父类DefaultResourceLoader中getResourceByPath的覆盖。


[code]: https://github.com/spring-projects/spring-framework/blob/master/spring-context/src/main/java/org/springframework/context/support/AbstractApplicationContext.java
