# Install guide


## Download
下载 gcc 5.4  
http://ftp.tsukuba.wide.ad.jp/software/gcc/releases/gcc-5.4.0/  

下载 mpc-0.8.1，mpfr-2.4.2，gmp-4.3.2  
http://ftp.tsukuba.wide.ad.jp/software/gcc/infrastructure/  

## 准备
解压gcc后，在gcc根目录下，分别设置 mpc-0.8.1，mpfr-2.4.2，gmp-4.3.2的软连接mpc，mpfr，gmp
```bash
ln -sf /PATH/mpc-0.8.1 mpc
ln -sf /PATH/gmp-4.3.2 gmp
ln -sf /PATH/mpfr-2.4.2 mpfr
```

## 编译
创建build目录，然后configure 再make
```bash
mkdir build && cd build

# 如果不带--disable-multilib选项，则编译就会生成32bit和64bit的版本，即多平台交叉编译
../configure --enable-checking=release --enable-languages=c,c++ --disable-multilib

make -j4
make install
```

## 更新默认gcc
添加新GCC到可选项，倒数第三个是名字，倒数第二个参数为新GCC路径，最后一个参数40为优先级，值越大，就越先启用
```
update-alternatives --install /usr/bin/gcc gcc /usr/local/bin/gcc 101
```
说明（从最后一个参数说起）
* 101：版本优先级，值越大，就越先启用
* /usr/local/bin/gcc：新的gcc文件目录，以上的编译操作默认，会在路径/usr/local下生成相应的库文件和执行文件等。
* gcc：系统调用时，在命令行中的名字，也就是路径的一个别名吧。
* /usr/bin/gcc：之前版本gcc调用时的路径。

查看信息
```
update-alternatives --display gcc
```
如果想要，切换回旧版本，请参考
```
update-alternatives --config gcc
```

然后，执行updatedb，更新系统文件信息，并退出当前session，重新连接session：

检查`gcc -v`

