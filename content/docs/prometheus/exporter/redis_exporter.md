---
title: "redis-exporter"
linkTitle: "redis-exporter"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 56
description: >
  redis-exporter|exporter|prometheus

tags: ["prometheus","exporter","redis-exporter"]
categories: ["prometheus","监控","exporter"]
url: prometheus/exporter/redis-exporter.html
---

1. **[部署安装](https://github.com/oliver006/redis_exporter)**

   ```bash
   docker run --name redis-exporter --net=host quay.io/oliver006/redis_exporter \
   --redis.addr=127.0.0.1:6379 \
   --redis.password='pytc@2023' \
   --connection-timeout=60000ms \
   --config-command=config \
   --web.listen-address=:9121
   ```

   ```bash
   docker run --name redis-exporter-sentinel --net=host quay.io/oliver006/redis_exporter \
   --redis.addr=10.4.7.10:26379 \
   --redis.password= \
   --connection-timeout=60000ms \
   --config-command=config \
   --web.listen-address=:9122
   ```

   

2. **添加prometheus配置**

3. **常用指标**

   

   **进程相关**

   |                           |          |      |      |
   | ------------------------- | -------- | ---- | ---- |
   | `redis_up`                |          |      |      |
   | `redis_uptime_in_seconds` | 启动时长 |      |      |
   | `redis_instance_info`     |          |      |      |

   **内存相关**
   
   |                                    |                |                                                              |
   | ---------------------------------- | -------------- | ------------------------------------------------------------ |
   | `redis_memory_used_bytes`          | 内存使用量     |                                                              |
   | `redis_memory_used_peak_bytes`     | 内存使用峰值   |                                                              |
   | `redis_memory_used_rss_bytes`      |                |                                                              |
   | `redis_memory_max_bytes`           | maxmemory      |                                                              |
   | `redis_config_maxmemory`           |                |                                                              |
   | `redis_memory_used_dataset_bytes`  |                |                                                              |
   | `redis_memory_used_lua_bytes`      |                |                                                              |
   | `redis_memory_used_scripts_bytes`  |                |                                                              |
   | `redis_memory_used_startup_bytes`  |                |                                                              |
   | `redis_memory_used_overhead_bytes` |                |                                                              |
   | `redis_allocator_rss_bytes`        | 分配出常驻内存 |                                                              |
   | `redis_active_defrag_running `     | 内存碎片整理   | 表示没有活动的defrag任务正在运行，1表示有活动的defrag任务正在运行 |
   | `redis_allocator_frag_ratio`       | 内存碎片比     | used_memory_rss和used_memory之间的比率，小于1表示使用了swap，大于1表示碎片比较多 |

   
   
   **网络流量相关**
   
   |                                |      |      |
   | ------------------------------ | ---- | ---- |
   | `redis_net_input_bytes_total`  |      |      |
   | `redis_net_output_bytes_total` |      |      |
   
   **持久化相关**
   
   |                                           |                   |      |
   | ----------------------------------------- | ----------------- | ---- |
   | `redis_aof_enabled `                      | 是否开启aof持久化 |      |
   | `redis_aof_last_cow_size_bytes`           |                   |      |
   | `redis_aof_last_rewite_duration_sec`      |                   |      |
   | `redis_aof_last_write_status`             |                   |      |
   | `redis_aof_last_bgrewrite_status`         |                   |      |
   | `redis_aof_rewite_in_progress`            |                   |      |
   | `redis_aof_rewite_shceduled`              |                   |      |
   | `redis_aof_current_rewrite_duration_sec ` | aof rewrite耗时   |      |
   
   |                                         |      |      |
   | --------------------------------------- | ---- | ---- |
   | `redis_rdb_bgsave_in_progress`          |      |      |
   | `redis_rdb_changes_since_last_save`     |      |      |
   | `redis_rdb_current_bgsave_duration_sec` |      |      |
   | `redis_rdb_last_bgsave_duration_sec`    |      |      |
   | `redis_rdb_last_bgsave_status`          |      |      |
   | `redis_rdb_last_cow_size_bytes`         |      |      |
   | `redis_rdb_last_save_timestamp_seconds` |      |      |
   
   
   
   **key相关**
   
   |                                  |              | 示例 |
   | -------------------------------- | ------------ | ---- |
   | `redis_db_keys`                  | 实例keys数量 |      |
   | `redis_db_avg_ttl_seconds`       | 平均过期时长 |      |
   | `redis_db_keys_expiring`         |              |      |
   | `redis_expired_keys_total`       |              |      |
   | `redis_expired_stale_percentage` |              |      |
   | `redis_evicted_keys_total`       |              |      |
   | `redis_keyspace_hits_total `     | 缓存命中量   |      |
   | `redis_keyspace_misses_total `   | 未命中缓存量 |      |
   
   ```bash
   sum(redis_keyspace_hits_total{cluster_id="123"})/sum(redis_keyspace_hits_total{cluster_id="123"})+sum(redis_keyspace_misses_total{cluster_id="123"})
   ```
   
   
   
   **客户端连接相关**
   
   |                                                            |      |      |
   | ---------------------------------------------------------- | ---- | ---- |
   | `redis_connected_clients`                                  |      |      |
   | `redis_connected_slaves`                                   |      |      |
   | `redis_config_maxclients`                                  |      |      |
   | `redis_rejected_connections_total`                         |      |      |
   | `redis_connections_received_total`                         |      |      |
   | `redis_blocked_clients`                                    |      |      |
   | `redis_client_recent_max_input_buffer_bytes`               |      |      |
   | `redis_client_recent_max_output_buffer_bytes`              |      |      |
   | `redis_config_client_output_buffer_limit_bytes`            |      |      |
   | `redis_config_client_output_buffer_limit_overcome_seconds` |      |      |
   
   **慢日志**
   
   |                         |      |      |
   | ----------------------- | ---- | ---- |
   | `redis_slowlog_last_id` |      |      |
   | `redis_slowlog_length`  |      |      |
   
   
   
   性能
   
   |                                              |                      |      |
   | -------------------------------------------- | -------------------- | ---- |
   | `redis_last_slow_execution_duration_seconds` | 最慢的执行耗时       |      |
   | `redis_commands_duration_seconds_total`      | 命令出来耗时         |      |
   | `redis_commands_processed_total`             | 已处理命令的数量     |      |
   | `redis_commands_total`                       | 每一个命令调用的次数 |      |
   
   tps
   
   QPS
   
   
   
   **主从复制相关**
   
   |                                         |      |      |
   | --------------------------------------- | ---- | ---- |
   | `redis_connected_slaves`                |      |      |
   | `redis_mem_clients_slaves`              |      |      |
   | `redis_repl_backlog_first_byte_offset`  |      |      |
   | `redis_repl_backlog_history_bytes`      |      |      |
   | `redis_repl_backlog_is_active`          |      |      |
   | `redis_replication_backlog_bytes`       |      |      |
   | `redis_replica_partial_resync_accepted` |      |      |
   | `redis_replica_partial_resync_denied`   |      |      |
   | `redis_replica_resyncs_full`            |      |      |
   | `redis_master_repl_offset`              |      |      |
   | `redis_second_repl_offset`              |      |      |
   
   
   
   ```bash
   #!/bin/bash
   
   startMasterSlave() { 
   docker run -d --net=host --name=redis6379 redis:6.0.20 redis-server --bind 10.4.7.10 --port 6379 --daemonize no
   docker run -d --net=host --name=redis6380 redis:6.0.20 redis-server --bind 10.4.7.10 --port 6380 --daemonize no  --SLAVEOF 10.4.7.10 6379
   docker run -d --net=host --name=redis6381 redis:6.0.20 redis-server --bind 10.4.7.10 --port 6381 --daemonize no  --SLAVEOF 10.4.7.10 6379
   }
   
   startSentinel() {
   for port in 26379 26380 26381;do
   
   docker run -d --net=host --name=sentinel${port} redis:6.0.20 sh -c "echo 'sentinel monitor mymaster 10.4.7.10 6379 2\n' >/etc/redis-sentinel.conf;echo 'sentinel down-after-milliseconds mymaster 30000\n' >>/etc/redis-sentinel.conf;echo 'sentinel parallel-syncs mymaster 1\n' >>/etc/redis-sentinel.conf;echo 'sentinel failover-timeout mymaster 180000\n' >>/etc/redis-sentinel.conf; redis-server /etc/redis-sentinel.conf --sentinel --bind 10.4.7.10 --port ${port} --daemonize no"
   
   done
   
   }
   
   stop(){
   docker rm -f sentinel26379
   docker rm -f sentinel26380
   docker rm -f sentinel26381
   docker rm -f redis6379
   docker rm -f redis6380
   docker rm -f redis6381
   }
   
   main(){
   stop
   startMasterSlave
   startSentinel
   }
   
   main
   ```
   
   
   
   ```bash
   root@master01:~# docker exec -it sentinel26379 redis-cli -p 26379 -h 10.4.7.10 info sentinel
   # Sentinel
   sentinel_masters:1
   sentinel_tilt:0
   sentinel_running_scripts:0
   sentinel_scripts_queue_length:0
   sentinel_simulate_failure_flags:0
   master0:name=mymaster,status=ok,address=10.4.7.10:6379,slaves=2,sentinels=3
   ```
   
   ```bash
   redis_sentinel_master_ckquorum_status
   ```
   
   

