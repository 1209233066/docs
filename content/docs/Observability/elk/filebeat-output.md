---
date: '2025-06-12T15:22:40+08:00'
draft: false
title: 'output'
type: blog
toc_hide: false
hide_summary: true
weight: 4
description: >
  filebeat配置文件之output
tags: ["output","filebeat"]
categories: ["ELK"]
url: elk/output.html
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


### elasticsearch

```yaml
output.elasticsearch:
  hosts: ["192.168.0.161:9200"]
  indices:
    - index: "os-linux-warning-%{[agent.version]}-%{+yyyy.MM.dd}"
      when:
        contains:
          message: "WARN"
    - index: "os-linux-error-%{[agent.version]}-%{+yyyy.MM.dd}"
      when:
        contains:
          message: "ERR"
    - index: "os-linux-info-%{[agent.version]}-%{+yyyy.MM.dd}"
      when:
        contains:
          message: "INFO"
      # 默认索引
    - index: "os-linux-%{[agent.version]}-%{+yyyy.MM.dd}"

  # 启用ssl 和密码认证后的语法
  #protocol: "https"
  #username: "kibanauser"
  #password: "kibana"
  #ssl.verification_mode: none
  
# 禁用索引生命周期管理，默认为true。在启用 setup.ilm.enabled 状态下setup.template 配置不会生效
# https://www.elastic.co/guide/en/beats/filebeat/7.17/configuration-template.html
setup.ilm.enabled: false
# 加载索引模版，默认为true
setup.template.enabled: true
# 设置索引模板的名称，默认值为 filebeat-%{[agent.version]}
setup.template.name: "os-linux"

# 设置索引模板的匹配模式,默认值为 filebeat-%{[agent.version]}-*
setup.template.pattern: "os-linux-*"
# 覆盖已有的索引模板，默认值为false
setup.template.overwrite: true

# 配置索引模板属性
setup.template.settings:
  # 设置索引分片数量
  index.number_of_shards: 3
  # 设置索引副本数量，要求小于集群的数量
  index.number_of_replicas: 0
```





### Redis



### Kafka

{{< tabpane text=true right=false >}}
  {{% tab header="**输出到到kafka**:" disabled=true /%}}
  {{% tab header="格式样例一：" lang="en" %}}

  




```yaml
output.kafka:
  hosts: ["kafka1:9092","kafka2:9092","kafka3:9092"]
  topic: "logs-%{[agent.version]}"
  topics:
  - topic: "critical-%{[agent.version]}"
    when.contains:
      message: "CRITICAL"
  - topic: "error-%{[agent.version]}"
    when.contains:
      message: "ERR"
```

  {{% /tab %}}
  {{% tab header="格式样例二：" lang="en" %}}



```yaml
output.kafka:
  hosts: ["kafka1:9092","kafka2:9092","kafka3:9092"]
  topic: '%{[fields.log_topic]}'
  partition.round_robin"
    reachable_only: false
  required_acks: 1
  compression: gzip
  # 1MB
  max_message_bytes: 1000000
```



  {{% /tab %}}
{{< /tabpane >}}

