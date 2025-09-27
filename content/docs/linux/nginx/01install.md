---
date: '2025-05-22T15:08:39+08:00'
draft: false
title: '安装nginx'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  install|nginx
tags: ["nginx"]
categories: ["nginx"]
url: nginx/install.html
author: "wangendao"
---

![](https://rpic.origz.com/api.php?category=photography)



### 安装部署
第一步：安装依赖
{{< tabpane text=true right=true >}}

  {{% tab header="centos" lang="en" %}}

```bash
#GCC (gun compiler collection)c语言编译器
#gcc-c++ c++语言编译器
yum install gcc gcc-c++ -y
# rewrite模块需要  pcre (perl compatible regular expression  per 兼容正则表达式) 
yum install pcre pcre-devel -y
# zlib 配置中gizp on 使用
yum install zlib zlib-devel -y
# openssl 提供https 和md5 sha1等
yum install openssl openssl-devel -y
```

  {{% /tab %}}
  {{% tab header="ubuntu" lang="en" %}}

```bash
# 更新软件包列表
sudo apt-get update
# 安装GCC和G++编译器
sudo apt-get install gcc g++ -y
# 安装PCRE库
sudo apt-get install libpcre3 libpcre3-dev -y
# 安装zlib库
sudo apt-get install zlib1g zlib1g-dev -y
# 安装OpenSSL库
sudo apt-get install openssl libssl-dev -y
```

  {{% /tab %}}
{{< /tabpane >}}


第二步下载源码并修改源代码（非必须）


```bash
wget http://nginx.org/download/nginx-1.22.1.tar.gz
tar xf nginx-1.22.1.tar.gz && cd nginx-1.22.1
```

**隐藏nginx标识和版本信息**:
> 修改源码位置：src/http/ngx_http_header_filter_module.c

{{< tabpane text=true right=true >}}


  {{% tab header="源码" lang="en" %}}

```c
static u_char ngx_http_server_string[] = "Server: nginx" CRLF;
static u_char ngx_http_server_full_string[] = "Server: " NGINX_VER CRLF;
static u_char ngx_http_server_build_string[] = "Server: " NGINX_VER_BUILD CRLF;
```
  {{% /tab %}}
  {{% tab header="修改后" lang="en" %}}

```c
static u_char ngx_http_server_string[] = "Server: IIS" CRLF;
static u_char ngx_http_server_full_string[] = "Server: IIS" CRLF;
static u_char ngx_http_server_build_string[] = "Server: IIS" CRLF;
```

  {{% /tab %}}
{{< /tabpane >}}


> 修改源码位置：src/http/ngx_http_special_response.c

{{< tabpane text=true right=true >}}

  {{% tab header="源码" lang="en" %}}

```c
static u_char ngx_http_error_full_tail[] =
"<hr><center>" NGINX_VER "</center>" CRLF
"</body>" CRLF
"</html>" CRLF
;


static u_char ngx_http_error_build_tail[] =
"<hr><center>" NGINX_VER_BUILD "</center>" CRLF
"</body>" CRLF
"</html>" CRLF
;


static u_char ngx_http_error_tail[] =
"<hr><center>nginx</center>" CRLF
"</body>" CRLF
"</html>" CRLF
;
```



  {{% /tab %}}
  {{% tab header="修改后" lang="en" %}}

```c
static u_char ngx_http_error_full_tail[] =
"<hr><center> IIS </center>" CRLF
"</body>" CRLF
"</html>" CRLF
;


static u_char ngx_http_error_build_tail[] =
"<hr><center> IIS </center>" CRLF
"</body>" CRLF
"</html>" CRLF
;


static u_char ngx_http_error_tail[] =
"<hr><center>IIS</center>" CRLF
"</body>" CRLF
"</html>" CRLF
;
```

{{% /tab %}}

{{< /tabpane >}}


第三步执行编译


```bash
useradd nginx -M -s /bin/nologin
```



```bash
./configure \
--prefix=/opt/nginx \
--user=nginx \
--group=nginx \
--with-http_ssl_module \
--with-http_flv_module \
--with-http_mp4_module \
--with-http_stub_status_module \
--with-http_gzip_static_module \
--with-stream_ssl_module \
--with-stream \
--with-http_realip_module \
--with-pcre \
--with-debug
```

```bash
make && make install
#查看编译信息
/opt/nginx/sbin/nginx -V
```

```bash
# 启动服务
/opt/nginx/sbin/nginx
```


```bash
nginx-1.22.1]# curl -I 127.0.0.1
HTTP/1.1 200 OK
Server: IIS
Date: Thu, 22 May 2025 07:39:59 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Thu, 22 May 2025 07:39:16 GMT
Connection: keep-alive
ETag: "682ed4a4-267"
Accept-Ranges: bytes
```