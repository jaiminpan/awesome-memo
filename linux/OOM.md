# Out Of Memory (OOM)

Reference: http://learning-kernel.readthedocs.org/en/latest/mem-management.html

1. OOM启动是在分配内存时发生页面错误时触发的，没有剩余内存阙值可控制。  

2. OOM结束进程只是简单的搜寻哪个进程的`/proc/<PID>/oom_score`数值分最大。
  系统综合进程的内存消耗量、CPU时间、存活时间和oom_adj、oom_score_adj计算，消耗内存越多分越高，存活时间越长分越低，
  总的策略是：损失最少的工作，释放最大的内存同时不伤及无辜的用了很大内存的进程，并且杀掉的进程数尽量少。

3. 调整oom_score的值可通过更改`/proc/<PID>/oom_score_adj`或`/proc/<PID>/oom_adj`进行。
  oom_score_adj范围-1000~~+1000，数值越小越安全，-1000表示OOM对此进程禁用；
  同样oom_adj范围-17~~+15，数值越小越安全，-17表示OOM对此进程禁用。
  对oom_adj的支持基于兼容过去内核版本，尽量使用`/proc/<PID>/oom_score_adj`进行设置。

4. Linux在计算进程的内存消耗的时候，会将子进程所耗内存的一半同时算到父进程中。

```sh
# It's often a good idea to protect the postmaster from being killed by the
# OOM killer (which will tend to preferentially kill the postmaster because
# of the way it accounts for shared memory).  Setting the OOM_SCORE_ADJ value
# to -1000 will disable OOM kill altogether.  If you enable this, you probably
# want to compile PostgreSQL with "-DLINUX_OOM_SCORE_ADJ=0", so that
# individual backends can still be killed by the OOM killer.
#OOM_SCORE_ADJ=-1000
# Older Linux kernels may not have /proc/self/oom_score_adj, but instead
# /proc/self/oom_adj, which works similarly except the disable value is -17.
# For such a system, enable this and compile with "-DLINUX_OOM_ADJ=0".
#OOM_ADJ=-17

test x"$OOM_SCORE_ADJ" != x && echo "$OOM_SCORE_ADJ" > /proc/self/oom_score_adj
test x"$OOM_ADJ" != x && echo "$OOM_ADJ" > /proc/self/oom_adj
# then do your start proc here
start_my_proc
```
