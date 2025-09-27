---
title: "kube-state-metrics"
linkTitle: "kube-state-metrics"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 209
description: >
  exporter|prometheus

tags: ["prometheus","exporter","kubernetes"]
categories: ["prometheus","监控","exporter"]
url: prometheus/kubernetes/kube-state-metrics.html
---

[kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) 通过监听kube-apiserver生成资源状态指标。包括node、pod、container、deplpyment、statefulset、job、pv、pvc 等。

kube-state-metrics 使用client-go与kubernetes集成，因此在安装时需要选择对应的kubernetes版本。



> - `✓`完全支持的版本范围。
> - `-`Kubernetes 集群具有 client-go 库无法使用的功能（额外的 API 对象、已弃用的 API 等）。

| kube-state-metrics 指标 | **Kubernetes 1.20 版本** | **Kubernetes 1.21 版本** | **Kubernetes 1.22 版本** | **Kubernetes 1.23 版本** | **Kubernetes 1.24 版本** |
| ----------------------- | ------------------------ | ------------------------ | ------------------------ | ------------------------ | ------------------------ |
| **2.3.0 版**            | ✓                        | ✓                        | ✓                        | ✓                        | -                        |
| **2.4.2 版**            | -/✓                      | -/✓                      | ✓                        | ✓                        | -                        |
| **2.5.0 版**            | -/✓                      | -/✓                      | ✓                        | ✓                        | ✓                        |
| **2.6.0 版**            | -/✓                      | -/✓                      | ✓                        | ✓                        | ✓                        |

---

本示例kubernetes 版本 v1.23，kube-state-metrics版本2.6.0

> 资源清单位置：kube-state-metrics/examples/standard

```yaml
---
apiVersion: v1
automountServiceAccountToken: false
kind: ServiceAccount
metadata:
  labels:
    app.kubernetes.io/component: exporter
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: 2.6.0
  name: kube-state-metrics
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    app.kubernetes.io/component: exporter
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: 2.6.0
  name: kube-state-metrics
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  - secrets
  - nodes
  - pods
  - services
  - serviceaccounts
  - resourcequotas
  - replicationcontrollers
  - limitranges
  - persistentvolumeclaims
  - persistentvolumes
  - namespaces
  - endpoints
  verbs:
  - list
  - watch
- apiGroups:
  - apps
  resources:
  - statefulsets
  - daemonsets
  - deployments
  - replicasets
  verbs:
  - list
  - watch
- apiGroups:
  - batch
  resources:
  - cronjobs
  - jobs
  verbs:
  - list
  - watch
- apiGroups:
  - autoscaling
  resources:
  - horizontalpodautoscalers
  verbs:
  - list
  - watch
- apiGroups:
  - authentication.k8s.io
  resources:
  - tokenreviews
  verbs:
  - create
- apiGroups:
  - authorization.k8s.io
  resources:
  - subjectaccessreviews
  verbs:
  - create
- apiGroups:
  - policy
  resources:
  - poddisruptionbudgets
  verbs:
  - list
  - watch
- apiGroups:
  - certificates.k8s.io
  resources:
  - certificatesigningrequests
  verbs:
  - list
  - watch
- apiGroups:
  - storage.k8s.io
  resources:
  - storageclasses
  - volumeattachments
  verbs:
  - list
  - watch
- apiGroups:
  - admissionregistration.k8s.io
  resources:
  - mutatingwebhookconfigurations
  - validatingwebhookconfigurations
  verbs:
  - list
  - watch
- apiGroups:
  - networking.k8s.io
  resources:
  - networkpolicies
  - ingresses
  verbs:
  - list
  - watch
- apiGroups:
  - coordination.k8s.io
  resources:
  - leases
  verbs:
  - list
  - watch
- apiGroups:
  - rbac.authorization.k8s.io
  resources:
  - clusterrolebindings
  - clusterroles
  - rolebindings
  - roles
  verbs:
  - list
  - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    app.kubernetes.io/component: exporter
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: 2.6.0
  name: kube-state-metrics
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kube-state-metrics
subjects:
- kind: ServiceAccount
  name: kube-state-metrics
  namespace: kube-system
```

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/component: exporter
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: 2.6.0
  name: kube-state-metrics
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: kube-state-metrics
  template:
    metadata:
      labels:
        app.kubernetes.io/component: exporter
        app.kubernetes.io/name: kube-state-metrics
        app.kubernetes.io/version: 2.6.0
    spec:
      automountServiceAccountToken: true
      containers:
      - image: registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.6.0
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          timeoutSeconds: 5
        name: kube-state-metrics
        ports:
        - containerPort: 8080
          name: http-metrics
        - containerPort: 8081
          name: telemetry
        readinessProbe:
          httpGet:
            path: /
            port: 8081
          initialDelaySeconds: 5
          timeoutSeconds: 5
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true
          runAsUser: 65534
      nodeSelector:
        kubernetes.io/os: linux
      serviceAccountName: kube-state-metrics
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app.kubernetes.io/component: exporter
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: 2.6.0
    prometheus.io/external: 192.168.0.243 # 为项目改造
    prometheus.io/ports: "32080" # 为项目改造
  name: kube-state-metrics
  namespace: kube-system
