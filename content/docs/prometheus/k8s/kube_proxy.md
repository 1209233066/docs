---
title: "kube-proxy"
linkTitle: "kube-proxy"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 204
description: >
  exporter|prometheus

tags: ["prometheus","exporter","kubernetes"]
categories: ["prometheus","监控","exporter"]
url: prometheus/kubernetes/kube-proxy.html
---

kube-proxy 监听在   http://127.0.0.1:10249/metrics 

scheduler 监听在 https://127.0.0.1:10259/metrics

controller-manager监听在 https://127.0.0.1:10257/metrics

coredns http://172.168.0.10:9153/metric

收集k8s事件到mongodb  [GitHub - AliyunContainerService/kube-eventer: kube-eventer emit kubernetes events to sinks](https://github.com/AliyunContainerService/kube-eventer)

```bash
我来解释如何在 Kubernetes 中持久化事件（Events）。
Kubernetes 事件默认只保留1小时，如果要持久化存储事件，有以下几种主要方案：
使用 Event Exporter
这是一个比较常用的方案，可以将 k8s 事件导出到外部存储系统。例如使用官方的 event-exporter：
使用 Event Logger
apiVersion: apps/v1
kind: Deployment
metadata:
  name: event-exporter
  namespace: monitoring
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: event-exporter
        image: gcr.io/google-containers/event-exporter:v0.3.1
        command:
        - /event-exporter
        - --sink-opts=elasticsearch?hosts=http://elasticsearch:9200
可以部署一个自定义的 event logger，监听集群事件并写入到持久化存储中：
修改 kube-apiserver 配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: event-logger
spec:
  template:
    spec:
      containers:
      - name: event-logger
        image: k8s-event-logger
        env:
        - name: STORAGE_TYPE
          value: "elasticsearch"
        - name: ES_HOST
          value: "elasticsearch-service:9200"
可以通过修改 kube-apiserver 的配置来延长事件保留时间：
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
spec:
  containers:
  - command:
    - kube-apiserver
    - --event-ttl=168h # 保留7天
常见的事件持久化存储后端包括：
Elasticsearch
InfluxDB
MongoDB
MySQL/PostgreSQL
建议：
根据实际需求选择合适的存储后端
注意设置合理的数据保留策略，避免存储空间耗尽
考虑事件过滤，只存储重要事件
建立监控告警，及时发现异常事件
如果你需要具体某个存储方案的详细配置，我可以为你展开说明。
```

