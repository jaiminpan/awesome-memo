# Log4J使用教程

参考:[原文地址][1]

-------------

日志是应用软件中不可缺少的部分，Apache的开源项目log4j是一个功能强大的日志组件,提供方便的日志记录。

在apache网站：[log4j](www.jakarta.apache.org/log4j) 可以免费下载到Log4j最新版本的软件包。

## 一、入门实例
#### 1、 新建一个Java工程，导入Log4j包，pom文件中对应的配置代码如下：
```xml
<!-- log4j support -->
<dependency>
    <groupId>log4j</groupId>
    <artifactId>log4j</artifactId>
    <version>1.2.17</version>
</dependency>
```

#### 2、 resources目录下创建log4j.properties文件
```
 ### 设置###
log4j.rootLogger = debug,stdout,D,E

### 输出信息到控制抬 ###
log4j.appender.stdout = org.apache.log4j.ConsoleAppender
log4j.appender.stdout.Target = System.out
log4j.appender.stdout.layout = org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern = [%-5p] %d{yyyy-MM-dd HH:mm:ss,SSS} method:%l%n%m%n

### 输出DEBUG 级别以上的日志到=/home/duqi/logs/debug.log ###
log4j.appender.D = org.apache.log4j.DailyRollingFileAppender
log4j.appender.D.File = /home/duqi/logs/debug.log
log4j.appender.D.Append = true
log4j.appender.D.Threshold = DEBUG 
log4j.appender.D.layout = org.apache.log4j.PatternLayout
log4j.appender.D.layout.ConversionPattern = %-d{yyyy-MM-dd HH:mm:ss}  [ %t:%r ] - [ %p ]  %m%n

### 输出ERROR 级别以上的日志到=/home/admin/logs/error.log ###
log4j.appender.E = org.apache.log4j.DailyRollingFileAppender
log4j.appender.E.File =/home/admin/logs/error.log 
log4j.appender.E.Append = true
log4j.appender.E.Threshold = ERROR 
log4j.appender.E.layout = org.apache.log4j.PatternLayout
log4j.appender.E.layout.ConversionPattern = %-d{yyyy-MM-dd HH:mm:ss}  [ %t:%r ] - [ %p ]  %m%n
```

#### 3、输出日志的例子如下
```java
package com.javadu.log;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Log4JTest {
    private static final Logger logger = LoggerFactory.getLogger(Log4JTest.class);

    public static void main(String[] args) {
        // 记录debug级别的信息
        logger.debug("This is debug message.");
        // 记录info级别的信息
        logger.info("This is info message.");
        // 记录error级别的信息
        logger.error("This is error message.");
    }
}
```

