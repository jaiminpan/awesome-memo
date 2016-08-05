# Tomcat Deploy

把war部署到tomcat有三种方式

* 将xxx.war包直接复制到`webapps`目录中。
* 在`conf/server.xml`中定义
* 配置目录`conf/Catalina/localhost`，在该目录中新建一个后缀为xml的文件

#### 将war包直接放到`webapps`目录中
Tomcat的`webapps`目录是Tomcat默认的应用目录，当服务器启动时，会加载所有这个目录下的应用。

也可以将JSP程序打包成一个war包放在目录下，服务器会自动解开这个war包，并在这个目录下生成一个同名的文件夹。
一个war包就是有特性格式的jar包，它是将一个Web程序的所有内容进行压缩得到。
具体如何打包，可以使用许多开发工具的IDE环境，如Eclipse、NetBeans、ant、JBuilder等。
也可以用cmd 命令：`jar -cvf applicationname.war package.*;`


webapps这个默认的应用目录也是可以改变。打开Tomcat的`conf/server.xml`文件，找到下面内容：
```xml
<Host name="localhost" debug="0" appBase="webapps" unpackWARs="true" autoDeloy="true" xmlValidation="falase" xmlNamespaceAware="false">
```

#### 在server.xml中指定
在Tomcat的配置文件中，一个Web应用就是一个特定的Context，可以通过在server.xml中新建Context里部署一个JSP应用程序。
打开server.xml文件，在Host标签内建一个Context，内容如下。
```xml
<Context path="/myapp" reloadable="true" docBase="D:\myapp" debug="0" privileged="true" />
```
其中path是虚拟路径，docBase是JSP应用程序的物理路径。


#### 配置目录`conf/Catalina/localhost`, 加入一个Context文件
以上两种方法，Web应用被服务器加载后都会在Tomcat的conf\catalina\localhost目录下生成一个XML文件，其内容如下：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Context path="/admin" docBase="/data/webapps/admin" reloadable="false"></Context>
# OR
<Context path="/admin" docBase="${catalina.home}/server/webapps/admin" debug="0" privileged="true"></Context>
</Context>
```
可以看出，文件中描述一个应用程序的Context信息，其内容和server.xml中的Context信息格式是一致的，文件名便是虚拟目录名。
您可以直接建立这样的一个xml文件，放在Tomcat的conf\catalina\localhost目录下。

这个方法有个优点，可以定义别名。服务器端运行的项目名称为path，外部访问的URL则使用XML的文件名。
这个方法很方便的隐藏了项目的名称，对一些项目名称被固定不能更换，但外部访问时又想换个路径，非常有效。 


## 注意：
删除一个Web应用同时也要删除webapps下相应的文件夹祸server.xml中相应的Context，
还要将Tomcat的conf\catalina\localhost目录下相应的xml文件删除。
否则Tomcat仍会岸配置去加载。。。 
 
