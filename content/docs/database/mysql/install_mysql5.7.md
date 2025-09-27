---
date: '2025-07-28T10:57:00+08:00'
draft: false
title: 'install mysql5.7'
type: blog
toc_hide: false
hide_summary: true
weight: 2
description: >
  mysql 5.7版本二进制安装和编译安装
tags: ["安装mysql"]
categories: ["mysql"]
url: mysql/install5.7.html
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
   wget https://downloads.mysql.com/archives/get/p/23/file/mysql-5.7.40-linux-glibc2.12-x86_64.tar.gz
   ```

   ```bash
   tar xf mysql-5.7.40-linux-glibc2.12-x86_64.tar.gz -C /opt
   ```

   *安装到/opt/mysql下*

   ```bash
   ln -svf /opt/{mysql-5.7.40-linux-glibc2.12-x86_64,mysql}
   ln -svf /opt/mysql-5.7.40-linux-glibc2.12-x86_64/bin/mysql /usr/bin/mysql
   ```

    {{% /tab %}}
    {{% tab header="编译安装" lang="en" %}}
   *软件下载,5.7.5之后的版本需要boost*
   
   ```bash
   wget https://downloads.mysql.com/archives/get/p/23/file/mysql-boost-5.7.40.tar.gz
   ```
   
   ```bash
   tar xf mysql-boost-5.7.40.tar.gz -C /opt
   cd /opt/mysql-5.7.40
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
   -DWITH_ZLIB=system \
   -DWITH_SSL=system \
   -DENABLED_LOCAL_INFILE=1 \
   -DWITH_EMBEDDED_SERVER=1 \
   -DENABLE_DOWNLOADS=1 \
   -DWITH_DEBUG=0 \
   -DWITH_BOOST=boost
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
   ```
   配置文件
   {{% alert title="mysql从5.7开始支持 GTID(Global Transaction Identifiers)，开启gtid功能配置如下：" color="" %}}
   
   ```ini
   gtid-mode=on
   enforce-gtid-consistency=on
   ```
   {{% /alert %}}

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
   log_timestamps=SYSTEM
   binlog_format=row
   log-bin=/data/instances/${clsName}/binlog/log_bin
   log-bin-index=/data/instances/${clsName}/binlog/binlog.index
   gtid-mode=on
   enforce-gtid-consistency=on
   relay_log=/data/instances/${clsName}/relay_log
   relay_log_index=/data/instances/${clsName}/relaylog/relay-bin.index
   relay_log_recovery=on
   default_authentication_plugin=mysql_native_password
   master_info_repository=table
   relay_log_info_repository=table
   EOF
   ```

   初始化数据库
  {{% alert title="查看初始化密码" color="" %}}
  `cat /data/instances/${clsName}/logs/mysql-error.log`
  {{% /alert %}}
   
   ```bash
   /opt/mysql/bin/mysqld --defaults-file=/data/instances/${clsName}/conf/my.cnf --user=mysql --initialize
   ```
   
   
4. 启动服务

   ```bash
   tee /usr/lib/systemd/system/mysql.service <<'EOF'
   [Unit]
   Description=mysql service https://dev.mysql.com/doc/refman/5.7/en
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
