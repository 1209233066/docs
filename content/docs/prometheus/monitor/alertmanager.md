---
title: "alertmanager"
linkTitle: "alertmanager"
date: 2025-05-12
simple_list: true
weight: 102
tags: ["prometheus","exporter","alertmanager"]
categories: ["prometheus","exporter"]
url: prometheus/monitor/alertmanager.html
---

```yaml
  - job_name: alertmanager
    scrape_path: "/alert/metrics"
    static_configs:
    - targets:
      - 127.0.0.1:9093
```

