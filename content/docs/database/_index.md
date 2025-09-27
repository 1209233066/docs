---
title: ""
linkTitle: "database"
date: 2025-05-20
simple_list: true
weight: 6
description: >
  database 文档中心
icon: fa-solid fa-database
type: blog
---

通常数据库需要服务器提供低延迟、高i/o的能力

开启服务器的性能优化
```bash
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```