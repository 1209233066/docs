---
date: '2025-06-19T20:53:33+08:00'
draft: false
title: 'checkssh'
type: blog
toc_hide: false
hide_summary: true
weight: 5
description: >
  checkssh|tidb
tags: ["tiup工具"]
categories: ["tidb"]
url: tidb/checkssh.html
author: "wangendao"
---

![](https://docs-download.pingcap.com/media/images/docs-cn/tidb-architecture-v6.png)

```bash
#!/bin/bash
# description: 在中控机tidb用户下，检查集群节点ssh秘钥认证
# PasswordAuthentication=no  禁用密码认证
# StrictHostKeyChecking=no 禁用know_hosts 检查


declare -A info
clusterName=$(tiup cluster list |awk 'NR>2{print $1}')

for cls in $clusterName;do  
  iplist=$(tiup cluster display $cls|awk -F ":" '/^[0-9].*/{print $1}'|sort |uniq)
  info["$cls"]=$iplist
done


for cls in ${!info[@]}
do
  echo ""
  for host in ${info[$cls]};do
    rsa="/tidbdata/tiupshare/tiuptool/storage/cluster/clusters/${cls}/ssh/id_rsa"
    ssh -o PasswordAuthentication=no -o StrictHostKeyChecking=no -T -i ${rsa} ${host} exit 2>/dev/null
    if [ $? -eq 0 ];then
       printf "集群：%s,主机:%s  [OK]\n" $cls $host
    else
       printf "集群：%s,主机:%s  [Failed]\n" $cls $host
    fi
  done 
done
```

输出结果：
```bash
集群：cluster01,主机:192.168.0.105  [OK]
集群：cluster01,主机:192.168.0.106  [OK]
集群：cluster01,主机:192.168.0.107  [OK]

集群：tidb_dev_001,主机:192.168.0.223  [Failed]
集群：tidb_dev_001,主机:192.168.0.224  [OK]
集群：tidb_dev_001,主机:192.168.0.225  [OK]
```