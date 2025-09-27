---
date: '2025-07-28T10:57:00+08:00'
draft: false
title: 'install mysql5.6'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  mysql 5.6版本二进制安装和编译安装
tags: ["安装mysql"]
categories: ["mysql"]
url: mysql/install5.6.html
author: "wangendao"
---

### 部署安装

+ 实例名称 `mysql-01` 示例使用全局变量引用

  ```bash
  export clsName='mysql-01'
  ```

  

1. 添加用户

   ```bash
   useradd -s /sbin/nologin -u 3306 -M mysql
   ```
   
   
   
   安装mysql依赖
   
   ```bash
   # libaio提供 Linux 原生异步 I/O（AIO）支持，允许程序发起非阻塞的磁盘读写操作，提高高并发场景下的 I/O 性能
   yum install -y libaio libaio-devel ncurses ncurses-devel cpanminus
   ```
   
2. mysql软件安装，示例安装在`/opt/mysql`目录下

   {{< tabpane text=true right=true >}}
    {{% tab header="**软件安装**:" disabled=true /%}}
    {{% tab header="二进制安装" lang="en" %}}

   *软件下载*

   ```bash
   wget https://downloads.mysql.com/archives/get/p/23/file/mysql-5.6.40-linux-glibc2.12-x86_64.tar.gz
   ```

   ```bash
   tar xf mysql-5.6.40-linux-glibc2.12-x86_64.tar.gz -C /opt
   ```

   *安装到/opt/mysql下*

   ```bash
   ln -svf /opt/{mysql-5.6.40-linux-glibc2.12-x86_64,mysql}
   ln -svf /opt/mysql-5.6.40-linux-glibc2.12-x86_64/bin/mysql /usr/bin/mysql
   ```

   
    {{% /tab %}}
    {{% tab header="编译安装" lang="en" %}}
   *软件下载*

   ```bash
   wget https://downloads.mysql.com/archives/get/p/23/file/mysql-5.6.40.tar.gz
   ```

   ```bash
   tar xf mysql-5.6.40.tar.gz -C /opt
   cd /opt/mysql-5.6.40
   ```
   *安装编译依赖*

  


   ```bash
   yum install -y cmake  libaio-devel  gcc-c++ perl-devel cpanminus ncurses-devel
   ```

   ```bash
   cmake . -DCMAKE_INSTALL_PREFIX=/opt/mysql \
   -DMYSQL_DATADIR=/data/instances/${clsName}/data \
   -DMYSQL_UNIX_ADDR=/data/instances/${clsName}/mysql.sock \
   -DDEFAULT_CHARSET=utf8 \
   -DDEFAULT_COLLATION=utf8_general_ci \
   -DWITH_EXTRA_CHARSETs=all \
   -DWITH_INNOBASE_STORAGE_ENGINE=1 \
   -DWITH_FEDERATED_STORAGE_ENGINE=1 \
   -DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
   -DWITH_EXAMPLE_STORAGE_ENGINE=1 \
   -DWITH_ZLIB=bundled \
   -DWITH_SSL=bundled \
   -DENABLED_LOCAL_INFILE=1 \
   -DWITH_EMBEDDED_SERVER=1 \
   -DENABLE_DOWNLOADS=1 \
   -DWITH_DEBUG=0
   ```

   ```bash
   make -j 4 && make install
   ```
   ```bash
    ln -svf /opt/mysql/bin/mysql /usr/bin/mysql
   ```
{{% /tab %}}
{{< /tabpane >}}

   


