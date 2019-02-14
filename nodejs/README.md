# Node



## Install
目前，最推荐的使用nvm进行node版本管理及对应版本的npm安装。具体安装步骤如下：

```sh
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
nvm --version
```

#### Mirror
```sh
export NVM_NODEJS_ORG_MIRROR=https://npm.taobao.org/mirrors/node npm --registry=https://registry.npm.taobao.org
```

#### Quick-cmd
```sh
# 查看node版本
nvm ls-remote
# 查看本地安装的node版本
nvm list

nvm install [node版本号]
nvm uninstall [node 版本]

# 选定node版本作为开发环境
nvm use [node 版本]
```