---
date: '2025-05-30T15:22:40+08:00'
draft: false
title: '快速开始'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  coredns|kubernetes
tags: ["coredns"]
categories: ["coredns"]
url: kubernetes/coredns.html
author: "wangendao"
---
![](https://rpic.origz.com/api.php?category=photography)


[CoreDNS](https://coredns.io/manual/toc/)是由Go语言编写的[开源](https://www.apache.org/licenses/LICENSE-2.0.html)DNS服务，通过大量插件实现了复杂的功能。因此在实现上不同于[BIND](https://www.isc.org/bind/)，[Knot](https://www.knot-dns.cz/)，[PowerDNS](https://www.powerdns.com/)，[Unbound](https://www.unbound.net/) 等dns软件

### 基本概念
**A/AAAA 记录** 

**SRV 记录**

**PTR 记录**  是dns的反向解析，用于将ip地址解析为域名。例如存在一条A记录：  `172.168.0.1 kubernetes.default.svc.cluster.local`  使用PTR可以通过 172.168.0.1 找到对应的域名为`kubernetes.default.svc.in-addr.arpa` 域名。
PTR 记录存储在 DNS 的 `.arpa` 顶级域中，`.arpa` 是一个用于管理网络基础设施的域，是为互联网定义的[第一个](https://tools.ietf.org/html/rfc881)顶级域名。（“arpa”这个名字可以追溯到互联网的早期：它的名字来源于高级研究计划署 (ARPA)，它创建了互联网的重要前身 ARPANET。）
二级域名 `.in-addr` 代表了ipv4，因此表示为 `.in-addr.arpa` 。对于ipv6 对应 `.ip6.arpa`


### 安装部署

{{< tabpane text=true right=false >}}

  {{% tab header="容器" lang="en" %}}

```bash
docker run --name coredns -p53:53 coredns/coredns:latest
```

  {{% /tab %}}
  {{% tab header="二进制" lang="en" %}}
下载
```bash
wget https://github.com/coredns/coredns/releases/download/v1.10.0/coredns_1.10.0_linux_amd64.tgz
tar xf coredns_1.10.0_linux_amd64.tgz -C /usr/bin/
```

启动
```bash
[root@lavm-ioreaqndwv ~]# coredns -dns.port1053
.:1053
CoreDNS-1.10.0
linux/amd64, go1.19.1, 596a9f9
```

  {{% /tab %}}
{{< /tabpane >}}



### 配置文件

{{% alert title="" color="" %}}
+ 启动时默认查找当前目录下的`Corefile`配置文件， 可通过 `coredns -conf /etc/Corefile` 指定自定义配置文件

+ `#`开头视为注释

+ `{$ENV_VAR}` 引用操作系统变量

+ 支持片段定义和引用

  ```bash
  # 定义一个名为plg的片段
  (plg) {
      errors
      forward . 8.8.8.8 223.5.5.5
      reload
      log
  }
  .:53 {
      # 引用片段
      import plg
  }
  ```
{{% /alert %}}



{{% alert title="server 块的定义" color="" %}}
定义一组dns服务

```bash
<zone>[:<port>] {
    <plugin1> [参数...]
    <plugin2> [参数...]
    ...
}
```
{{% /alert %}}
```bash
. {
     <plugin1> [参数...]
}
.:53 {
     <plugin1> [参数...]
}

coredns.io:53 {
     <plugin1> [参数...]
}
```


**配置示例：** 配置了两个server,每个server有自己的插件链

```bash
# server 定义语法 [zone] [port...] {...}
# 对所有域名执行解析
(plg) {
    errors
    forward . 8.8.8.8 223.5.5.5
    reload
    log
}
.:53 {
        
    prometheus :9153
    hosts {
        1.2.3.4 zero-dew.cn
        fallthrough
    }
    import plg
}

# 仅解析 .com
com.:54 {
    prometheus :9154
    hosts {
        1.2.3.4 zero-dew.cn
        1.2.3.5 zero-dew.com
        fallthrough
    }
    import plg
}
```