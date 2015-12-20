# Emiller的Nginx模块开发指南(中文版)

  By [Evan Miller](http://www.evanmiller.org/) Last edit: January 16, 2013

  By [Jaimin](http://github.com/jaiminpan), update and format change base on Kongch's workout

  By [Kongch](http://www.kongch.com/) @2010年1月5日 0:04am -- 2010-01-06 13:55pm. 
  [Link](https://code.google.com/p/emillers-guide-to-nginx-module-chn/wiki/NginxModuleDevGuide_CHN)

## 0. 预备知识

  你应当比较熟悉C语言。不光是“C-语法"，你起码还得知道结构体和预处理指令，同时保证看到指针和函数引用出现时心里不会发毛。否则的话，就算信春哥也是没用的，看看[K&R](http://en.wikipedia.org/wiki/The_C_Programming_Language_(book))吧。

  你得对HTTP协议有一定的了解，毕竟你是在和一个web server打交道。

  如果你熟悉Nginx的配置文件就太好不过了。如果不熟悉，也没关系，这里简单介绍一下，知道概念先：Nginx配置文件主要分成四部分：_main（全局设置）_、_server（主机设置）_、_upstream（上游服务器设置）_和_location（URL匹配特定位置后的设置）_。每部分包含若干个**指令(directives)**。main部分设置的指令将影响其它所有设置；server部分的指令主要用于指定主机和端口；upstream的指令用于设置一组后端服务器；location部分的指令用于匹配网页位置（比如，根目录“/”，“/images”，等等）。他们之间的关系式：server继承main，location继承server；upstream既不会继承指令也不会被继承。它有自己的特殊指令，不需要在其他地方的应用。在下面很多地方都会涉及这四个部分，切记。

  好了，让我们开始吧。

## 1. Nginx模块委托概述

  Nginx的模块有三种角色：
  
    * _handlers_ 处理http请求并构造输出  
    * _filters_ 处理handler产生的输出  
    * _load-balancers_ 当有多于一个的后端服务器时，选择一台将http请求发送过去  

  许多可能你认为是web server的工作，实际上都是由模块来完成的：任何时候，Nginx提供文件或者转发请求到另一个server，都是通过handler来实现的；
  而当需要Nginx用gzip压缩输出或者在服务端加一些东东的话，filter就派上用场了；
  Nginx的core模块主要管理网络层和应用层协议，并启动针对特定请求的一系列后续模块。
  这种分散式的体系结构使得由**你自己**来实现强大的内部单元成为了可能。

  注意：不像Apache的模块那样，Nginx的模块都**不是**动态链接的。（换句话说，Nginx的模块都是静态编译的）

  模块是如何被调用的呢？典型地说，当server启动时，每一个handler都有机会去处理配置文件中的location定义，
  如果有多个handler被配置成需要处理某一特定的location时，只有其中一个handler能够“获胜”（掌握正确配置规则的你当然不会让这样的冲突发生啦）。

  一个handler有三种返回方式：

    * 正常  
    * 错误  
    * 拒绝处理转由默认的handler来处理（典型地如处理静态文件的时候）  

  如果handler的作用是把请求反向代理到后端服务器，那么就需要刚才说的一种模块类型：load-balancer。
  load-balancer主要是负责决定将请求发送给哪个后端服务器。Nginx目前支持两种load-balancer模块：

    1. round-robin（轮询，处理请求就像打扑克时发牌那样）  
    2. IP hash（保证来自同一个客户端的请求被分发到同一个后端服务器）  

  如果handler正确处理返回，那么fileter就被调用了。每个location配置里都可以添加多个filter，所以说（比如）响应可以被压缩和分块。多个filter的执行顺序是编译时就确定了的。
  filter采用了经典的“CHAIN OF RESPONSIBILITY”设计模式：一个filter被调用并处理，接下来调用下一个filter，直到最后一个filter被调用完成，Nginx才真正完成响应流程。

  最酷的部分是在filter链中，每个filter不会等待之前的filter完全完工，它可以处理之前filter正在输出的内容，这有点像Unix中的管道（pipeline）。
  Filter的操作都基于_buffers_，buffer通常情况下等于一个页（page）的大小（4k)，你也可以在 `nginx.conf` 里改变它的大小。
  这意味着，比如说，模块可以在从后端服务器收到全部的响应之前，就开始压缩这个响应并输出给客户端了。好牛逼啊~

  总结一下上面的内容，一个典型的处理周期应当是这样的：
  ```
  客户端发送HTTP request → Nginx基于location的配置选择一个合适的handler →  
  (如果有) load-balancer选择一个后端服务器 → Handler处理请求并顺序将每一个响应buffer发送给第一个filter →  
  第一个filter讲输出交给第二个filter → 第二个给第三个 → 第三个给第四个 → 以此类推 → 最终响应发送给客户端
  ```

  我之所以说“典型的”是因为Ngingx的模块具有 _很强_ 的定制性。模块开发者需要花很多精力精确定义模块在何时该如何产生作用（我认为是件不容易的事）。
  模块调用实际上是通过一系列的回调函数做到的，而且有很多很多。名义上来说，你的函数可以在以下时候被执行：

    * server读取配置文件之前
    * 读取location和server的每一条配置指令时
    * 当Nginx初始化main配置段时
    * 当Nginx初始化server配置段时（例如：host/port）
    * 当Nginx合并server配置和main配置时
    * 当Nginx初始化location配置时
    * 当Nginx合并location配置和它的父server配置时
    * 当Nginx的主进程启动时
    * 当一个新的worker进程启动时
    * 当一个worker进程退出时
    * 当主进程退出时
    * handle一个请求
    * Filter响应头
    * Filter响应体
    * 选择一个后端服务器
    * 初始化一个将发往后端服务器的请求
    * 重新初始化一个将发往后端服务器的请求
    * 处理来自后端服务器的响应
    * 完成与后端服务器的交互

 难以置信！有这么多的功能任你处置，而你只需仅仅通过多组有用的钩子（由函数指针组成的结构体）和相应的实现函数。让我们开始接触一些模块吧。


## 2. Nginx模块的组成

我说过，Nginx模块的构建是很灵活的。这一节讲描述的东西会经常出现。它可以帮助你理解模块，也可以作为开发模块的手册。

### 2.1. 模块的配置结构

模块的配置struct有三种，分别是main，server和location。绝大多数模块仅需要一个location配置。
名称约定如下：`ngx_http_<module name>_(main|srv|loc)_conf_t`. 这里有一个dav模块的例子：

```
typedef struct {
    ngx_uint_t  methods;
    ngx_flag_t  create_full_put_path;
    ngx_uint_t  access;
} ngx_http_dav_loc_conf_t;
```

注意到上面展示了Nginx的一些特殊类型(`ngx_uint_t` 和 `ngx_flag_t`); 这些只是基本类型的别名而已。(如果想知道具体是什么的别名，可以参考 [core/ngx_config.h](http://www.evanmiller.org/lxr/http/source/core/ngx_config.h#L79) ).

这些类型用在配置结构体中的情形很多。


### 2.2. 模块指令

模块的指令是定义在一个叫做`ngx_command_t`的静态数组中的。下面举个来自我自己写的小模块中的例子，来告诉你模块指令是如何声明的：

```
static ngx_command_t  ngx_http_circle_gif_commands[] = {
    { ngx_string("circle_gif"),
      NGX_HTTP_LOC_CONF|NGX_CONF_NOARGS,
      ngx_http_circle_gif,
      NGX_HTTP_LOC_CONF_OFFSET,
      0,
      NULL },

    { ngx_string("circle_gif_min_radius"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_LOC_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_num_slot,
      NGX_HTTP_LOC_CONF_OFFSET,
      offsetof(ngx_http_circle_gif_loc_conf_t, min_radius),
      NULL },
      ...
      ngx_null_command
};
```

下面是结构体`ngx_command_t`(静态数组里的每一个元素)的定义 , 来自[core/ngx_conf_file.h](http://www.evanmiller.org/lxr/http/source/core/ngx_conf_file.h#L77):

```
struct ngx_command_t {
    ngx_str_t             name;
    ngx_uint_t            type;
    char               *(*set)(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
    ngx_uint_t            conf;
    ngx_uint_t            offset;
    void                 *post;
};
```

看起来结构的成员变量多了点，不过它们都各有用处。

`name` 是指令的字符串名（顾名思义就是指令名称），不能包含空格. 它的类型是`ngx_str_t`, 通常都是以像(e.g.) `ngx_str("proxy_pass")`这样的方式来初始化. 注意： `ngx_str_t` 包含一个存放字符串内容的`data`字段，和一个存放字符串长度的`len`字段。Nginx广泛地使用这个类型来存放字符串。

`type`是标识的集合，表明这个指令在哪里出现是合法的、指令的参数有几个。应用中，标识一般是下面多个值的二进制或(bitwise-OR)组成：

  * `NGX_HTTP_MAIN_CONF`: 指令出现在main配置部分是合法的
  * `NGX_HTTP_SRV_CONF`: 指令在server配置部分出现是合法的 config
  * `NGX_HTTP_LOC_CONF`: 指令在location配置部分出现是合法的
  * `NGX_HTTP_UPS_CONF`: 指令在upstream配置部分出现是合法的

  * `NGX_CONF_NOARGS`: 指令没有参数
  * `NGX_CONF_TAKE1`: 指令读入1个参数
  * `NGX_CONF_TAKE2`: 指令读入2个参数
  * ...
  * `NGX_CONF_TAKE7`: 指令读入7个参数

  * `NGX_CONF_FLAG`: 指令读入1个布尔型数据 ("on" or "off")
  * `NGX_CONF_1MORE`: 指令至少读入1个参数
  * `NGX_CONF_2MORE`: 指令至少读入2个参数

这里还有很多其他的选项：参考[core/ngx_conf_file.h](http://www.evanmiller.org/lxr/http/source/core/ngx_conf_file.h#L1)。

结构体成员 `set` 是一个函数指针，它指向的函数用来进行模块配置；这个设定函数一般用来将配置文件中的参数传递给程序，并保存在配置结构体中。设定函数有三个入参：

  1. 指向结构体 `ngx_conf_t` 的指针, 这个结构体里包含需要传递给指令的参数
  2. 指向结构体 `ngx_command_t` 的指针
  3. 指向模块自定义配置结构体的指针

设定函数会在遇到指令时触发，Nginx提供了多个函数用来保存特定类型的数据，这些函数包含有：

  * `ngx_conf_set_flag_slot`: 将 "on" or "off" 转换成 1 or 0
  * `ngx_conf_set_str_slot`: 将字符串保存为 `ngx_str_t`
  * `ngx_conf_set_num_slot`: 解析一个数字并保存为`int`
  * `ngx_conf_set_size_slot`: 解析一个数据大小(如："8k", "1m") 并保存为`size_t`

当然还有其他的，参考[core/ngx_conf_file.h](http://www.evanmiller.org/lxr/http/source/core/ngx_conf_file.h#L329)。如果你觉得现有这些内置的函数还不能满足你，当然也可以传入自己的函数引用。

这些内置函数是如何知道把数据存放在哪里的呢？这就是接下来 `ngx_command_t` 的两个结构体成员 `conf` 和 `offset` 要做的事了. `conf` 告诉Nginx把数据存在模块的哪个配置中，是 main 配置、server 配置, 还是 location 配置 ？(通过 `NGX_HTTP_MAIN_CONF_OFFSET`, `NGX_HTTP_SRV_CONF_OFFSET`, 或者 `NGX_HTTP_LOC_CONF_OFFSET`). `offset` 确定到底是保存在结构体的哪个位置。

_最后_, `post`指向模块在读配置的时候需要的一些零碎变量。多数情况下它设为NULL。

`ngx_command_t`数组以设置 `ngx_null_command` 为最后一个元素当作结尾（就好像字符串以'\0'为终结符一样）。


