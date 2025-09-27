---
date: '2025-08-01T10:10:00+08:00'
draft: false
title: 'redis-shake2.1.2'
linkTitle: 'redis-shake2.1.2'
type: blog
toc_hide: false
hide_summary: true
weight: 3
description: >
  redis-shake2.1.2 docker镜像构建
tags: ["迁移案例"]
categories: ["redis"]
url: redis/redis-shake2.1.2.html
author: "wangendao"
---



{{% alert title="" color="" %}}
redis-shake2.1.2 版本支持 redis 2.x to 6.x
{{% /alert %}}

**参数**

| 变量名             | 可选值（举例）                    | **备注**                                              |
| ------------------ | --------------------------------- | ----------------------------------------------------- |
| sourceType         | standalone sentinel cluster proxy |                                                       |
| sourceAddress      | 10.1.1.1:20331;10.1.1.2:20441     |                                                       |
| sourcePassword     |                                   |                                                       |
| targetType         |                                   |                                                       |
| targetAddress      |                                   |                                                       |
| targetPassword     |                                   |                                                       |
| keyExists          | rewrite none ignore               |                                                       |
| filterKeyWhitelist | "abc;bzz"                         | filterKeyWhitelist 和 filterKeyBlacklist 不能同时设置 |
| filterKeyBlacklist | "abc;bzz"                         |                                                       |
| filterDbWhitelist  | 0;5;10                            |                                                       |
| filterDbBlacklist  | 0;5;10                            |                                                       |



### 构建镜像

{{< details >}}
启动脚本`entrypoint.sh`

```bash
#!/bin/sh

set -ex

config(){
cat >/etc/redis-shake.conf <<EOF
conf.version = 1

id = redis-shake
system_profile = 9310
http_profile = 9320
parallel = 32
source.type = ${sourceType:- "cluster"}
source.address = ${sourceAddress}
source.password_raw = ${sourcePassword}
source.auth_type = auth


target.type = ${targetType:- "cluster"}
target.address = ${targetAddress}
target.password_raw = ${targetPassword}
target.auth_type = auth
target.db = -1

key_exists = ${keyExists:-"ignore"}

filter.db.whitelist = ${filterDbWhitelist}
filter.db.blacklist = ${filterDbBlacklist}
filter.key.whitelist = ${filterKeyWhitelist}
filter.key.blacklist = ${filterKeyBlacklist}


big_key_threshold = 524288000

metric = true
metric.print_log = false

sender.size = 104857600
sender.count = 4095
sender.delay_channel_size = 65535

keep_alive = 0

scan.key_number = 50
scan.special_cloud =
scan.key_file =
qps = 200000
resume_from_break_point = false
replace_hash_tag = false
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
ARG version=2.1.2

RUN sed -i s#dl-cdn.alpinelinux.org#mirrors.tuna.tsinghua.edu.cn#g /etc/apk/repositories && \ 
    apk update && \
    apk add vim curl python3 && \
    alias python="python3" && \
    rm -rf /var/cache/apk/*
#wget https://github.com/tair-opensource/RedisShake/releases/download/release-v2.1.2-20220329/release-v2.1.2-20220329.tar.gz
COPY entrypoint.sh /
COPY redis-shake.linux /usr/bin/redis-shake.linux
EXPOSE 9320
ENTRYPOINT ["/entrypoint.sh"]
```

{{< /details >}}

构建镜像

```bash
chmod +x  entrypoint.sh
docker build . -t redis-shake:2.1.2-alpine
```



### 迁移示例

1. docker环境测试变量解析

   ```bash
   tee env<<EOF
   sourceType=cluster
   sourceAddress=127.0.0.1:6379;127.0.0.1:6380;127.0.0.1:6381;
   sourcePassword=123
   targetType=cluster
   targetAddress= 127.0.0.1:6479;127.0.0.1:6480;127.0.0.1:6481;
   targetPassword=456
   keyExists=rewrite
   filterKeyWhitelist="abc;bzz"
   filterKeyBlacklist="abc;bzz"
   filterDbWhitelist=0;5;10
   filterKeyBlacklist=0;5;10
   EOF
   ```

   ```bash
   docker run --rm -it  --env-file env redis-shak:2.1.2-alpine sh
   ```

   ```bash
   docker run --rm -it  --env-file env redis-shak:2.1.2-alpine redis-shake.linux -type=sync -conf=/etc/redis-shake.conf
   ```

2. 资源压力测试

   | 源端（版本5.0） | 目标端（版本5.0） | 数据量 |
   | --------------- | ----------------- | ------ |
   | 8分片           | 3分片             | 12GB   |

   

   2.1 在源端生成数据

   ```bash
   # 约12G数据
   
   nodelist=(
   node01
   node02
   node03
   node04
   node05
   node06
   node07
   node08
   )
   
   for i in ${nodelist[@]};do redis-cli -a 123 -h $i debug populate 12000000 $i;done
   ```

   

   {{< tabpane text=true right=false >}}
     {{% tab header="资源使用情况1" lang="en" %}}

   2.2.1  配置同步

   ```bash
   docker run -d --net=host --env-file env nosql.registry.io:5000/redis-shak:2.1.2-alpine redis-shake.linux -type=sync -conf=/etc/redis-shake.conf
   ```

   2.3.1 资源使用情况和同步耗时

   ![](/docs/database/redis/资源使用情况2.png)

   

     {{% /tab %}}
     {{% tab header="资源使用情况2" lang="en" %}}

   2.2.1  配置同步，限制为 3c 4g

   ```bash
   docker run -d --cpus=3 -m 4G --net=host --env-file env nosql.registry.io:5000/redis-shak:2.1.2-alpine redis-shake.linux -type=sync -conf=/etc/redis-shake.conf
   ```

   2.3.1 资源使用情况和同步耗时

   ![](/docs/database/redis/资源使用情况.png)

  {{% /tab %}}
{{< /tabpane >}}