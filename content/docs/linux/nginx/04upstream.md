---
date: '2025-05-22T15:43:37+08:00'
draft: false
title: '反向代理'
type: blog
toc_hide: false
hide_summary: true
weight: 3
description: >
  7层反向代理|nginx
tags: ["方向代理"]
categories: ["nginx"]
url: nginx/upstream.html
author: "wangendao"
---

![](https://rpic.origz.com/api.php?category=photography)

# 反向代理
nginx 是一个高性能的HTTP和反向代理服务器，本章主要介绍nginx的反向代理配置。

{{< tabpane text=true right=false >}}
  {{% tab header="四层代理" lang="en" %}}

{{% alert title="Info" color="" %}}
nginx 在1.9 版本后开始支持 4层代理
{{% /alert %}}

配置文件示例：

```nginx
user  nginx;
worker_processes  1;

events {
    worker_connections  1024;
}
stream {
        log_format main '$remote_addr [$time_local] '
             '$protocol $status $bytes_sent $bytes_received '
             '$session_time "$upstream_addr" '
             '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';
        upstream mysql {
                server 172.16.100.10:3306 weight=1 max_fails=3 fail_timeout=30s;
                server 172.16.100.11:3306 weight=1 max_fails=3 fail_timeout=30s;
                server 172.16.100.12:3306 weight=1 max_fails=3 fail_timeout=30s;
        }
        server {
                listen 3306;
                proxy_connect_timeout 2s;
                proxy_timeout 900s;
                proxy_pass mysql;
                access_log  /dev/stdout main;
          }
}
```

  {{% /tab %}}
  {{% tab header="七层代理" lang="en" %}}

```nginx
user  nginx;
worker_processes  1;

events {
    worker_connections  1024;
}
http {
upstream backend {
    # backup 当其他主机失败后使用该主机，不能用在 hash ip_hash 和random 调度算法中
    # down 当前主机不可用，当使用ip_hash 中标记为down不会影响hash值
    server 172.16.100.10:8080 weight=1 max_fails=3 fail_timeout=30s;
    server 172.16.100.11:8080 weight=1 max_fails=3 fail_timeout=30s;
    server 172.16.100.12:8080 weight=1 max_fails=3 fail_timeout=30s;
  
    server 172.16.100.13:8080   backup;
    server 172.16.100.14:8080   backup;
}

server {
    # 设置X-Real-IP头，让服务端看到客户端的真实IP地址。
    proxy_set_header  X-Real-IP $remote_addr;
    # 设置X-Forwarded-For头，添加原始请求的IP地址
    proxy_set_header  X-Forwarded-For $remote_addr;
    # 设置代理请求的Host头，使用请求的原始主机名
    proxy_set_header Host $host;
    # 设置客户端请求的最大body大小为50MB
    client_max_body_size 50m;
    # 设置客户端请求body的缓冲区大小为256KB
    client_body_buffer_size 256k;
    location / {
        
        proxy_pass http://backend;
        
        }
    }
}
```

  {{% /tab %}}
{{< /tabpane >}}



对于七层代理服务器主要有[ngx_http_upstream_module](https://nginx.org/en/docs/http/ngx_http_upstream_module.html)和[ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) 模块实现，

### **ngx_http_proxy_module**

1. proxy_set_header 设置 http 请求 header并传递给后端服务器。 格式 `proxy_set_header field value;`

2. proxy_pass 把用户的请求转向到反向代理定义的 upstream 服务器池

3. proxy_redirect 重写location并刷新从upstream server收到的报文的首部；

4. client_body_buffer_size  指定客户端请求主体缓冲区大小

5. proxy_connect_timeout 30s; 反向代理与后端节点服务器连接的超时时间

6. proxy_send_timeout 在规定时间之内后端服务器必须传完所有数据，否则 Nginx 将断开这个连接

7. proxy_read_timeout Nginx 从代理的后端服务器获取信息的超时时间

8. proxy_buffering on; #如果缓冲区开启，把内容保存在由指令 proxy_buffer_size  proxy_buffers

9. proxy_buffer_size 32k;  #默认来说,该缓冲区大小等于指令proxy_buffers

10. proxy_buffers 32 4k;  设置缓冲区的数量和大小，Nginx 从代理的后端服务器获取的响应信息会放置到缓冲区

11. proxy_busy_buffers_size 64k;  设置系统很忙时使用的 proxy_buffers 大小，官方推荐为 proxy_buffers * 2

12. proxy_temp_file_write_size  指定 proxy 缓存临时文件的大小

13. proxy_next_upstream error timeout  #请求发生错误分配到写一个web

14. proxy_cookie_domain 将upstream server通过Set-Cookie首部设定的domain属性修改为指定的值，其值可以为一个字符串、正则表达式的模式或一个引用的变量；

15. proxy_cookie_path 将upstream server通过Set-Cookie首部设定的path属性修改为指定的值，其值可以为一个字符串、正则表达式的模式或一个引用的变量；

16. proxy_hide_header 设定发送给客户端的报文中需要隐藏的首部；

**获取到真实的用户ip**
{{% alert title="" color="" %}}

位置：`server` `location ` 指令下

{{% /alert %}}

配置示例：

```nginx
location / {
    proxy_pass http://backend_server;


    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;                      # 客户端真实 IP（单值）
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # 记录完整的代理路径（多层代理时拼接所有中间节点 IP）
    proxy_set_header X-Forwarded-Proto $scheme;                   # 协议（http/https）
}
```

**重写发送给后端的http请求头的Host**
{{% alert title="" color="" %}}

位置：`server` `location ` 指令下

{{% /alert %}}

配置示例：

```nginx
location / {

    proxy_pass http://backend_server;
    proxy_set_header Host $host;

}
```

**设置代理连接超时时间**
{{% alert title="" color="" %}}

位置：`server` `location ` 指令下

{{% /alert %}}

配置示例：

```nginx
location / {
    
    proxy_pass http://backend_server;
    
    proxy_connect_timeout 30;           # 设置代理连接超时时间为30秒。
    proxy_send_timeout 30;              # 设置代理发送请求的超时时间为30秒。
    proxy_read_timeout 60;              # 设置代理读取响应的超时时间为60秒。
}
```

**设置代理buffer**
{{% alert title="" color="" %}}

位置：`server` `location ` 指令下

{{% /alert %}}

配置示例：

```nginx
location / {
    
    proxy_pass http://backend_server;

    proxy_buffering on;
    proxy_buffer_size 32k;            # 设置代理缓冲区的大小为4KB
    proxy_buffers 4 32k;             # 设置代理缓冲区的数量和大小 为4*32KB。
    proxy_busy_buffers_size 64k;     # 设置代理繁忙缓冲区的大小为64KB
}
```


**提高代理的容错能力**
{{% alert title="" color="" %}}

位置：`server` `location ` 指令下

{{% /alert %}}

配置示例：

```nginx
location / {
    
    proxy_pass http://backend_server;
    # 定义当出现错误、超时、无效头部、或HTTP状态码为500、503、404时，请求将被转发到下一个上游服务器。
    proxy_next_upstream error timeout invalid_header http_500 http_503 http_404;
}
```

**镜像静态内容到本地磁盘**
{{% alert title="" color="" %}}

位置：`server` `location ` 指令下

{{% /alert %}}

配置示例：

```nginx
location / {
    
    proxy_pass http://backend_server;

    proxy_store on;                             # 开启代理存储静态内容到磁盘的功能
    proxy_store_access user:rw group:rw all:r;  # 设置代理存储文件的访问权限。
    proxy_temp_path /dev/shm/nginx_proxy;       # 定义了代理临时文件存储的路径
}
```





### 调度算法

Nginx使用的负载均衡调度算法主要有以下几种：

1. **轮询（rr Round Robin）**：这是默认的负载均衡算法。每个请求按时间顺序逐一分配到不同的后端服务器，如果服务器down掉，能自动剔除。

2. **加权轮询（wrr Weighted Round Robin）**：与轮询类似，但是不同的后端服务器可以设置不同的权重，可以根据服务器的处理能力，分配不同数量的请求。权重越高，分配的请求越多。

3. **最少连接（least_conn Least Connections）**：优先分配给当前连接数最少的服务器，适用于请求处理时间相差较大的情况。

4. **IP Hash(ip_hash)**：根据请求的IP的hash结果分配，每个请求会固定访问一个后端服务器，适用于需要会话保持的应用。这有助于为缓存服务器实现更高的缓存命中率,如果其中一台服务器需要临时删除，则应使用down参数标记该服务器，以保留客户端IP地址的当前哈希值

5. **URL Hash(url_hash)**：根据请求的URL的hash结果来分配请求，使得每个URL定向到同一个后端服务器，适用于服务器缓存时提高效率。

6. **Fair（第三方）**：按后端服务器的响应时间来分配请求，响应时间短的优先分配。

7. **URL参数（第三方）**：按照URL中带的参数进行hash，然后进行请求分发，可以实现会话保持。

*以上算法可以通过在Nginx的http或stream模块中使用upstream指令来配置。*