---
title: "operator"
linkTitle: "operator"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 2
description: >
  安装|prometheus

tags: ["prometheus","安装"]
categories: ["prometheus","监控"]
url: prometheus/prometheus-operator.html
---


### 基于[prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)

版本矩阵

| kube-prometheus stack                                        | Kubernetes 1.21 | Kubernetes 1.22 | Kubernetes 1.23 | Kubernetes 1.24 | Kubernetes 1.25 | Kubernetes 1.26 | Kubernetes 1.27 |
| ------------------------------------------------------------ | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- |
| [`release-0.9`](https://github.com/prometheus-operator/kube-prometheus/tree/release-0.9) | ✔               | ✔               | ✗               | ✗               | ✗               | x               | x               |
| [`release-0.10`](https://github.com/prometheus-operator/kube-prometheus/tree/release-0.10) | ✗               | ✔               | ✔               | ✗               | ✗               | x               | x               |
| [`release-0.11`](https://github.com/prometheus-operator/kube-prometheus/tree/release-0.11) | ✗               | ✗               | ✔               | ✔               | ✗               | x               | x               |
| [`release-0.12`](https://github.com/prometheus-operator/kube-prometheus/tree/release-0.12) | ✗               | ✗               | ✗               | ✔               | ✔               | x               | x               |
| [`main`](https://github.com/prometheus-operator/kube-prometheus/tree/main) | ✗               | ✗               | ✗               | ✗               | x               | ✔               | ✔               |

1. 下载安装

   ```bash
   git clone https://github.com/prometheus-operator/kube-prometheus.git
   ```

   ```bash
   cd kube-prometheus/
   git checkout -b release-0.10
   ```

   ```bash
   # Create the namespace and CRDs, and then wait for them to be availble before creating the remaining resources
   kubectl create -f manifests/setup
   ```

   创建monitoring 名称空间，并创建以下crd

   + alertmanagerconfigs.monitoring.coreos.com 

   + alertmanagers.monitoring.coreos.com

   + podmonitors.monitoring.coreos.com

   + probes.monitoring.coreos.com

   + prometheuses.monitoring.coreos.com

   + prometheusagents.monitoring.coreos.com

   + prometheusrules.monitoring.coreos.com

   + scrapeconfigs.monitoring.coreos.com 

   + servicemonitors.monitoring.coreos.com

   + thanosrulers.monitoring.coreos.com

     

   ```bash
   # Wait until the "servicemonitors" CRD is created. The message "No resources found" means success in this context.until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
   
   kubectl create -f manifests/
   ```

2. 验证

   ```bash
   kubectl --namespace monitoring port-forward svc/prometheus-k8s 9090
   ```

   ```bash
   kubectl --namespace monitoring port-forward svc/alertmanager-main 9093
   ```

   ```bash
   kubectl --namespace monitoring port-forward svc/grafana 3000
   ```
   
   
