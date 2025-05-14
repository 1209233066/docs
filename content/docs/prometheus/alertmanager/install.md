---
title: "部署alertmanager"
linkTitle: "install"
date: 2025-05-14
toc_hide: false
hide_summary: true
weight: 1
description: >
  install|alertmanager|prometheus

tags: ["prometheus","alertmanager","install"]
categories: ["prometheus","alertmanager"]
url: prometheus/alertmanager/install.html
---

### 二进制安装

```bash
wget https://github.com/prometheus/alertmanager/releases/download/v0.26.0/alertmanager-0.26.0.linux-amd64.tar.gz
```

```bash
mkdir /data/alertmanager/{bin,conf/templates,data} -p
```

```bash
tar xf alertmanager-0.26.0.linux-amd64.tar.gz 
```

```bash
mv alertmanager-*.linux-amd64/alertmanager /data/alertmanager/bin/
mv alertmanager-*.linux-amd64/amtool /data/alertmanager/bin/
mv alertmanager-*.linux-amd64/alertmanager.yml /data/alertmanager/conf/
```

```bash
chown -R prometheus:prometheus /data/alertmanager
```

> 如果需要使用反向代理时启动参数新增： `--web.external-url="http://127.0.0.1:9003/alert"`

```bash
tee /usr/lib/systemd/system/alertmanager.service <<EOF
[Unit]
Description=alertmanager service https://prometheus.io/
After=network.target

[Service]
ExecStartPre=/data/alertmanager/bin/amtool check-config /data/alertmanager/conf/alertmanager.yml

ExecStart=/data/alertmanager/bin/alertmanager \\
    --config.file=/data/alertmanager/conf/alertmanager.yml \\
    --storage.path=/data/alertmanager/data \\
    --data.retention=120h \\
    --web.external-url=http://:9093/alert
    
User=prometheus
[Install]
WantedBy=multi-user.target
EOF
```

```bash
systemctl daemon-reload
systemctl enable alertmanager --now
systemctl status alertmanager
```

prometheus配置

````yaml
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - 127.0.0.1:9093
    path_prefix: /alert
````



#### [告警接收器](https://prometheus.io/docs/alerting/latest/configuration/#receiver)

