---
title: "minio"
linkTitle: "minio"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 55
description: >
  minio|exporter|prometheus

tags: ["prometheus","exporter","minio"]
categories: ["prometheus","监控","exporter"]
url: prometheus/exporter/minio.html
---

1. 部署安装

   > minio自身暴露了prometheus 兼容指标。我们只需要在启动前添加环境变量: `MINIO_PROMETHEUS_AUTH_TYPE="public"`

   ```bash
   wget https://dl.min.io/server/minio/release/linux-amd64/minio
   chmod +x minio
   sudo mv minio /usr/local/bin/
   ```

   ```bash
   tee  /etc/systemd/system/minio.service <<EOF
   [Unit]
   Description=minio serveice test
   After=network.target
    
   [Service]
   EnvironmentFile=/data/minio/conf/minio.env
   
   ExecStart=/data/minio/bin/minio server \
   /data/minio/data \
   --address :9000 \
   --console-address :9001
   User=root
   [Install]
   WantedBy=multi-user.target
   EOF
   ```

   ```bash
   tee /data/minio/conf/minio.env<<EOF
   MINIO_ROOT_USER=admin
   MINIO_ROOT_PASSWORD=admin12345
   MINIO_PROMETHEUS_AUTH_TYPE="public"
   EOF
   ```

   

   

2. 添加prometheus配置

   ```bash
   - job_name: minio
     honor_timestamps: true
     metrics_path: /minio/v2/metrics/cluster
     follow_redirects: true
     static_configs:
     - targets:
       - 10.4.7.251:9000
   ```

   

3. 常用指标

   minio 挂载磁盘的总大小，就是例子中 `/data/minio/data`

   ```bash
   minio_node_disk_total_bytes
   ```
   
   ```bash
   minio_node_disk_free_bytes
   ```

   ```bash
   minio_node_disk_used_bytes
   ```
   
   

   查看特定bucket池子的使用量 (gauge)

   ```bash
   minio_bucket_usage_total_bytes{bucket="loki"}
   ```
   
   ```bash
   minio_bucket_usage_object_total{bucket="loki"}
   ```

   对象存储大小分布 (gauge)

   ```bash
   minio_bucket_objects_size_distribution
   ```