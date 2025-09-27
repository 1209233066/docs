---
date: '2025-07-28T10:57:00+08:00'
draft: false
title: 'mysqldump'
type: blog
toc_hide: false
hide_summary: true
weight: 6
description: >
  mysqldump逻辑备份工具
tags: ["备份","mysqldump"]
categories: ["mysql"]
url: mysql/mysqldump.html
author: "wangendao"
---





{{% alert title="" color="warning" %}}

1. **InnoDB 优先用 `--single-transaction`**，避免锁表影响业务。
2. **MyISAM 必须锁表**（默认行为），需在低峰期操作。
3. **大表备份**：结合 `--quick` 和输出压缩（如 `gzip`）。

```sql
--备份前先执行flush tables 将内容写入磁盘（mysql必知必会中提到）
flush tables ;
```

{{% /alert %}}



{{< tabpane text=true right=false >}}
  {{% tab header="**逻辑备份**:" disabled=true /%}}
  {{% tab header="备份所有库" lang="en" %}}

创建备份用户

   ```sql
   create user 'backup'@'localhost' identified by 'd988ec6a93!@#MYSQL';
   GRANT SELECT, SHOW VIEW, RELOAD, LOCK TABLES, PROCESS ON *.* TO 'backup'@'localhost';
   
   flush privileges;
   ```

备份命令

```bash
# 备份所有数据库
/usr/local/mysql80/bin/mysqldump \
-A \
--single-transaction --master-data=2 \
-u root -p'd988ec6a93!@#MYSQL' -h 10.128.99.157 -P 6301 \
|gzip >/Backup/fullbackup`date +%F-%H:%M:%S`.sql.gz
```

  

{{% /tab %}}
  {{% tab header="备份指定库" lang="en" %}}

创建备份用户

```sql
create user 'backup'@'localhost' identified by 'd988ec6a93!@#MYSQL';
GRANT SELECT, SHOW VIEW, RELOAD, LOCK TABLES, PROCESS ON *.* TO 'backup'@'localhost';

flush privileges;
```

备份命令

   ```bash
   # 备份指定数据库
   /usr/local/mysql80/bin/mysqldump \
   -B infra_settle \
   --single-transaction --master-data=2 \
   -u root -p'd988ec6a93!@#MYSQL' -h 10.128.99.157 -P 6301 \
   |gzip >/Backup/fullbackup`date +%F-%H:%M:%S`.sql.gz
   ```

  {{% /tab %}}
{{< /tabpane >}}



| 参数               | 说明                           | 示例                       |
| :----------------- | :----------------------------- | :------------------------- |
| `-u`, `--user`     | 指定用户名                     | `-u root`                  |
| `-p`, `--password` | 密码（建议不加密码，后续输入） | `-p` 或 `-p'123'`          |
| `-h`, `--host`     | MySQL 服务器地址               | `-h 127.0.0.1`             |
| `-P`, `--port`     | 端口号（默认3306）             | `-P 6301`                  |
| `--socket`         | 指定 Unix Socket 文件路径      | `--socket=/tmp/mysql.sock` |
| `-A`, `--all-databases` | 备份所有数据库           | `mysqldump -A > full_backup.sql` |
| `-B`, `--databases`     | 备份指定数据库（可多个） | `-B db1 db2`                     |
| `--tables`              | 指定表（需先指定数据库） | `dbname --tables table1 table2`  |
| `--ignore-table`        | 排除指定表               | `--ignore-table=db.logs`         |
| `--no-data`        | 仅备份表结构，不备份数据 | `--no-data`        |
| `--no-create-info` | 仅备份数据，不备份表结构 | `--no-create-info` |
| `--routines`       | 包含存储过程和函数       | `--routines`       |
| `--triggers`       | 包含触发器               | `--triggers`       |
| `--events`         | 包含事件调度器           | `--events`         |
| `--skip-triggers`  | 排除触发器               | `--skip-triggers`  |
| `--single-transaction` | 开启事务保证 InnoDB 一致性快照            | InnoDB |
| `--lock-tables`        | 备份前锁定所有表（默认开启）              | MyISAM     |
| `--skip-lock-tables`   | 不锁表（可能导致不一致）                  | 紧急情况   |
| `--flush-logs`         | 备份前刷新日志（用于 Binlog 增量恢复）    | 所有引擎   |
| `--master-data`        | 记录 Binlog 位置（`=1`注释，`=2`SQL语句） | 主从复制   |
| `--result-file` | 指定输出文件（避免 Windows 换行问题） | `--result-file=backup.sql` |
| `--compress`    | 压缩传输（节省网络带宽）              | `--compress`               |
| `--tz-utc`      | 统一时区为 UTC（默认开启）            | `--tz-utc`                 |
| `--hex-blob`    | 二进制数据以十六进制导出              | `--hex-blob`               |
| `--quick`                | 逐行导出（避免内存溢出）     | 大表备份     |
| `--extended-insert`      | 合并多行 INSERT（默认开启）  | 减少备份体积 |
| `--skip-extended-insert` | 每行单独 INSERT（可读性高）  | 调试用途     |
| `--opt`                  | 启用所有优化选项（默认开启） | 综合优化     |







