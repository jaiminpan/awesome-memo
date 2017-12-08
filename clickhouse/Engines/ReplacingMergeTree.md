# ReplacingMergeTree

此引擎与MergeTree 的不同之处在于，它可以在合并时按主键消除重复数据。

对于ReplacingMergeTree模式，最后一个参数是作为'version(版本)'的列(可选)。

合并时，对于具有相同主键的所有行，只选取一行(如果没有指定版本列，选择最后一行，如果指定了版本，选择版本号最大的最后一行。)

version列的类型必须是`UInt`系列或`Date`或`DateTime`其中一种。

```
ReplacingMergeTree(EventDate, (OrderID, EventDate, BannerID, ...), 8192, ver)
```

请注意，只有在合并过程中才会对数据进行重复数据消除。合并在后台处理。未指定合并的确切时间，您无法依赖它。部分数据根本无法合并。
虽然您可以使用OPTIMIZE查询触发额外合并，但不建议这样做，因为OPTIMIZE将读取和写入大量数据。
此表引擎适用于重复数据的后台删除，以节省空间，但不适于保证重复数据消除。

*专为特殊目的开发*
