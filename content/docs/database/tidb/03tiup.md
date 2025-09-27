---
date: '2025-05-20T20:53:33+08:00'
draft: false
title: 'tiup工具'
type: blog
toc_hide: false
hide_summary: true
weight: 4
description: >
  tiup|tidb
tags: ["tiup工具"]
categories: ["tidb"]
url: tidb/03tiup.html
author: "wangendao"
---

![](https://docs-download.pingcap.com/media/images/docs-cn/tidb-architecture-v6.png)

```bash
# 查看集群列表
tiup cluster list
# 查看集群每个组件的运行状态
tiup cluster display <cluster-name>
# 启动集群
tiup cluster start <cluster-name>
# -R 启动指定组件
tiup cluster start <cluster-name> -R pd
# -N 启动指定进程
tiup cluster start ${cluster-name} -N 1.2.3.4:2379,1.2.3.5:2379
# show-config 查看当前配置
tiup cluster show-config cluster01
# edit-config 在线编辑配置
tiup cluster edit-config cluster01
# 查看tiup仓库
tiup mirror  show
# 默认读取变量 ${TIUP_MIRRORS} 的值
tiup mirror set 
# 
tiup mirror merge
# 查看仓库中可用的包 , 查看已安装包 tiup list --installed
tiup list
```


https://docs.pingcap.com/zh/tidb/stable/maintain-tidb-using-tiup/