3. 初始化

   ```bash
   # 构建目录结构
   mkdir -p /data/instances/${clsName}/{data,binlog,logs,relay_log,conf}
   chown -R mysql:mysql /data/instances/${clsName}
   # 初始化数据库
   /opt/mysql/scripts/mysql_install_db \
   --basedir=/opt/mysql/ \
   --datadir=/data/instances/${clsName}/data \
   --explicit_defaults_for_timestamp \
   --user=mysql
   ```
   
   {{< details >}}
   
   ```log
   [root@seagullcore01-uat-s2 ~]# /opt/mysql/scripts/mysql_install_db \
   > --basedir=/opt/mysql/ \
   > --datadir=/data/instances/${clsName}/data \
   > --explicit_defaults_for_timestamp \
   > --user=mysql
   Installing MySQL system tables...2025-07-28 11:23:40 0 [Note] Ignoring --secure-file-priv value as server is running with --bootstrap.
   2025-07-28 11:23:40 0 [Note] /opt/mysql//bin/mysqld (mysqld 5.6.40) starting as process 29771 ...
   2025-07-28 11:23:40 29771 [Note] InnoDB: Using atomics to ref count buffer pool pages
   2025-07-28 11:23:40 29771 [Note] InnoDB: The InnoDB memory heap is disabled
   2025-07-28 11:23:40 29771 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
   2025-07-28 11:23:40 29771 [Note] InnoDB: Memory barrier is not used
   2025-07-28 11:23:40 29771 [Note] InnoDB: Compressed tables use zlib 1.2.3
   2025-07-28 11:23:40 29771 [Note] InnoDB: Using Linux native AIO
   2025-07-28 11:23:40 29771 [Note] InnoDB: Using CPU crc32 instructions
   2025-07-28 11:23:40 29771 [Note] InnoDB: Initializing buffer pool, size = 128.0M
   2025-07-28 11:23:40 29771 [Note] InnoDB: Completed initialization of buffer pool
   2025-07-28 11:23:40 29771 [Note] InnoDB: The first specified data file ./ibdata1 did not exist: a new database to be created!
   2025-07-28 11:23:40 29771 [Note] InnoDB: Setting file ./ibdata1 size to 12 MB
   2025-07-28 11:23:40 29771 [Note] InnoDB: Database physically writes the file full: wait...
   2025-07-28 11:23:40 29771 [Note] InnoDB: Setting log file ./ib_logfile101 size to 48 MB
   2025-07-28 11:23:40 29771 [Note] InnoDB: Setting log file ./ib_logfile1 size to 48 MB
   2025-07-28 11:23:40 29771 [Note] InnoDB: Renaming log file ./ib_logfile101 to ./ib_logfile0
   2025-07-28 11:23:40 29771 [Warning] InnoDB: New log files created, LSN=45781
   2025-07-28 11:23:40 29771 [Note] InnoDB: Doublewrite buffer not found: creating new
   2025-07-28 11:23:40 29771 [Note] InnoDB: Doublewrite buffer created
   2025-07-28 11:23:40 29771 [Note] InnoDB: 128 rollback segment(s) are active.
   2025-07-28 11:23:40 29771 [Warning] InnoDB: Creating foreign key constraint system tables.
   2025-07-28 11:23:40 29771 [Note] InnoDB: Foreign key constraint system tables created
   2025-07-28 11:23:40 29771 [Note] InnoDB: Creating tablespace and datafile system tables.
   2025-07-28 11:23:40 29771 [Note] InnoDB: Tablespace and datafile system tables created.
   2025-07-28 11:23:40 29771 [Note] InnoDB: Waiting for purge to start
   2025-07-28 11:23:40 29771 [Note] InnoDB: 5.6.40 started; log sequence number 0
   2025-07-28 11:23:41 29771 [Note] Binlog end
   2025-07-28 11:23:41 29771 [Note] InnoDB: FTS optimize thread exiting.
   2025-07-28 11:23:41 29771 [Note] InnoDB: Starting shutdown...
   2025-07-28 11:23:42 29771 [Note] InnoDB: Shutdown completed; log sequence number 1625977
   OK
   
   Filling help tables...2025-07-28 11:23:42 0 [Note] Ignoring --secure-file-priv value as server is running with --bootstrap.
   2025-07-28 11:23:42 0 [Note] /opt/mysql//bin/mysqld (mysqld 5.6.40) starting as process 29794 ...
   2025-07-28 11:23:42 29794 [Note] InnoDB: Using atomics to ref count buffer pool pages
   2025-07-28 11:23:42 29794 [Note] InnoDB: The InnoDB memory heap is disabled
   2025-07-28 11:23:42 29794 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
   2025-07-28 11:23:42 29794 [Note] InnoDB: Memory barrier is not used
   2025-07-28 11:23:42 29794 [Note] InnoDB: Compressed tables use zlib 1.2.3
   2025-07-28 11:23:42 29794 [Note] InnoDB: Using Linux native AIO
   2025-07-28 11:23:42 29794 [Note] InnoDB: Using CPU crc32 instructions
   2025-07-28 11:23:42 29794 [Note] InnoDB: Initializing buffer pool, size = 128.0M
   2025-07-28 11:23:42 29794 [Note] InnoDB: Completed initialization of buffer pool
   2025-07-28 11:23:42 29794 [Note] InnoDB: Highest supported file format is Barracuda.
   2025-07-28 11:23:42 29794 [Note] InnoDB: 128 rollback segment(s) are active.
   2025-07-28 11:23:42 29794 [Note] InnoDB: Waiting for purge to start
   2025-07-28 11:23:43 29794 [Note] InnoDB: 5.6.40 started; log sequence number 1625977
   2025-07-28 11:23:43 29794 [Note] Binlog end
   2025-07-28 11:23:43 29794 [Note] InnoDB: FTS optimize thread exiting.
   2025-07-28 11:23:43 29794 [Note] InnoDB: Starting shutdown...
   2025-07-28 11:23:44 29794 [Note] InnoDB: Shutdown completed; log sequence number 1625987
   OK
   
   To start mysqld at boot time you have to copy
   support-files/mysql.server to the right place for your system
   
   PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
   To do so, start the server, then issue the following commands:
   
     /opt/mysql//bin/mysqladmin -u root password 'new-password'
     /opt/mysql//bin/mysqladmin -u root -h seagullcore01-uat-s2 password 'new-password'
   
   Alternatively you can run:
   
     /opt/mysql//bin/mysql_secure_installation
   
   which will also give you the option of removing the test
   databases and anonymous user created by default.  This is
   strongly recommended for production servers.
   
   See the manual for more instructions.
   
   You can start the MySQL daemon with:
   
     cd . ; /opt/mysql//bin/mysqld_safe &
   
   You can test the MySQL daemon with mysql-test-run.pl
   
     cd mysql-test ; perl mysql-test-run.pl
   
   Please report any problems at http://bugs.mysql.com/
   
   The latest information about MySQL is available on the web at
   
     http://www.mysql.com
   
   Support MySQL by buying support/licenses at http://shop.mysql.com
   
   New default config file was created as /opt/mysql//my.cnf and
   will be used by default by the server when you start it.
   You may edit this file to change server settings
   
   WARNING: Default config file /etc/my.cnf exists on the system
   This file will be read by default by the MySQL server
   If you do not want to use this, either remove it, or use the
   --defaults-file argument to mysqld_safe when starting the server
   ```
   
   {{< /details >}}
   
   
   
