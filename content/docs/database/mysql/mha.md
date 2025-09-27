---
date: '2025-07-28T10:57:00+08:00'
draft: false
title: 'mha'
type: blog
toc_hide: false
hide_summary: true
weight: 4
description: >
  mha是使用ruby语言实现的高可用方案
tags: ["mha","ha"]
categories: ["mysql"]
url: mysql/mha.html
author: "wangendao"
---

| 主机名       | IP             | server_id | 角色                | 版本   | 设置                                                        |
| ------------ | -------------- | --------- | ------------------- | ------ | ----------------------------------------------------------- |
| mysqldbphw01 | 172.32.4.10/24 | 1         | `master`/`MHA Node` | 5.6.40 | 1.设置server-id<br>2.开启binlog<br>3.配置vip 172.32.4.50/24 |
| mysqldbphw02 | 172.32.4.20/24 | 2         | `slave`/`MHA Node`  | 5.6.40 | 1.设置server-id<br>2.设置为只读                             |
| mysqldbphw03 | 172.32.4.30/24 | 3         | `slave`/`MHA Node`  | 5.6.40 | 1.设置server-id<br/>2.设置为只读                            |
| mysqldbphw04 | 172.32.4.40/24 |           | `MHA Manager`       |        |    
{{% alert title="" color="" %}}

+ 添加一个vip 用于应用接入
+ 设置ssh免密要认证，用于failover时执行网络、binlog拷贝等动作 
{{% /alert %}}


```bash
ifconfig eth0:2 172.32.4.50/24
ssh-keygen -t rsa -f /root/.ssh/id_rsa -N ""
```
```bash
2.5测试
主库手工绑定vip：ifconfig eth0:1 168.204.37.17/24 up 
masterha_check_ssh --conf=/etc/mha/app1.cnf 
masterha_check_repl --conf=/etc/mha/app1.cnf
2.6启动
[root@mysqldbphw04 /]# nohup masterha_manager --conf=/etc/mha/app1.cnf > /mha/manager.log < /dev/null &
[1] 933
查看运行状态
[root@mysqldbphw04 /]# masterha_check_status --conf=/etc/mha/app1.cnf
app1 (pid:933) is running(0:PING_OK), master:mysqldbphw01
2.7关闭
masterha_sotp  --conf=/etc/mha/app1.cnf
#
[root@mysqldbphw04 /]# masterha_secondary_check -s mysqldbphw01 -s  mysqldbp
hw02  -s mysqldbphw03 --user=root --master_host=mysqldbphw01 --master_ip=172
.32.4.10 --master_port=3306
Master is reachable from mysqldbphw01!
```

[MYSQL高可用架构MGR、MHA对比 - 小雨淅淅o0 - 博客园 (cnblogs.com)](https://www.cnblogs.com/xiaoyuxixi/p/13814811.html)