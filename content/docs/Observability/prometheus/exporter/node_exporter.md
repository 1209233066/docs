---
title: "node_exporter"
linkTitle: "node_exporter"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 51
description: >
  node_exporter|exporter|prometheus

tags: ["prometheus","exporter","node_exporter"]
categories: ["prometheus","监控","exporter"]
url: prometheus/exporter/node_exporter.html
---


提供操作系统级别的监控指标，`cpu` `memory` `disk space` `diskio` `network`



{{< tabpane text=true right=true >}}
  {{% tab header="**[部署安装](https://prometheus.io/download/#node_exporter)**:" disabled=true /%}}
  {{% tab header="二进制" lang="en" %}}

```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz

tar xf node_exporter-1.6.1.linux-amd64.tar.gz
mv node_exporter-*.linux-amd64/node_exporter /usr/bin
```

```bash
tee /usr/lib/systemd/system/node_exporter.service <<'EOF'
[Unit]
Description=node_exporter service https://prometheus.io/
After=network.target

[Service]

ExecStart=/usr/bin/node_exporter \
--web.listen-address=:9100 \
--web.telemetry-path=/metrics \
--collector.systemd \
--collector.systemd.unit-include="(sshd|docker|rsyslog|kubelet|kube-proxy).service" \
--no-collector.arp \
--log.format=json 

User=root
[Install]
WantedBy=multi-user.target
EOF
```

```bash
systemctl daemon-reload
systemctl enable node_exporter --now
systemctl status node_exporter
```



  {{% /tab %}}
  {{% tab header="kubernetes" lang="en" %}}

 ```yaml
     apiVersion: apps/v1
     kind: DaemonSet
     metadata:
       name: node-exporter
       namespace: kube-system
     spec:
       selector:
         matchLabels:
           app: node-exporter
       template:
         metadata:
           labels:
             app: node-exporter
         spec:
           tolerations:
           - key: ""
             operator: "Exists"
           volumes:
           - name: root
             hostPath:
               path: /
           hostNetwork: true
           hostPID: true
           containers:
           - name: node-exporter
             image: quay.io/prometheus/node-exporter:v1.6.1
             args:
             - --path.rootfs=/host
             volumeMounts:
             - mountPath: /host
               name: root
 ```

{{% /tab %}}

 {{< /tabpane >}}


​     

{{< tabpane text=true right=true >}}
  {{% tab header="**添加prometheus配置**:" disabled=true /%}}
  {{% tab header="静态配置" lang="en" %}}

```yaml
- job_name: node-exporter
  honor_timestamps: true
  scrape_interval: 1m
  scrape_timeout: 20s
  metrics_path: /metrics
  scheme: http
  static_configs:
  - targets:
    - 127.0.0.1:9100
```



{{% /tab %}}





  {{% tab header="kuernetes_sd_configs" lang="en" %}}

> `kubeconfig_file` 和 `api_server` 二选其一

```yaml
  - job_name: node-exporter
    kubernetes_sd_configs:
    - kubeconfig_file: /root/.kube/config
      role: node
    relabel_configs:
    - source_labels: [__address__]
      regex: (.*):(.*)
      replacement: "$1:9100"
      target_label: __address__
      
  - job_name: node-exporter-ca
    kubernetes_sd_configs:
    - api_server: https://192.168.0.244:6443
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.crt
        cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
        key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
        # 测试改成false也没问题
        insecure_skip_verify: true
      role: node
    relabel_configs:
    - source_labels: [__address__]
      regex: (.*):(.*)
      replacement: "$1:9100"
      target_label: __address__
```



{{% /tab %}}

 {{< /tabpane >}}



*由于node_export 返回大量指标，通过prometheus配置文件的collect 收集指定的指标*

> curl -g -X GET 127.0.0.1:9100/metrics?collect[]=xfs
> curl -g -X GET 127.0.0.1:9100/metrics?collect[]=cpu

```yaml
global:
  external_labels:
  prometheus: prom-xxx
scrape_configs:
- job_name: node_exporter
  params:
    collect[]:
    - cpu
    - meminfo
    - netstat
    - systemd
    - xfs
    - filefd
    - filesystem
  kubernetes_sd_configs:
    - api_server: https://127.0.0.1:6443
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.pem
        cert_file: /etc/kubernetes/pki/cert.pem
        key_file: /etc/kubernetes/pki/cert.key
        # 测试改成false也没问题
        insecure_skip_verify: true
      role: node
    relabel_configs:
    - source_labels: [__address__]
      regex: (.*):(.*)
      replacement: "$1:9100"
      target_label: __address__
```









