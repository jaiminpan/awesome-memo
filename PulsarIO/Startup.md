# Startup 启动

## JetstreamApplication
启动入口的的main函数位置在 [JetstreamApplication][C_JetstreamApplication]中。
这个类使用了singleton模式，主要提供了启动位置，还有shutdown的清理。

核心是在init()中使用了RootConfiguration进行spring bean的初始化工作，RootConfiguration继承自AbstractApplicationContext。

首先使用getInstance进行初始化
```java
public static void main(String[] args) throws Exception {
...
try {
    ta = getInstance();
    // Allow JetstreamApplication option handling methods to be protected
    final JetstreamApplication optionHandler = ta;
    new CliOptions(new CliOptionHandler() {
      public Options addOptions(Options options) {
        return optionHandler.addOptions(options);
      }

      public void parseOptions(CommandLine line) {
        optionHandler.parseOptions(line);
      }
    }, args);
...
    ta.init();
  }
...
}
```

再使用CliOptions解析参数(ref:parseOptions函数)
```java
    options.addOption("b", "beans", true, "Beans to start during initialization");
    options.addOption("c", "config", true, "Configuration URL or file path");
    options.addOption("cv", "configversion", true, "Version of configuration");
    options.addOption("n", "name", true, "Name of application");
    options.addOption("p", "port", true, "Monitoring port");
    options.addOption("z", "zone", true, "URL or path of dns zone content");
    options.addOption("nd", "nodns", false, "Not a network application");
    options.addOption("wqz", "workqueuesz", true, "work queue size");
    options.addOption("wt", "workerthreads", true, "worker threads");
```

## RootConfiguration
RootConfiguration是一个全局的spring ApplicationContext，使用singleton模式可以让任意的class获取相关bean。
此类获取环境变量`$JETSTREAM_HOME/JetstreamConf`，定位相关资源目录, 通过调用 getDefaultContexts()获取所有资源，
然后使用父类Configuration的构造函数初始化。
Configuration真正实现相关的函数接口，如
* getConfigResources()
* getResourceByPath()
* loadBeanDefinitions()

在父类AbstractUpdateableApplicationContext中定义 UpdateableListableBeanFactory，所以可以动态更新相关的bean信息。


[C_JetstreamApplication]: https://github.com/pulsarIO/jetstream/blob/master/jetstreamframework/src/main/java/com/ebay/jetstream/application/JetstreamApplication.java
