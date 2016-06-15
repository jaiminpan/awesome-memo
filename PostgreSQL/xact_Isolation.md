# 事务隔离
Reference: [WiKi](https://zh.wikipedia.org/wiki/事務隔離)

# 隔离级别(Isolation levels)
有四种隔离级别:
* 可序列化(Serializable)
* 可重复读(Repeatable reads)
* 提交读(Read committed)
* 未提交读(Read uncommitted)

讨论一个提问: 当存在表test(id int)有id=1 一条记录, 以下两种行为  
a. SessionA启动事务后，SessionB做了更新id=2操作后，此时SessionA进行 `UPDATE test SET id=id+2`，结果如何。  
b. SessionA启动事务后，SessionB在事务中做了更新id=2操作后，先不提交，此时SessionA进行 `UPDATE test SET id=id+2`，结果如何。  

顺着源码分析一下Postgres的是如何实现这种行为的。

#### 提交读（PostgreSQL的默认设置）
在提交读的隔离级别下，  
1.行为a的结果，SessionA 进行更新操作前查询id变为2，更新操作成功后，查询id为4。  
2.行为b的结果，在SessionB提交前，SessionA的查询id为1，如进行update操作，会一直阻塞直到SessionB提交或回滚，如SessionB成功提交查询id为4，若SessionB回滚，查询id结果为3。

行为1分析  
SessionA的运行流程和普通的更新流程类似，先得到需要更新的row，然后进入`heap_update`，对选定的row使用`HeapTupleSatisfiesUpdate`进行版本(MVCC)检查，由于SessionB的事务已经提交，所以会得到`HeapTupleMayBeUpdated`的状态，然后真正进行更新操作。（其中包括hot-update等各种流程就不在此描述）

行为2分析  
此时的运行流程会和上面略有不同，当获取目标row时候会得到尚未更新的那行row（因为此row虽然被标记为已删除，但是因为SessionB尚未提交，所以仍然可见），对row进行更新版本检查时，发现此row已经删除，且SessionB还未提交，标记为HeapTupleBeingUpdated，接着尝试取得该row的锁（会等待直到SessionB提交或者回滚），之后检查此row，如果被更新成功（SessionB提交），则进行row的refresh，对refresh后的row重新进行之前的操作，如果更新失败（SessionB回滚），则直接更新。


#### 可重复读
在可重复读的隔离级别下，  
1.行为a的结果， SessionA 进行更新操作前查询id为1，若进行更新操作, 则报错 “could not serialize access due to concurrent update”。  
2.行为b的结果， 在SessionB提交前，SessionA的查询id为1，如进行update操作，会一直阻塞直到SessionB提交或回滚，如SessionB成功提交则报错 “could not serialize access due to concurrent update”， 若SessionB回滚，则sessionA 的 UPDATE操作成功，查询id结果为3, 

行为1分析  
和提交读隔离级别的行为有点类似，但由于是可重复读的快照，所以一开始取得的目标row是更新前的row，也就是id=1(提交读id=2)的行，于是在更新操作的mvcc版本检查中会认为此row是HeapTupleUpdated状态，需要重新refresh row，在refresh对隔离级别进行检查，如果大于等于可重复读的级别，则抛错。

行为2分析  
和提交读隔离级别的代码路径一致，只是在 refresh row 时 对隔离级别进行检查，因为此时为可重复读，所以抛错。
