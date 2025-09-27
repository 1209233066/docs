---
date: '2025-09-10T15:22:40+08:00'
draft: false
title: 'kibana'
linkTitle: 'kibana'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  安装使用kibana
tags: ["kibana"]
categories: ["elk"]
url: elk/kibana.html
author: "wangendao"
---





{{% alert title="" color="" %}}
文档适用于操作系统centos7.x  和 elasticsearch `7.15.2 ` 、`8.8.1`。
在elasticsearch 8.8.1版本中已经开启了用户认证，需要创建用户给kibana 并授予权限：

```bash
# 创建用户
./elasticsearch-8.8.1/bin/elasticsearch-users useradd kibanauser
# 把 superuser,kibana_system,kibana_user 角色授权给kubanauser
./elasticsearch-8.8.1/bin/elasticsearch-users roles -a superuser,kibana_system,kibana_user kibanauser
```

{{% /alert %}}

### 安装部署

1. 下载安装包

   ```bash
   version=7.15.2
   #wget https://repo.huaweicloud.com/kibana/${version}/kibana-${version}-linux-x86_64.tar.gz
   wget https://artifacts.elastic.co/downloads/kibana/kibana-${version}-linux-x86_64.tar.gz
   
   tar xf kibana-${version}-linux-x86_64.tar.gz -C /data/elasticsearch/
   ln -svf /data/elasticsearch/{kibana-${version}-linux-x86_64,kibana}
   ```

   

2. 修改配置文件

   ```bash
   tee /data/elasticsearch/kibana/config/kibana.yml <<EOF
   server.port: 5601
   server.host: "192.168.0.161"
   elasticsearch.hosts: ["https://192.168.0.161:9200"]
   elasticsearch.username: "kibanauser"
   elasticsearch.password: "kibana"
   # 取消自签证书的ca 验证
   elasticsearch.ssl.verificationMode: "none"
   #i18n.locale: "en"
   i18n.locale: "zh-CN"
   EOF
   ```

   ```bash
   chown -R elasticsearch:elasticsearch /data/elasticsearch/kibana*
   ```

   

3. 创建systemd启动文件

   ```bash
   tee /etc/systemd/system/kibana.service <<EOF
   [Unit]
   Description= kibana serveice
   After=network.target
    
   [Service]
   WorkingDirectory=/data/elasticsearch/kibana
   
   ExecStart=/data/elasticsearch/kibana/bin/kibana
   User=elasticsearch
   LimitNOFILE=65535
   [Install]
   WantedBy=multi-user.target
   EOF
   ```

   ```bash
   systemctl daemon-reload
   systemctl enable kibana --now
   systemctl status  kibana
   ```
   
   检查kibana状态
   
   ```bash
   http://127.0.0.1:5601/status
   ```
   





