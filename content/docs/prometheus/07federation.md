---
title: "federation"
linkTitle: "federation"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 7
description: >
  federation|prometheus

tags: ["prometheus","federation",]
categories: ["prometheus","监控"]
url: prometheus/federation.html
---

安装部署

> federation 可以实现全局视图。主节点不仅可以提取聚合指标，还可以为Grafana等工具暴露指标或者作为可视化的默认数据源

{{< tabpane text=true right=true >}}
  {{% tab header="**联邦配置**:" disabled=true /%}}
  {{% tab header="<span id='static_configs'>**节点1**</span>" lang="en" %}}

  ```yaml
global:
  external_labels:
    worker: 0
rule_files:
- "rules/node_rules.yml"

scrape_configs:
- job_name: 'node'
  file_sd_configs:
  - files:
    - targets/nodes/*.json
    refresh_interval: 5m
  relabel_configs:
  - source_labels: [__address__]
    modulus: 3
    target_label: __tmp_hash
    action: hashmod
  - source_labels: [__tmp_hash]
    regex: ^0$
    action: keep
  ```

  {{% /tab %}}

  {{% tab header="<span id='static_configs'>**节点2**</span>" lang="en" %}}

  ```yaml
global:
  external_labels:
    worker: 1
rule_files:
- "rules/node_rules.yml"

scrape_configs:
- job_name: 'node'
  file_sd_configs:
  - files:
    - targets/nodes/*.json
    refresh_interval: 5m
  relabel_configs:
  - source_labels: [__address__]
    modulus: 3
    target_label: __tmp_hash
    action: hashmod
  - source_labels: [__tmp_hash]
    regex: ^1$
    action: keep
  ```

  {{% /tab %}}




  {{% tab header="<span id='static_configs'>**节点3**</span>" lang="en" %}}

  ```yaml
global:
  external_labels:
    worker: 1
rule_files:
- "rules/node_rules.yml"

scrape_configs:
- job_name: 'node'
  file_sd_configs:
  - files:
    - targets/nodes/*.json
    refresh_interval: 5m
  relabel_configs:
  - source_labels: [__address__]
    modulus: 3
    target_label: __tmp_hash
    action: hashmod
  - source_labels: [__tmp_hash]
    regex: ^2$
    action: keep
  ```

  {{% /tab %}}

  {{% tab header="<span id='dns_sd_configs'>**主节点**</span>" lang="en" %}}

  ```yaml
  scrape_configs:
    - job_name: 'federate'
      scrape_interval: 15s
  
      honor_labels: true
      metrics_path: '/federate'
  
      params:
        'match[]':
          - '{job="prometheus"}'
          - '{__name__=~"job:.*"}'
  
      static_configs:
        - targets:
          - 'source-prometheus-1:9090'
          - 'source-prometheus-2:9090'
          - 'source-prometheus-3:9090'
  ```

  {{% /tab %}}

{{< /tabpane >}}