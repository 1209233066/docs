---
title: "config"
linkTitle: "config"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 3
description: >
  promethes.yaml|prometheus

tags: ["prometheus","配置"]
categories: ["prometheus","监控"]
url: prometheus/config.html
---

配置文件全景图

 ```mermaid
   graph LR
   A>prometheus.yml] ==> |全局配置|B(<a href=#global>global</a>)
   A ==> |对接alert|C(<a href='#alterings'>alterings</a>)
   A ==> |评估/告警规则|D(<a href='#rule_files'>rule_files</a>)
   A ==> |指标抓取|E(<a href='#scrape_configs'>scrape_configs</a>)
   E --> |静态配置|E1(<a href=#static_configs>static_configs</a>)
   E --> |文件自动发现|E2(<a href=#file_sd_configs>file_sd_configs</a>)
   E --> |consul自动发现|E3(<a href=#consul_sd_configs>consul_sd_configs</a>)
   E --> |kubernetes自动发现|E4(<a href='#kubernetes_sd_configs'>kubernetes_sd_configs</a>)
   E --> |dns自动发现|E5(<a href='#dns_sd_configs'>dns_sd_configs</a>)
   E --> |基于单个job重新打标,在指标采集之前完成|E6(<a href='#relabel_configs'>relabel_configs</a>)
   E --> |基于单个metrics重新打标,在指标采集之后数据存储之前完成|E7(metric_relabel_configs)
   E --> |发送给alertmanger时重新打标|E8(alert_relabel_configs)
   E --> |远程写入样本时重新打标|E9(write_relabel_configs)
   A ==> |外部存储|F(remote_write/remote_read)
 ```


### <span id='global'>**global**</span>


```yaml
global:
# 1m 抓取一次target
  scrape_interval: 1m
# 10s 抓取不到超时
  scrape_timeout: 20s
# 1m 评估一次rules
  evaluation_interval: 1m
# 全局标签(在每一个时间序列上添加zoon=shanghai 的标签)
  external_labels:
    center: "shanghai"
    env: "staging"
# 记录promql 的查询记录
  query_log_file: "/data/prometheus/log/promql"
```

### <span id='alterings'>**alterings**</span>

```yaml
alerting:
  alertmanagers:
  - path_prefix: /
    static_configs:
    - timeout: 30s
      targets: # 通常情况 这三个节点是一个集群
      - 'alert1:9093'
      - 'alert2:9093'
      - 'alert3:9093'
     
```

### <span id='rule_files'>**rule_files**</span>

在`prometheus.yml`主配置文件加载 `record 规则` 和 `alert规则`

```yaml
rule_files:
# 相对于主配置文件
- "./rules/*.yaml"
```



- [x] 记录规则

  语法

  ```yaml
  ---
  groups:
    - name: example
      interval: 30s         # 规则评估周期, 省略时使用全局配置
      limit: 0            # 对时间序列的限制，0表示不做限制
      query_offset: 0       # 评估时的时间偏移量
      labels:             # 添加或修改标签
        -  <labelname>: <labelvalue> 
      rules:
      - record: code:prometheus_http_requests_total:sum
        expr: sum by (code) (prometheus_http_requests_total)
        labels:             # 添加或修改标签
          -  <labelname>: <labelvalue> 
  ```

  示例

  ```yaml
  #./rules/record.yaml
  groups:
  - name: node_cpu
    rules:
      # 命名规范 https://prometheus.io/docs/practices/rules/#recording-rules
    - record: instance:node_cpu_seconds:avg_rate5m  # record: level:metric:operation
      expr: avg by (job,instance,mode) (rate(node_cpu_seconds_total[5m]))
      
    - record: instance:node_cpu_seconds:avg_rate5m
      expr: avg by (job,instance,mode) (rate(node_cpu_seconds_total[5m]))
      labels:
        metric_type: "aggration"
  ```

  ```bash
  /data/prometheus/bin/promtool check rules  ./rules/record.yaml 
  ```