备份脚本{{< details >}}

```bash
#!/bin/bash
# 脚本名称: mysql_backup.sh
# 描述: MySQL数据库备份脚本，支持全库备份、binlog同步及过期清理
# 作者: wangendao(1209233066@qq.com)
# 创建日期: 2019/03/01
# 最后修改日期: $(date +%F)

# 调试选项 (取消注释以启用)
# set -euo pipefail  # 更严格的错误检查
# set -x            # 显示执行过程

# 配置变量
export PATH=/application/mysql5.6/bin:$PATH
datadir=/application/mysql5.6/
backupdir=/backup
logdir=/var/log/mysql_backup
timestamp=$(date +%F_%H%M%S)
user=root
password='123'
socket=/application/mysql5.6/mysql.sock
rsync_ip=168.204.37.25
retention_days=7  # 备份保留天数

# 创建必要的目录
mkdir -p "$backupdir" "$logdir"

# 日志函数
log() {
    echo "[$(date '+%F %T')] $1" >> "$logdir/mysql_backup_${timestamp}.log"
}

# 错误处理函数
error_exit() {
    log "ERROR: $1"
    sendEmail -f wangendao@crv.com.cn -t wangendao@crv.com.cn \
              -s 10.248.2.15 -u "MySQL备份失败警报" \
              -o tls=no -o message-content-type=html \
              -o message-charset=utf8 -xu wangendao@crv.com.cn \
              -xp Wed10203040 -m "MySQL备份失败: $1"
    exit 1
}

# 获取数据库列表
DBlist=($(mysql -u "${user}" -p"${password}" -S "${socket}" \
          -e "SHOW DATABASES;" | \
          awk '!/^(information_schema|performance_schema|test|database|mysql)$/' | \
          tail -n +2))

if [ ${#DBlist[@]} -eq 0 ]; then
    error_exit "未获取到数据库列表"
fi

# 备份每个数据库
for db in "${DBlist[@]}"; do
    backup_file="${backupdir}/${db}_${timestamp}.gz"
    md5_file="${backupdir}/${db}_${timestamp}.md5"
    
    log "开始备份数据库: $db"
    
    if ! mysqldump -B "$db" \
        -u"${user}" -p"${password}" -S "${socket}" \
        --master-data=2 \
        --single-transaction \
        --routines \
        --triggers | gzip > "$backup_file"; then
        error_exit "数据库 $db 备份失败"
    fi
    
    # 生成MD5校验文件
    if ! md5sum "$backup_file" > "$md5_file"; then
        error_exit "无法生成MD5校验文件"
    fi
    
    log "数据库 $db 备份完成, 文件: $backup_file"
done

# 同步备份文件
log "开始同步备份文件到远程服务器"
if ! rsync -az --delete "${backupdir}/" "rsync@${rsync_ip}::ftp" \
     --password-file=/etc/rsync.password >> "$logdir/rsync.log" 2>&1; then
    error_exit "备份文件同步失败"
fi

# 同步binlog文件
log "开始同步binlog文件"
if ! rsync -az "${datadir}/" --include 'mysql-bin*' --exclude '*' \
     "rsync@${rsync_ip}::ftp" --password-file=/etc/rsync.password \
     >> "$logdir/binlog_sync.log" 2>&1; then
    error_exit "binlog文件同步失败"
fi

# 清理过期备份
log "清理${retention_days}天前的备份"
find "$backupdir" -type f -name "*.gz" -mtime +"$retention_days" -delete
find "$backupdir" -type f -name "*.md5" -mtime +"$retention_days" -delete

# 发送成功通知
log "备份任务完成"
sendEmail -f wangendao@crv.com.cn -t wangendao@crv.com.cn \
          -s 10.248.2.15 -u "MySQL备份成功通知" \
          -o tls=no -o message-content-type=html \
          -o message-charset=utf8 -xu wangendao@crv.com.cn \
          -xp Wed10203040 -m "MySQL备份任务已完成<br><br>备份数据库列表:<br>${DBlist[*]}<br><br>备份文件已保留最近${retention_days}天"
```


{{< /details >}}