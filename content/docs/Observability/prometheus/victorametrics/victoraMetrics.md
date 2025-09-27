---
title: "victoriaMetrics"
linkTitle: "victoriaMetrics"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 2
description: >
  victoriaMetrics|prometheus

tags: ["prometheus","victoriaMetrics"]
categories: ["prometheus","victoriaMetrics"]
url: prometheus/victoriaMetrics/victoriaMetrics.html
---


[doc](https://docs.victoriametrics.com/)

## VictoriaMetrics

系统选型，硬件规划，容量规划（磁盘、内存、带宽）

**文件系统： 建议选择ext4**

> 如果您计划在 ext4 分区上存储超过 1TB 的数据或计划将其扩展到 16TB 以上，则建议将以下选项传
>
> ```bash
> # -O 64bit：启用64位文件系统特性，这允许文件系统支持大于2TB的文件和大于1EB的文件系统。
> # -O huge_file：启用大文件特性，这允许文件系统支持大于2TB的文件。
> # -O extent：启用扩展分配特性，这可以提高文件系统的效率，特别是在处理大文件时
> # -T huge 选项指定了文件系统的类型
> mkfs.ext4 ... -O 64bit,huge_file,extent -T huge
> ```

### 简介

`VictoriaMetrics`是一个兼容*prometheus*的监控解决方案和分布式时序数据库。相比于*prometheus*、*thanos*具有*速度快*、*资源占用量低*、*可扩展*等特征。

**版本：**

+ 分为企业版和社区版。企业版支持[TLS](https://docs.victoriametrics.com/lts-releases/)版本，社区版建议升级到最新版本。

  <table>
      <tr>
          <th>版本</th>
          <th>链接</th>
     </tr>
      <tr>
          <td>1.110.x</td>
          <td> https://github.com/VictoriaMetrics/VictoriaMetrics/releases/tag/v1.110.7</td>
      </tr>
      <tr>
          <td>1.102.x</td>
          <td>https://github.com/VictoriaMetrics/VictoriaMetrics/releases/tag/v1.102.20</td>
      </tr>
  </table>

**主要功能:**

+ 时序数据库。长期存储prometheus 指标，直接对接grafana。
+ 统一视图。支持多个promethues 对接到victorametrics中统一查询。
+ 简单易用
  1. 启动文件是一个没有任何依赖的go编译文件
  2. 配置完全支持命令行参数
  3. 支持兼容promQL 的的查询语言
+ 易扩展。微服务开发，集群化部署。支持对单个/多个组件水平扩展。
+ 支持多种方式数据抓取、采集和回填方式：
  1. 兼容`promethues exporter` 格式指标，[exporter可以直接对接victoria](https://docs.victoriametrics.com/#how-to-scrape-prometheus-exporters-such-as-node-exporter)
  2. [支持prometheus 远程写入](https://docs.victoriametrics.com/#prometheus-setup)
  3. 兼容prometheus 格式的数据导入[doc](https://docs.victoriametrics.com/#how-to-import-data-in-prometheus-exposition-format)
+ 支持标签[relabeling](https://docs.victoriametrics.com/#relabeling)



**优势：**

1. 内存占用更小

   It [uses 10x less RAM than InfluxDB](https://medium.com/@valyala/insert-benchmarks-with-inch-influxdb-vs-victoriametrics-e31a41ae2893) and [up to 7x less RAM than Prometheus, Thanos or Cortex](https://valyala.medium.com/prometheus-vs-victoriametrics-benchmark-on-node-exporter-metrics-4ca29c75590f) when dealing with millions of unique time series (aka [high cardinality](https://docs.victoriametrics.com/FAQ.html#what-is-high-cardinality)).

2. 更高的数据压缩比

   It provides high data compression, so up to 70x more data points may be stored into limited storage comparing to TimescaleDB according to [these benchmarks](https://medium.com/@valyala/when-size-matters-benchmarking-victoriametrics-vs-timescale-and-influxdb-6035811952d4) and up to 7x less storage space is required compared to Prometheus, Thanos or Cortex according to [this benchmark](https://valyala.medium.com/prometheus-vs-victoriametrics-benchmark-on-node-exporter-metrics-4ca29c75590f).

   

**组件：**

在VictoriaMetrics 生态中包括以下成员：

+ victoria-metrics : victorias的时序数据库
+ [vmagent](https://docs.victoriametrics.com/vmagent/)：服务发现、指标采集服务
+ [vmalert](https://docs.victoriametrics.com/vmalert/) ：告警和规则评估服务
+ [vmalert-tool](https://docs.victoriametrics.com/vmalert-tool/): 校验告警和规则语法的工具
+ [vmauth](https://docs.victoriametrics.com/vmauth/)：是一个http代理。提供认证、路由、负载均衡的功能
+ [vmgateway](https://docs.victoriametrics.com/vmgateway/)：多租户下提供租户限速服务
+ [vmctl](https://docs.victoriametrics.com/vmctl/) ：数据迁移和合并工具
+ [vmbackup](https://docs.victoriametrics.com/vmbackup/), [vmrestore](https://docs.victoriametrics.com/vmrestore/) and [vmbackupmanager](https://docs.victoriametrics.com/vmbackupmanager/) ：数据备份和还原工具



### 快速开始



+ **部署[victoriaMetrics](https://docs.victoriametrics.com/Quick-Start.html)**

  > 功能实现： 启动单实例victoriaMetrics, 并将node-exporter中指标存储到victoria中
  >
  > 监听端口 8428
  >
  > 参数解释：
  >
  > + `-storageDataPath`数据文件默认存储在当前工作目录中`./victoria-metrics-data`
  > + `-retentionPeriod`数据保存周期默认30d
  > + `-promscrape.config.strictParse` 必须严格遵守promethues.yaml 规则，主要用于校验`-promscrape.config` 参数指定的配置文件。默认为true
  > + `-promscrape.config` 指定抓取exporter的配置文件

  **二进制方式**

  

  ```bash
  wget https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.79.13/victoria-metrics-linux-amd64-v1.79.13.tar.gz
  
  tar xf victoria-metrics-linux-amd64-v1.79.13.tar.gz
  ```

  ```bash
  mkdir /opt/victoria-metrics/{bin,conf,data} -p
  useradd victoria -s /usr/sbin/nologin
  cp victoria-metrics-prod  /opt/victoria-metrics/bin/
  chown -R victoria:victoria  /opt/victoria-metrics
  ```

  

  > `-storageDataPath=/opt/victoria-metrics/data ` 数据存储目录
  >
  > `-retentionPeriod=1d ` 保留存储的数据。默认31d, 最短1d

  ```bash
  tee /usr/lib/systemd/system/victoria.service <<'EOF'
  [Unit]
  Description=victoria service https://victoriametrics.com/
  After=network.target
  
  [Service]
  
  ExecStart=/opt/victoria-metrics/bin/victoria-metrics-prod \
  -storageDataPath=/opt/victoria-metrics/data \
  -retentionPeriod=1d \
  -promscrape.config.strictParse=false \
  -promscrape.config=/etc/victoria-metrics/scrape.yml
  
  User=victoria
  [Install]
  WantedBy=multi-user.target
  EOF
  ```

  采集*node-exporter*指标

  ```bash
  tee /etc/victoria-metrics/scrape.yml<<EOF
  scrape_configs:
  - job_name: pcloudcore
    honor_labels: true
    honor_timestamps: true
    scrape_interval: 30s
    scrape_timeout: 10s
    metrics_path: /metrics
    scheme: http
    follow_redirects: true
    enable_http2: true
    static_configs:
    - targets:
      - 127.0.0.1:9100
  ```

  

  ```bash
  systemctl daemon-reload
  systemctl enable victoria --now
  ```

  <span style="color:red">截止到这里victoriaMetrics 已经可以正常工作了，访问http://xxxx:8428验证功能</span>

+ **对接prometheus** <sub>prometheus版本 v2.12.0+</sub>

  > <font color=orange size=5px>[info]</font>
  >
  > 1. promethues远程写入会导致promethues内存使用 上浮25%左右
  >
  > 2. 对于高负载的 Prometheus 实例（每秒 200k+ 个样本），可以应用以下调整：
  >
  >    <sub>`queue_config` 字段，用于配置 `remote_write` 的发送队列:<br><br>`max_samples_per_send`: 一个 HTTP 请求中包含的最大样本数，默认值为 `0`，表示没有限制。如果远程写入端点要求HTTP请求能够包含有限数量的样本，则可以设置此项。当超过指定数量时，Prometheus 会自动将队列中的数据拆分成多个请求来发送。<br><br>`capacity`: 发送队列的最大缓存容量。当队列中的样本数量超过此值时，Prometheus 将会阻塞新的写入操作，直到队列中的样本数量下降到可接受的范围内。注意，队列满了时不会丢弃数据，而是会将新写入的数据缓存起来，等待队列有足够容量之后再进行发送。<br><br>`max_shards`: 配置发送队列线程池中最大的线程数，默认值为 `1`。当 `remote_write` 并发写入的数量较大时，可以将此值调大，以便更快地处理写入请求。</sub>
  >
  >    需要注意的是，队列中的数据可能会占用的内存较大，因此需要根据实际情况仔细考虑合理的配置。在实际使用时，应根据数据规模、写入速度、服务器资源等因素逐步调整参数，以平衡发送队列的性能和稳定性。
  >
  >    ```yaml
  >    remote_write:
  >      - url: http://<victoriametrics-addr>:8428/api/v1/write
  >        queue_config:
  >          max_samples_per_send: 10000
  >          capacity: 20000
  >          max_shards: 30
  >    ```

  

  1. 为promethues添加全局标签（多个prometheus向同一victorametrics远程写入数据时）

     ```yaml
     global:
       external_labels:
         datacenter: dc-123
     ```

     

  2. 增加远程写入

     ```yaml
     # promethues.yml 中开启远程写入
     remote_write:
       - url: http://<victoriametrics-addr>:8428/api/v1/write
     ```

     

  

+ **对接grafana**

  ```bash
  # 数据源选择prometheus，地址填写
  http://<victoriametrics-addr>:8428
  ```




### [集群架构](https://docs.victoriametrics.com/Cluster-VictoriaMetrics.html)

集群模式支持单体架构的所有功能，同时**支持多租户**的功能。考虑到架构复杂度，官方建议指标采集率在 100w/s 时，可以使用单体架构。

#### 架构图

VictoriaMetrics 集群由以下服务组成：

- `vmstorage`- 存储原始数据，并返回给定标签过滤器在给定时间范围内查询的数据
- `vminsert`- 接受摄取的数据，并根据指标名称及其所有标签的一致哈希值将其分布在节点之间`vmstorage`
- `vmselect`- 通过从所有配置的节点获取所需的数据来执行传入查询`vmstorage`



![img](https://docs.victoriametrics.com/victoriametrics/Cluster-VictoriaMetrics_cluster-scheme.webp)



#### 安装部署



>  <font color=orange size=5px>[info]</font>
>
>  <sub>victoraMetrics 属于io密集型应用，[官方建议使用ext4 文件系统](https://docs.victoriametrics.com/BestPractices.html),如果计划存储超过1TB 文件系统格式化时添加一下参数：</sub>
>
>  <sub>`mkfs.ext4 ... -O 64bit,huge_file,extent -T huge`<br>例如：<br>
>  `lvcreate -n test -L 1g data`<br>
>  `mkfs.ext4 /dev/data/test -O 64bit,huge_file,extent -T huge`</sub>



| 主机名           | ip            | 服务(端口)                                                   |
| ---------------- | ------------- | ------------------------------------------------------------ |
| victora-dev01-s2 | 192.168.0.226 | \|vmstorage(8400 8401 8482)\|vminsert(8480) \|vmselect(8481) |
| victora-dev02-s2 | 192.168.0.227 | \|vmstorage(8400 8401 8482)\|vminsert(8480) \|vmselect(8481) |
| victora-dev03-s2 | 192.168.0.228 | \|vmstorage(8400 8401 8482)\|vminsert(8480) \|vmselect(8481) |

1. **软件下载**

   ```bash
   pvcreate /dev/sdb
   vgcreate victora /dev/sdb
   lvcreate -L 49GB victora -n data
   mkfs.ext4 /dev/mapper/victora-data 
   ```

   ```bash
   base_dir=/data/victoriaMetrics
   mkdir $base_dir -p
   echo /dev/mapper/victora-data  $base_dir ext4 defaults 0 0  >>/etc/fstab
   mount -a
   
   df -hT ${base_dir}
   ```

   

   ```bash
   version=v1.93.16
   
   wget https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/${version}/victoria-metrics-linux-amd64-${version}-cluster.tar.gz
   ```

   ```bash
   mkdir ${base_dir}/{bin,conf,data,log} -p
   tar xf victoria-metrics-linux-amd64-${version}-cluster.tar.gz -C ${base_dir}/bin
   ```

2. **安装vmstorage**

   > vmstorage 同时监听 8400 8401 8482
   >
   > 8400 接受 vminsert 的写入
   >
   > 8401 接受 vmselect 的查询
   >
   > 8482 对接文件存储
   
   节点1：
   
   > `-retentionPeriod` 默认保留期为 1 个月。最短保留期为 24 小时或 1 天
   
   ```bash
   ipaddr=192.168.0.228
   
   tee /etc/systemd/system/vmstorage.service<<'EOF'
   [Unit]
   Description=victoriaMetrics vmstorage serveice
   After=network.target
    
   [Service]
   ExecStart=${base_dir}/bin/vmstorage-prod \
   -storageDataPath ${base_dir}/data \
   -retentionPeriod 10d \
   -httpListenAddr ${ipaddr}:8482 \
   -vminsertAddr ${ipaddr}:8400 \
   -vmselectAddr ${ipaddr}:8401 
   
   User=root
   [Install]
   WantedBy=multi-user.target
   EOF
   ```
   
   
   
3. **安装vminsert**

   > 监听8480
   >
   > `-storageNode` 支持多个，用逗号分隔

   节点1:

   ```bash
   ipaddr=192.168.0.226
   storageNodeInsert=192.168.0.226:8400,192.168.0.227:8400,192.168.0.228:8400
   
   tee /etc/systemd/system/vminsert.service <<'EOF'
   [Unit]
   Description=victoriaMetrics vminsert serveice
   After=network.target
    
   [Service]
   ExecStart=${base_dir}/bin/vminsert-prod \
   -storageNode=${storageNodeInsert} \
   -httpListenAddr ${ipaddr}:8480
   User=root
   [Install]
   WantedBy=multi-user.target
   EOF
   ```

   

4. **安装vmselect**

   > 监听8481
   >
   > `-storageNode` 支持多个，用逗号分隔

   ```bash
   ipaddr=192.168.0.227
   storageNodeSelect=192.168.0.226:8401,192.168.0.227:8401,192.168.0.228:8401
   
   tee /etc/systemd/system/vmselect.service<<'EOF'
   [Unit]
   Description=victoriaMetrics vmselect serveice
   After=network.target
    
   [Service]
   ExecStart=${base_dir}/bin/vmselect-prod \
   -storageNode=${storageNodeSelect} \
   -httpListenAddr ${ipaddr}:8481
   
   User=root
   [Install]
   WantedBy=multi-user.target
   EOF
   ```

5. **启动服务**

   ```bash
   systemctl daemon-reload
   
   systemctl enable vminsert --now && systemctl status vminsert 
   systemctl enable vmselect --now && systemctl status vmselect 
   systemctl enable vmstorage --now && systemctl status vmstorage
   ```

6. **读写验证**

   ```bash
   # 写入测试
   curl -d 'metric_name{foo="bar"} 123' -X POST http://192.168.0.226:8480/insert/1/prometheus/api/v1/import/prometheus
   
   # 查询测试
   curl http://192.168.0.226:8481/select/1/prometheus/api/v1/query -d 'query=metric_name'
   
   # 删除测试
   curl -v http://192.168.0.226:8481/delete/1/prometheus/api/v1/admin/tsdb/delete_series -d 'match[]=metric_name'
   ```

   

6. **修改prometheus配置**

   > 对于高负载的 Prometheus 实例（每秒 200k+ 个样本），可以应用以下调整：
   >
   > ```bash
   > remote_write:
   >   - url: http://<victoriametrics-addr>:8480/insert/0/prometheus
   >     queue_config:
   >       max_samples_per_send: 10000
   >       capacity: 20000
   >       max_shards: 30
   > ```

   ```bash
   remote_write:
     #- url: http://<victoriametrics-host>:8480/insert/<tenantId>/<suffix>
     # prometheus and - for ingesting data with Prometheus remote write API.prometheus/api/v1/write
     - url: http://10.4.7.250:8480/insert/0/prometheus
     - url: http://10.4.7.251:8480/insert/0/prometheus
   ```

7. **配置grafana数据源**

   > victoraMetrics 与 grafana 存在兼容性问题：
   >
   > 1. VictoriaMetrics v1.44 - v1.58.x 与 Grafana 5.0 - 7.5.x 兼容。
   > 2. VictoriaMetrics v1.59.x - v1.65.x 与 Grafana 5.3 - 8.1.x 兼容（需要输入默认的 Prometheus 插件 URL）。

   ```bash
   #http://<victoriametrics-host>:8480/insert/<tenantId>/<suffix>
   http://10.4.7.250:8481/select/0/prometheus
   ```

8. **victoraMetrics ui**【非必须】

   ```bash
   http://10.4.7.250:8481/select/0/vmui/
   ```

9. **组件暴露的监控指标**

   ```bash
   10.4.7.250:8480/metrics
   10.4.7.250:8481/metrics
   10.4.7.250:8482/metrics
   ```





#### **vmauth**

vmauth 提供http的反向代理和用户鉴权认证

> 8427

```bash
version=v1.93.16
wget https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/${version}/vmutils-linux-amd64-${version}.tar.gz
```

```bash
tar xf vmutils-linux-amd64-${version}.tar.gz -C  ${base_dir}/bin
```



```yaml
tee ${base_dir}/conf/vmauth.yml <<EOF
unauthorized_user:
  url_map:
  - src_paths:
    - "/insert/.*"
    url_prefix:
    - "http://192.168.0.226:8480/"
    - "http://192.168.0.227:8480/"
    - "http://192.168.0.228:8480/"

  - src_paths:
    - "/select/.*"
    - "/delete/.*"
    url_prefix:
    - "http://192.168.0.226:8481"
    - "http://192.168.0.227:8481"
    - "http://192.168.0.228:8481"
EOF
```



```bash
ipaddr=192.168.0.226

tee /etc/systemd/system/vmauth.service <<'EOF'
[Unit]
Description=victoriaMetrics vmauth serveice
After=network.target
 
[Service]
ExecStart=${base_dir}/bin/vmauth-prod -auth.config ${base_dir}/conf/vmauth.yml \
-configCheckInterval 20s \
-httpListenAddr ":8427"

User=root
[Install]
WantedBy=multi-user.target
EOF
```

```bash
systemctl daemon-reload

systemctl enable vmauth --now && systemctl status vmauth 
```



```bash
# 写入测试
curl -d 'metric_name{foo="bar"} 456' -X POST http://192.168.0.226:8427/insert/1/prometheus/api/v1/import/prometheus

# 查询测试
curl http://192.168.0.226:8427/select/1/prometheus/api/v1/query -d 'query=metric_name'
curl http://192.168.0.226:8481/select/1/prometheus/api/v1/query -d 'query=metric_name'
curl http://192.168.0.227:8481/select/1/prometheus/api/v1/query -d 'query=metric_name'
curl http://192.168.0.228:8481/select/1/prometheus/api/v1/query -d 'query=metric_name'

# 删除测试
curl -v http://192.168.0.226:8427/delete/1/prometheus/api/v1/admin/tsdb/delete_series -d 'match[]=metric_name'
```



**添加认证： 用户名和密码**

```bash
tee ${base_dir}/conf/vmauth.yml <<EOF
users:
- username: foo
  password: bar
  url_map:
  - src_paths:
    - "/insert/.*"
    url_prefix:
    - "http://192.168.0.226:8480/"
    - "http://192.168.0.227:8480/"
    - "http://192.168.0.228:8480/"

  - src_paths:
    - "/select/.*"
    - "/delete/.*"
    url_prefix:
    - "http://192.168.0.226:8481"
    - "http://192.168.0.227:8481"
    - "http://192.168.0.228:8481"
EOF
```

```bash
# 写入测试
curl -ufoo:bar -d 'metric_name{foo="bar"} 456' -X POST http://192.168.0.226:8427/insert/1/prometheus/api/v1/import/prometheus

# 查询测试
curl -ufoo:bar http://192.168.0.226:8427/select/1/prometheus/api/v1/query -d 'query=metric_name'
curl http://192.168.0.226:8481/select/1/prometheus/api/v1/query -d 'query=metric_name'
curl http://192.168.0.227:8481/select/1/prometheus/api/v1/query -d 'query=metric_name'
curl http://192.168.0.228:8481/select/1/prometheus/api/v1/query -d 'query=metric_name'

# 删除测试
curl -ufoo:bar -v http://192.168.0.226:8427/delete/1/prometheus/api/v1/admin/tsdb/delete_series -d 'match[]=metric_name'
```



**添加认证：token认证**

```bash
tee ${base_dir}/conf/vmauth.yml <<EOF
users:
- bearer_token: ABCDEF
  url_map:
  - src_paths:
    - "/insert/.*"
    url_prefix:
    - "http://192.168.0.226:8480/"
    - "http://192.168.0.227:8480/"
    - "http://192.168.0.228:8480/"

  - src_paths:
    - "/select/.*"
    - "/delete/.*"
    url_prefix:
    - "http://192.168.0.226:8481"
    - "http://192.168.0.227:8481"
    - "http://192.168.0.228:8481"
EOF
```

```bash
curl  -H "Authorization: Bearer ABCDEF" -d 'metric_name{foo="bar"} 789' -X POST http://192.168.0.226:8427/insert/1/prometheus/api/v1/import/prometheus
```

```bash
curl  -H "Authorization: Bearer ABCDEF"  http://192.168.0.226:8427/select/1/prometheus/api/v1/query -d 'query=metric_name'
```

```bash
curl  -H "Authorization: Bearer ABCDEF"   http://192.168.0.226:8427/select/1/prometheus/api/v1/query -d 'query=metric_name'
```



#### 集群环境数据高可用

默认数据是hash 后分片存储的，可以在vminsert 中修改参数，设置数据的高可用

```bash
./vminsert-prod --help|gep repli
-replicationFactor int
        Replication factor for the ingested data, i.e. how many copies to make among distinct -storageNode instances. Note that vmselect must run with -dedup.minScrapeInterval=1ms for data de-duplication when replicationFactor is greater than 1. Higher values for -dedup.minScrapeInterval at vmselect is OK (default 1)
```



### 监控

