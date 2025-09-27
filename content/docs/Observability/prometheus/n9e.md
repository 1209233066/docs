---
title: "夜莺·监控系统"
linkTitle: "夜莺·监控系统"
date: 2025-05-13
toc_hide: false
hide_summary: true
weight: 7
description: >
  夜莺·监控系统
tags: ["夜莺·监控系统"]
categories: ["夜莺·监控系统","监控"]
url: prometheus/n9e.html
---

通过自行构建image，快速体验夜莺
```bash
git clone https://github.com/ccfos/nightingale.git
```
> 位置 nightingale/Dockerfile.nightingale
```Dockerfile
FROM node:16-alpine AS fe-builder

RUN apk add git

RUN git clone https://github.com/n9e/fe.git && cd fe && \
    git checkout $(git describe --tags --abbrev=0) && \
    npm config set registry https://registry.npmmirror.com &&\
    npm install && \
    npm run build


FROM golang:1.23.4-alpine3.20 AS builder

COPY --from=fe-builder /fe/pub /pub
RUN apk add git
RUN git clone https://github.com/ccfos/nightingale.git && cd nightingale &&\
    git checkout $(git describe --tags --abbrev=0) &&\
    export GOPROXY="https://goproxy.cn,direct" &&\
    go install github.com/rakyll/statik@latest &&\
    statik --src=/pub -dest=./front &&\
    go build -ldflags "-w -s -X github.com/ccfos/nightingale/v6/pkg/version.Version=$(git describe --tags --abbrev=0)" -o /n9e ./cmd/center/main.go


FROM python:3-slim

WORKDIR /app
COPY --from=builder /n9e /app/
ADD etc /app/etc/
ADD integrations /app/integrations/

RUN pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 17000

CMD ["/app/n9e", "-h"]
```


> 位置 nightingale/docker/compose-bridge/docker-compose.yaml
```Dockerfile
networks:
  nightingale:
    driver: bridge

services:
  mysql:
    image: "mysql:8"
    container_name: mysql
    hostname: mysql
    restart: always
    environment:
      TZ: Asia/Shanghai
      MYSQL_ROOT_PASSWORD: 1234
    volumes:
      - ./data/mysqldata:/var/lib/mysql/
      - ../initsql:/docker-entrypoint-initdb.d/
      - ./etc-mysql/my.cnf:/etc/my.cnf
    networks:
      - nightingale
    ports:
      - "3306:3306"

  redis:
    image: "redis:6.2"
    container_name: redis
    hostname: redis
    restart: always
    environment:
      TZ: Asia/Shanghai
    networks:
      - nightingale
    ports:
      - "6379:6379"

  # prometheus:
  #   image: prom/prometheus
  #   container_name: prometheus
  #   hostname: prometheus
  #   restart: always
  #   environment:
  #     TZ: Asia/Shanghai
  #   volumes:
  #     - ./etc-prometheus:/etc/prometheus
  #   command:
  #     - "--config.file=/etc/prometheus/prometheus.yml"
  #     - "--storage.tsdb.path=/prometheus"
  #     - "--web.console.libraries=/usr/share/prometheus/console_libraries"
  #     - "--web.console.templates=/usr/share/prometheus/consoles"
  #     - "--enable-feature=remote-write-receiver"
  #     - "--query.lookback-delta=2m"
  #   networks:
  #     - nightingale
  #   ports:
  #     - "9090:9090"

  victoriametrics:
    image: victoriametrics/victoria-metrics:v1.79.12
    container_name: victoriametrics
    hostname: victoriametrics
    restart: always
    environment:
      TZ: Asia/Shanghai
    ports:
      - "8428:8428"
    networks:
      - nightingale
    command:
      - "--loggerTimezone=Asia/Shanghai"
    volumes:
      - "./data/victoriametrics:/victoria-metrics-data"

  loki:
    image: grafana/loki:3.5.0
    container_name: loki
    hostname: loki
    restart: always
    user: root
    environment:
      TZ: Asia/Shanghai
    ports:
      - "3100:3100"
    volumes:
      - ./data/loki:/loki
    networks:
      - nightingale
 

  nightingale:
    build:
      context: ../..
      dockerfile: Dockerfile.nightingale
    container_name: nightingale
    hostname: nightingale
    restart: always
    environment:
      GIN_MODE: release
      TZ: Asia/Shanghai
      WAIT_HOSTS: mysql:3306, redis:6379
    volumes:
      - ./etc-nightingale:/app/etc
    networks:
      - nightingale
    ports:
      - "17000:17000"
      - "20090:20090"
    depends_on:
      - mysql
      - redis
      - victoriametrics
    command: >
      sh -c "/app/n9e"

  categraf:
    image: "flashcatcloud/categraf:latest"
    container_name: "categraf"
    hostname: "categraf01"
    restart: always
    environment:
      TZ: Asia/Shanghai
      HOST_PROC: /hostfs/proc
      HOST_SYS: /hostfs/sys
      HOST_MOUNT_PREFIX: /hostfs
      WAIT_HOSTS: nightingale:17000, nightingale:20090
    volumes:
      - ./etc-categraf:/etc/categraf/conf
      - /:/hostfs
    networks:
      - nightingale
    depends_on:
      - nightingale

```

```bash
cd nightingale/docker/compose-bridge/
docker-compose up 
```