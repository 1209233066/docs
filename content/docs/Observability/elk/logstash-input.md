---
date: '2025-09-12T15:22:40+08:00'
draft: false
title: 'logstash-input'
linkTitle: 'logstash-input'
type: blog
toc_hide: false
hide_summary: true
weight: 9
description: >
  logstash之input配置
tags: ["linux","logstash"]
categories: ["ELK"]
url: elk/logstash/input.html
author: "wangendao"
---

{{% alert title="文档环境" color="" %}}

os 版本： `CentOS Linux release 7.9.2009 (Core)`

filebeat版本：`7.17.19`

logstash版本：`7.15.0`

elasticsearch版本： `7.15.0`

{{% /alert %}}

![](https://www.elastic.co/guide/en/logstash/7.15/static/images/basic_logstash_pipeline.png)

### INPUT 配置

**[redis](https://www.elastic.co/guide/en/logstash/7.15/plugins-inputs-redis.html#plugins-inputs-redis-key)**

+ **data_type**[必选参数，数据类型为字符串] 可选值 `list` `channel` `pattern_channel`

+ **key**[必选参数，数据类型为字符串] 日志记录在那个名字的list /channel中

+ **host**[必选参数]  redis绑定的服务ip

+ **port** redis绑定的服务端口，默认6379

+ **password** redis服务密码

+ **threads** [数据类型为整型]多线程消费redis数据，默认1

+ **tags**[所有类型intput都支持，数据类型为列表] 添加tag

  ```ruby
  tags => ["linux","dev"]
  ```

  

+ **add_field**[所有类型intput都支持，数据类型为hash]添加自定义字段

  ```ruby
  add_field => { 
      "env" => "pro" 
      "app" => "mobile"
      }
  ```

  

+ 示例

  ```bash
  cat >/data/elasticsearch/logstash/config/logstash.conf<<'EOF'
  input {
    redis {
      data_type => "list"
      key => "logstash:beat:logstash"
      host => "192.168.0.161"
      password => "mypass"
      threads => 4
      add_field => { 
        "env" => "pro" 
        "app" => "mobile"
      }
      tags => ["linux","dev"]
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

  

**[file](https://www.elastic.co/guide/en/logstash/7.15/plugins-inputs-file.html)** 

> 将日志读取位置记录在`sincedb` 文件中，当重启logstash 后仍然可以继续读取。示例中记录在
>
> `/data/elasticsearch/logstash/data/plugins/inputs/file/.sincedb_452905a167cf4509fd08acb964fdb20c`

+ **path**[必选参数，数据类型为数组] 

+ **start_position**[数据类型字符串] logstash从哪里开始读取日志，可选参数`begining` `end` 默认为`end`。如果需要从头读取数据请设置为 `begining`

  该参数只作用在logstash 首次启动，也就是不存在`sincedb` 文件时

  

+ **exclude**[数据类型为数组] 排除匹配的文件不跟踪

  ```ruby
  input {
      file {
          path => ["/var/log/*"]
          exclude => ["*.gz"]
          }
      }
  ```

+ **tags**[所有类型intput都支持，数据类型为列表] 添加tag

  ```ruby
  tags => ["linux","dev"]
  ```

  

+ **add_field**[所有类型intput都支持，数据类型为hash]添加自定义字段

  ```ruby
  add_field => { 
      "env" => "pro" 
      "app" => "mobile"
      }
  ```

  

+ 示例

  ```bash
  cat >/data/elasticsearch/logstash/config/logstash.conf<<'EOF'
  input {
      file {
          path => ["/var/log/messages"]
  		start_position => "beginning"
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

[exec](https://www.elastic.co/guide/en/logstash/7.15/plugins-inputs-exec.html) 周期调用系统命令，logstash收集命令输出

+ **command**[必选参数，数据类型为字符串]  要执行的命令

+ **interval** 执行命令的间隔，单位s

  ```ruby
  input {
    exec {
      command => "TERM=xterm /usr/bin/top -n 1 -b" 
      interval => 30
    }
  }
  ```

  

+ **schedule**按照crontab格式周期执行命令

  ```ruby
  input {
    exec {
      command => "TERM=xterm /usr/bin/top -n 1 -b" 
      schedule => "*/1 * * * *"
    }
  }
  ```

+ **tags**[所有类型intput都支持，数据类型为列表] 添加tag

  ```ruby
  tags => ["linux","dev"]
  ```

  

+ **add_field**[所有类型intput都支持，数据类型为hash]添加自定义字段

  ```ruby
  add_field => { 
      "env" => "pro" 
      "app" => "mobile"
      }
  ```

  

+ 示例

  ```bash
  cat >/data/elasticsearch/logstash/config/logstash.conf<<'EOF'
  input {
    exec {
      command => "TERM=xterm /usr/bin/top -n 1 -b" 
      interval => 30
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

  

[http](https://www.elastic.co/guide/en/logstash/7.15/plugins-inputs-http.html) 用户 可以传递纯文本、JSON 或任何格式化数据

+ **host** 默认0.0.0.0

+ **port** 默认8080

+ **threads** 线程数默认 1

+ **user/password** 开启用户名密码认证

  ```ruby
  cat >/data/elasticsearch/logstash/config/logstash.conf<<'EOF'
  input {
    http {
  	host => "0.0.0.0"
  	port => "8080"
  	threads => 4
      user => "log"
  	password => "Q!123"
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

  ```bash
  curl -u 'log:Q!123'  -X POST --data '{"a":"123"}' 192.168.0.115:8080
  ```

  

[kafka](https://www.elastic.co/guide/en/logstash/7.15/plugins-inputs-kafka.html) 从kafka消费信息



+ **topics**[数据类型数组] 默认值 `["logstash"]`

+ **topics_pattern**[数据类型字符串] 正则模式匹配

+ **consumer_threads** 默认值 `1`

  

+ 示例

  ```ruby
  cat >/data/elasticsearch/logstash/config/logstash.conf<<'EOF'
  input {
    kafka {
      bootstrap_servers => "192.168.0.161:9092"   # Kafka 集群地址，多个用逗号分隔
      topics            => ["app-log"]            # 消费的 topic
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

  
