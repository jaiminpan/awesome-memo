# Supervisord

## 安装配置
```
pip install supervisor

mkdir /etc/supervisor
echo_supervisord_conf > /etc/supervisor/supervisord.conf 
```


#### 配置管理进程

进程管理配置参数，不建议全都写在supervisord.conf文件中，应该每个进程写一个配置文件放在include指定的目录下包含进supervisord.conf文件中。 
1> 创建/etc/supervisor/config.d目录，用于存放进程管理的配置文件 
2> 修改/etc/supervisor/supervisord.conf中的include参数，将/etc/supervisor/conf.d目录添加到include中

```
[include]
files = /etc/supervisor/config.d/*.ini
```

#### Tomcat 例子

下面是配置Tomcat进程的一个例子：`cat /etc/supervisor/config.d/tomcat.ini`
```
[program:tomcat]
command=/opt/apache-tomcat-8.0.35/bin/catalina.sh run
stdout_logfile=/opt/apache-tomcat-8.0.35/logs/catalina.out
autostart=true
autorestart=true
startsecs=5
priority=1
stopasgroup=true
killasgroup=true
```

#### 启动Supervisor服务
supervisord -c /etc/supervisor/supervisord.conf

#### 命令控制 supervisorctl
```
supervisorctl status
supervisorctl stop tomcat
supervisorctl start tomcat
supervisorctl restart tomcat
supervisorctl reread
supervisorctl update
```

#### 开机启动Supervisor服务

##### 配置systemctl服务

进入/etc/systemd/system/目录，并创建[supervisor.service][supervisor_service]文件
设置开机启动
```
chmod 766 supervisor.service
systemctl enable supervisor.service
systemctl daemon-reload
```

##### 配置service类型服务
将上述脚本内容保存到`cd /etc/rc.d/init.d/`, 创建[supervisor][supervisor_init]文件中，修改文件权限为755，并设置开机启动
```
chmod 755 /etc/rc.d/init.d/supervisor
chkconfig --add supervisor
chkconfig supervisor on
```

注意：修改脚本中supervisor配置文件路径为你的supervisor的配置文件路径


## 解释
```
command：启动程序使用的命令，可以是绝对路径或者相对路径
process_name：一个python字符串表达式，用来表示supervisor进程启动的这个的名称，默认值是%(program_name)s
numprocs：Supervisor启动这个程序的多个实例，如果numprocs>1，则process_name的表达式必须包含%(process_num)s，默认是1
numprocs_start：一个int偏移值，当启动实例的时候用来计算numprocs的值
priority：权重，可以控制程序启动和关闭时的顺序，权重越低：越早启动，越晚关闭。默认值是999
autostart：如果设置为true，当supervisord启动的时候，进程会自动重启。
autorestart：值可以是false、true、unexpected。false：进程不会自动重启，unexpected：当程序退出时的退出码不是exitcodes中定义的时，进程会重启，true：进程会无条件重启当退出的时候。
startsecs：程序启动后等待多长时间后才认为程序启动成功
startretries：supervisord尝试启动一个程序时尝试的次数。默认是3
exitcodes：一个预期的退出返回码，默认是0,2。
stopsignal：当收到stop请求的时候，发送信号给程序，默认是TERM信号，也可以是 HUP, INT, QUIT, KILL, USR1, or USR2。
stopwaitsecs：在操作系统给supervisord发送SIGCHILD信号时等待的时间
stopasgroup：如果设置为true，则会使supervisor发送停止信号到整个进程组
killasgroup：如果设置为true，则在给程序发送SIGKILL信号的时候，会发送到整个进程组，它的子进程也会受到影响。
user：如果supervisord以root运行，则会使用这个设置用户启动子程序
redirect_stderr：如果设置为true，进程则会把标准错误输出到supervisord后台的标准输出文件描述符。
stdout_logfile：把进程的标准输出写入文件中，如果stdout_logfile没有设置或者设置为AUTO，则supervisor会自动选择一个文件位置。
stdout_logfile_maxbytes：标准输出log文件达到多少后自动进行轮转，单位是KB、MB、GB。如果设置为0则表示不限制日志文件大小
stdout_logfile_backups：标准输出日志轮转备份的数量，默认是10，如果设置为0，则不备份
stdout_capture_maxbytes：当进程处于stderr capture mode模式的时候，写入FIFO队列的最大bytes值，单位可以是KB、MB、GB
stdout_events_enabled：如果设置为true，当进程在写它的stderr到文件描述符的时候，PROCESS_LOG_STDERR事件会被触发
stderr_logfile：把进程的错误日志输出一个文件中，除非redirect_stderr参数被设置为true
stderr_logfile_maxbytes：错误log文件达到多少后自动进行轮转，单位是KB、MB、GB。如果设置为0则表示不限制日志文件大小
stderr_logfile_backups：错误日志轮转备份的数量，默认是10，如果设置为0，则不备份
stderr_capture_maxbytes：当进程处于stderr capture mode模式的时候，写入FIFO队列的最大bytes值，单位可以是KB、MB、GB
stderr_events_enabled：如果设置为true，当进程在写它的stderr到文件描述符的时候，PROCESS_LOG_STDERR事件会被触发
environment：一个k/v对的list列表
directory：supervisord在生成子进程的时候会切换到该目录
umask：设置进程的umask
serverurl：是否允许子进程和内部的HTTP服务通讯，如果设置为AUTO，supervisor会自动的构造一个url
```



[supervisor_service]: https://github.com/jaiminpan/fast-memo/blob/master/supervisord/script/supervisor.service
[supervisor_init]: https://github.com/jaiminpan/fast-memo/blob/master/supervisord/script/supervisor_init_script.sh
