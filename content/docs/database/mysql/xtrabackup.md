---
date: '2025-07-23T10:10:00+08:00'
draft: false
title: 'xtrabackup'
type: blog
toc_hide: false
hide_summary: true
weight: 7
description: >
  mysql 备份工具之xtrabackup
tags: ["备份","xtrabackup"]
categories: ["mysql"]
url: mysql/xtrabackup.html
author: "wangendao"
---

### xtrabackup

xtrabackup 与mysql版本矩阵：

| XtraBackup 版本 | 支持的 MySQL 版本           | 关键限制                                        |
| :-------------- | :-------------------------- | :---------------------------------------------- |
| **8.0 系列**    | MySQL 8.0.x（推荐 8.0.20+） | 完全兼容 MySQL 8.0，**不支持 MySQL 5.7 及以下** |
| **2.4 系列**    | MySQL 5.6、5.7              | 不支持 MySQL 8.0                                |

> **注意**：
>
> - XtraBackup **8.0 不支持备份 MySQL 5.7**。若需备份 MySQL 5.7，必须使用 XtraBackup 2.4。
> - Percona 强烈建议 **XtraBackup 小版本号与 MySQL 大版本一致**（例如 MySQL 8.0.32 搭配 XtraBackup 8.0.32）。



##### 安装xtrabackup

```bash
cat >/etc/yum.repos.d/percona-original-release.repo <<'EOF'
[percona-release-x86_64]
name = Percona Original release/x86_64 YUM repository
baseurl = http://repo.percona.com/percona/yum/release/$releasever/RPMS/x86_64
enabled = 1
gpgcheck = 0
gpgkey = file:///etc/pki/rpm-gpg/PERCONA-PACKAGING-KEY

[percona-release-noarch]
name = Percona Original release/noarch YUM repository
baseurl = http://repo.percona.com/percona/yum/release/$releasever/RPMS/noarch
enabled = 1
gpgcheck = 0
gpgkey = file:///etc/pki/rpm-gpg/PERCONA-PACKAGING-KEY

[percona-release-sources]
name = Percona Original release/sources YUM repository
baseurl = http://repo.percona.com/percona/yum/release/$releasever/SRPMS
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/PERCONA-PACKAGING-KEY
EOF
```

```bash
yum install -y percona-xtrabackup-80.x86_64 
```



##### 全量备份

> 170G 数据压缩后16g,全备耗时7分钟,占用1.5核心cpu
```bash
xtrabackup \
--defaults-file=/etc/mysql80/mysql80_6301.cnf \
--backup \
--user="root" --password='d988ec6a93!@#MYSQL' --port=6301 \
--target-dir="/Backup/fullbackup-$(date +%F)" \
--compress --compress-threads=2  2>&1 | tee /tmp/mysql6301_$(date +%F_%H%M%S).log
```

##### 恢复全量备份

> 限速100Mb 传输16G, 耗时3分钟
```bash
scp -l 819200 -rp /Backup/fullbackup-2025-07-22/* bak@10.128.99.157:/Data/bak/
```

```bash
rm -fr /Data/mysql6301/{binlog,data,log}
mkdir  /Data/mysql6301/{binlog,data,log} -p
touch /Data/mysql6301/log/mysqld-error.log
```



```bash
# 解压 16gb 耗时 2分钟
xtrabackup --decompress --parallel=2 --target-dir=/Data/bak --remove-original
# 应用undolog
xtrabackup --prepare --apply-log-only --target-dir=/Data/bak
xtrabackup --prepare --target-dir=/Data/bak
# 拷贝全量备份到datadir
xtrabackup --defaults-file=/etc/my.cnf --copy-back --target-dir=/Data/bak
```

```bash
chown -R mysql.mysql /Data/mysql6301
service mysql start 
chkconfig mysql on
```

##### 增量同步数据

{{< tabpane text=true right=false >}}

  {{% tab header="主库" lang="sql" %}}
  创建复制用户
```sql
CREATE USER 'replUser'@'%' IDENTIFIED BY 'Repl#0001'; 
GRANT REPLICATION SLAVE ON *.* TO 'replUser'@'%'; 
flush privileges ;
```
  {{% /tab %}}
  {{% tab header="从库" lang="bash" %}}

设置只读，预防多点写入
```bash
/usr/local/mysql80/bin/mysql -uroot  -p'd988ec6a93!@#MYSQL' --socket=/Data/mysql6301/mysql6301.sock --port=6301

mysql> set global read_only=on;
Query OK, 0 rows affected (0.00 sec)

mysql> set global super_read_only=on;
Query OK, 0 rows affected (0.00 sec)

mysql> show variables like '%read_only%';
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| innodb_read_only      | OFF   |
| read_only             | ON    |
| super_read_only       | ON    |
| transaction_read_only | OFF   |
+-----------------------+-------+
4 rows in set (0.00 sec)
```


找到全备时的binlog位置
```bash
[root@db3-mysql80-m data]# cat xtrabackup_binlog_info 
mysql-bin.000362        156
```

```sql
/*从库*/
reset slave all;
CHANGE MASTER TO 
    MASTER_HOST='10.128.111.157',
    MASTER_PORT=6301,
    MASTER_USER='replUser',
    MASTER_PASSWORD='Repl#0001',
    MASTER_LOG_FILE='mysql-bin.000362',
    MASTER_LOG_POS=156;

start slave ;
show slave status \G
```
检查slave状态
```bash
[root@db3-mysql80 ~]# /usr/local/mysql80/bin/mysql -uroot  -p'd988ec6a93!@#MYSQL' --socket=/Data/mysql6301/mysql6301.sock --port=6301 -e "show slave status\G"|grep -E "Slave_IO_Running|Slave_SQL_Running:|Seconds_Behind_Master"
mysql: [Warning] Using a password on the command line interface can be insecure.
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
        Seconds_Behind_Master: 0
```

  {{% /tab %}}
{{< /tabpane >}}