- [x] 告警规则

  语法：相比record 规则，labels 支持**字符串模版**

  ```yaml
  ---
  groups:
    - name: example
      interval: 30s         # 规则评估周期, 省略时使用全局配置
      limit: 0            # 对时间序列的限制，0表示不做限制
      query_offset: 0       # 评估时的时间偏移量
      labels:             # 添加或修改标签
        -  <labelname>: <labelvalue> 
      rules:
      - alert: nodeCpuHight
        expr: 100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance)) >
        for: 2m           # 达到expr 条件并持续2m,则告警从pending 转为firing
        keep_firing_for: 0s   # 不满足expr 条件后，告警继续保持的时长
        labels:           # 添加或修改标签
          - <labelname>: <tmpl_string>
        annotations:
          - <labelname>: <tmpl_string> 
  ```

  示例

  ```yaml
  #./rules/alert.yaml
  groups:
  - name: node_cpu
    rules:
    - alert: nodeCpuHigh
      expr: 100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance)) >85
      for: 5m
      labels:
        severity: WARNING
      annotations:
        summary: "主机【Instance {{ $labels.instance }}】cpu 使用率高"
        description: {{$labels.instance}} of job {{ $labels.job }} cpu 使用率超过85%,当前值{{ $value |printf "%.1f"}}%
  ```

### <span id='scrape_configs'>scrape_configs</span>


