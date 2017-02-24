# Airflow
Airflow 是一个工作流分配管理系统。

官网
github: https://github.com/apache/incubator-airflow
文档地址: 
* https://airflow.incubator.apache.org/
* http://pythonhosted.org/airflow/


#### 安装和使用
最简单安装
```bash
# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
export AIRFLOW_HOME=/usr/local/airflow

# install from pypi using pip
pip install airflow
pip install airflow[hive]

# initialize the database
airflow initdb

# start the web server, default port is 8080
airflow webserver -p 8080
```

安装成功之后，就可以使用了，默认使用SequentialExecutor, 顺次执行任务。


#### 初始化数据库
```bash
airflow initdb
airflow webserver -p 8080 # 启动web服务器
airflow scheduler	# 启动任务
airflow worker		# 启动 worker
airflow test ct1 print_date 2016-05-14 # 或者测试文章末尾的DAG
```

#### 使用mysql
```bash
#首先要安装mysql客户端
sudo yum install -y mysql
sudo yum install -y mysql-devel

CREATE USER airflow;
CREATE DATABASE airflow CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE DATABASE celery_result_airflow CHARACTER SET utf8 COLLATE utf8_general_ci;

GRANT all privileges on airflow.* TO 'airflow'@'%' IDENTIFIED BY 'airflow';
GRANT all privileges on celery_result_airflow.* TO 'airflow'@'%' IDENTIFIED BY 'airflow';

#安装mysql模块
wget https://pypi.python.org/packages/a5/e9/51b544da85a36a68debe7a7091f068d802fc515a3a202652828c73453cad/MySQL-python-1.2.5.zip#md5=654f75b302db6ed8dc5a898c625e030c
unzip MySQL-python-1.2.5.zip
cd MySQL-python-1.2.5
python setup.py install

#在airflow的配置文件中配置mysql为元数据的存储库
sudo vi $AIRFLOW_HOME/airflow.cfg

#更改数据库链接：
sql_alchemy_conn = mysql://airflow:airflow@localhost:3306/airflow

#对应字段解释如下：
dialect+driver://username:password@host:port/database

#初始化元数据库
airflow initdb

#重置元数据库
airflow resetdb
```

## 安全登录配置
```bash
#安装password模块
pip install airflow[password]

#在airflow的配置文件中修改需要认证
sudo vi $AIRFLOW_HOME/airflow.cfg
[webserver]
authenticate = True
filter_by_owner = True
auth_backend = airflow.contrib.auth.backends.password_auth
```


#### 添加用户
```
import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

user = PasswordUser(models.User())
user.username = 'test'
user.email = 'test@test.com'
user.password = 'test'
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
```

## scheduler调度器

启动后台守护进程了之后，Airflow才能实时监控任务的调度情况。将任务脚本放到${AIRFLOW_HOME}/dags下在web UI 就能看到任务执行情况。

主要作用
* collect dags， 遍历dags目录下面的.py文件，导入模块，找出定义的dag对象保存到dag列表dagbag
* 进入循环
	* 优先处理处于排队中的task实例
	* 认每10次循环检查一次dags目录，加载更新的dag，否则，只加载dagbag中更新的dag
	* 遍历dagbag中的dag，开始调度
		* 实例化一个对应执行日期的dagrun，如果dag是第一次执行并且没有执行过的task，则从dag定义的start_date开始调度,如果dag是第一次运行但是有执行过的属于这个dag的task，会从task最后执行时间前5天开始调度；如果dag不是第一次执行，则从上一次的执行日期开始，下次执行日期是（开始日期+调度间隔），并且在下下次执行日期（下次执行日期+调度间隔）到来之后才调度。也就是，开始日期是2015-10-01，调度间隔是1天，下次执行日期是2015-10-02，然后这个任务会在 2015-10-03 调度执行。
		* 对于每个dag，查找状态为running的实例dagrun，每个dagrun是dag在某个执行日期的实例，对于构成dag的每个task，实例化task instance（task对应某个执行日期的实例），判断是否能执行，例如依赖的上级task有没有成功等，如果可以执行，则组装一条airflow run命令放入队列中。
		* 处理SLA miss，如果task在配置的预计执行完成日期没有执行成功，会发邮件通知。
		* 处理僵尸进程，即没有心跳的执行状态的job。
		* executor异步执行队列中的命令
		* 检查当前调度进程（SchedulerJob）数据库中的状态，是SHUTDOWN就kill掉自己，否则更新心跳
		* sleep直到与上次心跳间隔为scheduler_heartbeat_sec，进入下一次循环

