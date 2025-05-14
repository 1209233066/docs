---
title: "prometheus-sdk"
linkTitle: "prometheus-sdk"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 99
description: >
  prometheus-sdk|exporter|prometheus

tags: ["prometheus","exporter","prometheus-sdk"]
categories: ["prometheus","监控","exporter"]
url: prometheus/exporter/prometheus-sdk.html
---

promethues 为用户提供了自定义开发exporter的[sdk](https://prometheus.io/docs/instrumenting/clientlibs/), 支持大多数常见语言。

{{< tabpane text=true right=false >}}
  {{% tab header="**sdk**:" disabled=true /%}}
  {{% tab header="python" lang="en" %}}
```python
#!/usr/bin/env python3
import http.server
from prometheus_client import start_http_server
from prometheus_client import Counter  #从prometheus_client 库导入 Counter

REQUESTS = Counter('hello_worlds_total','Hello Worlds requested.') # 定义`hello_worlds_total` 指标，帮助信息为'Hello Worlds requested.'

class MyHandler(http.server.BaseHTTPRequestHandler):
   def do_GET(self):
         REQUESTS.inc()  # 请求后自动+1
         self.send_response(200)
         self.end_headers()
         self.wfile.write(b"Hello World")


if __name__ == "__main__":
   start_http_server(8000)
   server = http.server.HTTPServer(('localhost', 8001), MyHandler)
   server.serve_forever()
```
  {{% /tab %}}
{{% tab header="golang" lang="go" %}}

```go
package main

import (
	"fmt"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"net/http"
)

func main() {
	var l = map[string]string{
		"app": "ping",
		"env": "pro",
	}

	var pingCounter = prometheus.NewCounter(
		prometheus.CounterOpts{
			Namespace:   "pay",
			Subsystem:   "wechart",
			Name:        "ping_request_count",
			Help:        "No of request handled by Ping handler",
			ConstLabels: l,
		},
	)

	var pingGuage = prometheus.NewGauge(
		prometheus.GaugeOpts{
			Namespace:   "pay",
			Subsystem:   "wechart",
			Name:        "ping_request_gauge",
			Help:        "No of request handled by Ping handler",
			ConstLabels: l,
		},
	)

	//http.HandleFunc
	http.HandleFunc("/ping", func(w http.ResponseWriter, req *http.Request) {
		pingCounter.Inc()
		pingGuage.Set(2.2)
		fmt.Fprint(w, "pong")
	})
	// 注册metrics
	prometheus.MustRegister(pingCounter)
	prometheus.MustRegister(pingGuage)

	http.Handle("/metrics", promhttp.Handler())
	//启动服务
	http.ListenAndServe(":9998", nil)
}
```
  {{% /tab %}}
{{< /tabpane >}}
