# locale

在Linux中通过locale来设置程序运行的不同语言环境，locale由ANSI C提供支持。
locale的命名规则为<语言>_<地区>.<字符集编码>，如zh_CN.UTF-8，zh代表中文，CN代表大陆地区，UTF-8表示字符集。
在locale环境中，有一组变量，代表国际化环境中的不同设置。

## 内容
1.    `LC_COLLATE`:
定义该环境的排序和比较规则

2.    `LC_CTYPE`:
用于字符分类和字符串处理，控制所有字符的处理方式，包括字符编码，字符是单字节还是多字节，如何打印等。是最重要的一个环境变量。

3.    `LC_MONETARY`:
货币格式

4.    `LC_NUMERIC`:
非货币的数字显示格式

5.    `LC_TIME`:
时间和日期格式

6.    `LC_MESSAGES`:
提示信息的语言。另外还有一个LANGUAGE参数，它与LC_MESSAGES相似，但如果该参数一旦设置，则LC_MESSAGES参数就会失效。LANGUAGE参数可同时设置多种语言信息，如
LANGUANE=”zh_CN.GB18030:zh_CN.GB2312:zh_CN”。

7.    `LANG`:
LC_*的默认值，是最低级别的设置，如果LC_*没有设置，则使用该值。类似于 LC_ALL。

8.    `LC_ALL`:
它是一个宏，如果该值设置了，则该值会覆盖所有LC_*的设置值。注意，LANG的值不受该宏影响。

## 例子：
设置前，使用默认locale：
```
debian:~# locale
LANG=”POSIX”
LC_CTYPE=”POSIX”
LC_NUMERIC=”POSIX”
LC_TIME=”POSIX”
LC_COLLATE=”POSIX”
LC_MONETARY=”POSIX”
LC_MESSAGES=”POSIX”
LC_PAPER=”POSIX”
LC_NAME=”POSIX”
LC_ADDRESS=”POSIX”
LC_TELEPHONE=”POSIX”
LC_MEASUREMENT=”POSIX”
LC_IDENTIFICATION=”POSIX”
LC_ALL=
```

设置后，使用zh_CN.GDK中文locale：
```
debian:~# export LC_ALL=zh_CN.GBK
debian:~# locale
LANG=zh_CN.UTF-8
LC_CTYPE=”zh_CN.GBK”
LC_NUMERIC=”zh_CN.GBK”
LC_TIME=”zh_CN.GBK”
LC_COLLATE=”zh_CN.GBK”
LC_MONETARY=”zh_CN.GBK”
LC_MESSAGES=”zh_CN.GBK”
LC_PAPER=”zh_CN.GBK”
LC_NAME=”zh_CN.GBK”
LC_ADDRESS=”zh_CN.GBK”
LC_TELEPHONE=”zh_CN.GBK”
LC_MEASUREMENT=”zh_CN.GBK”
LC_IDENTIFICATION=”zh_CN.GBK”
LC_ALL=zh_CN.GBK
```

“C”是系统默认的locale，”POSIX”是”C”的别名。所以当我们新安装完一个系统时，默认的locale就是C或POSIX。

在Debian中安装locales的方法如下：

· 通过apt-get install locales命令安装locales包
· 安装完成locales包后，系统会自动进行locale配置，你只要选择所需的locale，可以多选。最后指定一个系统默认的locale。这样系统就会帮你自动生成相应的locale和配置好系统的locale。

· 增加新的locale也很简单，用dpkp-reconfigure locales重新配置locale即可。

· 我们也可手动增加locale，只要把新的locale增加到/etc/locale.gen文件中，再运行locale-gen命令即可生成新的 locale。再通过设置上面介绍的LC_*变量就可设置系统的locale了。下面是一个locale.gen文件的样例。
引用
```
· # This file lists locales that you wish to have built. You can find a list
· # of valid supported locales at /usr/share/i18n/SUPPORTED. Other
· # combinations are possible, but may not be well tested. If you change
· # this file, you need to rerun locale-gen.
· #
·zh_CN.GBK GBK
·zh_CN.UTF-8 UTF-8
```

要在Shell中正常显示系统的中文提示信息和支持中文输入。
LANG和shell的编码配置需一致，并安装有中文locale。
如：LANG和 shell的编码都配置成zh_CN.utf8，并安装有zh_CN.utf8这个locale。
如果shell和LANG配置不同，则中文显示乱码；如果LANG里设置的locale没有安装，则不能显示系统的中文提示信息，只会显示英文提示信息。
