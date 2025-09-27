---
date: '2025-09-12T15:22:40+08:00'
draft: false
title: 'logstash'
linkTitle: 'logstash'
type: blog
toc_hide: false
hide_summary: true
weight: 8
description: >
  使用filebeat收集linux操作系统日志
tags: ["linux","filebeat"]
categories: ["ELK"]
url: elk/example/logstash.html
author: "wangendao"
---

{{% alert title="文档环境" color="" %}}

os 版本： `CentOS Linux release 7.9.2009 (Core)`

filebeat版本：`7.17.19`

logstash版本：`7.15.0`

elasticsearch版本： `7.15.0`

{{% /alert %}}





Logstash 使用jruby 语言开发，软件运行依赖jdk[兼容矩阵](https://www.elastic.co/support/matrix#matrix_jvm)，如果无法确认该使用什么版本可以下载带有jdk环境的logstash安装包。

![](https://www.elastic.co/guide/en/logstash/7.15/static/images/basic_logstash_pipeline.png)

*安装java（非必须）*

```bash
wget https://download.java.net/java/ga/jdk11/openjdk-11_linux-x64_bin.tar.gz
tar xf openjdk-11_linux-x64_bin.tar.gz -C /opt
ln -svf  /opt/{jdk-11,jdk}

cat>>/etc/profile<<'EOF'
export JAVA_HOME=/opt/jdk
export JAVA_JRE=$JAVA_HOME/jre
export CLASSPATH=$JAVA_HOME/lib:$JAVA_HOME/jre/lib
export PATH=$JAVA_HOME/bin:$JAVA_JRE/bin:$PATH:.
EOF

source /etc/profile
java -version
```



*安装logstash*

```bash
version=7.15.0
wget https://mirrors.huaweicloud.com/logstash/${version}/logstash-${version}-linux-x86_64.tar.gz

tar xf logstash-${version}-linux-x86_64.tar.gz -C /data/elasticsearch
ln  -svf /data/elasticsearch/logstash-${version}  /data/elasticsearch/logstash
```

> 测试运行
>
> ```bash
> /data/elasticsearch/logstash/bin/logstash -e 'input { stdin {} } output { stdout { codec=>rubydebug }}'
> ```



```bash
cat >/data/elasticsearch/logstash/config/logstash.conf<<'EOF'
# Sample Logstash configuration for creating a simple
# Beats -> Logstash -> Elasticsearch pipeline.

input {
  beats {
    port => 5044
  }
}

output {
  elasticsearch {
    hosts => ["http://192.168.0.114:9200"]
    index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
    #user => "elastic"
    #password => "changeme"
  }
}
EOF
```



```bash
tee /etc/systemd/system/logstash.service <<'EOF'
[Unit]
Description= logstash serveice
After=network.target
 
[Service]
WorkingDirectory=/data/elasticsearch/logstash

ExecStart=/data/elasticsearch/logstash/bin/logstash \
          -f /data/elasticsearch/logstash/config/logstash.conf \
          --config.reload.automatic

User=root
LimitNOFILE=65535
[Install]
WantedBy=multi-user.target
EOF
```



```bash
systemctl daemon-reload 
systemctl enable logstash --now
systemctl status logstash
```

### input

+ 

### filter

+ **grok** 日志解析

  ```bash
  input {
      beats {
          port => "5044"
      }
  }
  filter {
      grok {
          match => { "message" => "%{COMBINEDAPACHELOG}"}
      }
  }
  output {
      stdout { codec => rubydebug }
  }
  ```

  

+ **geoip** 通过ip定位地址

  ```bash
  input {
      beats {
          port => "5044"
      }
  }
   filter {
      grok {
          match => { "message" => "%{COMBINEDAPACHELOG}"}
      }
      geoip {
          source => "clientip"
      }
  }
  output {
      stdout { codec => rubydebug }
  }
  ```

  

### output

+ **elasticsearch**

  ```bash
  output {
      elasticsearch {
          hosts => ["IP Address 1:port1", "IP Address 2:port2", "IP Address 3"]
      }
  }
  ```

  

+ **file**

  ```bash
  file {
      path => "/path/to/target/file"
  }
  ```

  
