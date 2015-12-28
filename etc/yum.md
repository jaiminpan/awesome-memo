YUM
===========

yum是基于Red Hat的系统(如CentOS、Fedora、RHEl)上的默认包管理器。使用yum，你可以安装或者更新一个RPM包，并且他会自动解决包依赖关系。


#### 如何只从Red Hat 的标准仓库中下载一个RPM包，而不进行安装

yum命令本身就可以用来下载一个RPM包，标准的yum命令提供了--downloadonly(只下载)的选项来达到这个目的。
```sh
$ sudo yum install --downloadonly <package-name>
```
默认情况下，一个下载的RPM包会保存在下面的目录中:
```sh
/var/cache/yum/<arch>/[centos/fedora-version]/[repository]/packages
```
以上的[repository]表示下载包的来源仓库的名称(例如：base、fedora、updates)

如果你想要将一个包下载到一个指定的目录(如/tmp)：
```sh
$ sudo yum install --downloadonly --downloaddir=/tmp <package-name>
```
注意，如果下载的包包含了任何没有满足的依赖关系，yum将会把所有的依赖关系包下载，但是都不会被安装。

PS:
另外一个重要的事情是，在CentOS/RHEL 6或更早期的版本中，你需要安装一个单独yum插件(名称为 yum-plugin-downloadonly)才能使用--downloadonly命令选项：
```sh
$ sudo yum install yum-plugin-downloadonly
```
或者update yum也同样可以解决问题

如果没有该插件，你会在使用yum时得到以下错误：
```sh
Command line error: no such option: --downloadonly
```
