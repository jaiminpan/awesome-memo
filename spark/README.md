# Spark

## Install
#### Prepare
1. Linux 
2. Java environment(JDK)

Example:  
```
  sudo yum install java-1.8.0-openjdk
```

Download:  https://spark.apache.org/downloads.html 

Here we choose `spark-1.6.1-bin-hadoop2.4.tgz`

tar xvfz spark-1.6.1-bin-hadoop2.4.tgz

## Usage
#### standalone
You can use following 'standalone' Commands to execute your code directly.  

bin/spark-shell  scala  
bin/spark-sql    sql  
bin/pyspark      python  
bin/spark-class      java  

#### cluster
configuration your env in `conf/*` then execute the commands in 'sbin/*'  

Example:  
```
vi conf/slaves
sbin/start-all.sh # or start-master.sh && start-slaves.sh
```
You can specific your master(spark://IP:PORT) to connect the SparkContext
Example:  
```
MASTER=spark://localhost:7077 ./spark-shell
# OR
MASTER=spark://localhost:7077 ./pyspark
```

#### Web
The default web address `http://192.168.0.108:8080/` to view your spark    

## Reference:
* http://yixuan.cos.name/cn/2015/04/spark-beginner-1/
* http://colobu.com/2014/12/11/spark-sql-quick-start/
* http://blog.csdn.net/zwx19921215/article/details/41821147
* http://www.oschina.net/translate/spark-standalone?print
* https://spark.apache.org/docs/1.5.2/api/python/pyspark.sql.html
