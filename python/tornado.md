Tornado
---------

http://www.tornadoweb.org/

Tornado 由前 Facebook 开发，用 Apache License 开源。
代码非常精练，实现也很轻巧，加上清晰的注释和丰富的 demo，我们可以很容易的阅读分析 tornado， 通过阅读 Tornado 的源码，你将学到：

理解 Tornado 的内部实现，使用 tornado 进行 web 开发将更加得心应手。
* 如何实现一个高性能，非阻塞的 http 服务器。
* 如何实现一个 web 框架。
* 各种网络编程的知识，比如 epoll
* python 编程的绝佳实践

在tornado的子目录中，每个模块都应该有一个.py文件，你可以通过检查他们来判断你是否从已经从代码仓库中完整的迁出了项目。在每个源代码的文件中，你都可以发现至少一个大段落的用来解释该模块的doc string，doc string中给出了一到两个关于如何使用该模块的例子。

## 模块分类

1. Core web framework

  tornado.web — 包含web框架的大部分主要功能，包含RequestHandler和Application两个重要的类
  tornado.httpserver — 一个无阻塞HTTP服务器的实现
  tornado.template — 模版系统
  tornado.escape — HTML,JSON,URLs等的编码解码和一些字符串操作
  tornado.locale — 国际化支持
2. Asynchronous networking 底层模块

  tornado.ioloop — 核心的I/O循环
  tornado.iostream — 对非阻塞式的 socket 的简单封装，以方便常用读写操作
  tornado.httpclient — 一个无阻塞的HTTP服务器实现
  tornado.netutil — 一些网络应用的实现，主要实现TCPServer类
3. Integration with other services

  tornado.auth — 使用OpenId和OAuth进行第三方登录
  tornado.database — 简单的MySQL服务端封装
  tornado.platform.twisted — 在Tornado上运行为Twisted实现的代码
  tornado.websocket — 实现和浏览器的双向通信
  tornado.wsgi — 与其他python网络框架/服务器的相互操作
4. Utilities

  tornado.autoreload — 生产环境中自动检查代码更新
  tornado.gen — 一个基于生成器的接口，使用该模块保证代码异步运行
  tornado.httputil — 分析HTTP请求内容
  tornado.options — 解析终端参数
  tornado.process — 多进程实现的封装
  tornado.stack_context — 用于异步环境中对回调函数的上下文保存、异常处理
  tornado.testing — 单元测试
  
## 架构

![image](https://cloud.githubusercontent.com/assets/1400297/11799835/537fb22e-a312-11e5-99e0-0330aa205511.png)  

从上面的图可以看出，Tornado 不仅仅是一个WEB框架，它还完整地实现了HTTP服务器和客户端，在此基础上提供WEB服务。它可以分为四层：

* 最底层的EVENT层处理IO事件；
* TCP层实现了TCP服务器，负责数据传输；
* HTTP/HTTPS层基于HTTP协议实现了HTTP服务器和客户端；
* 最上层为WEB框架，包含了处理器、模板、数据库连接、认证、本地化等等WEB框架需要具备的功能。


## Book
[Introduction to Tornado 中文翻译](https://github.com/alioth310/itt2zh)
