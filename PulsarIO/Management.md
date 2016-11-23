# Management 资源管理

## 相关类
#### Management
Management 是资源管理最核心的实现。主要功能如下：
* bean相关
  * addBean(), getBeanOrFolder(), removeBeanOrFolder()
  * ManagementListener接口，调用registerManagementListener注册，实现对上述add remove方法的监听。
* ResourceFormatters相关: 主要作用就是以哪种格式输出的策略模式，如html json等
  * registerResourceFormatter 
  * getResourceFormatter

#### ResourceFormatter
ResourceFormatter 有一组类，功能就是格式输出
* 接口类ManagedResourceFormatter
* 抽象实现类 AbstractResourceFormatter，提供主要子类如下
  * HtmlResourceFormatter
  * JsonResourceFormatter
  * HelpFormatter
  * XmlResourceFormatter
  * SpringResourceFormatter

#### ManagementServlet
可调用的Servlet接口，在JetstreamAppliation.xml使用jetty提供服务。服务端口由JetstreamAppliation启动项-p指定，否则默认9999

static方法初始化xml、spring、html、json、help五种输出格式。
内部使用 BeanController 输出具体内容。

BeanController有两个主要方法 process()和 write()
* process实现了对bean的控制，内部使用了反射进行函数调用，调用此方法前需要鉴权，鉴权由ManagementNetworkSecurity类提供功能，主要就是对比ip，需要提前进行初始化
* write则只是对bean的内容进行了简单的输出。
* 注意的是，如果控制的是ControlBean的实例，则可以调用ControlBean的process函数，进行具体参数的自定义处理。

#### PingServlet
如其名字，是一个简单提供状态输出的接口，用来看服务是否存活的公共实现。

#### JvmManagement
没什么好说的，代码如下，很简单
```java
public class JvmManagement {
  public JvmManagement() {
    XMLSerializationManager.registerXSerializable(MemoryManagerMXBean.class);
    XMLSerializationManager.registerXSerializable(MemoryPoolMXBean.class);
    Management.addBean("Jvm/ClassLoading", ManagementFactory.getClassLoadingMXBean());
    Management.addBean("Jvm/Compilation", ManagementFactory.getCompilationMXBean());
    Management.addBean("Jvm/GarbageCollector", ManagementFactory.getGarbageCollectorMXBeans());
    Management.addBean("Jvm/MemoryManager", ManagementFactory.getMemoryManagerMXBeans());
    Management.addBean("Jvm/Memory", ManagementFactory.getMemoryMXBean());
    Management.addBean("Jvm/MemoryPool", ManagementFactory.getMemoryPoolMXBeans());
    Management.addBean("Jvm/OS", ManagementFactory.getOperatingSystemMXBean());
    Management.addBean("Jvm/Runtime", ManagementFactory.getRuntimeMXBean());
    Management.addBean("Jvm/Threads", ManagementFactory.getThreadMXBean());
  }
}
```



