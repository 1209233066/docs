---
date: '2025-07-28T10:57:00+08:00'
draft: false
title: 'config'
type: blog
toc_hide: false
hide_summary: true
weight: 8
description: >
  mysql 配置文件解析
tags: ["mysql配置"]
categories: ["mysql"]
url: mysql/my_cnf.html
author: "wangendao"
---

```ini
[mysqld]
innodb_lock_wait_timeout = 60
sort_buffer_size = 8M
query_cache_limit = 32M
auto_increment_offset = 1 
auto_increment_increment = 1
character_set_database = utf8
character_set_results = utf8
character_set_server  = utf8
init_connect='启动时自动执行的内容'

#php设置为短连接
interactive_timeout = 30;  #合作的超时时间
wait_tiemout = 30;	#闲置的超时时间

#java 设置长连接
interactive_timeout = 28800;  
wait_tiemout = 28800;

#一个端口最大连接数
max_connections = 800
#一个用户的最大连接数
#max_user_connections = 800
#连接错误的最大数量
max_connect_errors = 3000
#兼容旧的密码模式
#old_password = on


read_only = on
#默认情况下从库启动自动开始同步，添加参数后需要手动start slave ;
skip_slave_start = on
#更新master_info 信息
sync_master_info = 1
记录relaylog，默认开启
sync_relay_log = 1
记录relaylog info 
sync_relay_log_info = 1


[client]
character_set_client =utf8
character_set_connection =utf8
character_set_results =utf8


[mysql]
character_set_connection=utf8
```



mysql 乱码字符集设置

```sql
字符集设置
set names utf8 ;
等同于 
set @@session.character_set_client =utf8;
set @@session.character_set_connection =utf8;
set @@session.character_set_results =utf8;

set @@session.character_set_database =utf8;
set @@session.character_set_server =utf8;
```

```ini
[client]
character_set_client =utf8
character_set_connection =utf8
character_set_results =utf8


[mysql]
character_set_connection=utf8
```







