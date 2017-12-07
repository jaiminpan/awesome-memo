# AggregatingMergeTree

此引擎与MergeTree不同，因为合并操作将存储在表中的聚合函数的状态合并为具有相同的主键值的行。

为了使这种行为能正常工作，它使用AggregateFunction数据类型和 -State和 -Merge修饰符来实现聚合函数。

## 
有一个aggregatefunction数据类型，它是一个参数数据类型。第一个参数是聚合函数的名称，然后的参数是这个函数的参数类型。例子:
```
CREATE TABLE t
(
    column1 AggregateFunction(uniq, UInt64),
    column2 AggregateFunction(anyIf, String, UInt8),
    column3 AggregateFunction(quantiles(0.5, 0.9), UInt64)
) ENGINE = ...
```
这个列的类型是存储聚合函数的state的类型。


要获取此类型的值，请使用带有'State'后缀的聚合函数。
示例: uniqState(UserID), quantilesState(0.5, 0.9)(SendTiming)-与对应的'uniq'和'quantiles'函数相比，这些函数返回state状态，而不是准备的值。
换句话说，它们返回一个AggregateFunction 类型的值。
AggregateFunction 类型值不能以漂亮的格式输出。在其他格式中，这些类型的值作为特定的二进制数据输出。AggregateFunction 类型值不用于输出或备份。

唯一使用AggregateFunction类型值的地方是合并state并获得结果，这实质上意味着完成聚合操作。具有'Merge'后缀的聚合函数用于完成聚合。
示例: uniqMerge(UserIDState), 其中UserIDState 具有AggregateFunction 类型。

换句话说，带有'Merge'后缀的聚合函数使用一组state，合并它们并返回结果。例如，下面这两个查询返回相同的结果:
```
SELECT uniq(UserID) FROM table

SELECT uniqMerge(state) FROM (SELECT uniqState(UserID) AS state FROM table GROUP BY RegionID)
```

有一个AggregatingMergeTree引擎。它在合并期间的工作是将来自不同表的数据，以相同的主键值，合并聚合函数的state。

对于含有AggregateFunction 列的表，不能使用普通的insert操作。因为不能显式定义AggregateFunction 的值。
而是使用INSERT SELECT with '-State' 聚合函数插入数据。

从AggregatingMergeTree 引擎的表中进行SELECT，使用GROUP BY和aggregate函数以及'-Merge'修饰符完成数据聚合。

您可以使用AggregatingMergeTree 表进行增量数据聚合，包括聚合物化视图(materialized views)。

示例:创建一个AggregatingMergeTree类型的物化视图，追踪'test.visits'表:
```
CREATE MATERIALIZED VIEW test.basic
ENGINE = AggregatingMergeTree(StartDate, (CounterID, StartDate), 8192)
AS SELECT
    CounterID,
    StartDate,
    sumState(Sign)    AS Visits,
    uniqState(UserID) AS Users
FROM test.visits
GROUP BY CounterID, StartDate;
```

在'test.visits'表中插入数据，同样还将在视图中插入数据，数据将在视图中聚合:
```
INSERT INTO test.visits ...
```

通过对视图进行 GROUP BY 查询完成数据聚合:
```
SELECT
    StartDate,
    sumMerge(Visits) AS Visits,
    uniqMerge(Users) AS Users
FROM test.basic
GROUP BY StartDate
ORDER BY StartDate;
```

您可以创建这样的物化视图，并为其分配完成数据聚合的普通视图。

请注意，在大多数情况下，使用AggregatingMergeTree 是不合理的，因为查询可以在非聚合数据上足够高效地运行。
