---
title: "amtool"
linkTitle: "amtool"
date: 2025-05-14
toc_hide: false
hide_summary: true
weight: 3
description: >
  amtool|alertmanager|prometheus

tags: ["prometheus","alertmanager","amtool"]
categories: ["prometheus","alertmanager"]
url: prometheus/alertmanager/amtool.html
---

### amtool

`amtool` is a cli tool for interacting with the Alertmanager API.

go get github.com/prometheus/alertmanager/cmd/amtool

配置文件

> 需要配置到`/etc/amtool/config.yml`
>
> 或`$HOME/.confg/amtool/config.yml`

```bash
tee /etc/amtool/config.yml <<EOF
alertmanager.url: http://127.0.0.1:9093
author: "1209233066@qq.com"
require-comment: true
output: josn
date.format: "2006-01-02 15:04:05 MST"
EOF
```



| 命令         | 子命令 | 举例                                                         | 举例解释                                                     |
| ------------ | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| alert        |        | <font color=#78bd5b80>amtool alert</font>                    | 查看所有告警                                                 |
|              | add    | <font color=#6ed6c680>amtool alert add alertname=test labe-a=value-b </font> | 添加一个名称为`test`的带有标签为：`labe-a=value-b`的告警     |
|              | query  | <font color=#bda85b80>amtool alert query alertname=test labe-a=value-b</font> | 查看指定标签的告警                                           |
|              |        | <font color=#bda85b80>amtool alert query alertname=test labe-a=value-b -o json</font> | json 格式展示告警详细信息                                    |
|              |        | <font color=#bda85b80>amtool alert query alertname=test labe-a=value-b -o extended</font> | 扩展格式显示告警                                             |
| silence      |        | <font color=#78bd5b80>amtool silence </font>                 | 查看所有维护期的告警                                         |
|              | add    | <font color=#6ed6c680>amtool silence add alertname=test labe-a=value-b  --commen “this is test”</font> | 添加一个名称为`test`的带有标签为：`labe-a=value-b`的维护期，默认1h |
|              |        | <font color=#6ed6c680>amtool silence add alertname=test labe-a=value-b  --commen “this is test” --duration="2h"</font> | 设置2h维护期                                                 |
|              | query  | <font color=#bda85b80>amtool silence query alertname=test labe-a=value-b -o extended</font> | 查看指定标签的维护期                                         |
|              |        | <font color=#bda85b80>amtool silence query alertname=test labe-a=value-b -o json</font> | json 格式展示维护期的详细信息                                |
|              |        | <font color=#bda85b80>amtool silence query alertname=test labe-a=value-b -o extended</font> | 扩展格式显示维护期                                           |
|              | expire | <font color=#f63bce80>amtool silence expire 223eb624-f49d-498d-ac7d-34bb7570adea</font> | 提前取消维护期(id 通过 amtool silence 查询)                  |
| config       |        |                                                              |                                                              |
| template     |        |                                                              |                                                              |
| check-config |        | amtool check-config alertmanager.yml                         |                                                              |
