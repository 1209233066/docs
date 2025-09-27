---
date: '2025-06-30T15:04:12+08:00'
draft: false
title: '音乐'
type: blog
toc_hide: false
hide_summary: true
weight: 3
description: >
  自建音乐播放器
tags: ["navidrome","music_tag_web","filebrowser "]
categories: ["娱乐"]
url: 2025-07-03/music.html
author: "wangendao"
---





组件：
- [x] navidrome 音乐服务端程序
- [x] music-tag-web 负责刮削音乐原数据信息
- [x] filebrowser 负责通过网页端上传音乐文件

---

### 部署
```bash
mkdir -p data/filebrowser 
touch data/filebrowser/database.db
```
```bash
services:
  navidrome:
    #image: deluan/navidrome:latest
    image: harbor.pytc.com/music/navidrome:0.54.3
    container_name: navidrome
    privileged: true
    ports:
      - "8001:4533"
    volumes:
      - ./data/music:/music # 音乐
      - ./data/navidrome:/data # 数据库和cache
    command:
    - /navidrome 
    - --datafolder=/data
    - --musicfolder=/music
    restart: unless-stopped
  music-tag:
    #image: xhongc/music_tag_web:latest
    image: harbor.pytc.com/music/xhongc/music_tag_web:2.3.2
    container_name: music-tag-web
    ports:
      - "8002:8002"
    volumes:
      - ./data/music:/app/media:rw
      - ./data/music-tag/config:/app/data
    restart: unless-stopped
  filebrowser:
    image: harbor.pytc.com/music/filebrowser/filebrowser:v2.31.2
    container_name: filebrowser
    ports:
      - "8003:80"
    volumes:
      - ./data/filebrowser/database.db:/database.db
      - ./data/music:/srv
```

### 使用


