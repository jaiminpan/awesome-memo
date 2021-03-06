# Merge

Merge引擎(不要与Mergetree混淆)本身不存储数据，但允许同时读取任意数量的其他表。读取将自动并行化。不支援写入表。
读取时，使用实际正在读取的表的索引(如果存在)。合并引擎接受参数:数据库名称和表的正则表达式。范例:
```
Merge(hits, '^WatchLog')
```

* 将使用hits中，所有匹配正则`^WatchLog`的表中读取数据。

您可以使用传回字串的常数表达式，而不是数据库字符串名。例如，`currentDatabase()`。

正则表达式是re2 (类似于PCRE)，区分大小写。请参阅“匹配”部分中有关在正则表达式中转义符号的注释。

选择要读取的表时，Merge 表本身将不会被选择，即使它与regex匹配。
这是为了避免循环。比如可以创建两个合并表，它们将无休止地尝试读取彼此的数据。但不要这样做。

使用Merge 引擎的典型方法是，把大量的TinyLog表，用起来像使用单个表一样。

## Virtual columns

虚拟列是由表引擎提供的列，与表定义无关。换句话说，`CREATE TABLE`中未指定这些列，但可以用SELECT访问这些列。

虚拟列与普通列的不同之处如下:
* 表定义中未指定它们。
* 无法使用`INSERT`将数据添加到其中。
* 在不指定列列表的情况下使用`INSERT`时，将忽略虚拟列。
* `SELECT *`时，不会选择它们。
* `SHOW CREATE TABLE`和`DESC TABLE`查询中不显示虚拟列。

Merge 表包含String类型的虚拟列**_table**。(如果表中已有`_table`列，则虚拟列名为`_table1`，如果已有`_table1`，则名为`_table2`，依此类推)。
它包含读取数据的表的名称。

如果WHERE或PREWHERE子句包含不依赖于其他表列的`_table`列的条件(作为连接元素之一或作为整个表达式)，则这些条件将用作索引。
对要从中读取数据的表名数据集执行条件，并且将仅从触发条件的那些表执行读取操作。


