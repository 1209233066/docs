---
date: '2025-08-01T10:10:00+08:00'
draft: false
title: 'redis-shake3.1.11'
linkTitle: 'redis-shake3.1.11'
type: blog
toc_hide: false
hide_summary: true
weight: 4
description: >
  redis-shake3.1.11 docker镜像构建
tags: ["迁移案例"]
categories: ["redis"]
url: redis/redis-shake2.1.2.html
author: "wangendao"
---



{{% alert title="" color="" %}}

Tested on Redis 5.0, Redis 6.0 and Redis 7.0

{{% /alert %}}

**参数**

| 变量名             | 可选值（举例）                            | 备注                                                         |
| ------------------ | ----------------------------------------- | ------------------------------------------------------------ |
| redisSourceVersion | such as 2.8, 4.0, 5.0, 6.0, 6.2, 7.0, ... | 浮点类型，赋值不需要加引号                                   |
| sourceAddress      | 10.1.1.1:20331                            | 字符串类型，赋值需要加引号。集群中任意节点                   |
| sourcePassword     |                                           | 字符串类型，赋值需要加引号                                   |
| targetType         | "standalone" or "cluster"                 | 字符串类型，赋值需要加引号                                   |
| redisTargetVersion | such as 2.8, 4.0, 5.0, 6.0, 6.2, 7.0, ... | 浮点类型，赋值不需要加引号                                   |
| targetAddress      | 10.1.1.1:20331                            | 如果是集群模式，只写其中一个node,其他node信息redis-shake 通过 `cluster nodes`获取 |
| targetPassword     |                                           | 字符串类型，赋值需要加引号                                   |
| keyExists          | rewrite panic ignore                      | 字符串类型，赋值需要加引号                                   |
| prefixfilter       | true false                                | 确定前缀后后缀匹配                                           |
| filterKey          | {"ABC","abc","def","def_"}                |                                                              |
| blackfilter        | true false                                | 确定是黑名单还是白名单过滤                                   |

### 构建镜像

{{< details >}}
启动脚本`entrypoint.sh`

```bash
#!/bin/sh

set -ex

config(){
cat >/etc/sync.toml <<EOF
type = "sync"

[source]
version = ${redisSourceVersion}
address = ${sourceAddress}
username = "" # keep empty if not using ACL
password = ${sourcePassword}
tls = false


[target]
type = ${targetType}
version = ${redisTargetVersion}
address = ${targetAddress}
username = "" # keep empty if not using ACL
password = ${targetPassword}
tls = false

[advanced]
dir = "data"

# runtime.GOMAXPROCS, 0 means use runtime.NumCPU() cpu cores
ncpu = 4
pprof_port = 9310
metrics_port = 9320
rdb_restore_command_behavior = ${keyExists:-"ignore"}
pipeline_count_limit = 1024
target_redis_client_max_querybuf_len = 1024_000_000
target_redis_proto_max_bulk_len = 512_000_000
EOF

#array = {"ABC","abc","def","def_"}
array=${filterKey:-"{}"}
if ${prefixfilter};then
    prefix='"^"'
    suffix='""'
else
    prefix='""'
    suffix="$"
fi

if ${blackfilter};then
    allow=1
    disallow=0
else
    allow=0
    disallow=1
fi
        
cat >/etc/filter.lua<<EOF
function filter(id, is_base, group, cmd_name, keys, slots, db_id, timestamp_ms)
    
    -- 对mset多key的判断
    if #keys ~= 1 then
        for _k,key in ipairs(keys)
        do
            for k,v in ipairs(${array})
            do
                -- if string.match(key,string.format("^%s",v)) then
                if string.match(key,string.format("%s%s%s",${prefix:-""},v,${suffix:-""})) then
                    -- print(key,v)
                    return ${allow:-0}, db_id -- 0 is  allow
                end
            end
        end
        return ${disallow:-0}, db_id --1 is disallow
    end

    for k,v in ipairs(${array})
    do
        -- if string.sub(keys[1], -3, -1) == v then
        if string.match(keys[1],string.format("%s%s%s",${prefix},v,${suffix})) then
            return ${allow:-0}, db_id -- allow
        end
    end
    return ${disallow:-0}, db_id -- disallow
end
EOF
}

config

exec "$@"
```

{{< /details >}}



{{< details >}}

`Dockerfile.yml`

```bash
FROM alpine:3.13
ARG version=3.1.11

RUN sed -i s#dl-cdn.alpinelinux.org#mirrors.tuna.tsinghua.edu.cn#g /etc/apk/repositories && \ 
    apk update && \
    apk add vim curl python3 && \
    alias python="python3" && \
    rm -rf /var/cache/apk/*
#wget https://github.com/tair-opensource/RedisShake/releases/download/v3.1.11/redis-shake-linux-amd64.tar.gz
COPY entrypoint.sh /
COPY redis-shake /usr/bin/redis-shake
EXPOSE 9320
ENTRYPOINT ["/entrypoint.sh"]
```

{{< /details >}}

构建镜像

```bash
chmod +x  entrypoint.sh
docker build . -t redis-shake:3.1.11-alpine 
```



### 迁移示例

1. docker环境测试变量解析

   ```bash
   tee env<<EOF
   redisSourceVersion=5.0
   sourceAddress="127.0.0.1:6379"
   sourcePassword="123"
   redisTargetVersion=5.0
   targetType="cluster"
   targetAddress="127.0.0.1:6479"
   targetPassword="456"
   keyExists="rewrite"
   prefixfilter=true
   filterKey={"ABC","abc","def","def_"}
   blackfilter=false
   EOF
   ```

   ```bash
   docker run --rm -it  --env-file env redis-shake:3.1.11-alpine sh
   ```

   ```bash
   docker run --rm -it  --env-file env redis-shake:3.1.11-alpine  redis-shake /etc/sync.toml
   ```

   ```bash
   docker run --rm -it  --env-file env redis-shake:3.1.11-alpine  redis-shake /etc/sync.toml /etc/filter.lua
   ```

   ```bash
   docker exec -it 36e54 curl 127.0.0.1:9320/metrics|python -m json.tool
   ```

   指标监控：

   ```bash
   syncing aof. allowOps=[0.60], disallowOps=[0.00], entryId=[2], InQueueEntriesCount=[0], unansweredBytesCount=[0]bytes, diff=[0], aofReceivedOffset=[9808], aofAppliedOffset=[9808]
   ```

   ```bash
   allowOps：代表每秒向目的端发送多少条命令
   disallowOps：代表每秒有多少条命令被过滤掉
   entryId：从 1 开始计数，代表 redis-shake 从启动开始总共处理多少条命令
   InQueueEntriesCount：代表多少条命令待发送
   unansweredBytesCount：代表多少 bytes 命令已经发送了，但是对端还没有答复
   diff：aofReceivedOffset-aofAppliedOffset
   aofReceivedOffset：已经从源端接收到的点位
   aofAppliedOffset：已经在目的端恢复的点位
   ```

   ```bash
   一般当 allowOps 为 0 时，代表数据迁移完成，可以停止 redis-shake。⚠️注意，因为源端会定时发送 PING 命令，所以哪怕源端没有写入，allowOps 偶尔也会不是 0。
   ```

   

2. 资源压力测试

   | 源端（版本5.0） | 目标端（版本5.0） | 数据量 |
   | --------------- | ----------------- | ------ |
   | 8分片           | 3分片             | 12GB   |

   测试结果

   ```bash
   单pod 消耗 220% cpu
   单pod 消耗 12MB memory
   全量同步耗时 6分钟
   ```
   
   
