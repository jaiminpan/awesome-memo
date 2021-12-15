# 介绍

## 限流限速
APISIX 内置了三个限流限速插件：

limit-count：基于“固定窗口”的限速实现。
limit-req：基于漏桶原理的请求限速实现。
limit-conn：限制并发请求（或并发连接）。
本小节，我们来演示使用 limit-req 插件，毕竟基于漏桶的限流算法，是目前较为常用的限流方式。

漏桶算法(Leaky Bucket)是网络世界中流量整形（Traffic Shaping）或速率限制（Rate Limiting）时经常使用的一种算法，它的主要目的是控制数据注入到网络的速率，平滑网络上的突发流量。
漏桶算法提供了一种机制，通过它，突发流量可以被整形以便为网络提供一个稳定的流量。


漏桶算法

5.1 配置 limit-req 插件
在「4. 动态负载均衡」小节中，我们已经创建了一个 APISIX Route。这里，我们给该 Route 配置下 limit-req 插件。

配置 limit-req 插件

rate：指定的请求速率（以秒为单位），请求速率超过 rate 但没有超过 （rate + brust）的请求会被加上延时
burst：请求速率超过 （rate + brust）的请求会被直接拒绝
rejected_code：当请求超过阈值被拒绝时，返回的 HTTP 状态码
key：是用来做请求计数的依据，当前接受的 key 有："remote_addr"(客户端 IP 地址), "server_addr"(服务端 IP 地址), 请求头中的"X-Forwarded-For" 或 "X-Real-IP"。
上述配置限制了每秒请求速率为 1，大于 1 小于 3 的会被加上延时，速率超过 3 就会被拒绝。


5.2 简单测试
快速多次请求 http://172.16.48.185:9080/demo/echo 地址，我们会看到页面返回 503 错误码，成功被 APISIX 所限流。如下图所示：

##  身份验证
APISIX 内置了四个身份验证插件：

key-auth：基于 Key Authentication 的用户认证。
JWT-auth：基于 JWT (JSON Web Tokens) Authentication 的用户认证。
basic-auth：基于 basic auth 的用户认证。
wolf-rbac：基于 RBAC 的用户认证及授权。
需要额外搭建 wolf 服务，提供用户、角色、资源等信息。
本小节，我们来演示使用 JWT-auth 插件，大家比较熟知的认证方式。不了解的胖友，可以阅读如下文章：

《JSON Web Token - 在Web应用间安全地传递信息》
《八幅漫画理解使用 JSON Web Token 设计单点登录系统》

6.1 配置 JWT-auth 插件
① 在 APISIX 控制台的「Consumer」菜单中，创建一个 APISIX Consumer，使用 JWT-auth 插件。如下图所示：

Consumer 是某类服务的消费者，需与用户认证体系配合才能使用。
更多 Consumer 的介绍，可以看《APISIX 官方文档 —— 架构设计（Consumer）》。


创建 Consumer 02其中每个属性的作用如下：
key: 不同的 consumer 对象应有不同的值，它应当是唯一的。不同 consumer 使用了相同的 key ，将会出现请求匹配异常。
secret: 可选字段，加密秘钥。如果您未指定，后台将会自动帮您生成。
algorithm：可选字段，加密算法。目前支持 HS256, HS384, HS512, RS256 和 ES256，如果未指定，则默认使用 HS256。
exp: 可选字段，token 的超时时间，以秒为单位的计时。比如有效期是 5 分钟，那么就应设置为 5 * 60 = 300。

② 在「4. 动态负载均衡」小节中，我们已经创建了一个 APISIX Route。这里，我们给该 Route 配置下 JWT-auth 插件。如下图所示：


配置 JWT-auth 插件

友情提示：是不是觉得配置过程有点怪怪的，淡定~

6.2 简单测试
① 调用 jwt-auth 插件提供的签名接口，获取 Token。


```sh
# key 参数，为我们配置 jwt-auth 插件时，设置的 key 属性。
$ curl http://172.16.48.185:9080/apisix/plugin/jwt/sign?key=yunai 
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ5dW5haSIsImV4cCI6MTU4ODQ3MzA5NX0.WlLhM_gpr-zWKXCcXEuSuw-7JosU9mnHwfeSPtspCGo
```
② 使用 Postman 模拟调用示例 /demo/echo 接口，并附带上 JWT。如下图所示：


Postman 模拟请求

友情提示：至此，我们已经完成了 JWT-auth 插件的学习。
胖友可以先删除示例 Route 配置的 JWT-auth 插件，方便模拟请求哈。

## 健康检查
因为 APISIX 控制台暂未提供健康检查的配置功能，艿艿等后续有了在补充。

胖友可以先阅读《APISIX 官方文档 —— 健康检查》，使用 APISIX Admin API 进行添加健康检查的配置

