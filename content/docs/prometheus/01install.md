---
title: "install"
linkTitle: "install"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 1
description: >
  安装|prometheus

tags: ["prometheus","安装"]
categories: ["prometheus","监控"]
url: prometheus/install.html
---

![架构图](https://prometheus.io/assets/architecture.png)

### 二进制安装

1. 添加用户
   ```bash
   useradd prometheus --system -s /sbin/nologin
   ```
   
2. 挂载磁盘
   
   ```bash
   # 创建一个名为data的thinpool
   vgName=centos
   lvcreate -L 100G --thinpool data ${vgName}
   # 创建名为prometheus的lv
   lvcreate -n prometheus --virtualsize 500G --thinpool data ${vgName}
   # 格式化
   mkfs.ext4 /dev/${vgName}/prometheus
   # 创建prometheus目录
   mkdir /data/prometheus -p
   # 开机自启动挂载
   echo "$(blkid /dev/mapper/${vgName}-prometheus|awk '{print $2}') /data/prometheus ext4 defaults 0 0"  >>/etc/fstab
   
   # 挂载验证
   mount -a
   df -hT /data/prometheus/
   ```
   
3. [下载长期支持版](https://prometheus.io/docs/introduction/release-cycle/)
   
   | Release         | Date       | End of support |
   | :-------------- | :--------- | :------------- |
   | Prometheus 2.37 | 2022-07-14 | 2023-07-31     |
   | Prometheus 2.45 | 2023-06-23 | 2024-07-31     |
   | Prometheus 2.53 | 2024-06-16 | 2025-07-31     |
   
   ```bash
   version=2.53.0
   ```
   
   ```bash
   wget https://github.com/prometheus/prometheus/releases/download/v${version}/prometheus-${version}.linux-amd64.tar.gz
   ```
   ```bash
   tar xf prometheus-${version}.linux-amd64.tar.gz -C /data
   ```
   
   
   ```bash
   mkdir /data/prometheus/{bin,conf,conf/rules,data,log} -p
   ```
   ```bash
   cp /data/prometheus-${version}.linux-amd64/prometheus /data/prometheus/bin/
   cp /data/prometheus-${version}.linux-amd64/promtool /data/prometheus/bin/
   cp /data/prometheus-${version}.linux-amd64/prometheus.yml /data/prometheus/conf
   cp -a /data/prometheus-${version}.linux-amd64/console* /data/prometheus/conf
   ```
   
   ```bash
   chown -R prometheus:prometheus /data/prometheus*
   ```
   
   ```bash
   /data/prometheus
   ├── bin
   │   ├── prometheus
   │   └── promtool
   ├── conf
   │   └── prometheus.yml
   ├── data
   └── log
   
   4 directories, 3 files
   ```
   
   
   
4. 通过systemd管理服务
   
   > <sub>`--storage.tsdb.retention.time 替代了--storage.tsdb.retention`</sub>
   >
   > <sub>提供远程写入到prometheus的功能:<br>老版本` --enable-feature=remote-write-receiver`<br>新版本--web.enable-remote-write-receiver</sub>
   
   ```bash
   tee /usr/lib/systemd/system/prometheus.service <<'EOF'
   [Unit]
   Description=promethues service https://prometheus.io/
   After=network.target
   
   [Service]
   ExecStartPre=/data/prometheus/bin/promtool check config /data/prometheus/conf/prometheus.yml
   
   ExecStart=/data/prometheus/bin/prometheus \
   --web.listen-address=0.0.0.0:9090 \
   --config.file=/data/prometheus/conf/prometheus.yml \
   --web.read-timeout=5m \
   --web.max-connections=10 \
   --storage.tsdb.retention.time=15d \
   --storage.tsdb.retention.size=100GB \
   --storage.tsdb.path=/data/prometheus/data \
   --query.max-concurrency=20 \
   --query.timeout=2m \
   --web.console.templates=/data/prometheus/conf/consoles \
   --web.console.libraries=/data/prometheus/conf/console_libraries \
   --web.enable-lifecycle \
   --web.enable-admin-api \
   --web.external-url=/prom
   
   ExecReload=/usr/bin/curl -s -X POST 127.0.0.1:9090/-/reload
   User=prometheus
   [Install]
   WantedBy=multi-user.target
   EOF
   ```
   
   ```bash
   systemctl daemon-reload
   systemctl enable prometheus --now  
   systemctl status prometheus
   ```
   
  