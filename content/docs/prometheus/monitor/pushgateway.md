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



> prometheus 默认使用pull 的方式拉取指标，但对于转瞬即逝的指标可能prometheus还未来得及抓取服务已经结束。因此pushgateway就弥补了这些。
>
> pushgateway 更倾向于解决服务级别的指标暴露，对于主机级别的指标使用 node_exporter提供的 [textfile](https://github.com/prometheus/node_exporter/blob/master/README.md#textfile-collector)更加适合。



1. 安装部署
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
   
2. 指标推送
   ```bash
   echo "metrics_01 1.0" | curl --data-binary @-  http://127.0.0.1:9091/metrics/job/my_job
   echo "metrics_02 2.0" | curl --data-binary @- http://127.0.0.1:9091/metrics/job/my_job
   ```
   此时通过访问 `http://127.0.0.1:9091` 可以看到指标已经上传，

   `job="my_job"`  为job名称

   `metrics_01` 为自定义指标名称
   
   `metrics_02` 为自定义指标名称
   
   `push_failure_time_seconds`  记录失败的时间戳
   
   `push_time_seconds`  记录成功的时间戳
   ![Alt text](../docs/prometheus/monitor/pushgateway01.png)
   
   
   
4. 对接到promethues

   ```yaml
   global:
     external_labels:
       prometheus: prom-xxx
   scrape_configs:
   - job_name: pushgateway
     scrape_interval: 5m
     # 特别提醒设置为true,否则后面设置的job，instance等标签将会被舍弃
     honor_labels: true
     static_configs:
     - targets:
       - "localhost:9091"
   ```
   
4. 推送指标

   4.1 通过命令行推送指标

   语法一：

   > metrics_01{job="my_job"}

   ```bash
   echo "metrics_01 1.0" | curl --data-binary @-  http://127.0.0.1:9091/metrics/job/my_job
   ```

   ```bash
   # 删除分组为job="my_job"的指标
   curl -X DELETE http://127.0.0.1:9091/metrics/job/my_job
   ```

   

   语法二：

   >metrics_01{job="my_job",instance="host01"}

   ```bash
   echo "metrics_01 1.0" | curl --data-binary @-  http://127.0.0.1:9091/metrics/job/my_job/instance/host01
   ```

   ```bash
   echo "metrics_01 1.0" | curl --data-binary @- http://127.0.0.1:9091/metrics/job/my_job/instance/host01/env/test
   ```

   

   ```bash
   # 删除分组为job="my_job" ,instance="host01" 的指标
   curl -X DELETE http://127.0.0.1:9091/metrics/job/my_job/instance/host01
   ```

   ```bash
   # 删除所有分组指标，启动时需要开启--web.enable-admin-api
   curl -X PUT http://127.0.0.1:9091/api/v1/admin/wipe
   ```

   

   4.2 通过prometheus 客户端推送指标

   

   [Peter Bourgon · Go: Best Practices for Production Environments](http://peter.bourgon.org/go-in-production/#formatting-and-style)

   [prometheus/client_golang: Prometheus instrumentation library for Go applications (github.com)](https://github.com/prometheus/client_golang)

   [When to use the Pushgateway | Prometheus](https://prometheus.io/docs/practices/pushing/)

   

   