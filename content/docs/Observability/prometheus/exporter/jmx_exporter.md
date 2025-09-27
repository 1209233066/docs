---
title: "jmx_exporter"
linkTitle: "jmx_exporter"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 53
description: >
  jmx_exporter|exporter|prometheus

tags: ["prometheus","exporter","jmx_exporter"]
categories: ["prometheus","监控","exporter"]
url: prometheus/exporter/jmx_exporter.html
---

1. [部署安装](https://github.com/prometheus/jmx_exporter)

   ```bash
   # 下载地址1： https://github.com/prometheus/jmx_exporter/tree/release-0.20.0
   # 下载地址2： https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/
   
   wget https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/1.0.1/jmx_prometheus_javaagent-1.0.1.jar
   ```

   

   配置文件：

   ```bash
   tee javaagent.yaml <<EOF
   rules:
   - pattern: ".*"
   EOF
   ```

   以javaagent方式启动

   ```bash
   java -jar -Duser.timezone=Asia/Shanghai \
   -javaagent:jmx_prometheus_javaagent-1.0.1.jar=$(hostname -i):${M_PORT:-"12345"}:javaagent.yaml \
   <yourjar>
   ```

2. 添加prometheus配置

3. 常用指标

   ```bash
   # 堆内存使用量
   jvm_memory_used_bytes{area="heap"}
   # 堆内存提交量
   jvm_memory_committed_bytes{area="heap"}
   # 堆内存最大可用量
   jvm_memory_max_bytes{area="heap"}
   ```

   ```bash
   # Young GC 触发次数
   jvm_gc_collection_seconds_count{gc="G1 Young Generation"}
   #  Old GC 总耗时
   jvm_gc_collection_seconds_sum{gc="G1 Old Generation"}
   ```

   ```bash
   # 当前活动线程数
   jvm_threads_current
   # 守护线程数
   jvm_threads_daemon
   #  峰值线程数
   jvm_threads_peak
   ```

   ```bash
   # 总加载的类数量
   jvm_classes_loaded_total
   # 总卸载类数量
   jvm_classes_unloaded_total
   # 当前加载类数量
   jvm_classes_currently_loaded
   ```

   
