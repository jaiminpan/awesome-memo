
## 简介
在查看以下内容之前需要注意：  
  1、本篇所涉及内容只在cache占用大量内存时导致系统内存不够用，系统运行缓慢的情况下使用；  
  2、强制回收前需要先进行sync 同步数据到硬盘操作，避免强制回收时造成数据丢失；  
  3、当buffer/cached使用的内存并不大时，而系统本身确实不足时无法回收。  

## 清理
使用内存回收用到的主要为drop_caches参数，具体文档如下：
```
Writing to this will cause the kernel to drop clean caches, 
dentries and inodes from memory, causing that memory to become free.
To free pagecache:
* echo 1 > /proc/sys/vm/drop_caches
To free dentries and inodes:
* echo 2 > /proc/sys/vm/drop_caches
To free pagecache, dentries and inodes:
* echo 3 > /proc/sys/vm/drop_caches
As this is a non-destructive operation, and dirty objects are notfreeable, 
the user should run "sync" first in order to make sure allcached objects are freed.
This tunable was added in 2.6.16.
```
这里有三个级别可以使用。使用1时只清理pagecahe ，使用2清理dentries和inodes ，使用3时三者都清理。操作方法是：
```
$echo 3 > /proc/sys/vm/drop_caches
```

## 设置
和内存相关的tcp/ip参数以下部分，在/etc/sysctl.conf中添加以下选项后就不会内存持续增加
```
vm.dirty_ratio = 1
vm.dirty_background_ratio=1
vm.dirty_writeback_centisecs=2
vm.dirty_expire_centisecs=3
vm.drop_caches=3
vm.swappiness =100
vm.vfs_cache_pressure=163
vm.overcommit_memory=2
vm.lowmem_reserve_ratio=32 32 8
kern.maxvnodes=3
```
上面的设置比较粗暴，使cache的作用基本无法发挥。需要根据机器的状况进行适当的调节寻找最佳的折衷。

### 解释
* `/proc/sys/vm/dirty_ratio`  
  这个参数控制文件系统的文件系统写缓冲区的大小，单位是百分比，表示系统内存的百分比，表示当写缓冲使用到系统内存多少的时候，
  开始向磁盘写出数据。增大之会使用更多系统内存用于磁盘写缓冲，也可以极大提高系统的写性能。
  但是，当你需要持续、恒定的写入场合时，应该降低其数值，一般启动上缺省是10。设1加速程序速度。

* `/proc/sys/vm/dirty_background_ratio`  
  这个参数控制文件系统的pdflush进程，在何时刷新磁盘。单位是百分比，表示系统内存的百分比，意思是当写缓冲使用到系统内存多少的时候，pdflush开始向磁盘写出数据。
  增大之会使用更多系统内存用于磁盘写缓冲，也可以极大提高系统的写性能。但是，当你需要持续、恒定的写入场合时，应该降低其数值，一般启动上缺省是 5

* `/proc/sys/vm/dirty_writeback_centisecs`
  这个参数控制内核的脏数据刷新进程pdflush的运行间隔。单位是 1/100 秒。缺省数值是500，也就是 5 秒。
  如果你的系统是持续地写入动作，那么实际上还是降低这个数值比较好，这样可以把尖峰的写操作削平成多次写操

* `/proc/sys/vm/dirty_expire_centisecs`  
  这个参数声明Linux内核写缓冲区里面的数据多“旧”了之后，pdflush进程就开始考虑写到磁盘中去。单位是 1/100秒。
  缺省是30000，也就是 30秒的数据就算旧了，将会刷新磁盘。
  对于特别重载的写操作来说，这个值适当缩小也是好的，但也不能缩小太多，因为缩小太多也会导致IO提高太快。建议设置为1500，也就是15秒算旧。 

* `/proc/sys/vm/drop_caches`  
  释放已经使用的cache

* `/proc/sys/vm/page-cluster`  
  该文件表示在写一次到swap区的时候写入的页面数量，0表示1页，1表示2页，2表示4页。

* `/proc/sys/vm/swapiness`  
  该文件表示系统进行交换行为的程度，数值（0-100）越高，越可能发生磁盘交换。

* `/proc/sys/vm/vfs_cache_pressure`  
  该文件表示内核回收用于directory和inode cache内存的倾向
