---
date: '2025-09-12T15:22:40+08:00'
draft: false
title: '如何快速启动一个kafka服务'
linkTitle: '安装kafka'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  *Apache Kafka 是一个开源分布式事件流平台，由Scala和Java编写。kafka 的运行依赖zookeeper，本章节介绍在linux环境下如何快速启动一个kafka,该环境仅用于开发环境*
tags: ["zookeeper","kafka"]
categories: ["kafka"]
url: elk/kafka/install.html
author: "wangendao"
---



### 安装部署

{{< tabpane text=true right=false >}}
  {{% tab header="**安装zookeeper**" lang="en" %}}

1. 安装依赖`jdk` 和 `zookeeper`

   参考 [部署zookeeper](zookeeper)

   | java版本 | zookeeper版本 | kafka版本  |
   | -------- | ------------- | ---------- |
   | java8    |               | 0.7 至 3.0 |
   | java11   |               | 0.7 至 3.7 |
   | java17   |               | 0.7 至     |

   **jdk**

   ```bash
   wget https://download.java.net/java/ga/jdk11/openjdk-11_linux-x64_bin.tar.gz
   
   tar xf openjdk-11_linux-x64_bin.tar.gz -C /opt
   ln -svf  /opt/{jdk-11,jdk}
   
   cat>>/etc/profile<<EOF
   export JAVA_HOME=/opt/jdk
   export JAVA_JRE=\$JAVA_HOME/jre
   export CLASSPATH=\$JAVA_HOME/lib:\$JAVA_HOME/jre/lib
   export PATH=\$JAVA_HOME/bin:\$JAVA_JRE/bin:$PATH:.
   EOF
   
   source /etc/profile
   java -version
   ```

   
   
   | 端口          | 作用                                                         |
   | ------------- | ------------------------------------------------------------ |
   | 2181          | 用于接受客户端连接的主要端口                                 |
   | 2888          | 用于 ZooKeeper 集群内节点从leader同步数据，只有leader才监听该端口 |
   | 3888          | 用于 ZooKeeper 集群中的 Leader 选举过程中节点之间的通信      |
   | tickTime=2000 | 每隔2000毫秒检查一下集群心跳                                 |
   
   ```bash
   wget https://archive.apache.org/dist/zookeeper/zookeeper-3.4.14/zookeeper-3.4.14.tar.gz
   
   tar xf zookeeper-3.4.14.tar.gz -C /opt
   rm -f zookeeper-3.4.14.tar.gz
   ln -sv /opt/{zookeeper-3.4.14,zookeeper}
   
   mkdir -p /opt/zookeeper/{data,logs} 
   ```
   
   单节点配置 
   
   ```bash
   tee /opt/zookeeper/conf/zoo.cfg<<EOF
   tickTime=2000
   initLimit=10
   syncLimit=5
   dataDir=/opt/zookeeper/data
   dataLogDir=/opt/zookeeper/log
   clientPort=2181
   EOF
   ```
   
   ```bash
   /opt/zookeeper/bin/zkServer.sh start && /opt/zookeeper/bin/zkServer.sh  status
   ```
   
   查看当前节点状态

   ```bash
   [root@hdss7-12 bin]#  /opt/zookeeper/bin/zkCli.sh -server localhost:2181
   [zk: localhost:2181(CONNECTED) 2] ls /
   ```
   
   

     {{% /tab %}}
     {{% tab header="**安装Kafka**" lang="en" %}}
   
2. 部署安装<sub>【elk建议Kafka 版本 0.8.2.0+】</sub>

   ```bash
   wget https://archive.apache.org/dist/kafka/3.3.2/kafka_2.13-3.3.2.tgz
   tar xf kafka_2.13-3.3.2.tgz -C /opt
   rm -fr kafka_2.13-3.3.2.tgz
   ln -sv  /opt/{kafka_2.13-3.3.2,kafka}

3. 修改配置文件

   ```bash
   mkdir /opt/kafka/data
   ```

   ```bash
   cat >/opt/kafka/config/server.properties <<'EOF'
   broker.id=0
   num.network.threads=3
   num.io.threads=8
   socket.send.buffer.bytes=102400
   socket.receive.buffer.bytes=102400
   socket.request.max.bytes=104857600
   log.dirs=/tmp/kafka-logs
   num.partitions=1
   num.recovery.threads.per.data.dir=1
   offsets.topic.replication.factor=1
   transaction.state.log.replication.factor=1
   transaction.state.log.min.isr=1
   log.retention.hours=168
   log.retention.check.interval.ms=300000
   zookeeper.connect=localhost:2181
   zookeeper.connection.timeout.ms=18000
   group.initial.rebalance.delay.ms=0
   EOF
   ```
   
   
   
4. [启动服务](https://kafka.apache.org/documentation/#quickstart)

   ```bash
   /opt/kafka/bin/kafka-server-start.sh -daemon server.properties
   ```

   

   

5. 测试服务

   

   ```bash
   # 创建topics
   /opt/kafka/bin/kafka-topics.sh --create --topic app-log --bootstrap-server localhost:9092
   ```
   
   ```bash
   # 列出topics
   ]# /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
   app-log
   ```
   
   ```bash
   # 查看指定topics详情
   /opt/kafka/bin/kafka-topics.sh --describe --topic app-log --bootstrap-server localhost:9092
   ```
   
   ```bash
   # 向topics产生一个事件
   echo -e "This is my first event\nThis is my second event" | /opt/kafka/bin/kafka-console-producer.sh --topic  app-log --bootstrap-server localhost:9092
   ```
   
   
   
   ```bash
   # 消费topics事件
   /opt/kafka/bin/kafka-console-consumer.sh --topic app-log --from-beginning --bootstrap-server localhost:9092
   This is my first event
   This is my second event
   ```
   
   

  {{% /tab %}}
{{< /tabpane >}}

### 可视化工具



+ [雅虎开源的kafka管理工具CMAK](https://github.com/yahoo/CMAK.git)
+ [滴滴开源的kafka管理工具](https://github.com/didi/KnowStreaming.git)
+ [Offset Explorer (kafkatool.com)](https://www.kafkatool.com/download.html)



### 配置文件

[Kafka集群搭建及必知必会 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/278252465)|[Apache Kafka](https://kafka.apache.org/31/documentation.html)



| 参数                            | 值                             | 注释                                                 |
| ------------------------------- | ------------------------------ | ---------------------------------------------------- |
| broker.id                       | 0                              | Broker唯一标识                                       |
| listeners                       | PLAINTEXT://192.168.88.53:9092 | 监听信息，PLAINTEXT表示明文传输                      |
| log.dirs                        | kafka/logs                     | kafka数据存放地址，可以填写多个。用”,”间隔           |
| message.max.bytes               | message.max.bytes              | 单个消息长度限制，单位是字节                         |
| num.partitions                  | 1                              | 默认分区数                                           |
| log.flush.interval.messages     | Long.MaxValue                  | 在数据被写入到硬盘和消费者可用前最大累积的消息的数量 |
| log.flush.interval.ms           | Long.MaxValue                  | 在数据被写入到硬盘前的最大时间                       |
| log.flush.scheduler.interval.ms | Long.MaxValue                  | 检查数据是否要写入到硬盘的时间间隔。                 |
| log.retention.hours             | 24                             | 控制一个log保留时间，单位：小时                      |
| zookeeper.connect               | 192.168.88.21:2181             | ZooKeeper服务器地址，多台用”,”间隔                   |

