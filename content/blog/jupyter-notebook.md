---
date: '2025-08-12T08:34:29+08:00'
draft: false
title: 'jupyter-notebook'
type: blog
toc_hide: false
hide_summary: true
weight: 9
description: >
  jupyter-notebook 运行python程序
tags: ["jupyter-notebook"]
categories: ["python"]
url: 2025-08-12/jupyter-notebook.html
author: "wangendao"
---



**安装jupyter-notebook**

```bash
FROM python:3.11.12-alpine3.21

LABEL maintainer=1209233066@qq.com
RUN apk add gcc musl-dev linux-headers
RUN pip3 install akshare jupyter notebook pandas -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 80

WORKDIR /opt
CMD ["jupyter","notebook","--ip","0.0.0.0","--port","80","--allow-root"]
```



**启动jupyter-notebook**

```bash
jupyter-notebook --ip 0.0.0.0 --port 80 --allow-root
```











