---
date: '2025-05-21T15:16:30+08:00'
draft: false
title: 'Hpa'
type: blog
toc_hide: false
hide_summary: true
weight: 5
description: >
  hpa|k8s
tags: ["hpa"]
categories: ["kubernetes"]
url: kubernetes/hpa.html
author: "wangendao"
---

![](https://rpic.origz.com/api.php?category=photography)

创建hpa配置文件
> kubectl autoscale deployment python --min=2 --max=5 --cpu-percent=80

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: python
  namespace: default
spec:
  maxReplicas: 5
  minReplicas: 2
  targetCPUUtilizationPercentage: 80
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: python
```

deployment 示例
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alpine
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: alpine
  template:
    metadata:
      labels:
        app: alpine
    spec:
      nodeName: hdss7-21.host.com
      containers:
      - name: alpine
        image: alpine
        imagePullPolicy: IfNotPresent
        command: ["sleep","10000"]
        resources:
          limits:
            cpu: 1000m
            memory: 1000Mi
          requests:
            cpu: 1000m
            memory: 1000Mi
```