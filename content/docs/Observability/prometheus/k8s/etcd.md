---
title: "etcd"
linkTitle: "etcd"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 206
description: >
  exporter|prometheus

tags: ["prometheus","exporter","kubernetes"]
categories: ["prometheus","监控","exporter"]
url: prometheus/kubernetes/etcd.html
---

1. 部署安装

   参见部署k8s

   > <sub>【参数说明】</sub>
   >
   > <sub>snapshot-count  每50000次修改执行一次snapshot</sub>
   >
   > <sub>auto-compaction-retention  自动压缩，默认为 0 不开启</sub>
   >
   > <sub>max-request-bytes 单个请求最大字节，默认1.5MB</sub>
   >
   > <sub>quota-backend-bytes  指定数据库在磁盘上的配额大小，默认2GB</sub>
   >
   > <sub>heartbeat-interval leader向leaner发送心跳周期，默认 100ms</sub>
   >
   > <sub>election-timeout  选举超时,默认1s</sub>
   >
   > <sub>max-snapshots 最大保留快照数，默认 5 个</sub>

   

   ```bash
   ExecStart=/opt/kube/bin/etcd \
     --name=master3 \
     --cert-file=/etc/etcd/ssl/etcd.pem \
     --key-file=/etc/etcd/ssl/etcd-key.pem \
     --peer-cert-file=/etc/etcd/ssl/etcd.pem \
     --peer-key-file=/etc/etcd/ssl/etcd-key.pem \
     --trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
     --peer-trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
     --initial-advertise-peer-urls=https://10.4.7.12:2380 \
     --listen-peer-urls=https://10.4.7.12:2380 \
     --listen-client-urls=https://10.4.7.12:2379,http://127.0.0.1:2379 \
     --advertise-client-urls=https://10.4.7.12:2379 \
     --initial-cluster-token=etcd-cluster-0 \
     --initial-cluster=master1=https://10.4.7.22:2380,master2=https://10.4.7.21:2380,master3=https://10.4.7.12:2380 \
     --initial-cluster-state=new \
     --data-dir=/var/lib/etcd/ \
     --snapshot-count=50000 \
     --auto-compaction-retention=1 \
     --max-request-bytes=10485760 \
     --enable-v2=true \
     --quota-backend-bytes=8589934592
   Restart=always
   RestartSec=15
   LimitNOFILE=65535
   OOMScoreAdjust=-999
   ```

   

2. 添加prometheus配置

   

   ```yaml
     - job_name: 'etcd'
       tls_config:
         ca_file: /etc/kubernetes/pki/etcd/ca.crt
         cert_file: /etc/kubernetes/pki/etcd/peer.crt
         key_file: /etc/kubernetes/pki/etcd/peer.key
       scheme: https
       static_configs:
       - targets:
         - '192.168.0.244:2379'
   ```
   
   
   
