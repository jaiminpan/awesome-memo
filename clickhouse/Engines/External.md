# External data for query processing

ClickHouse 允许向服务器发送SELECT语句的同时，发送处理查询所需的数据。此数据放在临时表中(请参阅'Temporary tables'章节)，并可用于查询(例如，IN运算符)。

例如，如果您有一个包含重要用户标识符的文本文件，则可以将其与使用此列表筛选的查询一起上载到服务器。

如果需要使用大量外部数据运行多个查询，请不要使用此功能。最好提前将数据上载到DB。

外部数据可以使用命令行客户端(在非交互模式下)或HTTP接口上传。

在命令行客户端中，可以按以下格式指定参数部分
```
--external --file=... [--name=...] [--format=...] [--types=...|--structure=...]
```

对于传输的数据，您可能有多个类似的部分。
* -external： 开始的标记。
* -file：具有表转储的文件的文件路径，或–仅可从stdin检索到一个表，该表转储引用stdin。

以下参数是可选的:
* –Name-表的名称。如果省略，则使用_data。
* –format-文件中的数据格式。如果省略，则使用TabSeparated。

以下参数至少需要一个:
* –types：列类型的逗号分隔列表。例如uint64，String。列将命名为_1、_2
* –structure： Table结构，格式为UserID UInt64, URL String。定义列名和类型。


**file**中指定的文件将，使用**types**或**structure**中指定的数据类型，使用**format**指定的格式分析。该表将上载到服务器，并可通过**name**临时表访问。

Examples:
```
echo -ne "1\n2\n3\n" | clickhouse-client --query="SELECT count() FROM test.visits WHERE TraficSourceID IN _data" --external --file=- --types=Int8
849897
cat /etc/passwd | sed 's/:/\t/g' | clickhouse-client --query="SELECT shell, count() AS c FROM passwd GROUP BY shell ORDER BY c DESC" --external --file=- --name=passwd --structure='login String, unused String, uid UInt16, gid UInt16, comment String, home String, shell String'
/bin/sh 20
/bin/false      5
/bin/bash       4
/usr/sbin/nologin       1
/bin/sync       1
```

使用HTTP接口时，外部数据以multipart / form -data格式传递。
每个表作为单独的文件传输。表名取自文件名。“query_string”传递参数 ‘name_format’, ‘name_types’, and ‘name_structure’，
其中name是这些参数对应的表的名称。参数的含义与使用命令行客户端时相同。

```
cat /etc/passwd | sed 's/:/\t/g' > passwd.tsv

curl -F 'passwd=@passwd.tsv;' 'http://localhost:8123/?query=SELECT+shell,+count()+AS+c+FROM+passwd+GROUP+BY+shell+ORDER+BY+c+DESC&passwd_structure=login+String,+unused+String,+uid+UInt16,+gid+UInt16,+comment+String,+home+String,+shell+String'
/bin/sh 20
/bin/false      5
/bin/bash       4
/usr/sbin/nologin       1
/bin/sync       1
```

对于分布式查询处理，临时表被发送到所有远程服务器。