> [**static_configs**](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#static_config)|[<span id='file_sd_configs'>**file_sd_configs**</span>](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#file_sd_config)|[<span id='consul_sd_configs'>**consul_sd_configs**</span>](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#consul_sd_config)|[<span id='kubernetes_sd_configs'>**kubernetes_sd_configs**</span>](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config)

{{< tabpane text=true right=true >}}
  {{% tab header="**抓取方法**:" disabled=true /%}}
  {{% tab header="<span id='static_configs'>**static_configs**</span>" lang="en" %}}

  ```yaml
scrape_congfigs:
  - job_name: prometheus
    scrape_interval: 5m
    scrape_timeout: 10s
    metrics_path: /metrics
    scheme: http
    static_configs:
    - targets: ['localhost:8080','localhost:8081']
      labels:
        env: 'production'

  - job_name: 'node'
    static_configs:
    - targets:
      - localhost:9100
    # 只收集指定的指标
    params:
      collect[]:
      - cpu
      - meminfo
      - diskstats
      - netdev
      - filefd
      - filesystem
      - xfs
      - systemd
# curl -g -X GET http://127.0.0.1:9100/metrcs?collect[]=cpu
  ```

  {{% /tab %}}

  {{% tab header="<span id='file_sd_configs'>**file_sd_configs**</span>" lang="en" %}}

  ```yaml
scrape_congfigs:
  - job_name: prometheus
    scrape_interval: 5m
    scrape_timeout: 10s
    metrics_path: /metrics
    scheme: http
    file_sd_configs:
      - files:
        - file/*.yml
        refresh_interval: 5m
        
#cat file/file_sd.yaml 

- targets:
  - 172.29.1.11:9090
    labels:
      app: prometheus
      job: primetheus
  ```

  {{% /tab %}}

  {{% tab header="<span id='consul_sd_configs'>**consul_sd_configs**</span>" lang="en" %}}

  ```yaml
scrape_configs:
  - job_name: "node"
    consul_sd_configs:
    - server: "47.113.100.31:8500"
      tags:
      - "nodes"
      refresh_interval: 2m
  ```

  {{% /tab %}}


  {{% tab header="<span id='kubernetes_sd_configs'>**kubernetes_sd_configs**</span>" lang="en" %}}

  ```yaml
scrape_configs:
- job_name: kube-apiserver
  scheme: https
  kubernetes_sd_configs:
    - api_server: https://127.0.0.1:6443
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.pem
        cert_file: /etc/kubernetes/pki/cert.pem
        key_file: /etc/kubernetes/pki/cert.key
        insecure_skip_verify: true
      role: endpoints   # 如果prometheus部署在集群中，则使用endpoints,如果部署在集群外，则使用service或node
  relabel_configs:
    - source_labels:
        [
          __meta_kubernetes_namespace,
          __meta_kubernetes_service_name,
          __meta_kubernetes_endpoint_port_name,
        ]
      action: keep
      regex: default;kubernetes;https
  ```

  {{% /tab %}}

  {{% tab header="<span id='dns_sd_configs'>**dns_sd_configs**</span>" lang="en" %}}

  ```yaml
  依赖于A AAAA 或SRV 记录
  ```

  {{% /tab %}}

{{< /tabpane >}}


### <span id='relabel_configs'>**relabel_configs**</span>

> [relabel_configs](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config) 用于在指标抓取前对标签进行预处理。应用场景包括丢弃指定指标、替换抓取指标的端口、新增或修改label。



语法：

```yaml
scrape_congfigs:
- relabel_configs:
  - source_labels: [' <labelname> [, ...] ']      	# 定义预处理的标签列表
    separator: <string> | default = ;       		# 定义source_labels 中的标签以哪个字符串作为分隔符
    regex: <regex> | default = (.*)         		# 对source_labels中的标签按照指定正则表达式匹配
    action: <relabel_action> | default = replace  	# 正则匹配到的部分进行处理动作
    target_label: <labelname>           			# 指明匹配到的标签计划被哪标签替换。对于replace来说标签是必须的 
    replacement: <string> | default = $1      		# relace中定义替换后 **值** 应该替换为什么，支持正则向后引用
```



**source_labels 和 target_label**

>  可以利用指标标签以及prometheus、consul、kubernetes等特有标签作为 `source_labels` 和 `target_labels` 

例如prometheus 可以识别的标签:

| 标签名                | 标签值                          |
| --------------------- | ------------------------------- |
| `__scheme__`          | http 或 https                   |
| `__address__`         | ip:port  instance标签会使用该值 |
| `__metrics_path__`    | 默认为 /metrics                 |
| `__param__`           | url 中传递过来的参数            |
| `__scrape_interval__` | 抓取周期                        |
| `__name__`            | 指标名称                        |
| `__tmp                | 在打标阶段需要存储临时标签      |



**action**

> 动作包括：replace、lowercase、uppercase、keep、drop、keepequal、dropequal、hashmod、labelmap、labeldrop、labelkeep


**示例**
{{< tabpane text=true right=true >}}
  {{% tab header="**action**:" disabled=true /%}}
  {{% tab header="<span id='static_configs'>**新增标签**</span>" lang="yaml" %}}

  ```yaml
scrape_congfigs:
- relabel_configs:  # 添加固定标签,给当前job添加一个env="pro"
    - replacement: pro
      target_label: env
  ```

  {{% /tab %}}

  {{% tab header="<span id='file_sd_configs'>**replace**</span>" lang="en" %}}

  ```yaml
scrape_congfigs:
- relabel_configs:
    - source_labels: ["__address__"]
      separator: ";"
      regex: "(^[0-9].*):[0-9]+"
      action: replace
      replacement: "$1"   # 新的标签值
      target_label: "IP"  # 新的标签名称
  ```

  {{% /tab %}}

  {{% tab header="<span id='consul_sd_configs'>**drop**</span>" lang="en" %}}

  ```yaml
scrape_congfigs:
- relabel_configs:
    - source_labels: ["__name__"]
      separator: ";"
      regex: "go_gc_duration_seconds"
      action: drop  # 删除匹配的metrics
  ```

  {{% /tab %}}


  {{% tab header="<span id='kubernetes_sd_configs'>**keep**</span>" lang="en" %}}

  ```yaml
scrape_congfigs:  
- relabel_configs:
    - source_labels: ["__name__"]
      separator: ";"
      regex: "^(node|pod|kube|mysql|redis|mongo)"
      action: keep  # 保存匹配的metrics
  ```

  {{% /tab %}}

  {{% tab header="<span id='dns_sd_configs'>**labeldrop**</span>" lang="en" %}}

  ```yaml
scrape_congfigs:
- relabel_configs:
    - regex: "job"
      action: labeldrop # 删除了job 标签
  ```

  {{% /tab %}}

  {{% tab header="<span id='dns_sd_configs'>**labelkeep**</span>" lang="en" %}}

  ```yaml
scrape_congfigs:
- relabel_configs:
    - regex: ".*"
      action: labelkeep
  ```

  {{% /tab %}}
{{< /tabpane >}}


