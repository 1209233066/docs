---
title: "consul_sd_configs"
linkTitle: "consul_sd_configs"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 5
description: >
  kconsul_sd_configs|prometheus

tags: ["prometheus","配置","consul_sd_configs"]
categories: ["prometheus","监控"]
url: prometheus/consul-sd-configs.html
---



[<span id='consul_sd_configs'>**consul_sd_configs**</span>](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#consul_sd_config)

```bash
# 启动一个单实例的[consul](https://www.consul.io/downloads)
consul agent -bootstrap \
--client=0.0.0.0  \
-config-dir=/etc/conf.d \
-data-dir=/consul/data/ \
-dev \
-enable-local-script-checks  \
-ui
# 在consul 中注册服务
vi /etc/conf.d/node.json
{
    "services": [
        {
            "id": "node_exporter-node01",
            "name": "node01",
            "address": "10.4.7.11",
            "port": 9100,
            "tags": ["nodes"],
            "checks": [{
                "http": "http://10.4.7.11:9100/metrics",
                "interval": "5s"
            }]
        },
        {
            "id": "node_exporter-node02",
            "name": "node02",
            "address": "10.4.7.12",
            "port": 9100,
            "tags": ["nodes"],
            "checks": [{
                "http": "http://10.4.7.12:9100/metrics",
                "interval": "5s"
            }]
        }
    ]
}
# 加载配置文件/etc/conf.d/node.json
consul reload
scrape_configs:
- job_name: "node"
  consul_sd_configs:
  - server: "47.113.100.31:8500"
    tags:
    - "nodes"
    refresh_interval: 2m
```



```bash
# 通过测试命令测试服务的注册发现
consul services register -id="node_exporter-node02"
consul services deregister -id="node_exporter-node02"
```

