---
date: '2025-05-20T22:13:52+08:00'
draft: false
title: 'etcd'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  etcd|kubernetes
tags: ["etcd"]
categories: ["etcd"]
url: kubernetes/etcd.html
author: "wangendao"
---
![](https://rpic.origz.com/api.php?category=photography)


### 简介

[**etcd**](https://etcd.io/) 是CoreOS团队2013年6月发起的分布式k-v 数据库。采用[raft](http://thesecretlivesofdata.com/raft/)协议作为一致性算法。



由于 etcd 将数据写入磁盘，因此其性能很大程度上取决于磁盘性能。强烈建议使用ssd硬盘并做好性能测试[fio](https://github.com/axboe/fio)。，etcd 默认将可配置的存储大小配额设置为 2GB，因此需留足RAM。对于生产环境建议最大不超过8GB，如果配置的值超过该值，etcd 在启动时发出警告。


硬件最小建议：

- 8GB 内存
- 100GB 磁盘
- 4核 CPU



## 第一节集群安装

| 主机名         | 主机ip        | etcd节点名称 | 版本                                                         |
| -------------- | ------------- | ------------ | ------------------------------------------------------------ |
| etcd-1.k8s.com | 10.4.7.200/24 | etcd-1       | [v.13.5.0](https://github.com/etcd-io/etcd/releases/tag/v3.5.0) |
| etcd-2.k8s.com | 10.4.7.201/24 | etcd-2       | [v.13.5.0](https://github.com/etcd-io/etcd/releases/tag/v3.5.0) |
| etcd-3.k8s.com | 10.4.7.202/24 | etcd-3       | [v.13.5.0](https://github.com/etcd-io/etcd/releases/tag/v3.5.0) |

**第一步生成证书**

*请求文件*

```bash
cat etcd.cnf 
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[ req_distinguished_name ]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation,digitalSignature,keyEncipherment
subjectAltName = @alt_names
[alt_names]
IP.1 = 10.4.7.200
IP.2 = 10.4.7.201
IP.3 = 10.4.7.202
```

*ca证书*

```bash
openssl genrsa -out ca.key 2048
openssl req -new -key ca.key -out ca.csr -subj "/CN=etcd"
openssl x509 -req -in ca.csr -out ca.crt -signkey ca.key -days 365
```

*server证书*

```bash
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj "/CN=etcd-server" -config etcd.cnf
openssl x509 -req -in server.csr -out server.crt -signkey server.key -CA ca.crt -CAkey ca.key -CAcreateserial -days 365 -extensions v3_req -extfile etcd.cnf

```

*peer证书*

```bash
openssl genrsa -out peer.key 2048
openssl req -new -key peer.key -out peer.csr -subj "/CN=etcd-peer" -config etcd.cnf
openssl x509 -req -in peer.csr -out peer.crt -signkey peer.key -CA ca.crt -CAkey ca.key -CAcreateserial -days 365 -extensions v3_req -extfile etcd.cnf
```

**第二步配置启动文件**

<span id=config></span>

><font color=EF5A04 size=5>注意</font>
>
>每个节点需要按需修改
>
>`--name `
>`--listen-peer-urls`
>`--initial-advertise-peer-urls`
>`--listen-client-urls`
>`--advertise-client-urls`

```bash
 #!/bin/bash
 # v3.4+ 可以不指定ETCDCTL_API 
 export ETCDCTL_API=3
 /opt/etcd/etcd \
 --name etcd-3 \
 --listen-peer-urls 'https://10.4.7.202:2380' \
 --initial-advertise-peer-urls 'https://10.4.7.202:2380' \
 # etcd 服务监听的地址，用于客户端连接
 --listen-client-urls 'https://10.4.7.202:2379,http://127.0.0.1:2379' \
 # etcd 对外广播的地址，用户客户端和其他etcd成员连接
 --advertise-client-urls 'https://10.4.7.202:2379' \
 --initial-cluster-state 'new' \
 --initial-cluster-token 'etcd-cluster' \
 --initial-cluster 'etcd-1=https://10.4.7.200:2380,etcd-2=https://10.4.7.201:2380,etcd-3=https://10.4.7.202:2380' \
 --client-cert-auth --trusted-ca-file=./ca.crt \
 --cert-file=server.crt --key-file=server.key  \
 --peer-client-cert-auth --peer-trusted-ca-file=./ca.crt \
 --peer-cert-file=./peer.crt --peer-key-file=./peer.key
```

**第三步启动etcd并检查**

```bash
/opt/etcd/etcdctl \
--endpoints=https://10.4.7.200:2379,https://10.4.7.201:2379,https://10.4.7.202:2379 \
--cacert=./ca.crt \
--cert=peer.crt \
--key=peer.key \
member list -w table
```


![](https://img2022.cnblogs.com/blog/2108528/202211/2108528-20221113192958390-1282145596.png)





****



## 第二节集群备份和恢复

```bash
COMMANDS:
        restore Restores an etcd member snapshot to an etcd directory
        save    Stores an etcd node backend snapshot to a given file
        status  [deprecated] Gets backend snapshot status of a given file
```



**第一步生成测试内容**

```bash
/opt/etcd/etcdctl --endpoints=https://10.4.7.200:2379 --cacert=./ca.crt --cert=peer.crt --key=peer.key put name 张三
```

**第二步备份数据**

> 连接到集群任意节点

```bash
/opt/etcd/etcdctl \
--endpoints=https://10.4.7.200:2379 \
--cacert=./ca.crt \
--cert=peer.crt \
--key=peer.key \
snapshot save /data/backup/2022-11-13.db
```

*查看备份文件状态*

```bash
/opt/etcd/etcdctl snapshot status /data/backup/2022-11-13.db -w table
```

![](https://img2022.cnblogs.com/blog/2108528/202211/2108528-20221113193027066-1955276160.png)




**第三步模拟破坏数据**

```bash
/opt/etcd/etcdctl --endpoints=https://10.4.7.200:2379 --cacert=./ca.crt --cert=peer.crt --key=peer.key del name
```

**第四步恢复数据**

><font color=EF5A04 size=5>注意</font>
>
>+ 停止集群所有节点etcd进程，备份原数据文件
>+ 停止所有kube-apiserver
>+ 集群所有节点执行恢复动作，注意修改 `--name` `--initial-advertise-peer-urls` `--data-dir`
>+ 执行启动命令

```bash
ETCDCTL_API=3 
/opt/etcd/etcdctl \
snapshot restore /data/backup/2022-11-13.db \
--name etcd-1 \
--initial-cluster "etcd-1=https://10.4.7.200:2380,etcd-2=https://10.4.7.201:2380,etcd-3=https://10.4.7.202:2380" \
--initial-cluster-token etcd-cluster \
--initial-advertise-peer-urls https://10.4.7.200:2380 \
--data-dir=./etcd-1.etcd
```

**第五步启动集群**

参考集群安装中启动脚本<a href=#config>启动集群</a>

*验证恢复*

```bash
[root@radius-db03 ~]# /opt/etcd/etcdctl --endpoints=https://10.4.7.200:2379 --cacert=./ca.crt --cert=peer.crt --key=peer.key get name
name
张三
```

**备份脚本**

{{<details>}}
```bash
#！/bin/bash

# describe: this scribe to backup etcd 
# create by 1209233066@qq.com
# usage: 
# MAILTO=""
# 59 23 * * * /bin/bash /scribe/etcd_backup.sh >/dev/null 2>&1

# 主机名
hostName=$(hostname)
# IP
hostIp=$(hostname -i|awk '{print $NF}')

# 备份路径
backupDir=/data/backup/etcd
# 证书文件
caCert=/etc/kubernetes/pki/etcd/ca.crt
cert=/etc/kubernetes/pki/etcd/server.crt
key=/etc/kubernetes/pki/etcd/server.key

# 是否为leader
ETCDCTL_API=3
isLeader=$(/usr/bin/etcdctl --endpoints=${hostIp}:2379 endpoint status|awk -F "," '{print $5}')


# 备份
if ${isLeader};then
   echo "The ${hostName} instance is the etcd leader,does not require backup"
else
   /usr/bin/etcdctl --cacert=${caCert} --cert=${cert} --key=${key}  snapshot save ${backupDir}/etcd-${hostName}-`date+%Y%m%d`.db
fi
# 推送s3

# 本地保留
find  ${backupDir} -name *.db -mtime +30 |xargs rm -f
```
{{</details>}}
****



## 第三节下线节点

**第一步获取节点id**

```bash
/opt/etcd/etcdctl \
--endpoints=https://10.4.7.200:2379,https://10.4.7.201:2379,https://10.4.7.202:2379 \
--cacert=./ca.crt \
--cert=peer.crt \
--key=peer.key  \
member list
```

**第二步下线节点**

```bash
/opt/etcd/etcdctl \
--endpoints=https://10.4.7.200:2379,https://10.4.7.201:2379,https://10.4.7.202:2379 \
--cacert=./ca.crt \
--cert=peer.crt \
--key=peer.key  \
member remove 19a4c376178d5b49
```

```bash
Member 19a4c376178d5b49 removed from cluster d5f1887e154dc473
```

****



## 第四节集群扩容



**第一步集群中执行添加**

> <font color=EF5A04 size=5>注意</font>
>
> 示例中`10.4.7.202` 需要在签证书时已经存在在`etcd.cnf` 中

```bash
/opt/etcd/etcdctl \
--endpoints=https://10.4.7.200:2379,https://10.4.7.201:2379 \
--cacert=./ca.crt \
--cert=peer.crt \
--key=peer.key  \
member add etcd-2 \
--peer-urls=https://10.4.7.202:2380
```

*执行命令后返回值*

```bash
Member 8c993ee76df9da92 added to cluster d5f1887e154dc473

ETCD_NAME="etcd-2"
ETCD_INITIAL_CLUSTER="etcd-1=https://10.4.7.200:2380,etcd-2=https://10.4.7.201:2380,etcd-2=https://10.4.7.202:2380"
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://10.4.7.202:2380"
ETCD_INITIAL_CLUSTER_STATE="existing"
```

**第二步启动新加入节点**

参考集群安装中启动脚本<a href=#config>启动集群</a>，需要把`--initial-cluster-state 'new' ` 修改为 `--initial-cluster-state 'existing' `

****

## 第五节其他指令

节点的健康状态 *endpoint health*

```bash
etcdctl --endpoints=10.4.7.250:2379 \
--cacert="/etc/kubernetes/ssl/ca.pem" \
--cert="/etc/kubernetes/ssl/etcd.pem" \
--key="/etc/kubernetes/ssl/etcd-key.pem" \
endpoint health --write-out=table

+-----------------+--------+-------------+-------+
|    ENDPOINT     | HEALTH |    TOOK     | ERROR |
+-----------------+--------+-------------+-------+
| 10.4.7.250:2379 |   true | 12.901855ms |       |
+-----------------+--------+-------------+-------+
```



集群成员 *member list*

```bash
etcdctl member list --write-out=table
+------------------+---------+-----------------+-------------------------+-------------------------+------------+
|        ID        | STATUS  |      NAME       |       PEER ADDRS        |      CLIENT ADDRS       | IS LEARNER |
+------------------+---------+-----------------+-------------------------+-------------------------+------------+
| 5c3282345e325481 | started | etcd-10.4.7.250 | https://10.4.7.250:2380 | https://10.4.7.250:2379 |      false |
+------------------+---------+-----------------+-------------------------+-------------------------+------------+
```



节点状态*endpoint status*

```bash
etcdctl --endpoints=10.4.7.250:2379 \
--cacert="/etc/kubernetes/ssl/ca.pem" \
--cert="/etc/kubernetes/ssl/etcd.pem" \
--key="/etc/kubernetes/ssl/etcd-key.pem" \
endpoint status --write-out=table

+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT     |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
| 10.4.7.250:2379 | 5c3282345e325481 |   3.5.0 |  2.9 MB |      true |      false |         2 |     216020 |             216020 |        |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
```

性能测试*check perf*

```bash
[root@etcd-1 ~]# etcdctl check perf
 60 / 60 Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo! 100.00% 1m0s
PASS: Throughput is 150 writes/s
PASS: Slowest request took 0.017941s
PASS: Stddev is 0.000807s
PASS
```


**查询**

```bash
查询key
1. 拿到所有key
etcdctl get / --prefix --keys-only
2. 查询指定key.值是被序列化过的，因此可能会乱码
etcdctl get /registry/storageclasses/csi-rbd-sc
```

**增加**

```bash
etcdctl put /name wang
OK
```

**查询**

```bash
etcdctl get /name
/name
wang
# watch 一直监听 /name 这个key的变动
etcdctl watch /name
```

**删除**

```bash
[root@ceph ~]# etcdctl del /name
1
```


## 参考

[raft](https://www.jdon.com/artichect/raft.html)|[raft](https://raft.github.io/raft.pdf)

[https证书最佳实战目录 - _毛台 - 博客园 (cnblogs.com)](https://www.cnblogs.com/iiiiher/p/7873737.html)

[ETCD数据的备份与恢复 - taotaozh - 博客园 (cnblogs.com)](https://www.cnblogs.com/hsyw/p/15652417.html)
