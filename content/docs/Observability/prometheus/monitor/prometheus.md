---
title: "prometheus"
linkTitle: "prometheus"
date: 2025-05-12
simple_list: true
weight: 101
tags: ["prometheus","exporter"]
categories: ["prometheus","exporter"]
url: prometheus/monitor/prometheus.html
---

1. 部署安装

   参见部署[prometheus](zh-cn/安装promethues)

2. 添加prometheus配置
   
   ```yaml
   global:
     external_labels:
     prometheus: prom-xxx
   scrape_configs:
   - job_name: prometheus
     scrape_interval: 5s
     static_configs:
     - targets:
       - "localhost:9090"
   ```
   
3. 常用指标
   
      
   
      | 指标                                                         | 释义                                         | 指标类型 |
      | ------------------------------------------------------------ | -------------------------------------------- | -------- |
      | `prometheus_config_last_reload_successful`                   | 最后重启是否成功 1 表示成功 0表示失败        |          |
      | `ceil(time()-prometheus_config_last_reload_success_timestamp_seconds)` | 最后成功重启的距离现在过去了多少秒           |          |
      | `prometheus_notifications_alertmanagers_discovered`          | 发现alertmanager并处于活跃状态               |          |
      | `delta(prometheus_notifications_dropped_total[1h])`          | 由于发生错误而导致发送到alert 失败的告警数量 |          |
      | `prometheus_notifications_sent_total`                        | 自最后一次启动发送了多少条告警通知           |          |
      | `prometheus_notifications_queue_capacity`                    | prometheus 处理告警队列的配额                |          |
      | `prometheus_notifications_queue_length`                      | 有多少条告警位于当前队列中                   |          |
      | `irate(process_cpu_seconds_total{ job="prometheus"}[15m])`   | cpu 使用时长                                 |          |
      | `process_open_fds{ job="prometheus"}`                        | 已打开文件描述符数量                         |          |
      | `prometheus_engine_query_duration_seconds`                   | prometheus 引擎查询响应时长                  | summary  |
      | `sum(rate(prometheus_tsdb_head_samples_appended_total[15m]))` | 指标采集率                                   |          |
      
      ```bash
      evaluation_intervalrule_group_iterations_missed_total
      ```
      
      
      
      空间预估
      
      ```bash
      # 预估磁盘大小
      # needed_disk_space = retention_time_seconds * ingested_samples_per_second * bytes_per_sample
      						86400（1天）		   *  10000/s  					 * 2byte
      ```
      
4. 告警

      1. 服务不可用 [严重]
      2. 查询响应高[警告]
      3. 存在告警发出失败[警告]

      