# Linux终端

## 显示色彩

#### 1. 属性介绍: 
(1). 来自网络的ANSI属性控制码:
```
\033[0m                 关闭所有属性
\033[1m                 设置高亮度
\033[4m                 下划线
\033[5m                 闪烁
\033[7m                 反显
\033[8m                 消隐
\033[30m -- \033[37m    设置前景色
\033[40m -- \033[47m    设置背景色
\033[nA                 光标上移n行
\033[nB                 光标下移n行
\033[nC                 光标右移n列
\033[nD                 光标左移n列
\033[y;H                设置光标位置
\033[2J                 清屏
\033[K                  清除从光标到行尾的内容
\033[s                  保存光标位置
\033[u                  恢复光标位置
\033[?25l               隐藏光标
\033[?25h               显示光标
```

(2). 文字背景色彩数字: (颜色范围:40 - 49)
```
40:    黑色
41:    深红色
42:    绿色
43:    黄色
44:    蓝色
45:    紫色
46:    深绿色
47:    白色
```
(3). 文字前景色数字: (颜色范围: 30 - 39)
```
30:    黑色
31:    红色
32:    绿色
33:    黄色
34:    蓝色
35:    紫色
36:    深绿色
37:    白色
```

#### 2. 使用例子:
Linux终端会解析这些控制码, 并且依据控制码来设置终端的绘制属性, 所以, 只要输出流中包含ANSI控制码就可以工作, 这里使用linux的echo命令来演示:  (你可以使用任何你熟悉的语言来代替...)

(1). 字体红色输出:   

查看上面的ANSI控制码可以知道: \033[30m -- \033[37m是控制前景色, 并且红色使用31表示, 即: 红色ANSI控制码为:  \033[31m
```
echo -e "\033[31m红色字体\033[0m"     #需要加上-e参数
```

从\033[31m处开始使用"红色"作为字体的前景色, 后面全部的绘制都使用红色, 直到遇到属性关闭控制码. 所以: 后面使用\033[0m来关闭属性, 要不然终端后面的输入的文字将全部是红色的. 效果图:

(2). 使用多个控制码产生叠加效果:  红色+高亮
```
echo -e "\033[31m\033[1m红色+高亮\033[0m"   #高亮控制码为: \033[1m
```

(3). 红底+白字+高亮+下划线:
```
echo -e "\033[41m\033[37m\033[1m\033[4m红底+白字+高亮+下划线\033[0m"
```
多个控制码可以一起使用, 从而看到叠加的效果, 控制码之间的顺序无所谓, 例如: 上面的高亮和下划线.  其他的控制码就可以自己试试了.

## 终端进度条

#### PHP
```php
<?php
for ($i = 0; $i <= 50; $i++) {
  printf("progress: [%-50s] %d%%\r", str_repeat('#',$i), $i * 2); 
  usleep(1000 * 100); 
} 
echo "\n"; 
echo "Done.\n";
?>
```

#### BASH
```
#!/bin/sh
b=''
for ((i=0;$i<=100;i+=2))
do
	printf "progress: [%-50s] %d%%\r" $b $i
	sleep 0.1
	b+='#'
done
echo
```

### C的进度条

头文件
```
#ifndef progress_h
#define progress_h
 
#include <stdio.h>
 
typedef struct {
    char chr;       /*tip char*/
    char *title;    /*tip string*/
    int style;      /*progress style*/
    int max;        /*maximum value*/
    float offset;
    char *pro;
} progress_t;
 
#define PROGRESS_NUM_STYLE 0
#define PROGRESS_CHR_STYLE 1
#define PROGRESS_BGC_STYLE 2
 
extern void progress_init(progress_t *, char *, int, int);
 
extern void progress_show(progress_t *, float);
 
extern void progress_destroy(progress_t *);
 
#endif  /*ifndef*/
```

c文件
```
/**
 * linux terminal progress bar (no thread safe).
 *  @package progress.c
 *
 * @author chenxin <chenxin619315@gmail.com>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
#include "progress.h"

extern void progress_init(
    progress_t *bar, char *title, int max, int style)
{
    bar->chr = '#';
    bar->title = title;
    bar->style = style;
    bar->max = max;
    bar->offset = 100 / (float)max;
    bar->pro = (char *) malloc(max+1);
    if ( style == PROGRESS_BGC_STYLE )
    memset(bar->pro, 0x00, max+1);
    else {
    memset(bar->pro, 32, max);
    memset(bar->pro+max, 0x00, 1);
    }
}
 
extern void progress_show( progress_t *bar, float bit )
{
    int val = (int)(bit * bar->max);
    switch ( bar->style ) 
    {
    case PROGRESS_NUM_STYLE:
    printf("\033[?25l\033[31m\033[1m%s%d%%\033[?25h\033[0m\r",
        bar->title, (int)(bar->offset * val));
    fflush(stdout);
    break;
    case PROGRESS_CHR_STYLE:
    memset(bar->pro, '#', val);
    printf("\033[?25l\033[31m\033[1m%s[%-s] %d%%\033[?25h\033[0m\r", 
        bar->title, bar->pro, (int)(bar->offset * val));
    fflush(stdout);
    break;
    case PROGRESS_BGC_STYLE:
    memset(bar->pro, 32, val);
    printf("\033[?25l\033[31m\033[1m%s\033[41m %d%% %s\033[?25h\033[0m\r", 
        bar->title, (int)(bar->offset * val), bar->pro);
    fflush(stdout);
    break;
    }
}
 
//destroy the the progress bar.
extern void progress_destroy(progress_t *bar)
{
    free(bar->pro);
}
```

测试
```
/**
 * program bar test program.
 *
 * @author chenxin <chenxin619315@gmail.com>
 */
#include "progress.h"
#include <unistd.h>
 
int main(int argc, char *argv[] )
{
    progress_t bar;
    //progress_init(&bar, "", 50, PROGRESS_NUM_STYLE);
    progress_init(&bar, "", 50, PROGRESS_CHR_STYLE);
    //progress_init(&bar, "", 50, PROGRESS_BGC_STYLE);
 
    int i;
    for ( i = 0; i <= 50; i++ ) {
    progress_show(&bar, i/50.0f);
    sleep(1);
    }
    printf("\n+-Done\n");
 
    progress_destroy(&bar);
 
    return 0;
}
```

参考：
1. http://my.oschina.net/jcseg/blog/178047  
2. http://git.oschina.net/lionsoul/ltpro  