2. 常用指标

   | **指标**                                                     | **释义**                 | **指标类型** |
   | ------------------------------------------------------------ | ------------------------ | ------------ |
   | `irate(node_cpu_seconds_total{job="node_exporter",cpu="0"}[5m])` | cpu0 每秒使用率          | counter      |
   | `avg(irate(node_cpu_seconds_total{job="node_exporter",cpu="0"}[5m]))by(mode)` | cpu0 平均使用率          |              |
   | `count(node_cpu_seconds_total{mode="idle"})by(instance)`     | 查询有几个逻辑核心       |              |
   | `node_memory_MemTotal_bytes`                                 | 内存总量                 |              |
   | `node_memory_Buffers_bytes`                                  | buffer                   |              |
   | `node_memory_Cached_bytes`                                   | cache                    |              |
   | `node_memory_MemFree_bytes`                                  | free                     |              |
   | `node_memory_MemAvailable_bytes`                             | 可用内存                 |              |
   | `node_memory_SUnreclaim_bytes`                               | 不可回收slab             |              |
   | `node_vmstat_pswpin`                                         | 磁盘加载到内存的字节数/s |              |
   | `node_vmstat_pswpout`                                        | 内存换出到磁盘的字节数/s |              |
   | `node_filesystem_size_bytes`                                 | mount的文件系统大小      |              |
   | `node_filesystem_free_bytes`                                 | mount的文件系统空闲      |              |
   | `node_systemd_unit_state`                                    | systemd管理服务状态      |              |
   | `node_uname_info`                                            | 主机名/os版本的信心      |              |
   | `node_filesystem_readonly`                                   | 文件系统只读             |              |

   ```bash
   node_netstat_Tcp_CurrEstab  tcp连接数
   # 入栈流量
   rate(node_network_receive_bytes_total{device="eth0"}[5m])
   # 出栈流量
   rate(node_network_transmit_bytes_total{device="eth0"}[5m])
   ```

   

   

