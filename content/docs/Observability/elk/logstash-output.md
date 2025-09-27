---
date: '2025-09-12T15:22:40+08:00'
draft: false
title: 'logstash-output'
linkTitle: 'logstash-output'
type: blog
toc_hide: false
hide_summary: true
weight: 10
description: >
  logstash之output配置
tags: ["linux","logstash"]
categories: ["ELK"]
url: elk/logstash/output.html
author: "wangendao"
---

{{% alert title="文档环境" color="" %}}

os 版本： `CentOS Linux release 7.9.2009 (Core)`

filebeat版本：`7.17.19`

logstash版本：`7.15.0`

elasticsearch版本： `7.15.0`

{{% /alert %}}

![](https://www.elastic.co/guide/en/logstash/7.15/static/images/basic_logstash_pipeline.png)

### OUTPUT配置



**[elasticsearch](https://www.elastic.co/guide/en/logstash/7.15/plugins-outputs-elasticsearch.html)**

+ hosts[非必须，数据类型数组] 默认值`http://127.0.0.1:9200`

+ index[非必须] 默认值 `logstash-%{+YYYY.MM.dd}`

+ user

+ password

+ 示例：

  ```ruby
  cat >/data/elasticsearch/logstash/config/logstash.conf<<'EOF'
  input {
    kafka {
      bootstrap_servers => "192.168.0.161:9092"   # Kafka 集群地址，多个用逗号分隔
      topics            => ["app-log","sys-log"]  # 消费的 topic
      group_id          => "logstash-consumer"    # 消费者组 ID
      auto_offset_reset => "earliest"             # 从头开始（第一次无 offset 时）
      codec             => "json"                 # 消息体是 JSON 就加，纯文本可删
      decorate_events   => true                   # 给事件加 @metadata[kafka] 字段（topic/partition/offset）
    }
  }
  output {
    elasticsearch {
      hosts => ["http://192.168.0.114:9200"]
      index => "logstash-%{+YYYY.MM.dd}"
      #user => "elastic"
      #password => "changeme"
    }
  }
  EOF
  
  ```

  

  将不同日志分流到不同的index

  > 都有哪些@metadata 元数据

  ```ruby
  cat >/data/elasticsearch/logstash/config/logstash.conf<<'EOF'
  input {
    kafka {
      bootstrap_servers => "192.168.0.161:9092"   # Kafka 集群地址，多个用逗号分隔
      topics            => ["app-log","sys-log"]  # 消费的 topic
      group_id          => "logstash-consumer"    # 消费者组 ID
      auto_offset_reset => "earliest"             # 从头开始（第一次无 offset 时）
      codec             => "json"                 # 消息体是 JSON 就加，纯文本可删
      decorate_events   => true                   # 给事件加 @metadata[kafka] 字段（topic/partition/offset）
    }
  }
  output {
    if [@metadata][kafka][topic] == "app-log" {
      elasticsearch {
          hosts => ["http://192.168.0.114:9200"]
          index => "app-log-%{+YYYY.MM.dd}"
      }
    }
    if [@metadata][kafka][topic] == "sys-log" {
      elasticsearch {
          hosts => ["http://192.168.0.114:9200"]
          index => "sys-log-%{+YYYY.MM.dd}"
      }
    }
  }
  EOF
  ```

+ template

  创建index模版，`sys-log-*`和 `app-log-*` 索引将关联该模版

  ```bash
  # 如果 ES 7.x 也可用老接口 _template，这里用新版 _index_template
  curl -X PUT localhost:9200/_index_template/host-logs-template \
       -H 'Content-Type: application/json' \
       -d '{
    "template": {
      "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 0,
        "refresh_interval": "5s"
      }
    },
    "index_patterns": [
      "sys-log-*",
      "app-log-*"
    ]
  }'
  ```

  

  ```bash
  cat >/data/elasticsearch/logstash/config/logstash.conf<<'EOF'
  input {
    kafka {
      bootstrap_servers => "192.168.0.161:9092"   # Kafka 集群地址，多个用逗号分隔
      topics            => ["app-log","sys-log"]  # 消费的 topic
      group_id          => "logstash-consumer"    # 消费者组 ID
      auto_offset_reset => "earliest"             # 从头开始（第一次无 offset 时）
      codec             => "json"                 # 消息体是 JSON 就加，纯文本可删
      decorate_events   => true                   # 给事件加 @metadata[kafka] 字段（topic/partition/offset）
    }
  }
  output {
    if [@metadata][kafka][topic] == "app-log" {
      elasticsearch {
          hosts => ["http://192.168.0.114:9200"]
          index => "app-log-%{+YYYY.MM.dd}"
      }
    }
    if [@metadata][kafka][topic] == "sys-log" {
      elasticsearch {
          hosts => ["http://192.168.0.114:9200"]
          index => "sys-log-%{+YYYY.MM.dd}"
      }
    }
  }
  EOF
  ```

  
