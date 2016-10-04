# npm

npm 是node.js 环境下的包管理器,非常强大智能.

生活这这片神奇的土地上,各种奇葩手段屡见不鲜啊.

为什么要换源? npm 官方站点 http://www.npmjs.org/ 并没有被墙,但是下载第三方依赖包的速度让人着急啊!

就拿阿里云环境来说,有时npm 一个包也需要耐心等待......等待过去也许是原地踏步,也许就是安装失败.

幸运的是,国内有几个镜像站点可以供我们使用,本人在使用 http://www.cnpmjs.org/ 

## 给npm换源

(1)通过 config 配置指向国内镜像源
```bash
npm config set registry http://registry.cnpmjs.org //配置指向源
npm info express  //下载安装第三方包
```

(2)通过 npm 命令指定下载源
```
npm --registry http://registry.cnpmjs.org info express
```

(3)在配置文件 ~/.npmrc 文件写入源地址
```bash
nano ~/.npmrc   //打开配置文件

registry =https://registry.npm.taobao.org   //写入配置文件
```

