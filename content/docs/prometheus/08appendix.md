---
title: "附录"
linkTitle: "附录"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 7
description: >
  附录|prometheus

tags: ["prometheus","附录",]
categories: ["prometheus","监控"]
url: prometheus/appendix.html
---
附录：

1. 检查配置语法 `promtool check config prometheus.yml`

2. 检查规则 `promtool check rules /path/to/example.rules.yml`

3. 调用接口执行查询

   > 查询接口`127.0.0.1:9090/api/v1/query` 支持post 和 get 方法

   {{< tabpane text=true right=true >}}
     {{% tab header="**查询**:" disabled=true /%}}
     {{% tab header="<span id='static_configs'>**查询瞬时向量**</span>" lang="en" %}}

   ```bash
   curl -s http://127.0.0.1:9090/api/v1/query?query=prometheus_build_info
   curl -X POST -d "query=prometheus_build_info"  http://127.0.0.1:9090/api/v1/query
   curl -X POST -d "query=prometheus_build_info"  http://127.0.0.1:9090/api/v1/query
   curl -s http://10.4.7.250:30090/api/v1/query?query=node_cpu|jq
   curl -s -g 'http://10.4.7.250:30090/api/v1/query?query=node_cpu{cpu="cpu0"}' |jq '.data.result[3].value'
   ```

   

     {{% /tab %}}

     {{% tab header="<span id='static_configs'>**查询范围向量**</span>" lang="en" %}}
   ```bash
  curl -s http://127.0.0.1:9090/api/v1/query_range?query=rate(prometheus_tsdb_head_samples_appended_total[5m])&start=1514764800&end=1514765700&step=60
   ```

     {{% /tab %}}

   


     {{% tab header="<span id='static_configs'>**查询告警/记录规则**</span>" lang="en" %}}
    
   ```bash
   curl -s http://127.0.0.1:9090/api/v1/rules|jq
   ```

     {{% /tab %}}
    
     {{% tab header="<span id='dns_sd_configs'>**查询活动的警报**</span>" lang="en" %}}
    
   ```bash
   curl -s http://127.0.0.1:9090/api/v1/alerts|jq
   ```

     {{% /tab %}}

   {{< /tabpane >}}


# FQA

问题描述：

1. 主机cpu配置了持续5分钟超过80%告警

   当前cpu使用率94% 并持续40分钟，告警没有正常发出来。同一个告警下又有主机能够正常告警出来。

   

问题排查：

1. 通过promQL 执行告警规则中的语句，确实达到了触发告警规则的基准。

2. 于是检查alertmanger,发现alertmanger并没有收到该告警。

3. 无意中重新执行第一步的查询发现了问题。<font color=red>【隐蔽问题：通过频繁查询发现有30%的概率查询不到符合告警规则的主机】</font>

4. Prometheus开启了远程写入和查询，开始怀疑是不是远程查询导致的查询失败。

   通过promQL 执行其他查询语句，未发现上述【隐蔽问题】

5. 尝试修改该告警规则中promQL 语句，意外发现上述隐蔽问题修复了。

   修改前

   ```bash
   label_replace(sum by(node) (rate(container_cpu_usage_seconds_total{id="/"}[2m])),"hostname", "$1", "node", "(.*)")
   / 
   label_replace(sum by(node) (machine_cpu_cores), "hostname", "$1", "node", "(.*)") * 100 > 80
   ```

   修改后

   ```bash
   label_replace(sum by(node) (rate(container_cpu_usage_seconds_total{id="/"}[5m])),"hostname", "$1", "node", "(.*)")
   / 
   label_replace(sum by(node) (machine_cpu_cores), "hostname", "$1", "node", "(.*)") * 100 > 80
   ```

   

   

总结：

在使用范围向量时，至少要跨越两个采集间隔