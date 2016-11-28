# Install

#### 下载

到http://www.boost.org/下载boost的安装包
以boost_1_62_0.tar.gz为例，下载完成后进行解压缩：
```bash
tar xvfz boost_1_62_0.tar.gz
```

## 准备
```bash
cd boost_1_58_0

./bootstrap.sh --with-libraries=all --with-toolset=gcc
```
* --with-toolset指定编译时使用哪种编译器，Linux下使用gcc即可，如果系统中安装了多个版本的gcc，在这里可以指定gcc的版本，比如--with-toolset=gcc-4.4
* --with-libraries指定编译哪些boost库，all的话就是全部编译，只想编译部分库的话就把库的名称写上，之间用 , 号分隔即可，可指定的库有以下几种：

库名 | 说明
---- |----
atomic | 
chrono | 
context | 
coroutine | 
date_time | 
exception | 
filesystem | 
graph | 图组件和算法
graph_parallel | 
iostreams | 
locale | 
log | 
math | 
mpi | 用模板实现的元编程框架
program_options | 
python | 把C++类和函数映射到Python之中
random | 
regex | 正则表达式库
serialization | 
signals | 
system | 
test | 
thread | 可移植的C++多线程库
timer | 
wave | 

结果
```bash
Building Boost.Build engine with toolset gcc... tools/build/src/engine/bin.linuxx86_64/b2
Detecting Python version... 2.6
Detecting Python root... /usr
Unicode/ICU support for Boost.Regex?... not found.
Generating Boost.Build configuration in project-config.jam...

Bootstrapping is done. To build, run:

    ./b2

To adjust configuration, edit 'project-config.jam'.
Further information:

   - Command line help:
     ./b2 --help

   - Getting started guide: 
     http://www.boost.org/more/getting_started/unix-variants.html

   - Boost.Build documentation:
     http://www.boost.org/build/doc/html/index.html
```

## 编译boost

执行以下命令开始进行boost的编译：
```
./b2 toolset=gcc
```
编译的时间需要几分钟，耐心等待，结束后会有以下提示：
```
...failed updating 60 targets...
...skipped 21 targets...
...updated 663 targets...
```

## 安装boost

最后执行以下命令开始安装boost：
```bash
./b2 install --prefix=/usr
```
--prefix=/usr用来指定boost的安装目录，不加此参数的话默认的头文件在/usr/local/include/boost目录下，库文件在/usr/local/lib/目录下。这里把安装目录指定为--prefix=/usr则boost会直接安装到系统头文件目录和库文件目录下，可以省略配置环境变量。

安装完毕后会有以下提示：
```bash
...failed updating 60 targets...
...skipped 21 targets...
...updated 11593 targets...
```
最后需要注意，如果安装后想马上使用boost库进行编译，还需要执行一下这个命令更新系统的动态链接库
```bash
ldconfig
```

## 测试
以boost_thread为例，测试刚安装完的boost库是否能正确使用，测试代码如下：
```c
#include <boost/thread/thread.hpp> //包含boost头文件
#include <iostream>
#include <cstdlib>
using namespace std;

volatile bool isRuning = true;

void func1()
{
    static int cnt1 = 0;
    while(isRuning)
    {
        cout << "func1:" << cnt1++ << endl;
        sleep(1);
    }
}

void func2()
{
    static int cnt2 = 0;
    while(isRuning)
    {
        cout << "\tfunc2:" << cnt2++ << endl;
        sleep(2);
    }
}

int main()
{
    boost::thread thread1(&func1);
    boost::thread thread2(&func2);

    system("read");
    isRuning = false;

    thread2.join();
    thread1.join();
    cout << "exit" << endl;
    return 0;
}
```
在编译程序时，需要加入对boost_thread库的引用：
```makefile
g++ main.cpp -g -o main -lboost_thread
```
如果boost库的安装位置不是在系统目录下，则还需要在编译时加上-I和-L指定boost头文件和库文件的位置


## Misc

http://repo.enetres.net/x86_64/
