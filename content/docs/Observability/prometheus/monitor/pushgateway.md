---
title: "pushgateway"
linkTitle: ""
date: 2025-05-12
simple_list: true
weight: 103
tags: ["prometheus","exporter","pushgateway"]
categories: ["prometheus","exporter"]
url: prometheus/monitor/pushgateway.html
---


> pushgateway 用于将瞬时指标推送到prometheus，更倾向于解决服务级别的指标暴露，对于主机级别的瞬时指标可以使用[textfile](https://github.com/prometheus/node_exporter/blob/master/README.md#textfile-collector)




1. 安装部署
{{< tabpane text=true right=false >}}
  {{% tab header="**部署环境**:" disabled=true /%}}
  {{% tab header="docker" lang="bash" %}}
  ```bash
  docker run -d -p 9091:9091 prom/pushgateway
  ```
  {{% /tab %}}
  {{% tab header="k8s" lang="yaml" %}}
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: pushgateway
   spec:
     externalIPs:
     - 10.4.7.10
     ports:
     - port: 9091
       protocol: TCP
       targetPort: 9091
     selector:
       app: pushgateway
   ---
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: pushgateway
   spec:
     selector:
       matchLabels:
         app: pushgateway
     template:
       metadata:
         labels:
           app: pushgateway
       spec:
         containers:
         - name: pushgateway
           image: prom/pushgateway:v1.5.0
           ports:
           - name: http
             containerPort: 9091
           args:
           - --web.enable-admin-api
           resources:
             limits:
               cpu: 500m
               memory: 1024Mi
             requests:
               cpu: 200m
               memory: 512Mi
           readinessProbe:
             httpGet: 
               port: 9091
               path: /-/ready
             initialDelaySeconds: 30
             failureThreshold: 3
             periodSeconds: 10
             successThreshold: 1
             timeoutSeconds: 2
           livenessProbe:
             httpGet: 
               port: 9091
               path: /-/healthy
             initialDelaySeconds: 30
             failureThreshold: 3
             periodSeconds: 10
             successThreshold: 1
             timeoutSeconds: 2
   ```
  {{% /tab %}}

{{< /tabpane >}}


   
2. 指标推送
{{< tabpane text=true right=false >}}
  {{% tab header="**客户端**:" disabled=true /%}}
  {{% tab header="curl" lang="bash" %}}
  推送指标 `metrics_01{job="my_job"} 1.0`
  ```bash 
  # metrics_01 和metrics_02 为自定义指标名称
  # job="my_job"  为job名称
  echo "metrics_01 1.0" | curl --data-binary @-  http://127.0.0.1:9091/metrics/job/my_job
  echo "metrics_02 2.0" | curl --data-binary @- http://127.0.0.1:9091/metrics/job/my_job
  ```

   推送指标 `metrics_01{job="my_job",instance="host01",env="test"} 1.0`
   ```bash
   # /metrics/job/<JOB_NAME>{/<LABEL_NAME>/<LABEL_VALUE>}
   echo "metrics_01 1.0" | curl --data-binary @- http://127.0.0.1:9091/metrics/job/my_job/instance/host01/env/test
   ```

  删除指标
  ```bash
   # 删除分组为job="my_job"的指标
   curl -X DELETE http://127.0.0.1:9091/metrics/job/my_job
   ```

   删除指标
   ```bash
   # 删除分组为job="my_job" ,instance="host01" 的指标
   curl -X DELETE http://127.0.0.1:9091/metrics/job/my_job/instance/host01
   ```

   ```bash
   # 删除所有分组指标，启动时需要开启--web.enable-admin-api
   curl -X PUT http://127.0.0.1:9091/api/v1/admin/wipe
   ```
  {{% /tab %}}
  {{% tab header="python-sdk" lang="python" %}}
    一切皆文件
  {{% /tab %}}
{{< /tabpane >}}




   
   
   
4. 对接到promethues
{{% alert title="Warning" color="warning" %}}
`honor_labels: true`,否则后面设置的job，instance等标签将会被舍弃
   ```yaml
   global:
     external_labels:
       prometheus: prom-xxx
   scrape_configs:
   - job_name: pushgateway
     scrape_interval: 5m
     honor_labels: true
     static_configs:
     - targets:
       - "localhost:9091"
   ```
{{% /alert %}}


   

   

   


参考:

[client_python](https://github.com/prometheus/client_python)|[doc](https://prometheus.github.io/client_python/)

[client_golang](https://github.com/prometheus/client_golang)


   [Peter Bourgon · Go: Best Practices for Production Environments](http://peter.bourgon.org/go-in-production/#formatting-and-style)

   

   [When to use the Pushgateway | Prometheus](https://prometheus.io/docs/practices/pushing/)