```bash

#导入表时关闭外检检查
set foreign_key_check = 0

#查询语句的性能
show profing;
show profie all;

#设置为分页查询
mysql> page less 

mysql> show master logs ;
mysql> purge master logs to 'binlog文件'

修复表
mysql> repair table 表名
myisamchk -r /var/lib/mysql/*.MYI



查询 innodb 的状态(比如死锁)
show engine innodb status \G

查询运行状态
show global status \G


查询增删改的数量
mysqladmin -uroot -i 3 -r exten|egrep -i '(com_insert\b)|(com_select)|(com_delete\b)|(com_update\b)' 



#查询进程号
pidof mysqld
gdb -p `pidof mysqld` -ex "set opt_log_slave_updates=1"


IO PS 每秒吞吐量
flashcache 开源软件 可以把ssd和sas磁盘虚拟化一块
把热数据存在ssd上把sas放在sas上


查询 cp io
mpstats -P ALL 1 100   查询所有cpu的使用情况 每秒打印一个打印100次
sar -u 1 100          查询所有cpu的使用情况 每秒打印一个打印100次
iostat -x 1 100
sar -b 1 100
sar -d 1 100
sar -q
sar -n DEV  查看网路
sar -W    查看内存
sar -r
sar -B
top 


dmesg -H --level=err,warn -k



优化
numad 

不使用swap
sysctl -a|grep swap 
echo "vm.swappiness = 0" >>/etc/sysctl.conf  
sysctl -p 

io调度
[root@localhost ~]# cat /sys/block/sda/queue/scheduler 
noop [deadline] cfq


ulimit 设定
软硬文件打开数
ulimit -HSn 65535
#stack size
ulimit -s 65535

查看raid信息
megacil 
[root@localhost ~]# top -b -n 1 | grep Cpu 
%Cpu(s):  0.0 us,  6.2 sy,  0.0 ni, 93.8 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st



性能调优
https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/6/html/performance_tuning_guide/index
https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/performance_tuning_guide/index


《mysql反范式》

数据类型
timestamp

mysql> select current_time(),now(),sysdate();
+----------------+---------------------+---------------------+
| current_time() | now()               | sysdate()           |
+----------------+---------------------+---------------------+
| 12:08:14       | 2020-03-08 12:08:14 | 2020-03-08 12:08:14 |
+----------------+---------------------+---------------------+
1 row in set (0.00 sec)

mysql> select inet_aton('192.168.0.1');
+--------------------------+
| inet_aton('192.168.0.1') |
+--------------------------+
|               3232235521 |
+--------------------------+
1 row in set (0.00 sec)

mysql> select inet_ntoa(3232235521);    
+-----------------------+
| inet_ntoa(3232235521) |
+-----------------------+
| 192.168.0.1           |
+-----------------------+
1 row in set (0.00 sec)



1.xtrabackup 安装
wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.4/binary/redhat/7/x86_64/percona-xtrabackup-24-2.4.4-1.el7.x86_64.rpm
yum install libev-devel.x86_64
yum install numactl-libs.x86_64
yum install perl-DBD-MySQL.x86_64
rpm -ivh percona-xtrabackup-24-2.4.4-1.el7.x86_64.rpm 
which xtrabackup
 
备份原理
xtrabackup 
首先启动备份innodb 引擎的线程 redolog 的备份和监听线程，
并开始备份ibd 数据文件。
当innodb引擎的数据文件备份完毕后，
flust table with read lock;
备份 .frm .myd .myi 文件。非innodb引擎数据文件备份完毕后
通知redolog 线程结束并记录数据文件的lsn号，便于下次增量
备份
 
 
 性能测试工具
 mysqlslap
 日志分析工具
https://www.jb51.net/article/75064.htm



### Centos7,centos6适用
yum groupinstall "X Window System"
yum groupinstall "GNOME Desktop"
通过命令 startx 进入图形界面
图形到dos：ctrl+alt+f2
dos到图形：输入startx
或者
在命令上输入 init 3 命令 切换到dos界面
输入 init 5命令 切换到图形界面
### centos 7
systemctl get-default
graphical.target代表开机时启动图形化界面
multi-user.target代表开机时启动dos界面
systemctl set-default graphical.target 
systemctl set-default multi-user.target 

ssh 连接客户端长时间不使用自动断开
export PATH=\$PATH:.
export PS1='\`hostname\`:\$PWD>'
set -o vi
stty erase ^H


back_log = 600
external-locking = FALSE
max_allowed_packet =8M
thread_stack = 192K
thread_stack = 192
[mysql]
no-auto-rehash

 



过滤
change master to Replicate_Ignore_DB = 'test';
Replicate_Do_DB:
Replicate_Ignore_DB: 
Replicate_Do_Table: 
Replicate_Ignore_Table: 
Replicate_Wild_Do_Table: 
Replicate_Wild_Ignore_Table:

http://itindex.net/index/mha
http://mysqlserverteam.com/
https://www.cnblogs.com/xiaoboluo768/p/5973827.html
https://blog.51cto.com/8370646/2150179
https://www.cnblogs.com/zengkefu/p/5600776.html
http://www.mamicode.com/info-detail-1488956.html?__cf_chl_jschl_tk__=864bd8082fbcc44cff88faa95540ef89c8b1b1ed-1584599149-0-AZzn7zH3F9Q-fMosxg8_z2LhSKfhM8v8fHU4CwyiFxVIk0VzRZI1cOMDw3H6MDQvflAFPsEL9s1MKiUp0hv-9DgUhwYnONrP7mGzp5ZLoSQBlxx9PK4W74ZQrzdsLbUqj3x_clEVUJwdXTPNq-3NiQ0Oz08ONGXWoF2Bx9WfddC9sPngJHUB9CgTE-TKk6o1ktyutexm0QT_zn1jyvml2RK4N133vdGwewmb4QttA_CjOSV4ftDAhu5284B86HQd3Q8VGbn0W9aIC0VGHARUdb5JE0tb2usYTx_IbtaG-QglcJIVYJD5eFWX8Vf7_Okbtw

```

