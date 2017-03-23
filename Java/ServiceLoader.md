# ServiceLoader与模块系统

## ServiceLoader介绍

我们通常所指的服务就是指一些接口和类的集合，而一个服务提供者就是指一个服务的具体实现，Java平台一般都是通过特定扩展机制来加载服务实现的。ServiceLoader就是这样一种扩展机制的实现。

ServiceLoader的机制要求服务提供方的jar必须包含一个META-INF/services目录，
* 目录里面需要存在以服务类型名称（包含包名和类名）命名的文本文件
* 文件内容要求很简单，每一行放一个这个接口的一个实现类的类型名称（包含包名和类名）
例如
```
$> cat META-INF/services/com.example.Service1

com.example.Service1Impl1
com.example.Service1Impl2
```

准备好这些后，我们就可以调用ServiceLoader获取这些服务实例，代码如下：
```
ServiceLoader<Service1> services = ServiceLoader.get(Service1.class);
```
这时候ServiceLoader会帮我们去扫描classpath下所有的META-INF/services/目录，如果包含com.example.Service1文件，他初始化配置文件中的服务提供方实例，每一条记录都会对应一个服务实例。

好了，ServiceLoader的机制大概讲完了，简单吧。接下来我们就拿ServiceLoader来实现一个简单的模块加载系统。

## 一个例子，模块系统定义

一个相对复杂的应用往往需要划分成多个模块来降低整体复杂度。每个模块各司其职，模块之间都是弱耦合关系。每个模块都有它的生命周期，一般都需要初始化，启动，关闭这几个步骤，所以我们可以定义一个模块的抽象接口，代码如下：
```
public interface TeslaModule {

    /**
     * 模块的启动级别，决定了模块启动关闭的顺序
     *
     * @return 模块的启动级别
     */
    int getStartLevel();

    /**
     * 模块的初始化方法
     *
     * @param context
     * @throws Exception
     */
    void init(FrameworkContext context) throws Exception;

    /**
     * 模块的启动入口
     *
     * @param context
     * @throws Exception
     */
    void start(FrameworkContext context) throws Exception;

    /**
     * 模块的关闭入口
     *
     * @param context
     * @throws Exception
     */
    void stop(FrameworkContext context) throws Exception;

}
```
大家看到这个TeslaModule接口的命名就应该知道了，这个模块系统的实现已经应用到了tesla-framework 1.1.5中。
同时这里还会有一个int getStartLevel();方法，用于返回模块的启动级别。模块之间往往会有先后的依赖关系，startLevel就是用于指定模块的启动和关闭的依赖顺序。

## 模块的启动和关闭

#### 模块配置文件

通过上面的ServiceLoader机制介绍我们知道，我们需要在每模块jar包中的META-INF/services目录下面包含一个com.mogujie.tesla.framework.TeslaModule的文件，内容需要包含特定的模块实现，如下：
```
com.mogujie.tesla.server.TeslaExposeModule
```
#### 模块加载

这些准备好了，我们就可以ServiceLoader来加载模块实例，代码如下：
```
List<TeslaModule> allServices = new ArrayList<>();
for(TeslaModule module : ServiceLoader.load(TeslaModule.class)) {
    allServices.add(module);
}
```
#### 模块启动

获取模块实例后，我们才开始正式的启动模块，代码如下：
```
// 1
Collections.sort(allServices, new Comparator<TeslaModule>() {
    @Override
    public int compare(TeslaModule o1, TeslaModule o2) {
        return o1.getStartLevel() - o2.getStartLevel();
    }
});
// 2
for (TeslaModule module : allServices) {
    module.init(frameworkContext);
}
this.logger.info("tesla framework inited!");
// 3
for (TeslaModule module : allServices) {
    module.start(frameworkContext);
}
this.logger.info("tesla framework started!");
```
根据startLevel由小到大排序，startLevel值最小的最先启动
调用每个模块的init方法用于初始化模块
调用每个模块的start方法用于启动模块

#### 模块关闭

在应用关闭的时候，我需要去主动关闭模块，因为有些模块内部需要在关闭时释放线程池等系统资源，代码如下：
```
// 1
Collections.sort(allServices, new Comparator<TeslaModule>() {
    @Override
    public int compare(TeslaModule o1, TeslaModule o2) {
        return o2.getStartLevel() - o1.getStartLevel();
    }
});
// 2
for (TeslaModule module : allServices) {
    module.stop(toClose);
}
```
根据startLevel由大到小排序，startLevel值最大的最先关闭
调用每个模块的stop方法依次关闭模块

## 总结

我们通过一个简单模块系统的实现讲解了ServiceLoader的应用场景。当然ServiceLoader不只局限于模块的加载，因为ServiceLoader本身是一个简单可靠的工具，JDK中很多SPI（Service Provider Interface）的实现都是通过ServiceLoader方式加载的。所以说在Java中需要用到接口扩展的时候，第一选择就是ServiceLoader了，因为它是JDK自带的，不需要引入第三方的库。

