---
title: "mysql-exporter"
linkTitle: "mysql-exporter"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 57
description: >
  mysql-exporter|exporter|prometheus

tags: ["prometheus","exporter","mysql-exporter"]
categories: ["prometheus","监控","exporter"]
url: prometheus/exporter/mysql-exporter.html
---

{{% alert title="" color="warning" %}}
mysql-exporter(0.17.2版本) 支持mysql>=5.6 、MariaDB >= 10.3
{{% /alert %}}

1. **[部署安装](https://github.com/prometheus/mysqld_exporter)**

   > 容器镜像 `prom/mysqld-exporter`

   *安装exporter*

   ```bash
   wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.17.2/mysqld_exporter-0.17.2.linux-amd64.tar.gz
   #
   tar xf mysqld_exporter-0.17.2.linux-amd64.tar.gz
   #
   mv mysqld_exporter-0.17.2.linux-amd64/mysqld_exporter /usr/bin/
   rm -fr mysqld_exporter*
   ```

   *添加监控用户*

   ```bash
   CREATE USER 'exporter'@'%' IDENTIFIED BY 'GlKUhymaO76zY' WITH MAX_USER_CONNECTIONS 3;
   GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'%';
   ```

   

   *启动服务*

   ```bash
   cat >/usr/lib/systemd/system/mysql_exporter_mysql01_3306.service<<'EOF'
   [Unit]
   Description = mysql-exporter
   Documentation = https://github.com/prometheus/mysqld_exporter
   After = network-online.target
   
   [Service]
   Type=Simple
   Environment="MYSQLD_EXPORTER_PASSWORD=GlKUhymaO76zY"
   ExecStart=/usr/bin/mysqld_exporter \
   --mysqld.address 10.128.99.158:6301 \
   --mysqld.username exporter 
   
   RestartSec=2
   Restart=on-failure
   User=root
   Group=root
   CPUQuota=20%
   MemoryLimit=128m
   
   [Install]
   WantedBy=multi-user.target
   EOF
   ```

   ```bash
   systemctl daemon-reload
   systemctl enable mysql_exporter_mysql01_3306 --now 
   systemctl status mysql_exporter_mysql01_3306
   ```

   

2. **添加prometheus配置**

   指标接口： `http://127.0.0.1:9104/metrics`

   类似于blackbox,可以采集其他redis: `http://127.0.0.1:9104/probe?127.0.0.1:3306`

   

3. **dashboar和告警**

   **进程相关**

   | 指标名称                  | 判断依据          |
   | ------------------------- | ----------------- |
   | `mysql_up`                | 进程状态1表示正常 |
   | `mysql_uptime_in_seconds` | 启动时长          |
   | `mysql_instance_info`     |                   |
   
   **内存相关**

   
   
   **网络流量相关**
   
   **持久化相关**
   
   **客户端连接相关**
   
   **慢日志**
   
   **性能**
   
   tps
   
   QPS
   
   **主从复制相关**

   
