# Listener 简介

[![ORIGIN](https://img.shields.io/badge/FROM-LINK-blue.svg)][1]

监听器Listener就是在application,session,request三个对象创建、销毁或者往其中添加修改删除属性时自动执行代码的功能组件。

Listener是Servlet的监听器，可以监听客户端的请求，服务端的操作等。

## Listener的分类与使用

主要有以下三类：

#### 1、ServletContext监听

ServletContextListener：用于对Servlet整个上下文进行监听（创建、销毁）。
```java
//上下文初始化
public void contextInitialized(ServletContextEvent sce);
//上下文销毁
public void contextDestroyed(ServletContextEvent sce);
//ServletContextEvent事件：取得一个ServletContext（application）对象
public ServletContext getServletContext();
```

ServletContextAttributeListener：对Servlet上下文属性的监听（增删改属性）。
```java
//增加属性
public void attributeAdded(ServletContextAttributeEvent scab);
//属性删除
public void attributeRemoved(ServletContextAttributeEvent scab);
//属性替换（第二次设置同一属性）
public void attributeRepalced(ServletContextAttributeEvent scab);

//ServletContextAttributeEvent事件：能取得设置属性的名称与内容
//得到属性名称
public String getName();
//取得属性的值
public Object getValue();
```

#### 2、Session监听

Session属于http协议下的内容，接口位于javax.servlet.http.*包下。

HttpSessionListener接口：对Session的整体状态的监听。
```java
//session创建
public void sessionCreated(HttpSessionEvent se);
//session销毁
public void sessionDestroyed(HttpSessionEvent se);

//HttpSessionEvent事件：
//取得当前操作的session
public HttpSession getSession();
```
HttpSessionAttributeListener接口：对session的属性监听。
```java
public void attributeAdded(HttpSessionBindingEvent se);//增加属性
public void attributeRemoved(HttpSessionBindingEvent se);//删除属性
public void attributeReplaced(HttpSessionBindingEvent se);//替换属性

//HttpSessionBindingEvent事件：
public String getName();//取得属性的名称
public Object getValue();//取得属性的值
public HttpSession getSession();//取得当前的session
```

session的销毁有两种情况：

1.session超时，web.xml配置：
```xml
<session-config>
    <session-timeout>120</session-timeout><!--session120分钟后超时销毁-->
</session-config>
```
2.手工使session失效
```java
//使session失效方法。session.invalidate();
public void invalidate();
```

#### 3、Request监听

ServletRequestListener：用于对Request请求进行监听（创建、销毁）。
```java
public void requestInitialized(ServletRequestEvent sre);//request初始化
public void requestDestroyed(ServletRequestEvent sre);//request销毁

//ServletRequestEvent事件：
public ServletRequest getServletRequest();//取得一个ServletRequest对象
public ServletContext getServletContext();//取得一个ServletContext（application）对象
```

ServletRequestAttributeListener：对Request属性的监听（增删改属性）。
```java
public void attributeAdded(ServletRequestAttributeEvent srae);//增加属性
public void attributeRemoved(ServletRequestAttributeEvent srae);//属性删除
public void attributeReplaced(ServletRequestAttributeEvent srae);//属性替换（第二次设置同一属性）

//ServletRequestAttributeEvent事件：能取得设置属性的名称与内容
public String getName();//得到属性名称
public Object getValue();//取得属性的值
```

#### 4、在web.xml中配置

Listener配置信息必须在Filter和Servlet配置之前，Listener的初始化（ServletContentListener初始化）比Servlet和Filter都优先，而销毁比Servlet和Filter都慢。
```xml
<listener>
    <listener-class>com.listener.class</listener-class>
</listener>
```

## Listener应用实例

#### Spring使用ContextLoaderListener加载ApplicationContext配置信息

ContextLoaderListener的作用就是启动Web容器时，自动装配ApplicationContext的配置信息。
因为它实现了ServletContextListener这个接口，在web.xml配置这个监听器，启动容器时，就会默认执行它实现的方法。

ContextLoaderListener如何查找ApplicationContext.xml的配置位置以及配置多个xml：
如果在web.xml中不写任何参数配置信息，默认的路径是`/WEB-INF/applicationContext.xml`，
在WEB-INF目录下创建的xml文件的名称必须是`applicationContext.xml`（在MyEclipse中把xml文件放置在src目录下）。
如果是要自定义文件名可以在`web.xml`里加入contextConfigLocation这个context参数。
```xml
<context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath:spring/applicationContext-*.xml</param-value>
    <!-- 采用的是通配符方式，查找WEB-INF/spring目录下xml文件。如有多个xml文件，以空格、逗号、分号(任意一种)分隔。 -->
</context-param>
<listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
```

#### Spring使用Log4jConfigListener配置Log4j日志

Spring使用Log4jConfigListener的好处：

动态的改变记录级别和策略，不需要重启Web应用。
把log文件定在 /WEB-INF/logs/ 而不需要写绝对路径。因为系统把web目录的路径压入一个叫webapp.root的系统变量。这样写log文件路径时不用写绝对路径了。
可以把log4j.properties和其他properties一起放在/WEB-INF/ ，而不是Class-Path。
设置log4jRefreshInterval时间，开一条watchdog线程每隔段时间扫描一下配置文件的变化。
```xml
<context-param>
    <param-name>webAppRootKey</param-name>
    <param-value>project.root</param-value>
    <!-- 用于定位log文件输出位置在web应用根目录下，
        log4j配置文件中写输出位置：log4j.appender.FILE.File=${project.root}/logs/project.log -->
</context-param>
<context-param>
    <param-name>log4jConfigLocation</param-name>
    <param-value>classpath:log4j.properties</param-value>
    <!-- 载入log4j配置文件 -->
</context-param>
<context-param>
    <param-name>log4jRefreshInterval</param-name>
    <param-value>60000</param-value>
    <!--Spring刷新Log4j配置文件的间隔60秒,单位为millisecond-->
</context-param>
<listener>
    <listener-class>org.springframework.web.util.Log4jConfigListener</listener-class>
</listener>
```

#### Spring使用IntrospectorCleanupListener清理缓存

这个监听器的作用是在web应用关闭时刷新JDK的JavaBeans的Introspector缓存，以确保Web应用程序的类加载器以及其加载的类正确的释放资源。

如果JavaBeans的Introspector已被用来分析应用程序类，系统级的Introspector缓存将持有这些类的一个硬引用。因此，这些类和Web应用程序的类加载器在Web应用程序关闭时将不会被垃圾收集器回收！而IntrospectorCleanupListener则会对其进行适当的清理，已使其能够被垃圾收集器回收。

唯一能够清理Introspector的方法是刷新整个Introspector缓存，没有其他办法来确切指定应用程序所引用的类。这将删除所有其他应用程序在服务器的缓存的Introspector结果。

在使用Spring内部的bean机制时，不需要使用此监听器，因为Spring自己的introspection results cache将会立即刷新被分析过的JavaBeans Introspector cache，而仅仅会在应用程序自己的ClassLoader里面持有一个cache。虽然Spring本身不产生泄漏，注意，即使在Spring框架的类本身驻留在一个“共同”类加载器（如系统的ClassLoader）的情况下，也仍然应该使用使用IntrospectorCleanupListener。在这种情况下，这个IntrospectorCleanupListener将会妥善清理Spring的introspection cache。

应用程序类，几乎不需要直接使用JavaBeans Introspector，所以，通常都不是Introspector resource造成内存泄露。相反，许多库和框架，不清理Introspector，例如： Struts和Quartz。

需要注意的是一个简单Introspector泄漏将会导致整个Web应用程序的类加载器不会被回收！这样做的结果，将会是在web应用程序关闭时，该应用程序所有的静态类资源（比如：单实例对象）都没有得到释放。而导致内存泄露的根本原因其实并不是这些未被回收的类！

注意：IntrospectorCleanupListener应该注册为web.xml中的第一个Listener，在任何其他Listener之前注册，比如在Spring’s ContextLoaderListener注册之前，才能确保IntrospectorCleanupListener在Web应用的生命周期适当时机生效。
```xml
<listener><!-- memory clean -->
    <listener-class>org.springframework.web.util.IntrospectorCleanupListener</listener-class>
</listener>
```


[1]: http://tianweili.github.io/blog/2015/01/27/java-listener/
