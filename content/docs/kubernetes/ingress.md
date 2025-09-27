---
date: '2025-05-21T15:22:40+08:00'
draft: false
title: 'Ingress'
type: blog
toc_hide: false
hide_summary: true
weight: 4
description: >
  ingress|k8s
tags: ["ingress"]
categories: ["kubernetes"]
url: kubernetes/ingress.html
author: "wangendao"
---

![](https://rpic.origz.com/api.php?category=photography)

按照uri 执行路由

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: flask
  namespace: default
spec:
  rules:
  - host: test.com
    http:
      paths:
      - path: "/"
        backend:
          serviceName: flask
          servicePort: 80
      - path: "/index"
        backend:
          serviceName: index
          servicePort: 80
```

按照servicename执行路由

```yaml
apiVersion: extensions/v1beata1
kind: Ingress
metadata:
  name: flask
  namespace: default
spec:
  rules:
  - host: test.com
    http:
      paths:
      - path: "/"
        backend:
          serviceName: flask
          servicePort: 80
  - host: pro.com
    http:
      paths:
      - path: "/"
        backend:
           serviceName: index
           servicePort: 80
```