spec:
  type: NodePort
  ports:
  - name: http-metrics
    port: 8080
    nodePort: 32080
    targetPort: http-metrics
  - name: telemetry
    port: 8081
    targetPort: telemetry
  selector:
    app.kubernetes.io/name: kube-state-metrics
```





1. 部署安装

   > 8080 端口提供k8s 指标
   >
   > 8081 端口提供kube_state_metrics 自身指标

   ```bash
   kubectl apply -f kube-state-metrics.yml
   ```

2. 添加prometheus配置

   静态配置

   ```yaml
     scrape_configs:
     - job_name: "kube-state-metrics"
       static_configs:
       - targets:
         - "192.168.0.244:8080"
       # 添加所属环境
       relabel_configs:
       - replacement: dev
         target_label: environment
   ```

   基于k8s动态发现

   > ```bash
   > curl --cacert /etc/kubernetes/pki/ca.crt \
   > 	 --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt \
   > 	 --key /etc/kubernetes/pki/apiserver-kubelet-client.key \
   > 	 https://192.168.0.244:6443/api/v1/services?limit=100&resourceVersion=0
   > ```
   >
   > `kubeconfig_file`和 `api_server` 二者选一

   

   

   ```yaml
     - job_name: kube-state-metrics
       kubernetes_sd_configs:
       - api_server: https://192.168.0.244:6443
         tls_config:
           ca_file: /etc/kubernetes/pki/ca.crt
           cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
           key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
           # 测试改成false也没问题
           insecure_skip_verify: true
         role: service
       relabel_configs:
       - source_labels: ["__meta_kubernetes_service_name"]
         action: keep
         regex: "kube-state-metrics"
       - source_labels: ["__meta_kubernetes_service_label_prometheus_io_external","__meta_kubernetes_service_label_prometheus_io_ports"]
         regex: ([0-9\.]+);(\d+)
         replacement: $1:$2
         action: replace
         target_label: __address__
   ```

   

   ```
     - job_name: kube-state-metrics
       kubernetes_sd_configs:
       - kubeconfig_file: config
         role: service
       relabel_configs:
       - source_labels: ["__meta_kubernetes_service_name"]
         action: keep
         regex: "kube-state-metrics"
       - source_labels: ["__meta_kubernetes_service_label_prometheus_io_external","__meta_kubernetes_service_label_prometheus_io_ports"]
         regex: ([0-9\.]+);(\d+)
         replacement: $1:$2
         action: replace
         target_label: __address__
   ```

   

3. 常用指标
   集群状态指标是哪个 
   svc 状态（缺少endpoint）
   
   + node
   
     ```bash
     #节点 数量
     sum(kube_node_info)
     #不可调度的节点数量
     sum(kube_node_spec_unschedulable)
     # 集群cpu 数量
     sum(kube_node_status_capacity{resource="cpu"})
     # 集群内存 数量
     sum(kube_node_status_capacity{resource="memory"})
     
     # 磁盘存在压力的节点
     kube_node_status_condition{condition="DiskPressure",status="true"}
     # 内存存在压力的节点
     kube_node_status_condition{condition="MemoryPressure",status="true"}
     # pid存在压力的节点
     kube_node_status_condition{condition="PIDPressure",status="true"}
     # 存在网络不可达节点
     kube_node_status_condition{condition="NetworkUnavailable",status="true"}
     ```
   
   + namespace
   
   + pod
   
     ```bash
     kube_pod_status_phase{phase="Failed"}
     kube_pod_status_phase{phase="Pending"}
     kube_pod_status_phase{phase="Running"}
     kube_pod_status_phase{phase="Succeeded"}
     kube_pod_status_phase{phase="Unknown"}
     ```
   
     
   
   + container
   
     ```bash
     # 容器状态
     kube_pod_container_status_running
     kube_pod_container_status_waiting
     kube_pod_container_status_ready
     kube_pod_container_status_terminated
     kube_pod_container_status_terminated_reason
     # 30分钟内重启过的pod
     changes(kube_pod_container_status_restarts_total[30m])
     # 容器资源配额
     kube_pod_container_resource_requests{resource="cpu"}
     kube_pod_container_resource_limits{resource="cpu"}
     kube_pod_container_resource_requests{resource="memory"}
     kube_pod_container_resource_limits{resource="memory"}
     ```
   
   + replicaset
   
   + deploy
   
     ```bash
     #各个deployment的副本数量
     kube_deployment_status_replicas
     
     #各个deployment不可用的副本数量
     kube_deployment_status_replicas_unavailable
     ```
   
     
   
   + daemonset
   
   + sts
   
   + job
   
   + cronjob
   
   + service
   
   + endpoint
   
   + ingress
   
   + storageclass
   
   + persistentvolume
   
     ```bash
     kube_persistentvolume_status_phase{phase="Available"}
     kube_persistentvolume_status_phase{phase="Bound"}
     kube_persistentvolume_status_phase{phase="Failed"}
     kube_persistentvolume_status_phase{phase="Pending"}
     kube_persistentvolume_status_phase{phase="Released"}
     ```
   
     
   
   + persistentvolumeclaim
   
     ```bash
     kube_persistentvolumeclaim_status_phase{phase="Bound"}
     kube_persistentvolumeclaim_status_phase{phase="Lost"}
     kube_persistentvolumeclaim_status_phase{phase="Pending"}
     ```
   
     
   
   + configmap
   
   + secret
   
   + poddisruptionbudget
   
   + horizontalpodautoscaler
   
   + networkpolicy
   
   + lease
   
   + limitrange
   
   + mutatingwebhookconfiguration
   
   + validatingwebhookconfiguration
   
   + volumeattachment
   
     

```yaml
groups:
- name: kube-state-metrics
  rules:
  - alert: KubeStateMetricsListErrors
    annotations:
      description: kube-state-metrics is experiencing errors at an elevated rate in list operations. This is likely causing it to not be able to expose metrics about Kubernetes objects correctly or at all.
      summary: kube-state-metrics is experiencing errors in list operations.
    expr: |
      (sum(rate(kube_state_metrics_list_total{job="kube-state-metrics",result="error"}[5m]))
        /
      sum(rate(kube_state_metrics_list_total{job="kube-state-metrics"}[5m])))
      > 0.01
    for: 15m
    labels:
      severity: critical
  - alert: KubeStateMetricsWatchErrors
    annotations:
      description: kube-state-metrics is experiencing errors at an elevated rate in watch operations. This is likely causing it to not be able to expose metrics about Kubernetes objects correctly or at all.
      summary: kube-state-metrics is experiencing errors in watch operations.
    expr: |
      (sum(rate(kube_state_metrics_watch_total{job="kube-state-metrics",result="error"}[5m]))
        /
      sum(rate(kube_state_metrics_watch_total{job="kube-state-metrics"}[5m])))
      > 0.01
    for: 15m
    labels:
      severity: critical
  - alert: KubeStateMetricsShardingMismatch
    annotations:
      description: kube-state-metrics pods are running with different --total-shards configuration, some Kubernetes objects may be exposed multiple times or not exposed at all.
      summary: kube-state-metrics sharding is misconfigured.
    expr: |
      stdvar (kube_state_metrics_total_shards{job="kube-state-metrics"}) != 0
    for: 15m
    labels:
      severity: critical
  - alert: KubeStateMetricsShardsMissing
    annotations:
      description: kube-state-metrics shards are missing, some Kubernetes objects are not being exposed.
      summary: kube-state-metrics shards are missing.
    expr: |
      2^max(kube_state_metrics_total_shards{job="kube-state-metrics"}) - 1
        -
      sum( 2 ^ max by (shard_ordinal) (kube_state_metrics_shard_ordinal{job="kube-state-metrics"}) )
      != 0
    for: 15m
    labels:
      severity: critical
```
