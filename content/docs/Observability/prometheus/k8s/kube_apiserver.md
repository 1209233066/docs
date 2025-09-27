---
title: "kube-apiserver"
linkTitle: "kube-apiserver"
date: 2025-05-14
toc_hide: false
hide_summary: true
weight: 201
description: >
  exporter|prometheus

tags: ["prometheus","exporter","kubernetes"]
categories: ["prometheus","监控","exporter"]
url: prometheus/kubernetes/kube-apiserver.html
---

1. 部署安装

2. 添加prometheus配置

   

   ```yaml
     - job_name: kube-apiserver
       honor_timestamps: true
       scrape_interval: 1m
       scrape_timeout: 1m
       metrics_path: /metrics
       scheme: https
       tls_config:
         ca_file: /etc/kubernetes/pki/ca.crt
         cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
         key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
         insecure_skip_verify: false
       follow_redirects: true
       enable_http2: true
       static_configs:
       - targets:
         - 192.168.0.244:6443
   ```

   

3. 常用指标

   >```bash
   >curl \
   >--cacert /etc/kubernetes/ssl/ca.crt \
   >--cert /etc/kubernetes/ssl/apiserver-kubelet-client.crt \
   >--key /etc/kubernetes/ssl/apiserver-kubelet-client.key \
   >https://10.4.7.12:6443/metrics
   >```

   

   + apiserver 进程是否正常

     ```
     up{job="kube-apiserver"}
     ```
   
   + 每秒QPS
   
   + API调用延时
   
   + ETCD调用延时

| 指标名                                              | 含义                                     | 类型    |
| --------------------------------------------------- | ---------------------------------------- | ------- |
| apiserver_request_total                             | 请求总数                                 | counter |
| apiserver_audit_event_total                         | 包含所有暴露的审计事件数量的指标。       | counter |
| apiserver_audit_error_total                         | 在暴露时由于发生错误而被丢弃的事件的数量 | counter |
| apiserver_request_duration_seconds_sum              | 请求耗时                                 | gauge   |
| apiserver_request_duration_seconds_count            |                                          |         |
| authentication_attempts                             |                                          |         |
| apiserver_tls_handshake_errors_total                |                                          |         |
| apiserver_client_certificate_expiration_seconds_sum |                                          |         |





[kube-apiserver组件监控介绍和常见异常指标_容器服务Kubernetes版(ACK)-阿里云帮助中心 (aliyun.com)](https://help.aliyun.com/zh/ack/ack-managed-and-ack-dedicated/user-guide/monitor-kube-apiserver)