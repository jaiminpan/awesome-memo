# Emiller的Nginx模块开发指南(中文版)

  By [Evan Miller](http://www.evanmiller.org/) Last edit: January 16, 2013
  [Link](http://www.evanmiller.org/nginx-modules-guide.html)

  By [Jaimin](http://github.com/jaiminpan), Update and Re-format base on Kongch's workout
  [Link](https://github.com/jaiminpan/MYWIKI/blob/master/nginx/ModuleDev.md)

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

### 2.3. 模块上下文

静态的`ngx_http_module_t`结构体，包含一大坨函数指针，用来创建和合并三段配置(main,server,location)，命名方式一般是：`ngx_http_<module name>_module_ctx`。 这些函数引用依次是:

    * preconfiguration 在读入配置前调用
    * postconfiguration 在读入配置后调用
    * create_main_conf 在创建main配置时调用（比如，用来分配空间和设置默认值）
    * init_main_conf 在初始化main配置时调用（比如，把原来的默认值用nginx.conf读到的值来覆盖）
    * init_main_conf 在创建server配置时调用
    * merge_srv_conf 合并server和main配置时调用
    * create_loc_conf 创建location配置时调用
    * merge_loc_conf 合并location和server配置时调用

 函数的入参各不相同，取决于他们具体要做的事情。这里是结构体的定义，来自[http/ngx_http_config.h](http://www.evanmiller.org/lxr/http/source/http/ngx_http_config.h#L22)：

```
typedef struct {
    ngx_int_t   (*preconfiguration)(ngx_conf_t *cf);
    ngx_int_t   (*postconfiguration)(ngx_conf_t *cf);

    void       *(*create_main_conf)(ngx_conf_t *cf);
    char       *(*init_main_conf)(ngx_conf_t *cf, void *conf);

    void       *(*create_srv_conf)(ngx_conf_t *cf);
    char       *(*merge_srv_conf)(ngx_conf_t *cf, void *prev, void *conf);

    void       *(*create_loc_conf)(ngx_conf_t *cf);
    char       *(*merge_loc_conf)(ngx_conf_t *cf, void *prev, void *conf);
} ngx_http_module_t;
```

可以把你不需要的函数设置为NULL，Nginx会忽略掉他们。

绝大多数的 handler 只使用最后两个：一个用来为特定location：配置分配内存，(叫做 `ngx_http_<module name>_create_loc_conf`)。
另一个用来设定默认值以及合并继承过来的配置值(叫做 `ngx_http_<module name>_merge_loc_conf`)。合并函数同时还会检查配置的有效性，如果有错误，则server的启动将被挂起。

下面是一个使用模块上下文结构体的例子:

```
static ngx_http_module_t  ngx_http_circle_gif_module_ctx = {
    NULL,                          /* preconfiguration */
    NULL,                          /* postconfiguration */

    NULL,                          /* create main configuration */
    NULL,                          /* init main configuration */

    NULL,                          /* create server configuration */
    NULL,                          /* merge server configuration */

    ngx_http_circle_gif_create_loc_conf,  /* create location configuration */
    ngx_http_circle_gif_merge_loc_conf /* merge location configuration */
};
```

现在开始讲得更深一点。这些配置回调函数看其来很像，所有模块都类似，而且Nginx的API都会用到这个部分，所以值得好好看看。

#### 2.3.1. create_loc_conf

下面这段摘自我自己写的模块[circle_gif](http://www.riceonfire.org/emiller/ngx_http_circle_gif_module.c.txt 源代码)，create_loc_conf的骨架大概就是这个样子. 它的入参是(`ngx_conf_t`)，返回值是模块配置结构体(在这里是`ngx_http_circle_gif_loc_conf_t`)。

```
static void *
ngx_http_circle_gif_create_loc_conf(ngx_conf_t *cf)
{
    ngx_http_circle_gif_loc_conf_t  *conf;

    conf = ngx_pcalloc(cf->pool, sizeof(ngx_http_circle_gif_loc_conf_t));
    if (conf == NULL) {
        return NGX_CONF_ERROR;
    }
    conf->min_radius = NGX_CONF_UNSET_UINT;
    conf->max_radius = NGX_CONF_UNSET_UINT;
    return conf;
}
```

首先需要指出的是Nginx的内存分配；只要使用了 `ngx_palloc` (`malloc`的一个封装) 或者 `ngx_pcalloc` (`calloc`的封装)，就不用担心内存的释放了（nigix的内存管理机制会替你释放内存）。

UNSET可能的常量有`NGX_CONF_UNSET_UINT`， `NGX_CONF_UNSET_PTR`， `NGX_CONF_UNSET_SIZE`， `NGX_CONF_UNSET_MSEC`，以及无所不包的`NGX_CONF_UNSET`，UNSET让合并函数知道变量是需要覆盖的。

#### 2.3.2. merge_loc_conf

下面的例子是我的模块circle_gif中的合并函数：

```
static char *
ngx_http_circle_gif_merge_loc_conf(ngx_conf_t *cf, void *parent, void *child)
{
    ngx_http_circle_gif_loc_conf_t *prev = parent;
    ngx_http_circle_gif_loc_conf_t *conf = child;

    ngx_conf_merge_uint_value(conf->min_radius, prev->min_radius, 10);
    ngx_conf_merge_uint_value(conf->max_radius, prev->max_radius, 20);

    if (conf->min_radius < 1) {
        ngx_conf_log_error(NGX_LOG_EMERG, cf, 0,
            "min_radius must be equal or more than 1");
        return NGX_CONF_ERROR;
    }
    if (conf->max_radius < conf->min_radius) {
        ngx_conf_log_error(NGX_LOG_EMERG, cf, 0,
            "max_radius must be equal or more than min_radius");
        return NGX_CONF_ERROR;
    }

    return NGX_CONF_OK;
}
```

这里的需要注意的是Nginx提供了一些好用的合并函数用来合并不同类型的数据(`ngx_conf_merge_<data type>_value`)，这类函数的入参是：

    1. _当前_ location的变量值
    2. 如果第一个参数没有被设置而采用的值
    3. 如果第一第二个参数都没有被设置而采用的值

结果会被保存在第一个参数中。能用的合并函数包括 `ngx_conf_merge_size_value`, `ngx_conf_merge_msec_value` 等等。可参见[core/ngx_conf_file.h](http://www.evanmiller.org/lxr/http/source/core/ngx_conf_file.h#L254).

    问: 第一个参数是传值的，那如何能做到将结果保存到第一个参数中？
    答: 这些函数都是由预处理命令定义的（在真正编译之前，它们会被扩展成一些if语句）

需要注意到错误的产生。函数会往log文件写一些东西，同时返回`NGX_CONF_ERROR`。这个返回值会将server的启动挂起。（因为被标示为`NGX_LOG_EMERG`级别，所以错误同时还会输出到标准输出。
参考[core/ngx_log.h](http://www.evanmiller.org/lxr/http/source/core/ngx_log.h#L1)列出了所有的日志级别。）

#### 2.4. 模块定义

接下来我们间接地介绍更深一层：结构体`ngx_module_t`。该结构体变量命名方式为`ngx_http_<module name>_module`。它包含模块的内容和指令执行方式，同时也还包含一些回调函数（退出线程，退出进程，等等）。
模块定义在有的时候会被用作查找的关键字，来查找与特定模块相关联的数据。模块定义通常像是这样：

```
ngx_module_t  ngx_http_<module name>_module = {
    NGX_MODULE_V1,
    &ngx_http_<module name>_module_ctx, /* module context */
    ngx_http_<module name>_commands,   /* module directives */
    NGX_HTTP_MODULE,               /* module type */
    NULL,                          /* init master */
    NULL,                          /* init module */
    NULL,                          /* init process */
    NULL,                          /* init thread */
    NULL,                          /* exit thread */
    NULL,                          /* exit process */
    NULL,                          /* exit master */
    NGX_MODULE_V1_PADDING
};
```

...仅仅替换掉`<module name>`就可以了。
模块可以添加一些回调函数来处理线程/进程的创建和销毁，但是绝大多数模块都用NULL忽略这些东东。
(关于这些回调函数的入参，可以参考[core/ngx_conf_file.h](http://www.evanmiller.org/lxr/http/source/core/ngx_conf_file.h#L110) ) 

#### 2.5. 模块装载

模块的装载方式取决于模块的类型：handler、filter还是load-balancer。
所以具体的装载细节将留在其各自的章节中再做介绍。

## 3. Handlers

接下来我们把模块的细节放到显微镜下面来看，它们到底怎么运行的。

### 3.1. 剖析Handler(非代理 Non-proxying)

Handler一般做4件事：获取location配置，生成合适的响应，发送响应头，发送响应体。Handler有一个参数，即request结构体。request结构体包含很多关于客户请求的有用信息，比如说请求方法，URI，请求头等等。我们一个个地来看。

#### 3.1.1. 获取location配置

这部分很简单。只需要调用 `ngx_http_get_module_loc_conf`，传入当前请求的结构体和模块定义即可。下面是我的`circle gif` handler的相关部分：

```
static ngx_int_t
ngx_http_circle_gif_handler(ngx_http_request_t *r)
{
    ngx_http_circle_gif_loc_conf_t  *circle_gif_config;
    circle_gif_config = ngx_http_get_module_loc_conf(r, ngx_http_circle_gif_module);
    ...
```

现在我们就可以访问之前在合并函数中设置的所有变量了。

#### 3.1.2. 生成响应

这才是模块真正干活的部分，相当有趣。

这里要用到请求结构体，主要是这些结构体成员：

```
typedef struct {
...
/* the memory pool, used in the ngx_palloc functions */
    ngx_pool_t                       *pool;
    ngx_str_t                         uri;
    ngx_str_t                         args;
    ngx_http_headers_in_t             headers_in;

...
} ngx_http_request_t;

```

`uri` 是请求的路径, e.g. "/query.cgi"。  
`args` 请求串参数中问号后面的参数 (e.g. "name=john")。  
`headers_in` 包含有很多有用的东西，比如说cookie啊，浏览器信息啊什么的，但是许多模块可能用不到这些东东。
如果你感兴趣的话，可以参考[http/ngx_http_request.h](http://www.evanmiller.org/lxr/http/source/http/ngx_http_request.h#L158)。  

用这些信息来生成输出应该是足够了。完整的`ngx_http_request_t`结构体定义来自[http/ngx_http_request.h](http://www.evanmiller.org/lxr/http/source/http/ngx_http_request.h#L316)。

#### 3.1.3. 发送响应头

响应头存放在结构体`headers_out`中，它的引用存放在请求结构体中。
Handler设置相应的响应头的值，然后调用`ngx_http_send_header(r)`。`headers_out`中比较有用的是：

```
typedef stuct {
...
    ngx_uint_t                        status;
    size_t                            content_type_len;
    ngx_str_t                         content_type;
    ngx_table_elt_t                  *content_encoding;
    off_t                             content_length_n;
    time_t                            date_time;
    time_t                            last_modified_time;
..
} ngx_http_headers_out_t;
```

(剩下的可以在 [http/ngx_http_request.h](http://www.evanmiller.org/lxr/http/source/http/ngx_http_request.h#L220)找到。)

举例来说，如果一个模块要设置Content-Type 为 "image/gif"，Content-Length 为 100，并返回 HTTP 200 OK 的响应，代码应当是这样的:
```
    r->headers_out.status = NGX_HTTP_OK;
    r->headers_out.content_length_n = 100;
    r->headers_out.content_type.len = sizeof("image/gif") - 1;
    r->headers_out.content_type.data = (u_char *) "image/gif";
    ngx_http_send_header(r);
```

上面的设定方式针对大多数参数都是有效的。但一些头部的变量设定要比上面的例子要麻烦。
比如，`content_encoding` 还含有类型`(ngx_table_elt_t*)`，所以必须先为此分配空间。可以用一个叫做`ngx_list_push`的函数来做，它传入一个`ngx_list_t`（与数组类似），返回一个list中的新成员（类型是`ngx_table_elt_t`）。下面的代码设置了Content-Encoding为"deflate"并发送了响应头：

```
    r->headers_out.content_encoding = ngx_list_push(&r->headers_out.headers);
    if (r->headers_out.content_encoding == NULL) {
        return NGX_ERROR;
    }
    r->headers_out.content_encoding->hash = 1;
    r->headers_out.content_encoding->key.len = sizeof("Content-Encoding") - 1;
    r->headers_out.content_encoding->key.data = (u_char *) "Content-Encoding";
    r->headers_out.content_encoding->value.len = sizeof("deflate") - 1;
    r->headers_out.content_encoding->value.data = (u_char *) "deflate";
    ngx_http_send_header(r);
```

当头部有多个值时，这个机制常常被用到。它（理论上讲）使得过滤模块添加、删除某个值而保留其他值的时候更加容易，在操纵字符串的时候，不需要把字符串重新排序。

#### 3.1.4. 发送响应体

现在模块已经生成了一个响应，并存放在了内存中。接下来它需要将这个响应分配给一个特定的缓冲区，然后把这个缓冲区加入到 _链表_ ，_然后_ 调用链表中“发送响应体”的函数。

链表在这里起什么作用呢？Nginx中，handler模块（其实filter模块也是）生成响应到buffer中是同时完成的；链表中的每个元素都有指向下一个元素的指针，如果是NULL则说明链表到头了。简单起见，我们假设只有一个buffer。

首先，模块需要先声明buffer和链表：
```
    ngx_buf_t    *b;
    ngx_chain_t   out;
```

接着，需要给buffer分配空间，并将我们的响应数据指向它：
```
    b = ngx_pcalloc(r->pool, sizeof(ngx_buf_t));
    if (b == NULL) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "Failed to allocate response buffer.");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    b->pos = some_bytes; /* first position in memory of the data */
    b->last = some_bytes + some_bytes_length; /* last position */

    b->memory = 1; /* content is in read-only memory */
    /* (i.e., filters should copy it rather than rewrite in place) */

    b->last_buf = 1; /* there will be no more buffers in the request */
```

现在就可以把数据挂在链表上了：
```
    out.buf = b;
    out.next = NULL;
```

最后，我们发送这个响应体，返回值是经过filter链表处理后的状态:
```
    return ngx_http_output_filter(r, &out);
```

Buffer链是Nginx IO模型中的关键部分，你得比较熟悉它的工作方式。

    问: 为什么buffer还需要有个`last_buf`变量啊，我们不是可以通过判断next是否是NULL来知道哪个是链表的最末端了吗？
    答: 链表可能是不完整的，比如说，当有多个buffer的时候，并不是所有的buffer都属于当前的请求和响应。
        所以有些buffer可能是buffer链表的表尾，但是不是请求的结束。这给我们引入了接下来的内容……


### 3.2. 剖析Upstream(又称 Proxy) Handler

我已经帮你了解了如何让你的handler来产生响应。有些时候你可以用一小段C代码就可以得到响应，但是通常情况下你需要同另外一台server打交道（比如你正在写一个用来实现某种网络协议的模块）。
你当然可以自己实现一套网络编程的东东，但是如果你只收到部分的响应，需要等待余下的响应数据，你会怎么办？你不会想阻塞整个事件处理循环吧？这样会毁掉Nginx的良好性能！
幸运的是，Nginx允许你在它处理后端服务器（叫做"upstreams"）的机制上加入你的回调函数,因此你的模块将可以和其他的server通信,同时还不会妨碍其他的请求。

这一节将介绍模块如何和一个upstream通信，如 Memcached，FastCGI，或者另一个 HTTP server。

#### 3.2.1. Upstream 回调函数概要

与其他模块的回调处理函数不一样，upstream模块的处理函数几乎不做“具体的”事。它_压根不_调用`ngx_http_output_filter`。它仅仅是设置当upstream server可读写时所触发的回调函数。
实际上它有6个可用的钩子(hooks)：

    `create_request` 生成发送到upstream server的请求缓冲（或者一条缓冲链）
    `reinit_request` 在与后端服务器连接被重置的情况下被调用（在`create_request` 被第二次调用之前）
    `process_header` 处理upstream 响应的第一个bit，通常是保存一个指向upstream "payload"的指针
    `abort_request` 在客户端放弃请求时被调用
    `finalize_request` 在Nginx完成从upstream读取数据后调用
    `input_filter` 这是一个消息体的filter，用来处理响应消息体(例如把尾部删除)

这些钩子是怎么挂载上去的呢？下面是一个例子，简单版本的代理模块处理函数：
```
static ngx_int_t
ngx_http_proxy_handler(ngx_http_request_t *r)
{
    ngx_int_t                   rc;
    ngx_http_upstream_t        *u;
    ngx_http_proxy_loc_conf_t  *plcf;

    plcf = ngx_http_get_module_loc_conf(r, ngx_http_proxy_module);

/* set up our upstream struct */
    u = ngx_pcalloc(r->pool, sizeof(ngx_http_upstream_t));
    if (u == NULL) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    u->peer.log = r->connection->log;
    u->peer.log_error = NGX_ERROR_ERR;

    u->output.tag = (ngx_buf_tag_t) &ngx_http_proxy_module;

    u->conf = &plcf->upstream;

/* attach the callback functions */
    u->create_request = ngx_http_proxy_create_request;
    u->reinit_request = ngx_http_proxy_reinit_request;
    u->process_header = ngx_http_proxy_process_status_line;
    u->abort_request = ngx_http_proxy_abort_request;
    u->finalize_request = ngx_http_proxy_finalize_request;

    r->upstream = u;

    rc = ngx_http_read_client_request_body(r, ngx_http_upstream_init);

    if (rc >= NGX_HTTP_SPECIAL_RESPONSE) {
        return rc;
    }

    return NGX_DONE;
}
```

看上去都是些例行事务，不过重要的是那些回调函数。同时还要注意的是`ngx_http_read_client_request_body`，它又设置了一个回调函数，在Nginx完成从客户端读数据后会被调用。

这些个回调函数都要做些什么工作呢？通常情况下，`reinit_request`, `abort_request`, 和 `finalize_request` 用来设置或重置一些内部状态，但这些都是几行代码的事情。真正做苦力的是`create_request` 和 `process_header`。

#### 3.2.2. create_request 回调函数

简单来说，假设我有一个upstream server，它读入一个字符打印出两个字符。那么函数应该如何来写呢？

`create_request`需要申请一个buffer来存放“一个字符”的请求，为buffer申请一个链表，并且把链表挂到upstream结构体上。看起来就像这样：
```
static ngx_int_t
ngx_http_character_server_create_request(ngx_http_request_t *r)
{
/* make a buffer and chain */
    ngx_buf_t *b;
    ngx_chain_t *cl;

    b = ngx_create_temp_buf(r->pool, sizeof("a") - 1);
    if (b == NULL)
        return NGX_ERROR;

    cl = ngx_alloc_chain_link(r->pool);
    if (cl == NULL)
        return NGX_ERROR;

/* hook the buffer to the chain */
    cl->buf = b;
/* chain to the upstream */
    r->upstream->request_bufs = cl;

/* now write to the buffer */
    b->pos = "a";
    b->last = b->pos + sizeof("a") - 1;

    return NGX_OK;
}
```

不是很难，对吧？当然实际应用中你很可能还会用到请求里面的URI。`r->uri`作为一个 `ngx_str_t`类型也是有效的，GET的参数在`r->args`中，最后别忘了你还能访问请求头和cookie信息。

#### 3.2.3. process_header 回调函数

现在轮到`process_header`了，就像`create_request`添加链表指针到请求结构体上去一样，`process_header` _把响应指针移到客户端可以接收到的那部分上_。同时它还会从upstream读入头信息，并且相应的设置发往客户端的响应头。

这里有个小例子，读进两个字符的响应。我们假设第一个字符代表“状态”字符。如果它是问号，我们将返回一个“404错误”并丢弃剩下的那个字符。
如果它是空格，我们将以”200 OK“的响应把另一个字符返回给客户端。好吧，这不是什么多有用的协议，不过可以作为一个不错的例子。那么我们如何来实现这个`process_header` 函数呢？
```
static ngx_int_t
ngx_http_character_server_process_header(ngx_http_request_t *r)
{
    ngx_http_upstream_t       *u;
    u = r->upstream;

    /* read the first character */
    switch(u->buffer.pos[0]) {
        case '?':
            r->header_only; /* suppress this buffer from the client */
            u->headers_in.status_n = 404;
            break;
        case ' ':
            u->buffer.pos++; /* move the buffer to point to the next character */
            u->headers_in.status_n = 200;
            break;
    }

    return NGX_OK;
```

就是这样。操作头部，改变指针，搞定！注意`headers_in`实际上就是我们之前提到过的响应头[http/ngx_http_request.h](http://www.evanmiller.org/lxr/http/source/http/ngx_http_request.h#L158)，但是它位于来自upstream的头中。一个真正的代理模块会在头信息的处理上做很多文章，不光是错误处理，做什么完全取决于你的想法。

但是...如果一个buffer没有能够装下全部的从upstream来的头信息，该怎么办呢？

#### 3.2.4. 状态保持

好了，还记得我说过`abort_request`, `reinit_request`和`finalize_request` 可以用来重置内部状态吗？
这是因为许多upstream模块都有其内部状态。模块需要定义一个 _自定义的上下文结构(custom context struct)_ ，来标记目前为止从upstream读到了什么。这跟之前说的“模块上下文(Module Context)”不是一个概念。
“模块上下文”是预定义类型，而自定义上下文结构可以包含任何你需要的数据和字段（这可是你自己定义的结构体）。这个结构体在`create_request`函数中被实例化，大概像这样：
```
    ngx_http_character_server_ctx_t   *p;   /* my custom context struct */

    p = ngx_pcalloc(r->pool, sizeof(ngx_http_character_server_ctx_t));
    if (p == NULL) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    ngx_http_set_ctx(r, p, ngx_http_character_server_module);
```

最后一行实际上将自定义上下文结构体注册到了特定的请求和模块名上，以便在稍后取用。当你需要这个结构体时（可能所有的回调函数中都需要它），只需要：
```
    ngx_http_proxy_ctx_t  *p;
    p = ngx_http_get_module_ctx(r, ngx_http_proxy_module);
```

指针 `p` 可以得到当前的状态。设置、重置、增加、减少、往里填数据... 你可以随心所欲的操作它。当upstream服务器返回一块一块的响应时，读取这些响应的过程中使用持久状态机是个很牛逼的办法，它不用阻塞主事件循环。很好很强大！

### 3.3. Handler的装载

Handler的装载通过往模块启用了指令的回调函数中添加代码来完成。比如，我的circle gif 中`ngx_command_t`是这样的：
```
    { ngx_string("circle_gif"),
      NGX_HTTP_LOC_CONF|NGX_CONF_NOARGS,
      ngx_http_circle_gif,
      0,
      0,
      NULL }
```

回调函数是里面的第三个元素，在这个例子中就是那个`ngx_http_circle_gif`。回调函数的参数是由指令结构体(`ngx_conf_t`, 包含用户配置的参数)，相应的`ngx_command_t`结构体以及一个指向模块自定义配置结构体的指针组成的。我的circle gif模块中，这些函数是这样子的：
```
static char *
ngx_http_circle_gif(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
{
    ngx_http_core_loc_conf_t  *clcf;

    clcf = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);
    clcf->handler = ngx_http_circle_gif_handler;

    return NGX_CONF_OK;
}
```

这里可以分为两步：首先，得到当前location的“core”结构体，再分配给它一个handler。很简单，不是吗？

我已经把我知道的关于hanler模块的东西全交代清楚了，现在可以来说说输出过滤链上的filter模块了。


## 4. Filters

Filter操作handler生成的响应。头部filter操作HTTP头，body filter操作响应的内容。

### 4.1. 剖析Header Filter

头部Filter由三个步骤组成：

  1. 决定是否处理响应
  2. 处理响应
  3. 调用下一个filter

举个例子，比如有一个简化版本的“不改变”头部filter：如果客户请求头中的“If-Modified-Since”和响应头中的“Last-Modified”相符，它把响应状态设置成“304 Not Modified”。注意这个头部filter只读入一个参数：`ngx_http_request_t`结构体，而我们可以通过它操作到客户请求头和一会将被发送的响应消息头。
```
static
ngx_int_t ngx_http_not_modified_header_filter(ngx_http_request_t *r)
{
    time_t  if_modified_since;

    if_modified_since = ngx_http_parse_time(r->headers_in.if_modified_since->value.data,
                              r->headers_in.if_modified_since->value.len);

/* step 1: decide whether to operate */
    if (if_modified_since != NGX_ERROR &&
        if_modified_since == r->headers_out.last_modified_time) {

/* step 2: operate on the header */
        r->headers_out.status = NGX_HTTP_NOT_MODIFIED;
        r->headers_out.content_type.len = 0;
        ngx_http_clear_content_length(r);
        ngx_http_clear_accept_ranges(r);
    }

/* step 3: call the next filter */
    return ngx_http_next_header_filter(r);
}
```

结构`headers_out`和我们在hander那一节中看到的是一样的，（参考[http/ngx_http_request.h](http://www.evanmiller.org/lxr/http/source/http/ngx_http_request.h#L220) ），也可以随意处置。

### 4.2. 剖析Body Filter

因为body filter一次只能操作一个buffer（链表），这使得编写body filter需要一定的技巧。模块需要知道什么时候可以_覆盖_输入buffer，用新申请的buffer_替换_已有的，或者在现有的某个buffer前或后_插入_一个新buffer。

有时候模块会收到许多buffer使得它不得不操作一个_不完整的链表_，这使得事情变得更加复杂了。而更加不幸的是，Nginx没有为我们提供上层的API来操作buffer链表，所以body filter是比较难懂（当然也比较难写）。但是，有些操作你还是可以看出来的。

一个body filter原型大概是这个样子（例子代码从Nginx源代码的“chunked” filter中取得）：
```
static ngx_int_t ngx_http_chunked_body_filter(ngx_http_request_t *r, ngx_chain_t *in);
```

第一个参数是request结构体，第二个参数则是指向当前部分链表头的指针（可能包含0，1，或更多的buffer）。

再来举个简单的例子。假设我们想要在每个请求之后插入文本"<l!-- Served by Nginx -->"。首先，我们需要判断给我们的 buffer 链表中是否已经包含响应的最终buffer。就像之前我说的，这里没有简便好用的API，所以我们只能自己来写个循环：
```
    ngx_chain_t *chain_link;
    int chain_contains_last_buffer = 0;

    chain_link = in;
    for ( ; ; ) {
        if (chain_link->buf->last_buf)
            chain_contains_last_buffer = 1;
        if (chain_link->next == NULL)
            break;
        chain_link = chain_link->next;
    }
```

如果我们没有最后的buffer，就返回：
```
    if (!chain_contains_last_buffer)
        return ngx_http_next_body_filter(r, in);
```

很好，现在最后一个buffer已经存在链表中了。接下来我们分配一个新buffer：
```
    ngx_buf_t    *b;
    b = ngx_calloc_buf(r->pool);
    if (b == NULL) {
        return NGX_ERROR;
    }
```

把数据放进去:
```
    b->pos = (u_char *) "<!-- Served by Nginx -->";
    b->last = b->pos + sizeof("<!-- Served by Nginx -->") - 1;
```

把这个buffer挂在新的链表上：
```
    ngx_chain_t   *added_link;

    added_link = ngx_alloc_chain_link(r->pool);
    if (added_link == NULL)
        return NGX_ERROR;

    added_link->buf = b;
    added_link->next = NULL;
```

最后，把这个新链表挂在先前链表的末尾：
```
    chain_link->next = added_link;
```

并根据变化重置变量"last_buf"的值：
```
    chain_link->buf->last_buf = 0;
    added_link->buf->last_buf = 1;
```

再将修改过的链表传递给下一个输出过滤函数：
```
    return ngx_http_next_body_filter(r, in);
```

编写这个函数比实际的具体工作消耗了更多的精力，简单如mod_perl(`$response->body =~ s/$/<!-- Served by mod_perl -->/`)，但是buffer链确实是一个强大的框架，它可以让程序员渐进地处理数据，这使得客户端可以尽可能早地得到一些响应。
但是依我来看，buffer链表实在需要一个更为干净的接口，这样程序员也可以避免操作不一致状态的链表。但是目前为止，所有的风险都得程序员自己控制。

### 4.3. Filter的装载

Filter在回调函数post-configuration中被装载。header filter和body filter都是在这里被装载的。

我们以chunked filter模块为例来具体看看：
```
static ngx_http_module_t  ngx_http_chunked_filter_module_ctx = {
    NULL,                                  /* preconfiguration */
    ngx_http_chunked_filter_init,          /* postconfiguration */
  ...
};
```

`ngx_http_chunked_filter_init`中的具体实现如下:
```
static ngx_int_t
ngx_http_chunked_filter_init(ngx_conf_t *cf)
{
    ngx_http_next_header_filter = ngx_http_top_header_filter;
    ngx_http_top_header_filter = ngx_http_chunked_header_filter;

    ngx_http_next_body_filter = ngx_http_top_body_filter;
    ngx_http_top_body_filter = ngx_http_chunked_body_filter;

    return NGX_OK;
}
```

发生了什么呢？好吧，如果你还记得，filter模块组成了一条”CHAIN OF RESPONSIBILITY“。当handler生成一个响应后，2个函数被调用：`ngx_http_output_filter`它调用全局函数`ngx_http_top_body_filter`；以及`ngx_http_send_header` 它调用全局函数`ngx_top_header_filter`。

`ngx_http_top_body_filter` 和 `ngx_http_top_header_filter`是body和header各自的头部filter链的”链表头“。链表上的每一个”连接“都保存着链表中下一个连接的函数引用(分别是 `ngx_http_next_body_filter` 和 `ngx_http_next_header_filter`)。
当一个filter完成工作之后，它只需要调用下一个filter，直到一个特殊的被定义成”写(write)“的filter被调用，这个”写“filter的作用是包装最终的HTTP响应。你在这个filter_init函数中看到的就是，模块把自己添加到filter链表中；它先把旧的”头部“filter当做是自己的”下一个“，然后再声明”它自己“是”头部“filter。（因此，最后一个被添加的filter会第一个被执行。）

    边注: 这到底是怎么工作的?

    每个filter要么返回一个错误码，要么用调用
    `return ngx_http_next_body_filter();`

    因此，如果filter顺利链执行到了链尾（那个特别定义的的”写“filter），将返回一个"OK"响应，
    但如果执行过程中遇到了错误，链将被砍断，同时Nginx将给出一个错误的信息。
    这是一个单向的，错误快速返回的，只使用函数引用实现的链表。帅啊！


## 5. Load-balancers

Load-balancer用来决定哪一个后端将会收到请求；目前存在的实现是用round-robin方式或者hash方式。
本节将介绍load-balancer模块的装载及其调用。我们将用[upstream_hash_module](http://www.evanmiller.org/nginx/ngx_http_upstream_hash_module.c.txt)作例子。
upstream_hash将对nginx.conf里配置的变量进行hash，来选择后端服务器。

一个load-balancer分为六个部分:

  1. 启用配置指令 (e.g, `hash;`) 将会调用_注册函数_
  2. 注册函数将定义一些合法的`server` 参数 (e.g., `weight=`) 并注册一个 _upstream初始化函数_
  3. upstream初始化函数将在配置经过验证后被调用，并且:

    * 解析 `server` 名称为特定的IP地址
    * 为每个sokcet连接分配空间
    * 设置 _对端初始化函数_ 的回调入口
  4. 对端初始化函数将在每次请求时被调用一次,它主要负责设置一些 _负载均衡函数_ 将会使用的数据结构。
  5. 负载均衡函数决定把请求分发到哪里；每个请求将至少调用一次这个函数（如果后端服务器失败了，那就是多次了），有意思的事情就是在这里做的。
  6. 最后，_对端释放函数_ 可以在与对应的后端服务器结束通信之后更新统计信息 (成功或失败)

好像很多嘛，我来逐一讲讲。


### 5.1. 启用指令

指令声明，既确定了他们在哪里生效又确定了一旦流程遇到指令将要调用什么函数。load-balancer的指令需要置 `NGX_HTTP_UPS_CONF` 标志位，一遍让Nginx知道这个指令只会在`upstream`块中有效。
同时它需要提供一个指向_注册函数_的指针。下面列出的是upstream_hash模块的指令声明：

```
    { ngx_string("hash"),
      NGX_HTTP_UPS_CONF|NGX_CONF_NOARGS,
      ngx_http_upstream_hash,
      0,
      0,
      NULL },
```

这都不是些新东西。

### 5.2. 注册函数

上面的回调函数`ngx_http_upstream_hash`就是所谓的注册函数。之所以这样命名（我起得名字）是因为它把_upstream初始化函数_和周边的`upstream`配置注册到了一块。
另外，注册函数还定义了特定`upstream`块中的`server`指令的一些选项（如`weight=`, `fail_timeout=`），下面是upstream_hash模块的注册函数：

```
ngx_http_upstream_hash(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
 {
    ngx_http_upstream_srv_conf_t  *uscf;
    ngx_http_script_compile_t      sc;
    ngx_str_t                     *value;
    ngx_array_t                   *vars_lengths, *vars_values;

    value = cf->args->elts;

    /* the following is necessary to evaluate the argument to "hash" as a $variable */
    ngx_memzero(&sc, sizeof(ngx_http_script_compile_t));

    vars_lengths = NULL;
    vars_values = NULL;

    sc.cf = cf;
    sc.source = &value[1];
    sc.lengths = &vars_lengths;
    sc.values = &vars_values;
    sc.complete_lengths = 1;
    sc.complete_values = 1;

    if (ngx_http_script_compile(&sc) != NGX_OK) {
        return NGX_CONF_ERROR;
    }
    /* end of $variable stuff */

    uscf = ngx_http_conf_get_module_srv_conf(cf, ngx_http_upstream_module);

    /* the upstream initialization function */
    uscf->peer.init_upstream = ngx_http_upstream_init_hash;

    uscf->flags = NGX_HTTP_UPSTREAM_CREATE;

    /* OK, more $variable stuff */
    uscf->values = vars_values->elts;
    uscf->lengths = vars_lengths->elts;

    /* set a default value for "hash_method" */
    if (uscf->hash_function == NULL) {
        uscf->hash_function = ngx_hash_key;
    }

    return NGX_CONF_OK;
 }
```

除了依葫芦画瓢的用来计算`$variable`的代码，剩下的都很简单，就是分配一个回调函数，设置一些标志位。哪些标志位是有效的呢？

  * `NGX_HTTP_UPSTREAM_CREATE`: 让upstream块中有 `server` 指令。我实在想不出那种情形会用不到它。
  * `NGX_HTTP_UPSTREAM_WEIGHT`: 让`server`指令获取 `weight=` 选项
  * `NGX_HTTP_UPSTREAM_MAX_FAILS`: 允许 `max_fails=` 选项
  * `NGX_HTTP_UPSTREAM_FAIL_TIMEOUT`: 允许 `fail_timeout=` 选项
  * `NGX_HTTP_UPSTREAM_DOWN`: 允许 `down` 选项
  * `NGX_HTTP_UPSTREAM_BACKUP`: 允许 `backup` 选项

每一个模块都可以访问这些配置值。_一切都取决于模块自己的决定_ 。
也就是说，`max_fails`不会被自动强制执行；所有的失败逻辑都是由模块作者决定的。过会我们再说这个。目前，我们还没有完成对回调函数的追踪呢。接下来，我们来看upstream初始化函数 (上面的函数中的回调函数`init_upstream` )。

### 5.3. upstream 初始化函数

upstream 初始化函数的目的是，解析主机名，为socket分配空间，分配（另一个）回调函数。下面是upstream_hash：

```
ngx_int_t
ngx_http_upstream_init_hash(ngx_conf_t *cf, ngx_http_upstream_srv_conf_t *us)
{
    ngx_uint_t                       i, j, n;
    ngx_http_upstream_server_t      *server;
    ngx_http_upstream_hash_peers_t  *peers;

    /* set the callback */
    us->peer.init = ngx_http_upstream_init_upstream_hash_peer;

    if (!us->servers) {
        return NGX_ERROR;
    }

    server = us->servers->elts;

    /* figure out how many IP addresses are in this upstream block. */
    /* remember a domain name can resolve to multiple IP addresses. */
    for (n = 0, i = 0; i < us->servers->nelts; i++) {
        n += server[i].naddrs;
    }

    /* allocate space for sockets, etc */
    peers = ngx_pcalloc(cf->pool, sizeof(ngx_http_upstream_hash_peers_t)
            + sizeof(ngx_peer_addr_t) * (n - 1));

    if (peers == NULL) {
        return NGX_ERROR;
    }

    peers->number = n;

    /* one port/IP address per peer */
    for (n = 0, i = 0; i < us->servers->nelts; i++) {
        for (j = 0; j < server[i].naddrs; j++, n++) {
            peers->peer[n].sockaddr = server[i].addrs[j].sockaddr;
            peers->peer[n].socklen = server[i].addrs[j].socklen;
            peers->peer[n].name = server[i].addrs[j].name;
        }
    }

    /* save a pointer to our peers for later */
    us->peer.data = peers;

    return NGX_OK;
}
```

这个函数包含的东西比我们预想的多些。大部分的工作似乎都该被抽象出来，但目前却不是，事实就是如此。
倒是有一种简化的策略：调用另一个模块的upstream初始化函数，把这些脏活累活（对端的分配等等）都让它干了，然后再覆盖其`us->peer.init`这个回调函数。例子可以参见[http/modules/ngx_http_upstream_ip_hash_module.c](http://www.evanmiller.org/lxr/http/source/http/modules/ngx_http_upstream_ip_hash_module.c#L80)。

在我们这个观点中的关键点是设置_对端初始化函数_的指向，在我们这个例子里是`ngx_http_upstream_init_upstream_hash_peer`。

### 6.4. 对端初始化函数

对端初始化函数每个请求调用一次。它会构造一个数据结构，模块会用这个数据结构来选择合适的后端服务器；这个数据结构保存着和后端交互的重试次数，通过它可以很容易的跟踪链接失败次数或者是计算好的哈希值。这个结构体习惯性地被命名为`ngx_http_upstream_<module name>_peer_data_t`。

另外，对端初始化函数还会构建两个回调函数：

  * `get`: load-balancing 函数
  * `free`: 对端释放函数 (通常只是在连接完成后更新一些统计信息)

似乎还不止这些，它同时还初始化了一个叫做`tries`的变量。只要`tries`是正数，Nginx将继续重试当前的load-banlancer。当`tries`变为0时，Nginx将放弃重试。一切都取决于`get` 和 `free` 函数如何设置合适的`tries`。

下面是upstream_hash中对端初始化函数的例子：
```
static ngx_int_t
ngx_http_upstream_init_hash_peer(ngx_http_request_t *r,
    ngx_http_upstream_srv_conf_t *us)
{
    ngx_http_upstream_hash_peer_data_t     *uhpd;

    ngx_str_t val;

    /* evaluate the argument to "hash" */
    if (ngx_http_script_run(r, &val, us->lengths, 0, us->values) == NULL) {
        return NGX_ERROR;
    }

    /* data persistent through the request */
    uhpd = ngx_pcalloc(r->pool, sizeof(ngx_http_upstream_hash_peer_data_t)
        + sizeof(uintptr_t)
          * ((ngx_http_upstream_hash_peers_t *)us->peer.data)->number
                  / (8 * sizeof(uintptr_t)));
    if (uhpd == NULL) {
        return NGX_ERROR;
    }

    /* save our struct for later */
    r->upstream->peer.data = uhpd;

    uhpd->peers = us->peer.data;

    /* set the callbacks and initialize "tries" to "hash_again" + 1*/
    r->upstream->peer.free = ngx_http_upstream_free_hash_peer;
    r->upstream->peer.get = ngx_http_upstream_get_hash_peer;
    r->upstream->peer.tries = us->retries + 1;

    /* do the hash and save the result */
    uhpd->hash = us->hash_function(val.data, val.len);

    return NGX_OK;
}
```

看上去不错，我们现在已经准备好选择一台upstream服务器了。

### 5.5. 负载均衡函数

主要部分现在才开始。货真价实的哦。模块就是在这里选择upstream服务器的。负载均衡函数的原型看上去是这样的：

```
static ngx_int_t
ngx_http_upstream_get__peer(ngx_peer_connection_t *pc, void *data);
```

`data`是我们存放所关注的客户端连接中有用信息的结构体。`pc`则是要存放我们将要去连接的server的相关信息。负载均衡函数做的事情就是填写`pc->sockaddr`, `pc->socklen`, 和 `pc->name`。
如果你懂一点网络编程的话，这些东西应该都比较熟悉了；但实际上他们跟我们手头上的任务来比并不算很重要。我们不关心他们代表什么；我们只想知道从哪里找到合适的值来填写他们。

这个函数必须找到一个可用server的列表，挑一个分配给`pc`。我们来看看upstream_hash是怎么做的吧。

之前upstream_hash模块已经通过调用`ngx_http_upstream_init_hash`，把server列表存放在了`ngx_http_upstream_hash_peer_data_t` 这一结构中。这个结构就是现在的`data`:
```
    ngx_http_upstream_hash_peer_data_t *uhpd = data;
```

对端列表现在在`uhpd->peers->peer`中了。我们通过对哈希值与server总数取模来从这个数组中取得最终的对端服务器：
```
    ngx_peer_addr_t *peer = &uhpd->peers->peer[uhpd->hash % uhpd->peers->number];
```

终于大功告成了:
```
    pc->sockaddr = peers->sockaddr;
    pc->socklen  = peers->socklen;
    pc->name     = &peers->name;

    return NGX_OK;
```

就是这样！如果load-balancer模块返回 `NGX_OK`，则意味着“来吧，就用这个server”。如果返回的是`NGX_BUSY`，说明所有的后端服务器目前都不可用，此时Nginx应该重试。

但是...我们怎么记录哪些个服务器不可用了？我们如果不想重试了怎么办？

### 5.6. 对端释放函数

对端释放函数在upstream连接就绪之后开始运行，它的目的是跟踪失败。函数原型如下：
```
void
ngx_http_upstream_free__peer(ngx_peer_connection_t *pc, void *data,
    ngx_uint_t state);
```

头两个参数和我们在load-balancer函数中看到的一样。第三个参数是一个`state`变量，它表明了当前连接是成功还是失败。
它可能是`NGX_PEER_FAILED` (连接失败) 和 `NGX_PEER_NEXT` (连接失败或者连接成功但程序返回了错误)按位或的结果。如果它是0则代表连接成功。

这些失败如何处理则由模块的开发者自己定。如果根本不再用，那结果则应存放到`data`中，这是一个指向每个请求自定义的结构体。

但是对端释放函数的关键作用是可以设置`pc->tries`为0来阻止Nginx在 load-balancer 模块中重试。最简单的对端释放函数应该是这样的：
```
    pc->tries = 0;
```

这样就保证了如果发往后端服务器的请求遇到了错误，客户端将得到一个502 Bad Proxy的错误。

这儿还有一个更为复杂的例子，是从upstream_hash模块中拿来的。如果后端连接失败，它会在位向量(叫做 `tried`,一个 `uintptr_t` 类型的数组)中标示失败，然后继续选择一个新的后端服务器直至成功。
```
#define ngx_bitvector_index(index) index / (8 * sizeof(uintptr_t))
#define ngx_bitvector_bit(index) (uintptr_t) 1 << index % (8 * sizeof(uintptr_t))

static void
ngx_http_upstream_free_hash_peer(ngx_peer_connection_t *pc, void *data,
    ngx_uint_t state)
{
    ngx_http_upstream_hash_peer_data_t  *uhpd = data;
    ngx_uint_t                           current;

    if (state & NGX_PEER_FAILED
            && --pc->tries)
    {
        /* the backend that failed */
        current = uhpd->hash % uhpd->peers->number;

       /* mark it in the bit-vector */
        uhpd->tried[ngx_bitvector_index(current)] |= ngx_bitvector_bit(current);

        do { /* rehash until we're out of retries or we find one that hasn't been tried */
            uhpd->hash = ngx_hash_key((u_char *)&uhpd->hash, sizeof(ngx_uint_t));
            current = uhpd->hash % uhpd->peers->number;
        } while ((uhpd->tried[ngx_bitvector_index(current)] & ngx_bitvector_bit(current)) && --pc->tries);
    }
}
```

因为load-balancer函数只会看新的`uhpd->hash`的值，所以这样是行之有效的。

许多应用程序不提供重试功能，或者在更高层的逻辑中进行了控制。但其实你也看到了，只需这么几行代码这个功能就可以实现了。

## 6. 编写并编译一个新的Nginx模块

至此，你应该可以来找一个现成的Nginx模块来看看，尝试着理解其工作原理。可以试试[src/http/modules/](http://www.evanmiller.org/lxr/http/source/http/modules/)，这里一些现成可用的模块。从里面找一个跟你想要的大概相似的模块深入地看看。看上去很熟悉？没错，应该很熟悉。对照着代码和这篇文章，慢慢理解吧。

但是Emiller并没有写一篇 _深入理解Nginx模块(Balls-In Guide to Reading Nginx Modules)_，真没有。这是一篇 _深入浅出(Balls-Out Guide)_。我们不光只是在理解，我们在编码、创造、和大家分享一起分享。

首先，你需要真正写一个自己的模块。在已有的Nginx源码目录外 (确保你已经有一份最新的nginx源码 [nginx.net](http://nginx.net) )，为你的模块新建一个目录吧。你模块的新目录需要包含下面两个文件:

  * "config"
  * "ngx_http_<your module>_module.c"

"config" 文件将会被 `./configure` 用到，文件的内容取决于模块的类型。

**filter 模块的 "config":**
```
ngx_addon_name=ngx_http_<your module>_module
HTTP_AUX_FILTER_MODULES="$HTTP_AUX_FILTER_MODULES ngx_http_<your module>_module"
NGX_ADDON_SRCS="$NGX_ADDON_SRCS $ngx_addon_dir/ngx_http_<your module>_module.c"
```

**其他模块的 "config":**
```
ngx_addon_name=ngx_http_<your module>_module
HTTP_MODULES="$HTTP_MODULES ngx_http_<your module>_module"
NGX_ADDON_SRCS="$NGX_ADDON_SRCS $ngx_addon_dir/ngx_http_<your module>_module.c"
```

对于具体的C语言文件，我推荐先拷贝一份已经存在且功能类似的模块，在重命名为你自己的 "ngx_http_<your module>_module.c"。再参考这篇文章，进行适当的改动以满足需要。

当你想进行编译，只要进入Nginx的目录然后输入：

```
./configure --add-module=path/to/your/new/module/directory
```

然后像通常一样输入 `make` 和 `make install`。如果一切顺利，你的模块已经打包进去。就这么简单？不用陷入Nginx源码的泥潭，同样把你的模块放进最新版本的Nginx也是小菜一碟。同样只需要输入 `./configure` 。顺便一提的是，如果你的模块需要动态链接库，需要在 "config" 文件中加入下面代码:
```
CORE_LIBS="$CORE_LIBS -lfoo"
```

`foo` 是你需要用到的动态库。如果你开发了一个有用的模块，请发一个通知给 [Nginx mailing list](http://wiki.codemongers.com/MailinglistSubscribe) 以便分享你的成果.

## 8. 高级话题

本指南只涵盖了Nginx模块开发的基础。想开发更为精巧的模块，一定要去 _[Emiller's Advanced Topics In Nginx Module Development](http://www.evanmiller.org/nginx-modules-guide-advanced.html)_ 看看。

## Appendix A: 代码参考

[Nginx source tree (cross-referenced)](http://www.evanmiller.org/lxr/http/source/)  
[Nginx module directory (cross-referenced)](http://www.evanmiller.org/lxr/http/source/http/modules/)  
[Example addon: circle_gif](http://www.evanmiller.org/nginx/ngx_http_circle_gif_module.c.txt)  
[Example addon: upstream_hash](http://www.evanmiller.org/nginx/ngx_http_upstream_hash_module.c.txt)  
[Example addon: upstream_fair](http://github.com/gnosek/nginx-upstream-fair/tree/master)  

## Appendix B: Changelog

  * November 11, 2009: Corrected code sample in 4.2.
  * August 13, 2009: Reorganized, and moved _[Advanced Topics](http://code.google.com/p/emillers-guide-to-nginx-module-chn/nginx-modules-guide-advanced.html)_ to a separate article.
  * July 23, 2009: Corrected code sample in 3.5.3.
  * December 24, 2008: Corrected code sample in 3.4.
  * July 14, 2008: Added information about subrequests; slight reorganization
  * July 12, 2008: Added [Grzegorz Nosek](http://localdomain.pl/)'s guide to shared memory
  * July 2, 2008: Corrected "config" file for filter modules; rewrote introduction; added TODO section
  * May 28, 2007: Changed the load-balancing example to the simpler upstream_hash module
  * May 19, 2007: Corrected bug in body filter example
  * May 4, 2007: Added information about load-balancers
  * April 28, 2007: Initial draft
