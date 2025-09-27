---
title: "ELK"
linkTitle: "ELK stack"
date: 2025-06-12
simple_list: true
weight: 2
url: Observability/logs
type: docs
---

| 服务          | 建议节点数 | 依赖                 | 端口           |
| ------------- | ---------- | -------------------- | -------------- |
| zookeeper     | 3          | jdk                  | 2181/2888/3888 |
| kafka         | 3          | jdk                  | 9092           |
| elasticsearch | 3          | jdk                  | 9200/9300      |
| filebeat      |            | go语言开发，没有依赖 |                |
| logstash      |            | java                 | 9600           |
| kibana        |            | 无                   | 5601           |



```mermaid
graph LR
    subgraph Prod
        Pod1[node] -->|日志| FB1[Filebeat]
        Pod2[node] -->|日志| FB2[Filebeat]

    end

    subgraph Test
        Pod3[node] -->|日志| FB3[Filebeat]
        Pod4[node] -->|日志| FB4[Filebeat]

    end
    
    FB1 -->|topic: prod| Kafka
    FB2 -->|topic: prod| Kafka
    FB3 -->|topic: test| Kafka
    FB4 -->|topic: test| Kafka
    Kafka -->|topic: prod| Logstash
    Kafka -->|topic: test| Logstash

    Logstash -->|index| Elasticsearch

    Elasticsearch -->|Index-pattern| Kibana

```

