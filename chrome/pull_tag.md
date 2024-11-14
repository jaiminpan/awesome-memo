Chromium 的每个版本都会打 tag，可以通过 git fetch origin tag [tag-name] 或取指定版本，减少拉取的时间，拉取完之后需要重新同步相关依赖，具体命令如下：

 

1. 拉取指定版本的 tag

```bash
git fetch origin tag [tag-name]
# git fetch origin --tags
```

1. 切换到拉取的 tag

```bash
git checkout tags/[tag-name]
```

1. 同步依赖

```bash
gclient sync
```

1. （可选）有时候可能会需要移除一些在当前版本没有用的依赖

```bash
gclient sync -D
```

1. 重新编译，这个步骤可能会报错，重试一遍即可

```bash
autoninja -C out\Default chrome
```

1. 生成最小的安装包

```bash
ninja -C out/Default mini_installer
```
