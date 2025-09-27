---
date: '2025-05-31T15:22:40+08:00'
draft: false
title: '示例'
type: blog
toc_hide: false
hide_summary: true
weight: 3
description: >
  demo|kubernetes
tags: ["coredns","demo"]
categories: ["coredns"]
url: kubernetes/demo.html
author: "wangendao"


---

![](https://rpic.origz.com/api.php?category=photography)

{{< tabpane text=true right=false >}}
  {{% tab header="物理机环境下作为dns服务器" lang="en" %}}

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


```bash

tee /usr/lib/systemd/system/coredns.service <<EOF
[Unit]
Description=coredns service https://coredns.io/
After=network.target

[Service]
ExecStart=/usr/bin/coredns -conf /etc/corefile -pidfile /var/run/coredns.pid 
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl enable coredns --now
```

  {{% /tab %}}
  {{% tab header="运行在k8s环境中" lang="en" %}}


```bash
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        hosts { 						      
          1.2.3.4 zero-dew.cn
          1.2.3.5 zero-dew.com
          ttl 600
          reload 30s
          fallthrough cluster.local in-addr.arpa ip6.arpa  # hosts 执行在kubernetes之前
        }
        cache 30
        loop
        reload
        loadbalance
    }
```
  {{% /tab %}}
{{< /tabpane >}}
