# Mac OS X读写NTFS磁盘的命令

## 方法一
配置/etc/fstab，此方法让系统开机自动以读写权限挂载NTFS分区，推荐用此法来挂载本地硬盘。
1.执行下面命令找出NTFS分区：
```bash
diskutil list | grep NTFS
# Sample:
# /dev/disk3 (external, physical):
#   #:                       TYPE NAME                    SIZE       IDENTIFIER
#   0:     FDisk_partition_scheme                        *1.0 TB     disk3
#   1:               Windows_NTFS Elements                1.0 TB     disk3s1
```
命令输出的第三列`Elements`就是NTFS分区的卷标。

2.执行下面命令修改/etc/fstab：
```bash
vifs
# OR
vi /etc/fstab
```
比如我有个NTFS分区的卷标是Elements，我就在/etc/fstab加上一行：
```
LABEL=Elements none ntfs rw,nobrowse,noowners,noatime,nosuid
# LABEL="卷标"。同理，其它分区也这么配置。
```

## 方法二
手工操作挂载，推荐用来挂载USB移动硬盘，这个方法总共分3个步骤：
1.找出NTFS磁盘和挂载点
2.卸载NTFS磁盘
3.加上读写参数重新挂载

3个步骤的详细操作：
1.找出NTFS磁盘和挂载点，输入以下命令：
```bash
mount | grep ntfs

输出如下：
/dev/disk0s1 on /Volumes/Win7boot (ntfs, local, noowners, read-only, nosuid)
/dev/disk0s2 on /Volumes/Windows7 (ntfs, local, noowners, read-only, nosuid)
/dev/disk0s3 on /Volumes/Programs (ntfs, local, noowners, read-only, nosuid)
/dev/disk0s5 on /Volumes/Data1 (ntfs, local, noowners, read-only, nosuid)
/dev/disk0s6 on /Volumes/Data2 (ntfs, local, noowners, read-only, nosuid)
```
第一列是NTFS格式磁盘，第三列是挂载点，括号内的是挂载参数
2.根据以上的信息，来卸载当前挂载的NTFS磁盘，比如要卸载/dev/disk0s1，就执行下面的命令：
```bash
umount /dev/disk0s1
```
 
用同样的方法来卸载其它的磁盘。这里要*注意*如果磁盘上有文件被打开，那么这个磁盘是卸载不了的。
3.还是以/dev/disk0s1为例说明怎么以读写方式挂载NTFS。从步骤1中的第三列找到默认的挂载点，执行下面命令创建它：
```bash
mkdir -p /Volumes/Win7boot
```
 
执行下面命令来以读写方式挂载：
```bash
mount_ntfs -o rw,auto,nobrowse,noowners,noatime  /dev/disk0s1 /Volumes/Win7boot
```
以上命令的 rw 选项添加了读写权限，到这里完成一个磁盘的挂载，其它的用同样的方法。如果是移动硬盘，在-o后再加一个nodev选项。

最后，
1.此方法挂载的磁盘不会显示在Finder边栏的“设备”里。所以我把/Volumes添加到Finder的“个人收藏”了。
2.系统读写NTFS有时会“弄脏”磁盘，windows开机的时候需要检查磁盘，一般不会损坏文件，如果担心损坏那就不要让系统读写NTFS磁盘了。
3.教程的步骤在10.8.4验证过，使用过程中没有出现损坏文件的情况，如果使用过程中你的文件损坏了与作者无关

PS：添加//Volumes下的磁盘到个人收藏的：
Finder-前往-前往文件夹-输入“/Volumes”，然后把各个磁盘拖到个人收藏。

## 解決「正由 Mac OS X 使用 所以无法打开」的方法
背景：used by osx and cannot be opened (正由 Mac OS X 使用 所以无法打开)

由于Mac OS X 并沒有正式支持到 NTFS 磁盘的写入，所以可能在某些情况下产生，写入的数据无法使用。
其实是因为 Mac OS X 在复制出来的资料中加了标记，这些标记在运行时做了特别处理。

#### 解决方法
使用`xattr`命令查看信息，如果有，则用`xattr -d`指令來把它刪除 
```
->$ xattr test_file
com.apple.FinderInfo

-> xattr -d com.apple.FinderInfo test_file
```