3. 告警规则

   ```yaml
   # 1. 运行时间
   # 2. cpu
   # 3. 内存
   # 4. 磁盘
   # 5. tcp 连接
   # 6. 网络流量
   groups:
   - name: node
     rules:
     # 机器宕机告警
     - alert: NodeDown
       expr: up{job=~"node(_|-|)exporter"} == 0
       for: 5m
       keep_firing_for: 1m
       labels:
         severity: critical
       annotations:
         summary: "主机宕机 ({{ $labels.instance }})"
         description: "实例 {{ $labels.instance }} 已宕机超过5分钟 (Job: {{ $labels.job }})"
         
     # 文件系统只读告警
     - alert: FilesystemReadOnly
       expr: node_filesystem_readonly{mountpoint="/"} == 1
       for: 5m
       keep_firing_for: 1m
       labels:
         severity: critical
       annotations:
         summary: "主机 ({{ $labels.instance }})挂载点 {{ $labels.mountpoint }} 只读"
         description: "实例 {{ $labels.instance }} 挂载点 {{ $labels.mountpoint }} 变为只读超过5分钟 (Job: {{ $labels.job }})"
   
     # CPU使用率告警
     - alert: NodeCpuUsageHigh
       expr: |
         100 - (
           avg by(instance) (
             rate(node_cpu_seconds_total{mode="idle"}[5m])
           ) * 100
         ) > 85
       for: 5m
       keep_firing_for: 1m
       labels:
         severity: warning
       annotations:
         summary: "主机CPU使用率过高 ({{ $labels.instance }})"
         description: "实例 {{ $labels.instance }} CPU使用率持续5分钟超过85%（当前值：{{ $value | printf \"%.2f\"}}%）"
   
     # 系统负载告警
     - alert: NodeLoad1High
       expr: |
         node_load1 
         > on(instance) 
         count by(instance) (node_cpu_seconds_total{mode="idle"}) * 2
       for: 5m
       keep_firing_for: 1m
       labels:
         severity: warning
       annotations:
         summary: "主机1分钟负载过高 ({{ $labels.instance }})"
         description: "实例 {{ $labels.instance }} 1分钟负载超过CPU核心数2倍（当前值：{{ $value | printf \"%.2f\"}}）"
   
     - alert: NodeLoad15High
       expr: |
         node_load15 
         > on(instance) 
         count by(instance) (node_cpu_seconds_total{mode="idle"}) * 2
       for: 5m
       keep_firing_for: 1m
       labels:
         severity: critical 
       annotations:
         summary: "主机15分钟负载过高 ({{ $labels.instance }})"
         description: "实例 {{ $labels.instance }} 15分钟负载持续超过CPU核心数2倍（当前值：{{ $value | printf \"%.2f\"}}）"
   
     # 内存使用率告警
     - alert: NodeMemoryUsageHigh
       expr: |
         (1 - 
           node_memory_MemAvailable_bytes{job=~"node.*exporter"} 
           / 
           node_memory_MemTotal_bytes
         ) * 100 > 90
       for: 5m
       keep_firing_for: 1m
       labels:
         severity: critical
       annotations:
         summary: "主机内存使用率过高 ({{ $labels.instance }})"
         description: "实例 {{ $labels.instance }} 内存使用率持续5分钟超过90%（当前值：{{ $value | printf \"%.2f\"}}%）"
   
     # 磁盘使用率告警
     - alert: NodeDiskUsageHigh
       expr: |
         (1 - 
           node_filesystem_free_bytes{
             fstype!~"^(tmpfs|rootfs|autofs|devpts|devtmpfs|overlay)$",
             mountpoint!~"^/(boot|run|var/lib/docker).*"
           } 
           / 
           node_filesystem_size_bytes
         ) * 100 > 85
       for: 5m
       keep_firing_for: 1m
       labels:
         severity: warning
       annotations:
         summary: "主机磁盘使用率过高 ({{ $labels.instance }}:{{ $labels.mountpoint }})"
         description: "实例 {{ $labels.instance }} 挂载点 {{ $labels.mountpoint }} 使用率超过85%（当前值：{{ $value | printf \"%.2f\"}}%）"
   
     # 磁盘空间预测告警
     - alert: NodeDiskWillFillIn8H
       expr: |
         predict_linear(
           node_filesystem_free_bytes{
             fstype!~"^(tmpfs|rootfs|autofs|devpts|devtmpfs|overlay)$",
             mountpoint!~"^/(boot|run|var/lib/docker).*"
           }[6h],
           8*3600
         ) < 0
       for: 5m
       keep_firing_for: 1m
       labels:
         severity: warning
       annotations:
         summary: "主机磁盘空间即将耗尽 ({{ $labels.instance }}:{{ $labels.mountpoint }})"
         description: "实例 {{ $labels.instance }} 挂载点 {{ $labels.mountpoint }} 预计8小时内空间将耗尽（当前预测值：{{ $value | printf \"%.2f\"}}）"
     
     # 网络流量
   ```

   

   + cpu饱和度

     通过1分钟 5分钟 15 分钟的负载展示。一般负载小于cpu 核心数1.5倍

     ```bash
     node_load1 >on (instance) (
     count by(instance) (node_cpu_seconds_total{mode="idle"})*1
     )
     node_load5
     node_load15
     ```

     

   + 内存使用率

     > <font color="#b2b503">[**INFO**]</font>
     >
     > node_memmory_MemeTotal_bytes
     > node_memmory_MemFress_bytes
     > node_memmory_Buffers_bytes
     > node_memmory_Cached_bytes

     ```bash
     1-(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) >0.85
     ```

     

   + 内存饱和度,判断内存的繁忙程度

     ```bash
     磁盘到到内存的  字节数/s
     node_vmstat_pswpin
     内存到到磁盘的 字节数/s
     node_vmstat_pswpout
     
     rate(node_vmstat_pswpout[1m])+rate(node_vmstat_pswpin[1m])
     
     sum(rate(node_vmstat_pswpout[1m])+rate(node_vmstat_pswpin[1m]))by(instance) *1024
     ```

   + 磁盘使用率

     ```bash
     node_filesystem_size_bytes{mountpoint="/"} # 总大小
     
     node_filesystem_free_bytes{mountpoint="/"} # 空闲大小
     #使用比例
     (1-(node_filesystem_free_bytes{mountpoint="/"}/node_filesystem_size_bytes{mountpoint="/"}))>0.85
     ```

     使用predict_linear线性函数预测未来4个小时中磁盘的剩余空间

     ```bash
     predict_linear(node_filesystem_free_bytes{mountpoint="/"}[1h],4*3600)<0
     ```

   + 入栈流量速率

     ```bash
     irate(node_network_receive_bytes_total{device="eth0"}[5m])
     ```

   + 出栈网络速率

     ```bash
     irate(node_network_transmit_bytes_total{device="eth0"}[5m])
     ```

   + 服务异常

     ```bash
     node_systemd_unit_state{name="docker.service"} == 0
     ```

   + bond 文件描述符 sr-iov 监控 tcp

4. 附录： 自定义指标

   node_exporter 允许用户自定义监控指标，具体方法如下：

   1. 修改node_exportrer启动文件,添加如下选项

      ```bash
      --collector.textfile \
      --collector.textfile.directory="."
      ```

      

   2. 在 `--collector.textfile.directory=` 定义的目录下写入要提供的指标内容，文件以`.prom` 结尾

      ```bash
      vi httpcod.prom
      
      #输入示例：
      method_code:http_errors:rate5m{method="get", code="500"}  24
      method_code:http_errors:rate5m{method="get", code="404"}  30
      method_code:http_errors:rate5m{method="put", code="501"}  3
      method_code:http_errors:rate5m{method="post", code="500"} 6
      method_code:http_errors:rate5m{method="post", code="404"} 21
      
      method:http_requests:rate5m{method="get"}  600
      method:http_requests:rate5m{method="del"}  34
      method:http_requests:rate5m{method="post"} 120
      ```

      

      

   3. 重启node_exporter