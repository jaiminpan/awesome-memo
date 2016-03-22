Ganglia
---------
Ganglia：http://ganglia.info/  
Ganglia Wiki：http://sourceforge.net/apps/trac/ganglia  
Source Code: https://github.com/ganglia/monitor-core  

Introduce
----------
![image](http://blog.itpub.net/attachments/2012/02/22664653_201202142044241.jpg)  

http://blog.itpub.net/22664653/viewspace-716292/  
http://m.blog.csdn.net/blog/tryhl/44494811  

Install
---------
* Download ganglia-3.7.2.tar.gz
* ./configure --prefix=/usr/local/ganglia --with-gmetad
* make && make install

Compile Error
---------
Q: No package 'apr-1' found  
A: yum install apr-devel.x86_64  

Q: libconfuse not found  
A: yum install libconfuse-devel.x86_64  

Q: libexpat not found  
A: yum install expat-devel.x86_64  

Q: pcre not found  
A: yum install pcre-devel.x86_64  

Q: rrd not found  
A: yum install rrdtool-devel.x86_64  

Setting
---------
setting gmetad

  ```
  # $ vim gmetad.conf // copy from etc
  data_source "cluster_name1" localhost:8649 // connect to gmetad

  rrd_rootdir "/var/lib/ganglia/rrds"
  # chown nobody:nobody -R  /var/lib/ganglia/rrds
  ```

setting gmond
  ```
  # $ vim gmond.conf // copy from etc, or gernerated by gmond -t > gmond.conf

  globals {
  ...
  # should change 0->60, if use unicast
  send_metadata_interval = 0 /*secs */
  ...
  }
  cluster {
    name = "cluster_name1"
    owner = "unspecified"
    latlong = "unspecified"
    url = "unspecified"
  }

  udp_send_channel {
    host = localhost # center gmond's ip, which gmetad pull total info
    port = 8649
    ttl = 1
  }

  udp_recv_channel {
    # mcast_join = 239.2.11.71
    port = 8649  # listen port if here is center gmond
    # bind = 239.2.11.71
    # retry_bind = true
    # Size of the UDP buffer. If you are handling lots of metrics you really
    # should bump it up to e.g. 10MB or even higher.
    # buffer = 10485760
  }

  tcp_accept_channel {
    port = 8649  // for all information collection
    # If you want to gzip XML output
    gzip_output = no
  }
  ```

#### Modules
Please reference https://github.com/ganglia/gmond_python_modules  

Q: `$GANGLIA_INSTALL/lib64/ganglia/modpython.so` not exists, which is for python modules  
A: make sure `python.h` is existed when make && make install for ganglia. Or `yum install python-devel.x86_64`  

## Ganglia Web
自定义界面，完成多指标在同一个界面   
https://github.com/ganglia/ganglia-web/wiki#Defining_Custom_Graphs_Via_JSON  

![image](https://github.com/ganglia/ganglia-web/wiki/network_report.png)
