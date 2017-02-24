Python
-----------

Install in manaul
---------

### Pre-install
```sh
yum install readline-devel
yum install zlib-devel
yum install openssl-devel
yum install sqlite-devel
yum install bzip2-devel
```
### Install Python
  wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz

  ```sh
    tar xf Python-2.7.7.tgz
    cd Python-2.7.7
    ./configure --prefix=/usr/local/python27 --enable-shared
    make && make install
    ls /usr/local/bin/python2.7
  ```
### Install setuptools + pip

  1. setuptools

    ```
      > wget https://bootstrap.pypa.io/ez_setup.py -O - | python
    ```
    For more to reference: https://pypi.python.org/pypi/setuptools
  2. pip
  
    Download from https://pypi.python.org/pypi/pip#download  
    ```
      # tar -xzvf pip-x.x.x.tar.gz
      # cd pip-x.x.x
      # python setup.py install
    ```
    For more to reference: https://pypi.python.org/pypi/pip
  3. After Installed

    ```
      # With pip installed you can now do things like this:
      pip install [packagename]
      pip install --upgrade [packagename]
      pip uninstall [packagename]
    ```


#### Misc

无论报错信息如何，意思很明确，我们编译的时候，系统没有办法找到对应的模块信息，为了解决这些报错，我们就需要提前安装依赖包，这些依赖包对应列表如下（不一定完全）：

模块 | 依赖 | 说明
---- | ---- | ----
_bsddb | bsddb | Interface to Berkeley DB library。Berkeley数据库的接口
_curses | ncurses | Terminal handling for character-cell displays。
_curses_panel | ncurses | A panel stack extension for curses。
_sqlite3 | sqlite | DB-API 2.0 interface for SQLite databases。SqlLite，CentOS可以安装sqlite-devel
_ssl | openssl-devel | TLS/SSL wrapper for socket objects。
_tkinter | N/A | a thin object-oriented layer on top of Tcl/Tk。如果不使用桌面程序可以忽略TKinter
bsddb185 | old bsddb module | 老的bsddb模块，可忽略。
bz2 | bzip2-devel | Compression compatible with bzip2。bzip2-devel
dbm | bsddb | Simple “database” interface。
dl | N/A | Call C functions in shared objects.Python2.6开始，已经弃用。
gdbm | gdbm-devel | GNU’s reinterpretation of dbm
imageop | N/A | Manipulate raw image data。已经弃用。
readline | readline-devel | GNU readline interface
sunaudiodev | N/A | Access to Sun audio hardware。这个是针对Sun平台的，CentOS下可以忽略
zlib | Zlib | Compression compatible with gzip
