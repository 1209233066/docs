---
title: "cadvisor"
linkTitle: "cadvisor"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 208
description: >
  exporter|prometheus

tags: ["prometheus","exporter","kubernetes"]
categories: ["prometheus","监控","exporter"]
url: prometheus/kubernetes/cadvisor.html
---

1. [部署安装](https://github.com/google/cadvisor) cadvisor提供容器资源cpu，内存、网络、文件系统等方面的信息，在k8s环境中通过daemonset 资源来部署相关资源

   ```bash
   VERSION=v0.36.0 # use the latest release version from https://github.com/google/cadvisor/releases
   sudo docker run \
     --volume=/:/rootfs:ro \
     --volume=/var/run:/var/run:ro \
     --volume=/sys:/sys:ro \
     --volume=/var/lib/docker/:/var/lib/docker:ro \
     --volume=/dev/disk/:/dev/disk:ro \
     --publish=8080:8080 \
     --detach=true \
     --name=cadvisor \
     --privileged \
     --device=/dev/kmsg \
     gcr.io/cadvisor/cadvisor:$VERSION
   ```

   

2. 添加prometheus配置

   ```bash
   - job_name: cadvisor
     static_configs:
     - targets:
       - 10.4.7.251:8080
   ```

   

3. 常用指标

   | 指标                                                         | 注释       |
   | ------------------------------------------------------------ | ---------- |
   | `rate(container_cpu_usage_seconds_total{name="cadvisor"}[1m])` | cup负载    |
   | `container_memory_usage_bytes{name="cadvisor"}`              | 内存使用率 |
   | `rate(container_network_transmit_bytes_total{name="cadvisor"}[1m])` | 网络发送   |
   | `rate(container_network_receive_bytes_total{name="cadvisor"}[1m])` | 网络接收   |






应用自身指标暴露

```
annotations:
  prometheus.io/port: "9153"
  prometheus.io/scrape: "true"
```

github 和招商银行内部使用了内嵌入的cadvisor 配置方式

- [x] 通过apiserver

  ```yaml
  - job_name: kubernetes-cadvisor
    scrape_interval: 30s
    scrape_timeout: 10s
    metrics_path: /metrics
    scheme: https
    kubernetes_sd_configs:
    - api_server: null
      role: node
      namespaces:
        names: []
  
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      insecure_skip_verify: false
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
    - separator: ;
      regex: __meta_kubernetes_node_label_(.+)
      replacement: $1
      action: labelmap
    - separator: ;
      regex: (.*)
      target_label: __address__
      replacement: kubernetes.default.svc:443
      action: replace
    - source_labels: [__meta_kubernetes_node_name]
      separator: ;
      regex: (.+)
      target_label: __metrics_path__
      replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
      action: replace
  ```

  

- [x] cadvisor 内嵌在kubelet 中

  > *prometheus运行在k8s外部* 
  >
  > kubernetes_sd_configs: 
  >
  > ​	`kubeconfig_file` 和 `api_server` 二选其一
  >
  > 
  >
  > https 可以通过证书方式认证或通过token 方法是认证
  
  ```yaml
    - job_name: cadvisor
      metrics_path: /metrics/cadvisor
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.crt
        cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
        key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
        insecure_skip_verify: true
      scheme: https
      #authorization:
      #  type: Bearer
      #  credentials_file: token
      kubernetes_sd_configs:
      - kubeconfig_file: config
        role: node
      relabel_configs:
      - source_labels: [__address__]
        regex: (.*):(.*)
        replacement: "$1:10250"
        target_label: __address__
  ```
  
  ```yaml
    - job_name: cadvisor
      metrics_path: /metrics/cadvisor
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.crt
      #  cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
      #  key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
        insecure_skip_verify: true
      scheme: https
      authorization:
        type: Bearer
        credentials_file: token
      kubernetes_sd_configs:
      - api_server: https://192.168.0.244:6443
        tls_config:
          ca_file: /etc/kubernetes/pki/ca.crt
          cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
          key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
        role: node
      relabel_configs:
      - source_labels: [__address__]
        regex: (.*):(.*)
        replacement: "$1:10250"
        target_label: __address__
  ```
  
  