- [x] webhook

  > 通过webhook 接收后可以放入数据库、消息队列等.

  1. 创建alertmanager配置

     ```bash
     tee  /data/alertmanager/conf/alertmanager.yml <<EOF
     global:
      
     route:
       receiver: 'webhook'
       group_by: ['alertname','cluster']
       group_wait: 30s
       group_interval: 5m
     receivers:
     - name: 'webhook'
       webhook_configs:
       - url: 'http://127.0.0.1:5001/'
     EOF
     ```

     
  2. 编写一个webhook接收告警
  {{< tabpane text=true right=false >}}
    {{% tab header="**webhook**:" disabled=true /%}}
    {{% tab header="python" lang="python" %}}
     tee app.py<<EOF
    
     import json
     
     from flask import Flask, request, jsonify
     # import smtplib 
     
     app = Flask(__name__)
     
     @app.route('/', methods=['POST'])
     def alert_webhook():
         # 获取post 请求传递是所有信息
         data=request.get_data()
         print(json.loads(data))
         return jsonify({'status': 'ok'})
     if __name__ == '__main__':
         app.run(host='0.0.0.0', port=5001, debug=True)
     EOF

     python3 app.py

    {{% /tab %}}
    {{% tab header="golang" lang="python" %}}



      package main

      import (
        "fmt"
        "io"
        "net/http"
      )

      func handlePostRequest(w http.ResponseWriter, r *http.Request) {

        body, _ := io.ReadAll(r.Body)
        defer r.Body.Close()

        fmt.Println(string(body))
        //fmt.Fprint(w, "POST request received")
      }

      func main() {
        http.HandleFunc("/", handlePostRequest)
        http.ListenAndServe(":5001", nil)
      }
      

    {{% /tab %}}
  {{< /tabpane >}}




     

  3. 触发一条告警

     ```bash
     curl -X POST -H "Content-Type: application/json" -d '[
         {
             "labels": {
                 "alertname": "cpuHigh",
                 "instance": "node01:9100",
                 "job": "node_exporter",
                 "severity": "warning"
             },
             "annotations": {
                 "description": "node01:9100 of job node_exporter has been used cpu >85 more than 5 minutes. (current value: 89.99%)",
                 "summary": "Instance node01:9100 cpu usage more than 85%"
             },
             "generatorURL": "http://prometheus.pytc.com.cn/prom"
             
         }
     ]' "http://127.0.0.1:9093/alert/api/v2/alerts"
     ```

     

  4. alertmanager 接收到了一条告警信息

     ![alertmanager01.png](/docs/prometheus/alertmanager/img/alertmanager01.png)

  5. webhook接收到告警信息

        > <font color=#faf>[Warning]</font>
        >
        > 细心的朋友发现`generatorurl` 和 `externalurl` 显示异常，可以通过修改启动命令调整。对于运行在容器中尤为有用
        >
        > ```bash
        > ./prometheus --config.file=prometheus.yml --web.external-url=http://x.x.x.x:9090
        > ./alertmanager --config.file=alertmanager.yml --web.external-url=http://x.x.x.x:9093
        > ```
     
     ```json
     {
         "receiver": "webhook",
         "status": "firing",
         "alerts": [
             {
                 "status": "firing",
                 "labels": {
                     "alertname": "cpuHigh",
                     "instance": "node01:9100",
                     "job": "node_exporter",
                     "severity": "warning"
                 },
                 "annotations": {
                     "description": "node01:9100 of job node_exporter has been used cpu >85 more than 5 minutes. (current value: 89.99%)",
                     "summary": "Instance node01:9100 cpu usage more than 85%"
                 },
                 "startsAt": "2025-01-12T16:04:33.208058295+08:00",
                 "endsAt": "0001-01-01T00:00:00Z",
                 "generatorURL": "http://127.0.0.1",
                 "fingerprint": "d2a2fb28d1488138"
             }
         ],
         "groupLabels": {
             "alertname": "cpuHigh"
         },
         "commonLabels": {
             "alertname": "cpuHigh",
             "instance": "node01:9100",
             "job": "node_exporter",
             "severity": "warning"
         },
         "commonAnnotations": {
             "description": "node01:9100 of job node_exporter has been used cpu >85 more than 5 minutes. (current value: 89.99%)",
             "summary": "Instance node01:9100 cpu usage more than 85%"
         },
         "externalURL": "http://:9093/alert",
         "version": "4",
         "groupKey": "{}:{alertname=\"cpuHigh\"}",
         "truncatedAlerts": 0
     }
     ```
     
     

  
