---
title: ""
linkTitle: "redis"
date: 2025-05-25
simple_list: true
weight: 3
type: docs
---


**BITCOUNT 统计字符串中存在多少个bit 位为1**

统计了字符串 “123” 中存在多少个1，1字节=8bit。

字节 “1” 对应ascii 码为 `0011 0001`

字节 “2” 对应ascii 码为 `0011 0010`

字节 “3” 对应ascii 码为 `0011 0011`



```redis
127.0.0.1:6379> set name 123 
OK
# BITCOUNT key [start end]
127.0.0.1:6379> BITCOUNT name
10
```



**[BITOP](https://redis.io/commands/bitop/)  为逻辑运算**

```redis
BITOP <AND | OR | XOR | NOT> destkey key [key ...]
```

字节 “1” 对应ascii 码为 `0011 0001`

字节 “2” 对应ascii 码为 `0011 0010`

 AND                              `0011 0000`

 OR                                 `0011 0011`

 XOR                              `0000 0011`

​                                      

```redis
127.0.0.1:6379> set a 1 
OK
127.0.0.1:6379> set b 2
OK
127.0.0.1:6379> BITOP and c a b 
1
127.0.0.1:6379> get c
0
```



**BITPOS  返回第一个符合条件的位置**

例如：

```redis
set a hello
```



```redis
127.0.0.1:6379> BITPOS a 1
1
```



**GETBIT 查找对应索引位置bit 的值 0|1**

例如：

```redis
set a hello
```



```redis
127.0.0.1:6379> GETBIT a 2
1
```

**SETBIT  修改指定位置bit 值**

例如

```redis
set a hello
```



```redis
127.0.0.1:6379> SETBIT a 0 1
0
127.0.0.1:6379> get a
o
```



**[bitfiled](https://redis.io/commands/bitfield/)**

0000

​    8 4 2  1=15

​       

  BITFIELD key [GET type offset] [SET type offset value] [INCRBY type offset increment] [OVERFLOW WRAP|SAT|FAIL]
  summary: Perform arbitrary bitfield integer operations on strings
  since: 3.2.0

hyperloglog

geo

stream

`MULTI`开启一个事务

`EXEC`执行事务

```redis
127.0.0.1:6379> MULTI
OK
127.0.0.1:6379> ZINCRBY salary 100 user01
QUEUED
127.0.0.1:6379> ZINCRBY salary -100 user02
QUEUED
127.0.0.1:6379> EXEC
1) "500"
2) "500

127.0.0.1:6379> ZRANGE salary 0 100 withscores
1) "user01"
2) "500"
3) "user02"
4) "500"
```



