---
title: ""
linkTitle: "prometheus"
date: 2025-05-12
simple_list: true
weight: 3
---



Prometheus是Go语言开发的开源监控和警报框架，遵循Apache 2.0许可协议。它起源于SoundCloud，并在2016年成为云原生计算基金会（CNCF）继Kubernetes之后的第二个项目。Prometheus不仅提供监控功能，还是一个时序[数据库](https://db-engines.com/en/ranking)。



本示例架构图

```nginx
        location /prom {
                proxy_pass http://127.0.0.1:9090;
        }

        location /alert {
                proxy_pass http://127.0.0.1:9093;
        }
        location /grafana {
                proxy_pass http://127.0.0.1:3000;
        }
```



```mermaid
flowchart LR
	A(nginx)
	B(prometheus)
	C(alertmanager)
	D(grafana)
	
	z>浏览器] --> A
	
	A -..->|/prom| B
	A -..->|/alert| C
	A -..->|/grafana| D
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#f66,stroke-width:2px,color:#fff,stroke-dasharray: 5 5
    style C fill:#bbf,stroke:#f66,stroke-width:2px,color:#fff,stroke-dasharray: 5 5
    style D fill:#bbf,stroke:#f66,stroke-width:2px,color:#fff,stroke-dasharray: 5 5
```