- [x] [email](https://prometheus.io/docs/alerting/latest/configuration/#email_config)

  ```bash
  tee /data/alertmanager/conf/alertmanager.yml <<EOF
  # 全局定义
  global:
    # The smarthost 
    smtp_smarthost: 'smtp.qq.com:465'
    # from who send email
    smtp_from: '810654947@qq.com'
    smtp_auth_username: '810654947@qq.com'
    smtp_auth_password: 'kqaexaxpbrbdbajd'
    #
    smtp_require_tls: false
  # 告警媒介  
  receivers:
  - name: 'email'
    email_configs:
    - to: '810654947@qq.com'
      send_resolved: true
  
  - name: 'webhook'
    webhook_configs:
    - url: 'http://192.168.0.20:5001/'
  # 告警路由  
  route:
    # 根路由，任何子路由不能匹配的路由都会发送到根路由
    receiver: 'email'
    group_by: ['alertname','cluster']
    group_wait: 30s
    group_interval: 5m
  
    routes:
    - receiver: 'webhook'
      matchers:
      - alertname=~"disk*"
      
  # 告警模版 
  templates:
  - '/data/alertmanager/conf/templates/*.tmpl'
  EOF
  ```

  告警模版支持html格式的渲染

  + 格式示例一：

    ```bash
    tee /data/alertmanager/conf/templates/email.tmpl <<EOF
    
    {{ define "email.default.html" }}
    {{ range .Alerts }}
        {{ if  eq .Status "firing" }}
            <span style="background-color:red">[{{.Status}}]</span>| {{ .Annotations.summary }} <br>
            告警级别: {{ .Labels.severity }} 级<br>
            告警名称: {{ .Labels.alertname }} <br>
            告警主机: {{ .Labels.instance }} <br>
            告警详情: {{ .Annotations.description }} <br>
            触发时间: {{ .StartsAt.Format "2006-01-02 15:04:05" }} <br>
    
        {{ else if eq .Status "resolved"  }}
            <span style="background-color:green">[{{.Status}}]</span>  {{ .Annotations.summary }} 已恢复正常<br>
            告警级别: {{ .Labels.severity }} 级<br>
            告警名称: {{ .Labels.alertname }} <br>
            告警主机: {{ .Labels.instance }} <br>
            告警详情: {{ .Annotations.description }} <br>
            恢复时间: {{ .StartsAt.Format "2006-01-02 15:04:05" }} <br>
        {{ end }}
    {{ end }}
    {{ end }}
    
    EOF
    ```

    模版效果

    

    ![email01.png](/docs/prometheus/alertmanager/img/email01.png)

    ![email02.png](/docs/prometheus/alertmanager/img/email02.png)

  + 格式示例二：

    ```bash
    tee /data/alertmanager/conf/templates/email.tmpl <<EOF
    
    {{ define "email.default.html" }}
    <table border=1>
        <th>告警来源</th>
        <th>告警级别</th>
        <th>告警名称</th>
        <th>告警主机</th>
        <th>告警主题</th>   
        <th>告警详情</th>
        <th>触发时间</th>
        {{ range .Alerts }}
        <tr>
            <td>prometheus_alert</td>
            <td>{{ .Labels.severity }}</td>
            <td>{{ .Labels.alertname }} </td>
            <td>{{ .Labels.instance }}</td>
            <td>{{ .Annotations.summary }}</td>
            <td>{{ .Annotations.description }}</td>
            <td>{{ .StartsAt.Format "2006-01-02 15:04:05" }}</td>
        </tr>
        {{ end }}
    </table>
    {{ end }}
    EOF
    ```

    模版效果

    ![email03](/docs/prometheus/alertmanager/img/email03.png)

    

    ![email04.png](/docs/prometheus/alertmanager/img/email04.png)

    

- [x] [wechart](https://prometheus.io/docs/alerting/latest/configuration/#wechat_config)

  ```bash
  tee /data/alertmanager/conf/alertmanager.yml <<EOF
  
  global:
    # The smarthost 
    smtp_smarthost: 'smtp.qq.com:465'
    # from who send email
    smtp_from: '810654947@qq.com'
    smtp_auth_username: '810654947@qq.com'
    smtp_auth_password: 'kqaexaxpbrbdbajd'
    #
    smtp_require_tls: false
  route:
    receiver: 'wechat'
    group_by: ['alertname','cluster']
    group_wait: 30s
    group_interval: 5m
    
  receivers:
  - name: 'email'
    email_configs:
    - to: '810654947@qq.com'
      send_resolved: true
  
  - name: 'wechat'
    wechat_configs:
    # 企业ID。我的企业--企业信息中查看
    - corp_id: 'wwa5d04854e39e7784'
      # 应用ID。应用管理
      agent_id: '1000002'
      # 应用secret。应用管理
      api_secret: 'Rc8nQbF8EiCvO1JP19S9vceTI4LJaNt-j-H1pCBba2U'
      # 发送给谁
      to_user: "@all"
      # 发送给哪个部门。部门ID， 在通讯录中查看
      to_party: '2'
  templates:
  - '/data/alertmanager/conf/templates/*.tmpl'
  EOF
  ```

  ```bash
  tee /data/alertmanager/conf/templates/wechat.tmpl <<EOF
  {{ define "wechat.default.message" }}
  状态: {{ .Status }}
  {{ range .Alerts }}
  ==============监控报警==============
  告警程序: prometheus_alert
  告警级别: {{ .Labels.severity }}
  告警名称: {{ .Labels.alertname }}
  告警主机: {{ .Labels.instance }}
  告警主题: {{ .Annotations.summary }}
  告警详情: {{ .Annotations.description }}
  触发事件: {{ .StartsAt.Format "2006-01-02 15:04:05" }}
  {{ end }}
  {{ end }}
  EOF
  ```

  

- [x] dingtalk

  ```bash
  tee /data/alertmanager/conf/alertmanager.yml <<EOF
  
  global:
    # The smarthost 
    smtp_smarthost: 'smtp.qq.com:465'
    # from who send email
    smtp_from: '810654947@qq.com'
    smtp_auth_username: '810654947@qq.com'
    smtp_auth_password: 'kqaexaxpbrbdbajd'
    #
    smtp_require_tls: false
  route:
    receiver: 'dingtalk'
    group_by: ['alertname','cluster']
    group_wait: 30s
    group_interval: 5m
    
  receivers:
  - name: 'email'
    email_configs:
    - to: '810654947@qq.com'
      send_resolved: true
  
  - name: 'wechat'
    wechat_configs:
    # 企业ID。我的企业--企业信息中查看
    - corp_id: 'wwa5d04854e39e7784'
      # 应用ID。应用管理
      agent_id: '1000002'
      # 应用secret。应用管理
      api_secret: 'Rc8nQbF8EiCvO1JP19S9vceTI4LJaNt-j-H1pCBba2U'
      # 发送给谁
      to_user: "@all"
      # 发送给哪个部门。部门ID， 在通讯录中查看
      to_party: '2'
  
  - name: 'dingtalk'
    webhook_configs:
    - url: 'http://127.0.0.1:8060/dingtalk/webhook1/send'
    
  templates:
  - '/data/alertmanager/conf/templates/*.tmpl'
  EOF
  ```

  安装钉钉webhook

  > ```bash
  > wget https://raw.githubusercontent.com/timonwong/prometheus-webhook-dingtalk/main/web/ui/react-app/src/pages/PlaygroundDemoAlert.json
  > 
  > # 测试prometheus-webhook-dingtalk 是否可以使用
  > [root@master prometheus]# curl -X POST -d'@PlaygroundDemoAlert.json' http://10.4.7.10:8060/dingtalk/webhook1/send 
  > OK
  > ```

  ```bash
  mkdir /data/dingtalk/{bin,conf,conf/templates} -p
  ```

  ```bash
  tee /data/dingtalk/conf/config.yml <<EOF
  templates:
  - "/prometheus-webhook-dingtalk/templates/*.tmpl"
  targets:
    webhook1:
      url: https://oapi.dingtalk.com/robot/send?access_token=2a8703f74d0960dd8effc6b846c7473520363e4c171fbdfa044b586df3e29be0
      # secret for signature
      secret: SEC2475a4ecdfae996614c6310b18bf948ce95b4c5df306cf75b2842b7a061bba43
      message:  
        text: '{{ template "ding.link.content" . }}'
  EOF
  ```

  ```bash
  tee /data/dingtalk/bin/start.sh <<EOF
  docker rm -f dingtalk
  docker run --name dingtalk -d \
  --restart=always \
  -p8060:8060 \
  -v /usr/share/zoneinfo/Asia/Shanghai:/etc/localtime \
  -v /data/dingtalk/conf/config.yml:/prometheus-webhook-dingtalk/config.yml \
  -v /data/dingtalk/conf/templates:/prometheus-webhook-dingtalk/templates \
  timonwong/prometheus-webhook-dingtalk:v2.0.0 \
  --config.file=/prometheus-webhook-dingtalk/config.yml \
  --web.enable-ui \
  --web.enable-lifecycle \
  --log.level=debug
  EOF
  ```

  ```bash
  http://192.168.0.161:8060/ui
  ```

  

  格式示例一：

  > 修改后重启webhook 

  ```bash
  tee /data/dingtalk/conf/templates/dingtalk.tmpl <<EOF
  {{ define "ding.link.content" }}
  状态: {{ .Status }}
  {{ range .Alerts }}
  ==============监控报警==============
  
  告警程序: prometheus_alert
  
  告警级别: {{ .Labels.severity }}
  
  告警名称: {{ .Labels.alertname }}
  
  告警主机: {{ .Labels.instance }}
  
  告警主题: {{ .Annotations.summary }}
  
  告警详情: {{ .Annotations.description }}
  
  触发事件: {{ .StartsAt.Format "2006-01-02 15:04:05" }}
  
  {{ end }}
  {{ end }}
  EOF
  ```

  格式示例二：

  > 修改后重启webhook 

  ```bash
  tee /data/dingtalk/conf/templates/dingtalk.tmpl <<EOF
  {{ define "ding.link.content" }}
  状态: {{ .Status }}
  {{ range .Alerts }}
  ==============监控报警==============
  
    | 告警程序         | 告警级别               | 告警名称                | 告警主机               | 告警主题                   | 告警详情                       | 告警时间                                     |
    | ---------------- | ---------------------- | ----------------------- | ---------------------- | -------------------------- | ------------------------------ | -------------------------------------------- |
    | prometheus_alert | {{ .Labels.severity }} | {{ .Labels.alertname }} | {{ .Labels.instance }} | {{ .Annotations.summary }} | {{ .Annotations.description }} | {{ .StartsAt.Format "2006-01-02 15:04:05" }} |
  
  {{ end }}
  {{ end }}
  EOF
  ```

  格式示例三：

  > 修改后重启webhook 
  


  ```bash
  tee /data/dingtalk/conf/templates/dingtalk.tmpl <<EOF
  {{ define "ding.link.content" }}
  ![](https://img1.baidu.com/it/u=1546227440,2897989905&fm=253&fmt=auto&app=138&f=JPEG?w=889&h=500)
  
  {{ range .Alerts }}
  ## 【{{ .Status }}】
  ---
  >【告警主题】<br> {{ .Annotations.summary }} 
  ---
  >【告警描述】<br> {{ .Annotations.description }}
  ---
  >【触发时间】{{ .StartsAt.Format "2006-01-02 15:04:05" }}
  ---
  [查看详情](http://baidu.com)
  
  ---
  
  {{ end }}
  {{ end }}
  EOF
  ```

  ![dingtalk](/docs/prometheus/alertmanager/img/dingtalk.png)

- [ ] message

 



### 高可用


> 集群间通过 gossip协议 管理成员和检测成员故障，集群成员默认通过`9094` 通讯，客户端通过`9093` 与alertmanager 通讯。
>
> 集群成员间并不存在主节点，所有节点对等，`alertmanager.yml` 配置文件内容相同，即使是3个节点的集群中2个成员都宕机也不影响功能

**节点1：**

```bash
tee /usr/lib/systemd/system/alertmanager.service <<EOF
[Unit]
Description=alertmanager service https://prometheus.io/
After=network.target

[Service]
ExecStartPre=/data/alertmanager/bin/amtool check-config /data/alertmanager/conf/alertmanager.yml

ExecStart=/data/alertmanager/bin/alertmanager \
--config.file=/data/alertmanager/conf/alertmanager.yml \
--storage.path="/data/alertmanager/data" \
--data.retention=120h \
--web.listen-address=":9093" \
--cluster.listen-address="0.0.0.0:9094" \
--cluster.peer 10.4.7.251:9094 \
--cluster.peer 10.4.7.252:9094 \
--cluster.peer 10.4.7.253:9094

User=prometheus
[Install]
WantedBy=multi-user.target
EOF
```

**节点2：**

```bash
tee /usr/lib/systemd/system/alertmanager.service <<EOF
[Unit]
Description=alertmanager service https://prometheus.io/
After=network.target

[Service]
ExecStartPre=/data/alertmanager/bin/amtool check-config /data/alertmanager/conf/alertmanager.yml

ExecStart=/data/alertmanager/bin/alertmanager \
--config.file=/data/alertmanager/conf/alertmanager.yml \
--storage.path="/data/alertmanager/data" \
--data.retention=120h \
--web.listen-address=":9093" \
--cluster.listen-address="0.0.0.0:9094" \
--cluster.peer 10.4.7.251:9094 \
--cluster.peer 10.4.7.252:9094 \
--cluster.peer 10.4.7.253:9094

User=prometheus
[Install]
WantedBy=multi-user.target
EOF
```

**节点3：**

```bash
tee /usr/lib/systemd/system/alertmanager.service <<EOF
[Unit]
Description=alertmanager service https://prometheus.io/
After=network.target

[Service]
ExecStartPre=/data/alertmanager/bin/amtool check-config /data/alertmanager/conf/alertmanager.yml

ExecStart=/data/alertmanager/bin/alertmanager \
--config.file=/data/alertmanager/conf/alertmanager.yml \
--storage.path="/data/alertmanager/data" \
--data.retention=120h \
--web.listen-address=":9093" \
--cluster.listen-address="0.0.0.0:9094" \
--cluster.peer 10.4.7.251:9094 \
--cluster.peer 10.4.7.252:9094 \
--cluster.peer 10.4.7.253:9094

User=prometheus
[Install]
WantedBy=multi-user.target
EOF
```

### 部署在k8s环境
> https://github.com/turnbullpress/prometheusbook-code/blob/master/12-13/alertmanager.yml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: alertmanager-webui
  namespace: monitoring
  labels:
    app: alertmanager
    component: core
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9093"
    external-dns.alpha.kubernetes.io/hostname: alertmanager.quicknuke.com.
spec:
  type: LoadBalancer
  ports:
    - port: 9093
      name: metrics
  selector:
    app: alertmanager
    component: core
---
apiVersion: v1
kind: Service
metadata:
  name: alertmanager
  namespace: monitoring
  labels:
    app: alertmanager
    component: core
spec:
  ports:
  - port: 9093
    name: cluster
  type: ClusterIP
  clusterIP: None
  selector:
    app: alertmanager
    component: core
---
apiVersion: apps/v1beta2
kind: StatefulSet
metadata:
  name: alertmanager
  namespace: monitoring
  labels:
    app: alertmanager
    component: core
spec:
  updateStrategy:
    type: RollingUpdate
  replicas: 3
  selector:
    matchLabels:
      app: alertmanager
      component: core
  serviceName: alertmanager
  template:
    metadata:
      labels:
        app: alertmanager
        component: core
    spec:
      containers:
      - name: alertmanager
        image: quay.io/prometheus/alertmanager:master
        imagePullPolicy: IfNotPresent
        command:
        - "sh"
        - "-c"
        args:
        - /bin/alertmanager
            --config.file=/etc/alertmanager/config.yml
            --web.listen-address=0.0.0.0:9093
            --cluster.listen-address=0.0.0.0:8001
            --storage.path=/alertmanager
            --cluster.peer="alertmanager-0.alertmanager.monitoring.svc:8001"
            --cluster.peer="alertmanager-1.alertmanager.monitoring.svc:8001"
            --cluster.peer="alertmanager-2.alertmanager.monitoring.svc:8001"
            --log.level=debug
        ports:
        - containerPort: 9093
          name: web
          protocol: TCP
        - containerPort: 8001
          name: cluster
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /api/v1/status
            port: web
            scheme: HTTP
          failureThreshold: 10
        readinessProbe:
          failureThreshold: 10
          httpGet:
            path: /api/v1/status
            port: web
            scheme: HTTP
          initialDelaySeconds: 3
          periodSeconds: 5
          successThreshold: 1
          timeoutSeconds: 3
        volumeMounts:
        - name: alertmanager-config-volume
          mountPath: /etc/alertmanager/
        - name: alertmanager-data-volume
          mountPath: /alertmanager/
      volumes:
      - name: alertmanager-config-volume
        configMap:
          name: alertmanager-server-conf
      - name: alertmanager-data-volume
        emptyDir: {}
```