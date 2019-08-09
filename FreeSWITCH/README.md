# FreeSWITCH
FreeSWITCH 是一个 免费、 开源 的软交换软件。 它采用 Mozilla Public License (MPL)授权协议, MPL是一个 开源的软件协议. 它的核心库libfreeswitch可以嵌入其它系统或产品中，也可以做一个单独的应用存在。

## 历史

FreeSWITCH 项目最初于2006年1月在O'Reilly Media's ETEL 会议上发布。[1] 2007年6月，FreeSWITCH 被Truphone 采用[2]。2007年8月, Gaboogie 宣布使用FreeSWITCH作为电话会议平台。[3]

[更多](https://zh.wikipedia.org/wiki/FreeSWITCH)

## Install
#### Prepare
1. Linux 
  
```
  $ sh support-d/prereq.sh
  $ sh bootstrap.sh

  $ ./configure
  # OR
  $ ./configure --enable-core-pgsql-support

  $ make
  $ sudo make install

  # 安装声音文件
  $ make cd-sounds
  $ sudo make cd-sounds-install
  $ make cd-moh
  $ sudo make cd-moh-install
```

#### 做成服务
```
[Unit]
Description=freeswitch
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/home/mintcode
ExecStart=/usr/local/freeswitch/bin/freeswitch
ExecStop=/usr/local/freeswitch/bin/freeswitch -stop 
Restart=always

[Install]
WantedBy=multi-user.target
```
