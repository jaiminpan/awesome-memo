# Lex & Flex

## 基本格式
Lex & Flex 文件一般以`.l`后缀结尾。

```
定义段
%%
规则段
%%
代码段
```
#### 例子
```
// test.l
%{
#include <stdio.h>
%}

digit			[0-9]
%%
stop    printf("Stop command received\n");
start   printf("Start command received\n");
%%
int yywrap(void)
{
   return 1;
} 
```

#### 编译
```
# flex test.l // 默认输出文件名 lex.core_yy.c
flex -o test.c test.l // 指定文件名 test.c
gcc -o test test.c
```
#### 输出
```
-># ./test
start stop
Start command received
 Stop command received
```

## 基本语法
#### 定义段
* 格式: 
```
DIGIT [0-9]
ID [a-z][a-z0-9]*
```
* 定义段的： /*注释内容*/ 也会被复制到输出“.c”文件中。

#### 规则段:
* pattern action
* 规则中也可以通过/**/加注释，但不会被复制到输出".c"文件中。　　

#### 代码段
* 原样复制到输出的“.c”文件中

#### 其它
* 在定义和规则段，任何缩进的文本，或者是放在“%{”和“%}”之间的内容会被原封不动的复制到输出".c"文件中。