3. [监控指标](https://etcd.io/docs/v3.6/metrics/)

   > ```bash
   > curl \
   > --cacert /etc/kubernetes/pki/etcd/ca.crt \
   > --cert /etc/kubernetes/pki/etcd/peer.crt \
   > --key /etc/kubernetes/pki/etcd/peer.key \
   > https://10.4.7.12:2379/metrics
   > ```
   
   
   
   指标主要包含 ：
   
   + **Server**相关，所有指标以`etcd_server` 开头。
   + **Disk**相关，所有指标以`etcd_disk 开头
   + **Network**相关，所有指标以`etcd_network` 开头
   + **mvcc**相关 ，所有指标以`etcd_mvcc` 开头
   + **snap**相关，所有指标以`etcd_snap` 开头
   + **degugging**相关，所有指标以`etcd_degugging` 开头
   
   **Server**相关，所有指标以`etcd_server` 开头
   
   | 名称                                    | 描述                                   | 类型    |
   | --------------------------------------- | -------------------------------------- | ------- |
   | `etcd_server_has_leader`                | 是否存在leader。1表示存在，0表示不存在 | Gauge   |
   | `etcd_server_leader_changes_seen_total` | 主从切换的总次数                       | Counter |
   | `etcd_server_proposals_committed_total` | 协商一致提交的请求                     | Counter |
   | `etcd_server_proposals_applied_total`   | 协商一致处理的请求                     | Counter |
   | `etcd_server_proposals_pending`         | 排队等待提交的提案数量                 | Gauge   |
   | `etcd_server_proposals_failed_total`    | 失败的提案                             | Counter |
   | `etcd_server_quota_backend_bytes`       | 数据库配额（磁盘）                     | Gauge   |
   
   **Disk**相关，所有指标以`etcd_disk 开头
   
   | 名称                                        | 描述                     | 类型      |
   | ------------------------------------------- | ------------------------ | --------- |
   | `etcd_disk_wal_fsync_duration_seconds`      | wal 写入磁盘延迟时长     | Histogram |
   | etcd_disk_`backend_commit_duration_seconds` | 增量快照写入磁盘延迟时长 | Histogram |
   
   | 名称                                       | 描述       | 类型  |
   | ------------------------------------------ | ---------- | ----- |
   | `etcd_debugging_mvcc_keys_total`           | key数量    | Gauge |
   | etcd_debugging_mvcc_db_total_size_in_bytes | 数据库大小 | Gauge |
   
   
   
   **Network**相关，所有指标以`etcd_network` 开头
   
   | 名称                                           | 描述                                                         | 类型          |
   | ---------------------------------------------- | ------------------------------------------------------------ | ------------- |
   | peer_sent_bytes_total                          | The total number of bytes sent to the peer with ID `To`.     | Counter(To)   |
   | peer_received_bytes_total                      | The total number of bytes received from the peer with ID `From`. | Counter(From) |
   | peer_sent_failures_total                       | The total number of send failures from the peer with ID `To`. | Counter(To)   |
   | peer_received_failures_total                   | The total number of receive failures from the peer with ID `From`. | Counter(From) |
   | peer_round_trip_time_seconds                   | Round-Trip-Time histogram between peers.                     | Histogram(To) |
   | client_grpc_sent_bytes_total                   | The total number of bytes sent to grpc clients.              | Counter       |
   | client_grpc_received_bytes_total               | The total number of bytes received to grpc clients.          | Counter       |
   | process_open_fds                               | Number of open file descriptors.                             | Gauge         |
   | process_max_fds                                | Maximum number of open file descriptors.                     | Gauge         |
   | etcd_server_proposals_applied_total            | 接收到的客户端请求                                           | Counter       |
   | etcd_server_etcd_network_peer_sent_bytes_total | etcd 成员之间发送的请求                                      | Counter       |
   | etcd_server_etcd_network_peer_latency_seconds  | etcd 成员之间网络延迟                                        | Gauge         |
   
   
   
   

4. 告警规则

   ```yaml
   - name: "Etcd"
     rules:
     # 主从切换
     - alert: "EtcdLeaderSwitch"
       expr: etcd_server_is_leader != etcd_server_is_leader offset 10m
       for: "5m"
       labels:
         app: etcd
         severity: "warnning"
       annotations: 
         summary: "Etcd Role changes"
         description: "{{ $labels.instace }}'s Role changes before 10 minute,now is {{ $value }}."
     # 宕机    
     - alert: "EtcdDown"
       expr: up{job=~".*etcd.*"} == 0
       for: "5m"
       labels:
         app: etcd
         severity: "critical"
       annotations: 
         summary: "Etcd is down "
         description: "{{ $labels.instace }} is down for more than 5 minute."
     # 缺少leader    
     - alert: "EtcdNoLeader"
       expr: etcd_server_has_leader == 0 
       for: "5m"
       labels:
         app: etcd
         severity: "critical"
       annotations:
         summary: "Etcd no leader"
         description: "{{ $labels.instace }} no leader for more than 5 minute."
   ```






[etcd 问题、调优、监控 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/466274302)

[etcd 原理解析：读《etcd 技术内幕》 | Vermouth | 博客 | docker | k8s | python | go | 开发 (xuyasong.com)](http://www.xuyasong.com/?p=1706)







