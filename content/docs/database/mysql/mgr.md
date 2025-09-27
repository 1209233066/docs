---
date: '2025-07-28T10:57:00+08:00'
draft: false
title: 'mgr'
type: blog
toc_hide: false
hide_summary: true
weight: 5
description: >
  MGR是 MySQL 官方提供的高可用、高一致性的分布式数据库解决方案
tags: ["mysql安装"]
categories: ["mysql"]
url: mysql/mgr.html
author: "wangendao"
---

MySQL Group Replication（MGR）是 MySQL 官方提供的高可用、高一致性的分布式数据库解决方案，基于原生 MySQL 实现多主/单主架构的同步复制。其核心原理是通过 Paxos 协议变种（Group Communication System, GCS） 实现节点间的数据强一致性，MGR和传统主从复制的本质区别——不是简单的异步复制改进，而是基于paxos的同步复制。

- 使用 **Paxos 分布式共识算法**（具体实现为 `XCom`）确保集群内节点状态一致。
- 所有事务需在组内**多数节点（N/2+1）** 确认后才提交（避免脑裂）。
- 通信基于 **MySQL 插件 `group_replication`** 实现。

```mermaid
graph LR
A[客户端发起事务] --> B[本地节点执行]
B --> C[生成Binlog Event]
C --> D[广播到组内所有节点]
D --> E[多数节点验证冲突]
E --> F{多数节点通过?}
F -->|Yes| G[提交事务并通知组]
F -->|No| H[回滚事务]
```
