---
date: '2025-07-04T10:57:00+08:00'
draft: false
title: 'master_slave'
type: blog
toc_hide: false
hide_summary: true
weight: 3
description: >
  mysql主从同步的原理和实现
tags: ["主从配置"]
categories: ["mysql"]
url: mysql/master_slave.html
author: "wangendao"
---





<table>
    <tr>
        <td><img src="/docs/database/mysql/主从架构.png" alt="主从架构图"></td>
        <td><img src="/docs/database/mysql/主从复制原理.png" alt="主从复制原理"></td>
    </tr>
</table>

---
### Mater-Slave 实现

主从是一种异步同步，主库在执行完客户端提交的事务后会立即将结果返回给客户端，并不关心从库是否已经接收并处理。
{{% alert title="" color="warning" %}}
1. 主库开启binlog
2. 主从之间设置不同的server_id
3. 从库设置为只读，防止多点写入
{{% /alert %}}

---


{{< tabpane text=true right=false >}}
  {{% tab header="**搭建主备关系**:" disabled=true /%}}
  {{% tab header="主库" lang="bash" %}}

  ```sql
  CREATE USER 'replUser'@'%' IDENTIFIED  BY 'RsU#58d1@'; 
  GRANT REPLICATION SLAVE,REPLICATION CLIENT ON *.* TO 'replUser'@'%'; 
  flush privileges;
  ```
  ```sql
  ---

  mysql> SHOW MASTER STATUS;
  +----------------+----------+--------------+------------------+------------------------------------------+
  | File           | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
  +----------------+----------+--------------+------------------+------------------------------------------+
  | log_bin.000002 |      551 |              |                  | b2a464ed-6c16-11f0-8445-000c299bad95:1-2 |
  +----------------+----------+--------------+------------------+------------------------------------------+
  ```

**同步指定库/表**

```ini
在主库的配置文件中执行
[mysqld]
binlog-do-db=mysql
binlog-do-db=radius
binlog-ignore-db=syslog
binlog-ignore-db=sys
```





  {{% /tab %}}
  {{% tab header="从库" lang="bash" %}}

  ### 5.7 之前没有开启gtid的数据库
  ```sql
  reset slave all;
  ---
  CHANGE MASTER TO 
    MASTER_HOST='10.128.99.157',
    MASTER_PORT=6301,
    MASTER_USER='rdsRpl',
    MASTER_PASSWORD='RsU#58d1@',
    master_log_file='log_bin.000002',
    MASTER_LOG_POS=551;
  start slave;show slave status \G
  ```

  ```sql
  -- 设置只读
  set global read_only=on;
  set global super_read_only=on;
  ```
  ### 5.7 及之后版本开始gtid的数据库

  ```sql
  reset slave all;
  --- 重置gtid执行历史
  reset slave all;
  reset master;
  SET @@GLOBAL.GTID_PURGED='b2a464ed-6c16-11f0-8445-000c299bad95:1-2';
  ---

  CHANGE MASTER TO 
    MASTER_HOST='10.128.99.157',
    MASTER_PORT=6301,
    MASTER_USER='rdsRpl',
    MASTER_PASSWORD='RsU#58d1@',
    MASTER_AUTO_POSITION=1;

  start slave;show slave status \G
  /*
  关键指标：
  Slave_IO_Running: Yes
  Slave_SQL_Running: Yes
  Seconds_Behind_Master: 0
  */
  ```
  ```sql
  -- 设置只读
  set global read_only=on;
  set global super_read_only=on;
  ```



**同步指定库/表--在配置文件中指定**

```ini
或在从库的配置文件中指定
[mysqld] 
replicate-do-db=mysql
replicate-do-db=radius
replicate-ignore-db=syslog
replicate-ignore-db=sys
# 通配符表级
replication-wild-do-table = db1.user_% 
replication-wild-ignore-table = db1.log_%
```

**同步指定库/表--动态修改**

```sql
-- 停止 SQL 线程
STOP SLAVE SQL_THREAD;

-- 修改过滤规则
CHANGE REPLICATION FILTER
    REPLICATE_DO_DB = (db1, db2),
    REPLICATE_IGNORE_TABLE = (db3.log);

-- 重新启动 SQL 线程
START SLAVE SQL_THREAD;
```





  {{% /tab %}}
{{< /tabpane >}}







### 主从报错处理

{{% alert title="从库连接异常" color="warning" %}}
```sql
Slave_IO_Running: Connecting
Last_IO_Errno: 1045
Last_IO_Error: error connecting to master 'rep@168.101.1.177:3306' - retry-time: 60  retries: 1
```
**处理办法**
```sql
update mysql.user set authentication_string=password('rep') where user='rep';
flush privileges;
```
{{% /alert %}}





{{% alert title="从库sql线程错误" color="warning" %}}

```sql
#跳过主从复制的sql线程错误
mysql> set sql_slve_skip_counter  = 1
```

{{% /alert %}}