4. 启动服务

   ```bash
   cat >/data/instances/${clsName}/conf/my.cnf<<EOF
   [mysqld]
   performance_schema=ON
   server_id=1921680152
   port=3306
   character-set-server=utf8mb4
   basedir=/opt/mysql
   datadir=/data/instances/${clsName}/data/
   pid-file=/data/instances/${clsName}/mysql.pid
   socket=/data/instances/${clsName}/mysql.sock
   log_error=/data/instances/${clsName}/logs/mysql-error.log
   slow_query_log_file=/data/instances/${clsName}/logs/mysql_slow_query.log
   slow_query_log=on
   long_query_time=1
   binlog_format=row
   log-bin=/data/instances/${clsName}/binlog/log_bin
   log-bin-index=/data/instances/${clsName}/binlog/binlog.index
   #gtid-mode=on
   #enforce-gtid-consistency=on
   relay_log=/data/instances/${clsName}/relay_log
   relay_log_index=/data/instances/${clsName}/relaylog/relay-bin.index
   relay_log_recovery=on
   default_authentication_plugin=mysql_native_password
   master_info_repository=table
   relay_log_info_repository=table
   EOF
   ```
   
   
   
   ```bash
   tee /usr/lib/systemd/system/mysql.service <<'EOF'
   [Unit]
   Description=mysql service https://dev.mysql.com/doc/refman/5.6/en
   After=network.target
   
   [Service]
   
   ExecStart=/opt/mysql/bin/mysqld_safe \
   --defaults-file=/data/instances/mysql-01/conf/my.cnf \
   --pid-file=/data/instances/mysql-01/mysql.pid
   ExecReload=/bin/kill -HUP $MAINPID
   
   User=mysql
   # 设置最大文件描述符
   LimitNOFILE=1024
   # 设置CPU使用率限制为50%
   CPUQuota=50%
   # 设置内存限制为1G
   MemoryLimit=1G
   [Install]
   WantedBy=multi-user.target
   EOF
   ```
   
   ```bash
   systemctl daemon-reload
   systemctl enable mysql --now
   systemctl status  mysql
   ```
   
5. 创建用户
   ```sql
   --- 修改root密码
   ALTER USER 'root'@'localhost' identified by 'li<)<#jyi9S)2024'; 
   ```
   ```sql
   --- 超管用户
   create user 'root'@'%' identified by 'li<)<#jyi9S)2024';
   grant all privileges on *.* to 'root'@'%' WITH GRANT OPTION ;
   ```
   ```sql
   --- 管理用户
   create user 'rdsAdmin'@'%' identified by 'li<)<#jyi9S)2024';
   grant all privileges on *.* to 'rdsAdmin'@'%' WITH GRANT OPTION  ; 
   ```
   ```sql
   --- 复制用户
   create user 'rdsRpl'@'%' identified by 'li<)<#jyi9S)2024';
   GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'rdsRpl'@'%';
   
   flush privileges;
   ```