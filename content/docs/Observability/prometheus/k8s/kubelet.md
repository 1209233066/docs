---
title: "kubelet"
linkTitle: "kubelet"
date: 2025-05-14
toc_hide: false
hide_summary: true
weight: 205
description: >
  exporter|prometheus

tags: ["prometheus","exporter","kubernetes"]
categories: ["prometheus","监控","exporter"]
url: prometheus/kubernetes/kubelet.html
---

kubelet 还会在 `/metrics/cadvisor`， `/metrics/resource` 和 `/metrics/probes` 端点中公开度量值

curl 127.0.0.1:10248/healthz

curl 127.0.0.1:10250/healthz


1. 部署安装
   
   参见部署k8s
   
   
   
2. 添加prometheus配置
   
    - [x] prometheus 部署在k8s 内，需要提前rbac授权
     
     ```yaml
     tls_config:
       ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
       insecure_skip_verify: true
     bearer_tonken_file: /var/run/secrets/kubernetes.io/serviceaccount/token  
     ```
   
   - [x] prometheus 部署在k8s 外
   
     > kubernetes_sd_configs 支持通过 api_server 或 kubeconfig_file 方式，二选一
     
     > ```bash
     > curl \
     > --cacert /etc/kubernetes/pki/ca.crt \
     > --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt \
     > --key /etc/kubernetes/pki/apiserver-kubelet-client.key \
     > https://192.168.0.243:10250/metrics
     > ```
     
     ```yaml
       - job_name: kubelet
        tls_config:
          ca_file: /etc/kubernetes/pki/ca.crt
          cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
          key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
          insecure_skip_verify: true
        scheme: https
        
         kubernetes_sd_configs:
         - kubeconfig_file: config
           role: node
         relabel_configs:
         - source_labels: [__address__]
           regex: (.*):(.*)
           replacement: "$1:10250"
           target_label: __address__
     ```
     
     > ```bash
     > curl -k  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5jb3R0bGdBVmwtalBuVW9JR0h3VG5nblRkMmVJZUFMdDRVaDd6U1ZNMDQifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImFkbWluLXRva2VuLTduejlwIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiYzEyNjYyNDktMWFkNS00ZjA1LTljZDUtYjhjNTdjYWU2NDkzIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6YWRtaW4ifQ.TXZNfk12OsTh5Z_dkOJOHmIGxV_YNS6QEB-ItgddleoQrlz85S43OMED7mPfnxt9CTuDuuTjRRThXwiw1CF4cdtmwj789IU0z67LyDbkdHC4uUwMnqnQrw3aeSv_dgEHlCJr1btqIImRlxHzxvRsP3Yeqb95hjOqDIMVN_HgfYdk835foAHawrOksHdneMwtoOlpiqjVm9bzjIjEF5ckdVX86hwBu3xB1Ml4R4xZwGIecs06nQoBEKO6MlSARgq8e5VQqdRVip7WJuoAlyq80AYW1gAR7I6RvXJVWECu2NpXzQoTROZ132VyCLAhVQVqf_yLrpnQTTxdOKgvS1tskA" https://192.168.0.243:10250/metrics
     > ```
     
     ```yaml
       - job_name: kubelet
        tls_config:
          ca_file: /etc/kubernetes/pki/ca.crt
          insecure_skip_verify: true
        authorization:
          type: Bearer
          #提前创建RBAC ,提取sa的secret 中token并保存到文件中 
          #kubectl create clusterrolebinding admin --clusterrole=cluster-admin --serviceaccount=default:admin
          credentials_file: token
        scheme: https
        
         kubernetes_sd_configs:
         - kubeconfig_file: config
           role: node
         relabel_configs:
         - source_labels: [__address__]
           regex: (.*):(.*)
           replacement: "$1:10250"
           target_label: __address__
     
     ```
     
   - [x] 通过api_server 执行动态发现
   
     ```yaml
       - job_name: kubelet
        tls_config:
          ca_file: /etc/kubernetes/pki/ca.crt
          insecure_skip_verify: true
        authorization:
          type: Bearer
          #提前创建RBAC ,提取sa的secret 中token并保存到文件中 
          #kubectl create clusterrolebinding admin --clusterrole=cluster-admin --serviceaccount=default:admin
          credentials_file: token
        scheme: https
        
         kubernetes_sd_configs:
         - api_server: https://127.0.0.1:6443
           tls_config:
             ca_file: /etc/kubernetes/pki/ca.pem
             cert_file: /etc/kubernetes/pki/cert.pem
             key_file: /etc/kubernetes/pki/cert.key
             insecure_skip_verify: true
           role: node
         relabel_configs:
         - source_labels: [__address__]
           regex: (.*):(.*)
           replacement: "$1:10250"
           target_label: __address__
     
     ```
   
     
   
3. 常用指标

   各节点running容器数量

   ```bash
   kubelet_running_containers{container_state="running"}
   ```

   各个节点运行pod数量

   ```bash
   kubelet_running_pods
   ```

   各个节点运行ds数量

   各个节点运行sts数量

   各个节点运行job数量

   各个节点运行cronjob数量

   各个节点运行pvc数量

   各个节点运行pv数量

   各个节点容器日志占用量

   kubelet 内存使用量

   kubelet cpu使用量

   节点是否ready

   

   告警

   kubelet 进程异常告警

   有pod 被驱逐时告警

   pod 、cpu 、memory数量即将超过限额告警

   

   Kubelet是Kubernetes集群中的一个核心组件，用于管理和监控运行在节点上的容器。Kubelet会通过暴露一些监控指标来提供关于其自身和节点的健康状况、资源使用情况和性能数据。以下是一些kubelet暴露的常见监控指标：
   
   1. kubelet_runtime_operations_errors_total：Kubelet在容器运行时处理期间遇到的错误数。
   
   2. kubelet_runtime_operations_latency_seconds：Kubelet处理容器运行时操作的延迟时间。
   
      
   
   3. kubelet_volume_stats_available_bytes：节点上可用的存储卷容量。
   
   4. kubelet_volume_stats_capacity_bytes：存储卷的总容量。
   
   5. kubelet_volume_stats_used_bytes：已使用的存储卷容量。
   
   6. kubelet_node_status_capacity_cpu_cores：节点上可用的CPU核心数量。
   
   7. kubelet_node_status_capacity_memory_bytes：节点上可用的内存容量。
   
   8. kubelet_node_status_allocatable_cpu_cores：节点上分配给Pod的可用CPU核心数量。
   
   9. kubelet_node_status_allocatable_memory_bytes：节点上分配给Pod的可用内存容量。
   
   10. kubelet_node_status_kubelet_version：Kubelet的版本信息。
   
   11. kubelet_node_status_machine_id：节点的机器ID。
   
   12. kubelet_node_status_system_uptime：节点的系统运行时间。
   
   15. kubelet_volume_stats_inodes：存储卷的Inode使用情况。
   
   这些指标可以通过Prometheus等监控系统进行收集和分析，以监控和调优Kubernetes集群中的节点和容器的运行情况。