## executor执行器

三种选择
* Sequential executor 单进程
* local executor 多进程，通过multiprocessing库预先建立worker池
* celery 分布式，利用celery库
执行过程
* 从调度任务队列拿task
* 开子进程用shell执行task的命令，父进程阻塞等待子进程完成
* 执行状态（SUCCESS/FAILED）放入结果队列

## Misc


#### Celery+MySQL
```bash
#Celery文档 http://docs.jinkan.org/docs/celery/index.html
#Celery4.0.0在airflow中有一些问题，所以安装Celery3
pip install -U Celery==3.1.24
pip install airflow[celery]
修改配置文件

vi airflow.cfg

[core]
executor = CeleryExecutor

[celery]
broker_url = sqla+mysql://airflow:airflow@localhost:3306/airflow

celery_result_backend = db+mysql://airflow:airflow@localhost:3306/airflow
```



## Celery+RabbitMQ
```
wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.6.5/rabbitmq-server-3.6.5-1.noarch.rpm

#安装RabbitMQ的依赖包
yum install erlang

yum install socat

#如果下载了rabbitmq的yum源 sudo yum install -y rabbitmq-server
rpm -ivh rabbitmq-server-3.6.5-1.noarch.rpm
```

#### 启动RabbitMQ服务
```
#启动rabbitmq服务
sudo service rabbitmq-server start 
#或者
sudo rabbitmq-server

#添加 -detached 属性来让它在后台运行（注意：只有一个破折号）
sudo rabbitmq-server -detached

#设置开机启动rabbitmq服务
chkconfig rabbitmq-server on

#永远不要用 kill 停止 RabbitMQ 服务器，而是应该用 rabbitmqctl 命令
sudo rabbitmqctl stop
```

#### 设置RabbitMQ
```
#创建一个RabbitMQ用户
rabbitmqctl add_user airflow airflow

#创建一个RabbitMQ虚拟主机
rabbitmqctl add_vhost vairflow

#将这个用户赋予admin的角色
rabbitmqctl set_user_tags airflow admin

#允许这个用户访问这个虚拟主机
rabbitmqctl set_permissions -p vairflow airflow ".*" ".*" ".*"

# no usage
rabbitmq-plugins enable rabbitmq_management 
```


#### 修改airflow配置文件支持Celery
```
vi $AIRFLOW_HOME/airflow/airflow.cfg

#更改Executor为CeleryExecutor
executor = CeleryExecutor

#更改broker_url
broker_url = amqp://airflow:airflow@localhost:5672/vairflow
Format explanation: transport://userid:password@hostname:port/virtual_host

#更改celery_result_backend
celery_result_backend = amqp://airflow:airflow@localhost:5672/vairflow
Format explanation: transport://userid:password@hostname:port/virtual_host
```

#### 安装airflow的celery和rabbitmq模块
```
pip install airflow[celery]
pip install airflow[rabbitmq]
```

airflow使用DAG(Directed Acyclic Graph,有向无环图为)来管理作业流的
```python
#创建DAG
from datetime import datetime, timedelta
from airflow.models import DAG
args = {
    'owner': 'airflow',
    'start_date': seven_days_ago,
    'email': ['airflow@airflow.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retries_delay': timedelta(seconds=60),
    'depends_on_past': True
}

dag = DAG(
    dag_id='dag',
    default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60)
)
```

#### 创建任务将任务添加到DAG中
```python
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

demo = DummyOperator(
    task_id='demo',
    dag=dag
)

last_execute = BashOperator(
    task_id='last_execute',
    bash_command='echo 1',
    dag=dag
)
```
配置任务的依赖关系
```python
demo.set_downstream(last_execute)
```

#### 相关启动项
```bash
airflow webserver -p 8080

airflow scheduler

#以非root用户运行
airflow worker

#启动Celery WebUI 查看celery任务
airflow flower 
http://localhost:5555/
```