#### 4、输出结果
首先，控制台输入如下图所示  
![image](http://upload-images.jianshu.io/upload_images/44770-ee816f46730e13a1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
然后，查看/Users/duqi/logs目录下的debug.log和error.log文件，内容分别如下

debug.log  
![image](http://upload-images.jianshu.io/upload_images/44770-7874d2d4d40b0579.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
error.log  
![image](http://upload-images.jianshu.io/upload_images/44770-1b2c57eadb32d1bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  

## 二、Log4J基本使用方法
* Log4j由三个重要的组件构成：日志信息的优先级，日志信息的输出目的地，日志信息的输出格式。
* 日志信息的优先级从高到低有ERROR、WARN、 INFO、DEBUG，分别用来指定这条日志信息的重要程度；
* 日志信息的输出目的地指定了日志将打印到控制台还是文件中；而输出格式则控制了日志信息的显示内容

#### 2.1 定义配置文件
其实您也可以完全不使用配置文件，而是在代码中配置Log4j环境。
但是，使用配置文件将使您的应用程序更加灵活。
Log4j支持两种配置文件格式，一种是XML格式的文件，一种是Java特性文件（键=值）。

下面我们介绍使用Java特性文件做为配置文件的方法：

配置根Logger，其语法为：
```
log4j.rootLogger = [ level ] , appenderName, appenderName, …
```

* level: 是日志记录的优先级，分为OFF、FATAL、ERROR、WARN、INFO、DEBUG、ALL或者您定义的级别。
Log4j建议只使用四个级别，优先级从高到低分别是ERROR、WARN、INFO、DEBUG。
通过在这里定义的级别，您可以控制到应用程序中相应级别的日志信息的开关。
比如在这里定义了INFO级别，则应用程序中所有DEBUG级别的日志信息将不被打印出来。 
* appenderName: 就是指把日志信息输出到哪个地方。
您可以同时指定多个输出目的地，例如上述例子我们制定了stdout、D和E这三个地方。
配置文件的输出目的地Appender，一般，配置代码的格式如下


```
log4j.appender.appenderName = fully.qualified.name.of.appender.class  
log4j.appender.appenderName.option1 = value1  
…  
log4j.appender.appenderName.option = valueN
```

其中，Log4j提供的appender有以下几种：
```
org.apache.log4j.ConsoleAppender（控制台），
org.apache.log4j.FileAppender（文件），
org.apache.log4j.DailyRollingFileAppender（每天产生一个日志文件），
org.apache.log4j.RollingFileAppender（文件大小到达指定尺寸的时候产生一个新的文件），
org.apache.log4j.WriterAppender（将日志信息以流格式发送到任意指定的地方）
```

配置日志信息的格式（布局），其语法为：
```
log4j.appender.appenderName.layout = fully.qualified.name.of.layout.class  
log4j.appender.appenderName.layout.option1 = value1  
…  
log4j.appender.appenderName.layout.option = valueN
```

其中，Log4j提供的layout有以下几种：
```
org.apache.log4j.HTMLLayout（以HTML表格形式布局），
org.apache.log4j.PatternLayout（可以灵活地指定布局模式），
org.apache.log4j.SimpleLayout（包含日志信息的级别和信息字符串），
org.apache.log4j.TTCCLayout（包含日志产生的时间、线程、类别等等信息）
```

Log4J采用类似C语言中的printf函数的打印格式格式化日志信息，打印参数如下：
```
%m 输出代码中指定的消息
%p 输出优先级，即DEBUG，INFO，WARN，ERROR，FATAL
%r 输出自应用启动到输出该log信息耗费的毫秒数
%c 输出所属的类目，通常就是所在类的全名
%t 输出产生该日志事件的线程名
%n 输出一个回车换行符，Windows平台为“rn”，Unix平台为“n”
%d 输出日志时间点的日期或时间，默认格式为ISO8601，也可以在其后指定格式，比如：%d{yyy MMM dd HH:mm:ss,SSS}，输出类似：2002年10月18日 22：10：28，921
%l 输出日志事件的发生位置，包括类目名、发生的线程，以及在代码中的行数。举例：Testlog4.main(TestLog4.java:10)
```

#### 2.2 在代码中使用Log4j
获取记录器
使用Log4j，第一步就是获取日志记录器，这个记录器将负责控制日志信息。
其语法为
```
public static Logger getLogger( String name);
```
通过指定的名字获得记录器，如果必要的话，则为这个名字创建一个新的记录器。
Name一般取本类的名字，比如
```
static Logger logger = Logger.getLogger ( ServerWithLog4j.class.getName () )
```

读取配置文件
当获得了日志记录器之后，第二步将配置Log4j环境，其语法为：
* BasicConfigurator.configure ()： 自动快速地使用缺省Log4j环境。  
* PropertyConfigurator.configure ( String configFilename) ：读取使用Java的特性文件编写的配置文件。  
* DOMConfigurator.configure ( String filename ) ：读取XML形式的配置文件。

插入记录信息（格式化日志信息）
当上两个必要步骤执行完毕，您就可以轻松地使用不同优先级别的日志记录语句插入到您想记录日志的任何地方，其语法如下：
```
Logger.debug ( Object message ) ;  
Logger.info ( Object message ) ;  
Logger.warn ( Object message ) ;  
Logger.error ( Object message ) ;
```

#### 2.3 日志级别
每个Logger都被了一个日志级别（log level），用来控制日志信息的输出。日志级别从高到低分为：
```
A：off 最高等级，用于关闭所有日志记录。
B：fatal 指出每个严重的错误事件将会导致应用程序的退出。
C：error 指出虽然发生错误事件，但仍然不影响系统的继续运行。
D：warn 表明会出现潜在的错误情形。
E：info 一般和在粗粒度级别上，强调应用程序的运行全程。
F：debug 一般用于细粒度级别上，对调试应用程序非常有帮助。
G：all 最低等级，用于打开所有日志记录。
```

上面这些级别是定义在org.apache.log4j.Level类中。Log4j只建议使用4个级别，优先级从高到低分别是error,warn,info和debug。
通过使用日志级别，可以控制应用程序中相应级别日志信息的输出。
例如，如果使用b了info级别，则应用程序中所有低于info级别的日志信息(如debug)将不会被打印出来。

三、Spring中使用Log4J
一般是在web.xml配置文件中配置Log4j监听器和log4j.properties文件，代码如下：
```
<context-param>
   <param-name>log4jConfigLocation</param-name>
   <param-value>classpath:/config/log4j.properties</param-value>
</context-param>
<context-param>
   <param-name>log4jRefreshInterval</param-name>
   <param-value>60000</param-value>
</context-param>
<listener>
   <listener-class>org.springframework.web.util.Log4jConfigListener</listener-class>
</listener>
```


## 动态调整例子
```java
//包
Level level = Level.toLevel(Level.DEBUG);  
Logger logger = LogManager.getLogger(“package”);  
logger.setLevel(level);  
//全局
Level level = Level.toLevel(Level.DEBUG);  
LogManager.getRootLogger().setLevel(level);  
```

```java
@Path("/conf")  
@Component("configurationResource")  
public class ConfigurationResource {  
    @GET  
    @Produces(MediaType.APPLICATION_XML)  
    @Path("/log/package/{package}/{level}")  
    public Response index(@PathParam("package") String p, @PathParam("level") String l) {  
        Level level = Level.toLevel(l);  
        Logger logger = LogManager.getLogger(p);  
        logger.setLevel(level);  
        return Response.ok().build();  
    }  
  
    @GET  
    @Produces(MediaType.APPLICATION_XML)  
    @Path("/log/root/{level}")  
    public Response index(@PathParam("level") String l) {  
        Level level = Level.toLevel(l);  
        LogManager.getRootLogger().setLevel(level);  
        return Response.ok().build();  
    }  
}  
```

[1]: http://www.codeceo.com/article/log4j-usage.html
