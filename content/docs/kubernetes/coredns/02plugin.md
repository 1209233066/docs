---
date: '2025-05-31T15:22:40+08:00'
draft: false
title: '基础插件'
type: blog
toc_hide: false
hide_summary: true
weight: 2
description: >
  plugin|kubernetes
tags: ["coredns","plugin"]
categories: ["coredns"]
url: kubernetes/plugin.html
author: "wangendao"


---

![](https://rpic.origz.com/api.php?category=photography)



目前coredns1.12.1已集成了30+内置插件，同时也支持用户在编译时引入更多的外部插件(*类似nginx*)，插件在`corefile`中的位置不影响插件的执行顺序（[`plugin.cfg`](https://github.com/coredns/coredns/blob/master/plugin.cfg) 文件定义顺序决定）。`./coredns --plugins` 查看当前coredns支持哪些插件



### health

> https://coredns.io/plugins/health/

{{% alert title="语法" color="" %}}

提供一个`http://0.0.0.0:8080/health` 的接口检查coredns是否就绪。主要关注coredns进程本身,通常使用在livenessProbe

{{% /alert %}}



```bash
.:53 {
      health localhost:8080 {
        lameduck 5s #当CoreDNS收到终止信号（如 Pod 被删除或重启时），会先进入lameduck状态 5 秒，在这 5 秒内/health检查仍然会返回 200 OK， /ready 不会返回 OK。
                    #作用：给负载均衡器（如 kube-proxy、Service、Ingress）时间把流量切走，避免请求丢失。
        }
}
```



### ready

> https://coredns.io/plugins/ready/

{{% alert title="语法" color="" %}}

提供一个`http://0.0.0.0:8181/ready ` 的接口,当所有plugins都就绪是返回200,如果某个plugin不可用时返回503。可以用于readinessProbe

{{% /alert %}}



```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
}
```

### reload

> https://coredns.io/plugins/reload/

{{% alert title="语法" color="" %}}

定期检查 Corefile 是否发生变化，通过读取并计算其 SHA512 校验和来实现自动重新加载

```bash
# INTERVAL和JITTER是Go语言时间持续时间。默认的INTERVAL是30s，默认的JITTER是15s
# INTERVAL 的最小值为2s， JITTER的最小值为 1s
# 如果 JITTER大于INTERVAL的一半，它将被设置为INTERVAL的一半。
reload [INTERVAL] [JITTER]
```

{{% /alert %}}



```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
}
```



### log

> https://coredns.io/plugins/log/

{{% alert title="语法" color="" %}}

记录日志，支持对日志格式的定制

{{% /alert %}}

```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
      log
}
```

### errors

> https://coredns.io/plugins/errors/

{{% alert title="语法" color="" %}}

查询处理过程中遇到的任何错误都会被打印到标准输出

{{% /alert %}}

```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
      log
      errors
}
```



### prometheus

> https://coredns.io/plugins/metrics/

{{% alert title="语法" color="" %}}

暴露一组prometheus格式的指标

{{% /alert %}}

```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
      log
      errors
      prometheus :9153
}
```





**主要指标**

| 指标解释         | 指标                                                         |      |
| ---------------- | ------------------------------------------------------------ | ---- |
| 版本信息         | `coredns_build_info{version, revision, goversion}`           |      |
| 开启的插件       | `coredns_plugin_enabled{server, zone, view, name}`           |      |
| 99%查询响应时长  | `histogram_quantile(0.99,coredns_dns_request_duration_seconds_bucket)` |      |
| reload失败次数   | `coredns_reload_failed_total`                                |      |
| 最后重启时间     | `coredns_hosts_reload_timestamp_seconds `                    |      |
| 健康检查失败次数 | `coredns_health_request_failures_total `                     |      |
| 缓存命中率       | `coredns_cache_hits_total/coredns_dns_requests_total`        |      |



### trace

> https://coredns.io/plugins/trace/

{{% alert title="语法" color="" %}}

链路追踪

{{% /alert %}}

```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```



```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
      log
      errors
      prometheus :9153
      trace zipkin
}
```



### forward

> https://coredns.io/plugins/forward/

{{% alert title="语法" color="" %}}

转发dns查询到上游dns服务器

```bash
# FROM 定义要转发的域，TO可以是上游dnsip或/etc/resolv.conf文件
forward FROM TO... {
    except IGNORED_NAMES...
    force_tcp
    prefer_udp
    expire DURATION
    max_fails INTEGER
    tls CERT KEY CA
    tls_servername NAME
    policy random|round_robin|sequential
    health_check DURATION [no_rec] [domain FQDN]
    max_concurrent MAX
    next RCODE_1 [RCODE_2] [RCODE_3...]
}
```

{{% /alert %}}



```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
      log
      errors
      prometheus :9153
      trace zipkin

      forward . 223.5.5.5 114.114.114.114 { expire 10s }
}
```





### cache

> https://coredns.io/plugins/cache/

{{% alert title="语法" color="" %}}

 缓存从后端（上游、数据库等）获取到的数据，默认 3600s

```bash
cache [TTL] [ZONES...] {
    success CAPACITY [TTL] [MINTTL]
    denial CAPACITY [TTL] [MINTTL]
    prefetch AMOUNT [[DURATION] [PERCENTAGE%]]
    serve_stale [DURATION] [REFRESH_MODE]
    servfail DURATION
    disable success|denial [ZONES...]
    keepttl
}
```

{{% /alert %}}



```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
      log
      errors
      prometheus :9153
      trace zipkin

      forward . 223.5.5.5 114.114.114.114 { expire 10s }
      cache 60
}
```





### hosts
> https://coredns.io/plugins/hosts/

{{% alert title="语法" color="" %}}

提供自定义dns解析的能力，默认5s扫描一次文件的变动

```bash
hosts [FILE [ZONES...]] {
    [INLINE]
    ttl SECONDS
    no_reverse
    reload DURATION
    fallthrough [ZONES...]
}
```

{{% /alert %}}

{{< tabpane text=true right=false >}}
  {{% tab header="样例1" lang="en" %}}

```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
      log
      errors
      prometheus :9153
      trace zipkin

      forward . 223.5.5.5 114.114.114.114 { expire 10s }
      cache 60
      
      hosts { 						# 使用本机的/etc/hosts文件
          1.2.3.4 zero-dew.cn 		# 扩展定义其他地址解析
          1.2.3.5 zero-dew.com
          ttl 600
          reload 30s
          fallthrough
        }
}
```



{{% /tab %}}

   {{% tab header="样例2" lang="en" %}}

```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
      log
      errors
      prometheus :9153
      trace zipkin

      forward . 223.5.5.5 114.114.114.114 { expire 10s }
      cache 60
      
      hosts /etc/test.host { 		# 使用/etc/test.host 文件中定义的地址解析
          1.2.3.4 zero-dew.cn 		# 扩展定义其他地址解析
          1.2.3.5 zero-dew.com
          ttl 600
          reload 30s
          fallthrough
        }
}
```



  {{% /tab %}}

{{< /tabpane >}}

监控指标

- `coredns_hosts_entries{}` DNS条目数量
- `coredns_hosts_reload_timestamp_seconds{}` 最近重载时间


### kubernetes

> https://coredns.io/plugins/kubernetes/


{{% alert title="语法" color="" %}}

动态提供svc、pod 等dns解析能力

```bash
kubernetes [ZONES...] {
    endpoint URL
    tls CERT KEY CACERT
    kubeconfig KUBECONFIG [CONTEXT]
    namespaces NAMESPACE...
    labels EXPRESSION
    pods POD-MODE
    endpoint_pod_names
    ttl TTL
    noendpoints
    fallthrough [ZONES...]
    ignore empty_service
}
```

{{% /alert %}}

```bash
.:53 {
      health localhost:8080 { 
            lameduck 5s 
      }
      ready localhost:8181
      reload
      log
      errors
      prometheus :9153
      trace zipkin

      forward . 223.5.5.5 114.114.114.114 { expire 10s }
      cache 60
      
      hosts { 						# 使用本机的/etc/hosts文件
          1.2.3.4 zero-dew.cn 		# 扩展定义其他地址解析
          1.2.3.5 zero-dew.com
          ttl 600
          reload 30s
          fallthrough
        }
      kubernetes cluster.local in-addr.arpa ip6.arpa {
          kubeconfig /root/.kube/kubeconfig # coredns 运行在k8s外
          pods insecure
          fallthrough in-addr.arpa ip6.arpa
          ttl 30
        }
}
```



```bash
dig @192.168.0.106 -p 53 a kubernetes.default.svc.cluster.local +short
# 反向解析
dig @192.168.0.106 -p 53 -x 172.168.0.1
```

