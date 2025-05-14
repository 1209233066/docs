---
title: "blackbox"
linkTitle: "blackbox"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 52
description: >
  blackbox|exporter|prometheus

tags: ["prometheus","exporter","blackbox"]
categories: ["prometheus","监控","exporter"]
url: prometheus/exporter/blackbox.html
---

blackbox是一个黑盒监控的代表，他通过各种模块来探测监控对象，并将结果返回给prometheus

1. 部署安装

   ```bash
   wget https://github.com/prometheus/blackbox_exporter/releases/download/v0.24.0/blackbox_exporter-0.24.0.linux-amd64.tar.gz
   ```

   ```bash
   tar xf blackbox_exporter-0.24.0.linux-amd64.tar.gz 
   ```

   ```bash
   mkdir /data/blackbox_exporter/{bin,conf} -p
   ```

   ```bash
   mv blackbox_exporter-*linux-amd64/blackbox_exporter /data/blackbox_exporter/bin/
   mv blackbox_exporter-*linux-amd64/blackbox.yml /data/blackbox_exporter/conf/
   ```

   ```bash
   tee /usr/lib/systemd/system/blackbox_exporter.service <<EOF
   [Unit]
   Description=blackbox_exporter service https://prometheus.io/
   After=network.target
   
   [Service]
   
   ExecStart=/data/blackbox_exporter/bin/blackbox_exporter \
   --web.listen-address=:9115 \
   --config.file=/data/blackbox_exporter/conf/blackbox.yml
    
   User=root
   [Install]
   WantedBy=multi-user.target
   EOF
   ```

   启动blackbox

   ```bash
   systemctl daemon-reload
   systemctl enable blackbox_exporter --now
   systemctl status blackbox_exporter 	
   ```

   [默认配置](https://github.com/prometheus/blackbox_exporter/blob/master/example.yml)

   

   功能验证,`probe_success  1`表示探测成功

   ```bash
   curl -s  "http://127.0.0.1:9115/probe?module=http_2xx&target=www.baidu.com"|grep probe_success
   # probe_success 1
   ```

   

2. 添加prometheus配置

   ```yaml
     - job_name: 'blackbox-http'
       metrics_path: /probe
       params:
         module: [http_2xx]  # 指定模块
       static_configs:
       - targets:
         - http://192.168.0.172:9999/magic/web/index.html  # Target to probe with http.
         - https://sg-web-bjuat.pytech.cn/qc/dash   # Target to probe with https.
       relabel_configs:
       - source_labels: [__address__]
         target_label: __param_target
       - source_labels: [__param_target]
         target_label: instance
       - target_label: __address__
         replacement: 127.0.0.1:9115
       
     - job_name: 'blackbox-icmp'
       metrics_path: /probe
       params:
         module: [icmp]  # 指定模块
       static_configs:
       - targets:
         - 192.168.0.172
       relabel_configs:
       - source_labels: [__address__]
         target_label: __param_target
       - source_labels: [__param_target]
         target_label: instance
       - target_label: __address__
         replacement: 127.0.0.1:9115
   ```

3. 常用指标

   | 主要指标                         | 解释              |      |
   | -------------------------------- | ----------------- | ---- |
   | `probe_dns_lookup_time_seconds ` | dns解析耗时       |      |
   | `probe_duration_seconds`         | 探测耗时          |      |
   | `probe_http_status_code `        | 解析状态码        | 200  |
   | `probe_success `                 | 探测是否成功1成功 |      |