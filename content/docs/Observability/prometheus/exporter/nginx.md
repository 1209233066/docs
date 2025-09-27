---
title: "nginx-exporter"
linkTitle: "nginx-exporter"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 54
description: >
  nginx-exporter|exporter|prometheus

tags: ["prometheus","exporter","nginx-exporter"]
categories: ["prometheus","监控","exporter"]
url: prometheus/exporter/nginx-exporter.html
---

[nginx-exporter](https://github.com/nginx/nginx-prometheus-exporter) 支持对nginx 、nginx plugin(nginx的企业版)、nginx-ingress 暴露符合prometheus格式的指标。该文档只讨论开源版本的nginx的实施方案。

前提条件nginx 需要开启`stub_status` 指令,样例格式如下：

```nginx
server {
        listen 127.0.0.1:8080;
        location /stub_status {
                stub_status on;
                access_log off;
                allow 127.0.0.1;
                deny all;
        }
}
```





**部署安装**

> docker 镜像：`nginx/nginx-prometheus-exporter:1.4.0`
>
> 二进制文件： ` https://github.com/nginx/nginx-prometheus-exporter/releases/download/v1.4.0/nginx-prometheus-exporter_1.4.0_linux_amd64.tar.gz`

```bash
docker run -d \
--net=host \
nginx/nginx-prometheus-exporter:1.4.0 \
--nginx.scrape-uri=http://127.0.0.1:8080/stub_status
```



**添加prometheus配置**

```yaml
  - job_name: nginx
    static_configs:
    - targets:
      - 127.0.0.1:9113
```



**常用指标**

| Name       | Type  | Description                                                  | Labels |
| ---------- | ----- | ------------------------------------------------------------ | ------ |
| `nginx_up` | Gauge | Shows the status of the last metric scrape: `1` for a successful scrape and `0` for a failed one | []     |

[Stub status metrics](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html)

| Name                         | Type    | Description                          | Labels |
| ---------------------------- | ------- | ------------------------------------ | ------ |
| `nginx_connections_accepted` | Counter | 接受的客户端连接总数                 | []     |
| `nginx_connections_active`   | Gauge   | 活跃的连接数，包括处于等待状态的连接 | []     |
| `nginx_connections_handled`  | Counter | Handled client connections.          | [      |
| `nginx_connections_reading`  | Gauge   | nginx 读取的客户端请求头             | []     |
| `nginx_connections_waiting`  | Gauge   | 空闲的连接数                         | []     |
| `nginx_connections_writing`  | Gauge   | nginx 返回给客户端的响应.            | []     |
| `nginx_http_requests_total`  | Counter | 客户端请求总数                       | []     |





其他第三方方案

[nginx-lua-prometheus](https://github.com/knyar/nginx-lua-prometheus) 

[nginx-module-vts](https://github.com/vozlt/nginx-module-vts)

```bash
yum install -y GeoIP-devel.x86_64 pcre-devel openssl-devel 


wget http://nginx.org/download/nginx-1.22.1.tar.gz
tar xf nginx-1.22.1.tar.gz && cd nginx-1.22.1
git clone git://github.com/vozlt/nginx-module-vts.git


./configure \
--prefix=/opt/nginx \
--with-http_ssl_module \
--with-http_realip_module \
--with-http_geoip_module \
--with-http_stub_status_module \
--with-stream \
--with-stream=dynamic \
--with-stream_ssl_module \
--with-stream_realip_module \
--with-stream_geoip_module \
--add-module=./nginx-module-vts

make -j 4 && make install
```

```bash
./configure \
--prefix=/opt/nginx \
--with-http_ssl_module \
--with-http_realip_module \
--with-http_geoip_module \
--with-http_stub_status_module \
--with-stream \
--with-stream \
--with-stream_ssl_module \
--with-stream_realip_module \
--with-stream_geoip_module \
--add-module=./nginx-module-vts

make -j 4 && make install
```



```bash
./configure \
--user=nginx \
--prefix=/opt/nginx \
--sbin-path=/usr/bin \
--conf-path=/etc/nginx/nginx.conf \
--with-http_ssl_module \
--with-http_realip_module \
--with-http_geoip_module \
--with-http_stub_status_module \
--with-stream \
--with-stream_ssl_module \
--with-stream_realip_module \
--with-stream_geoip_module \
--add-module=./nginx-module-vts
```



基本的指标样例

```nginx
http {
    vhost_traffic_status_zone;

    ...

    server {

        ...

        location /status {
            vhost_traffic_status_display;
            vhost_traffic_status_display_format html;
            access_log off;
        }
    }
}
```

统计客户端ip国家信息

```nginx
http {
    geoip_country /usr/share/GeoIP/GeoIP.dat;

    vhost_traffic_status_zone;
    vhost_traffic_status_filter_by_set_key $geoip_country_code country::*;

    ...

    server {

        ...

        vhost_traffic_status_filter_by_set_key $geoip_country_code country::$server_name;

        location /status {
            vhost_traffic_status_display;
            vhost_traffic_status_display_format html;
        }
    }
}
```

```yaml
  - job_name: nginx-module-vts
    metrics_path: /status/format/prometheus
    static_configs:
    - targets:
      - 127.0.0.1
```

