# MergeTree

MergeTree引擎支持一个按primary key和date的索引，并提供了实时更新数据的可能性。这是ClickHouse中最先进的表引擎。不要把它和Merge引擎搞混淆。

MergeTree引擎接受参数: 一个包含date类型的列名、一个采样表达式(可选)、定义主键的元组和索引粒度(index granularity)。例子:

```
Example without sampling support:
#> MergeTree(EventDate, (CounterID, EventDate), 8192)

Example with sampling support:
#> MergeTree(EventDate, intHash32(UserID), (CounterID, EventDate, intHash32(UserID)), 8192)
```

Datek列：MergeTree类型的表必须有一个单独包含date的列。在这个示例中，它是EventDate。date列的类型必须是Date(不是DateTime)。

主键：可以是来自任何表达式的元组(通常这是一个组列名)，或者一个表达式。

采样表达式(可选)：可以是任何表达式。它还必须存在于主键中。该示例使用UserID的哈希值对表中的每个CounterID和EventDatee散布数据。
换句话说，当查询示例时，您会得到一个UserID子集的数据均匀的伪随机样本。

MergeTree表会分为很多part，然后通过part的合集实现。每个part都按主键排序。此外，每个part都具有分配的最小和最大date。
当往表中插入数据时，将创建一个新的排序part。合并进程会在后台定期启动执行。在合并时，选择几个part，通常是数据量最小的part，然后合并成一个大的排序part。

换句话说，在插入到表时会发生增量排序。因此表总是由较少的排序part组成，合并本身不会做太多的工作。

在插入期间，属于不同月份的数据被分为不同的part。不同月份对应的part从不合并。其目的是提供本地数据修改(以方便备份)。
part合并后会有一定大小的threshold(阈值)限制，因此不会有耗时太长的合并发生。

对于每个part，对应生成一个索引文件。索引文件包含表中的每个'index_granularity(索引粒度)'行的主键值。换句话说，这是排序数据的简要索引(abbreviated index)。
对于列，每个'index_granularity(索引粒度)'行的'marks'也会写入，以便可以在特定范围内读取数据。

从表中读取时，SELECT查询会被分析是否可以使用索引。如果WHERE或PREWHERE子句具有等式操作或不等式比较操作的表达式(作为一个或全部的连接元素)，
或者主键、日期的以上列中有IN、Boolean运算符，则可以使用索引。

因此，可以对主键的一个或多个范围快速运行查询。查询很快的例子：
```
SELECT count() FROM table WHERE EventDate = toDate(now()) AND CounterID = 34
SELECT count() FROM table WHERE EventDate = toDate(now()) AND (CounterID = 34 OR CounterID = 42)
SELECT count() FROM table WHERE ((EventDate >= toDate('2014-01-01') AND EventDate <= toDate('2014-01-31')) OR EventDate = toDate('2014-05-01')) AND CounterID IN (101500, 731962, 160656) AND (CounterID = 101500 OR EventDate != toDate('2014-05-01'))
```
所有上面的例子都使用索引(日期和主键)。甚至复杂表达式都用了索引。对表的读取顺序是重新组织过的，以便使用索引的速度不会慢于全表扫描。


在下面的例中，无法使用索引:
```
SELECT count() FROM table WHERE CounterID = 34 OR URL LIKE '%upyachka%'
```

date索引从所需范围中仅仅读取包含此date的part。但是，数据部分可能包含其他date的数据(最多整个月)，而在单个part中，数据按主键排序，
主键可能不包含日期作为第一列。因此，使用仅具有未指定主键前缀的日期条件的查询将导致读取的数据多于单个日期的数据。

对于并发表查询，我们使用多版本控制。换句话说，当同时读取和更新表时，数据从当前正在查询的一组part中读取数据。没有长锁。插入不会妨碍读取操作。

从表中读取数据将自动并行化。

支持优化查询，这将调用额外的合并步骤。

您可以使用单个大表，并以chunks(小块)的形式向其连续添加数据，这就是MergeTree的设计目标。

MergeTree系列中所有类型的表都支持数据复制
