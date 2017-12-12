# Join

为JOIN 预处理的数据结构，始终位于RAM中。

```
Join(ANY|ALL, LEFT|INNER, k1[, k2, ...])
```

引擎参数:
* ANY | ALL ： 方式
* LEFT | INNER： join类型

这些参数设置为不带引号，并且必须与表将用于的JOIN 相匹配。k1，k2，…是将在其上进行连接的USING子句中的关键列。

表不能用于GLOBAL JOINs。

可以使用INSERT向表中添加数据，类似于Set引擎。对于ANY，将忽略重复键的数据。对于ALL，这将被计算在内。

不能直接从表中执行SELECT。检索数据的唯一方法是将其用作JOIN的“右侧”表。

在磁盘上存储数据与在Set engine中存储数据相同
