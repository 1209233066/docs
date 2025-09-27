---
title: "nginx"
linkTitle: "nginx"
date: 2025-05-22
simple_list: true
weight: 99
url: linux/nginx
type: docs
---

*简介*

Nginx (engine x http://nginx.org)是一个高性能的HTTP和反向代理服务器，也是一个IMAP/POP3/SMTP服务器。Nginx是由伊戈尔·赛索耶夫开发的，第一个公开版本0.1.0发布于2004年10月4日。其特点是占用内存少，并发能力强。

*应用场景*

| 应用场景                     | 竞争产品       |
| ---------------------------- | -------------- |
| 静态服务器（图片、视频服务器 | lighttpd       |
| 动态服务                     | nignx +fastcgi |
| 反向代理 负载均衡            | haproxy        |
| cache(web缓存)               | vanish         |




### 安装nginx
### 配置详解
1. 全局配置
2. http服务
3. location
4. upsteam
5. rewrite
6. log
### 模块


#### ngx_http_autoindex_module

生成目录列表所用
https://nginx.org/en/docs/http/ngx_http_autoindex_module.html



`http、 server、 location`

```nginx
location / {
    autoindex on;
    autoindex_exact_size on; # 精确输出文件大小
    autoindex_format html;   # 展示格式 html/xml/json/jsonp
    autoindex_localtime on; # 时间展示
}
```

#### [ngx_http_stub_status_module](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html)
**stub_status**

```nginx
stub_status
syntax: stub_status on
default: None
context: location
Enables the status handler in this location.


location /nginx_status {
  stub_status on;
  access_log   off;
  allow SOME.IP.ADD.RESS;
  deny all;
}

active connections -- number of all open connections including connections to backends 

server accepts handled requests -- nginx accepted 16630948 connections, handled 16630948 connections (no one was closed just it was accepted), and handles 31070465 requests (1.8 requests per connection) 

reading -- nginx reads request header 

writing -- nginx reads request body, processes request, or writes response to a client 

waiting -- keep-alive connections, actually it is active - (reading + writing)

```


#### [gx_http_rewrite_module](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html)

```nginx

```