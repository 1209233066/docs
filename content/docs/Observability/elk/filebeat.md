---
date: '2025-06-12T15:22:40+08:00'
draft: false
title: 'filebeat'
linkTitle: 'filebeat'
type: blog
toc_hide: false
hide_summary: true
weight: 2
description: >
  filebeat安装部署，
tags: ["filebeat"]
categories: ["ELK"]
url: elk/filebeat.html
author: "wangendao"
---

{{% alert title="文档环境" color="" %}}

os 版本： `CentOS Linux release 7.9.2009 (Core)`

filebeat版本：`7.17.29`

elasticsearch版本： `7.15.0`

{{% /alert %}}



<table>
    <tr>
        <td><img src="https://www.elastic.co/docs/reference/beats/filebeat/images/filebeat.png" alt="架构"></td>
        <td>
            <a href="https://www.elastic.co/guide/en/beats/filebeat/7.17/index.html">文档</a><br>
        </td>
        <td>
            <a href="https://mirrors.huaweicloud.com/filebeat/">下载</a><br>
        </td>
        <td>
            <a href="https://www.docker.elastic.co">docker镜像</a>
        </td>
    </tr>
</table>








1. 下载安装包

   ```bash
   version=7.17.29
   wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${version}-linux-x86_64.tar.gz
   
   #wget https://repo.huaweicloud.com/filebeat/${version}/filebeat-${version}-linux-x86_64.tar.gz
   
   tar xf filebeat-${version}-linux-x86_64.tar.gz -C /data/elasticsearch
   ln  -svf /data/elasticsearch/filebeat-${version}-linux-x86_64  /data/elasticsearch/filebeat
   ```

2. 修改配置文件

   > 测试配置
   >
   > ```yaml
   > filebeat.inputs:
   > - type: stdin
   > output.console:
   >   pretty: true
   > ```

   
   
   ```bash
   cat >/data/elasticsearch/filebeat/filebeat.yml<<'EOF'
   filebeat.inputs:
     - type: log
       id: log
       paths:
         - /var/log/dmesg
         - /var/log/messages
         - /var/log/secure
         - /var/log/cron
         - /var/log/audit/audit.log
         - /var/log/yum.log
   
   output.elasticsearch:
     hosts: ["192.168.0.114:9200"]
     indices:
       - index: "warning-%{[agent.version]}-%{+yyyy.MM.dd}"
         when:
           contains:
             message: "WARN"
       - index: "error-%{[agent.version]}-%{+yyyy.MM.dd}"
         when:
           contains:
             message: "ERR"
       - index: "info-%{[agent.version]}-%{+yyyy.MM.dd}"
         when:
           contains:
             message: "INFO"
         # 默认索引
       - index: "default-%{[agent.version]}-%{+yyyy.MM.dd}"
   EOF
   ```
   
   
   
3. 创建systemd启动文件

   ```bash
   tee /etc/systemd/system/filebeat.service <<'EOF'
   [Unit]
   Description=Filebeat sends log files to Logstash or directly to Elasticsearch.
   Documentation=https://www.elastic.co/products/beats/filebeat
   Wants=network-online.target
   After=network-online.target
   
   [Service]
   Environment="BEAT_LOG_OPTS="
   Environment="BEAT_CONFIG_OPTS=-c /data/elasticsearch/filebeat/filebeat.yml"
   Environment="BEAT_PATH_OPTS=--path.home /data/elasticsearch/filebeat --path.config /data/elasticsearch/filebeat --path.data /data/elasticsearch/filebeat/data --path.logs /data/elasticsearch/filebeat/logs"
   ExecStart=/data/elasticsearch/filebeat/filebeat --environment systemd $BEAT_LOG_OPTS $BEAT_CONFIG_OPTS $BEAT_PATH_OPTS
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   
   EOF
   ```
   
   ```bash
   systemctl daemon-reload
   systemctl enable filebeat --now
   systemctl status filebeat
   ```
   
   

