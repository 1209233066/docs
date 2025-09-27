---
date: '2025-06-12T15:22:40+08:00'
draft: false
title: 'processors'
linkTitle: 'processors'
type: blog
toc_hide: false
hide_summary: true
weight: 5
description: >
 
tags: ["processors","filebeat"]
categories: ["ELK"]
url: elk/processors.html
author: "wangendao"
---

{{% alert title="文档环境" color="" %}}

os 版本： `CentOS Linux release 7.9.2009 (Core)`

filebeat版本：`7.17.29`

elasticsearch版本： `7.15.0`

{{% /alert %}}



<table>
    <tr>
        <td><img src="https://www.elastic.co/docs/reference/beats/filebeat/images/filebeat.png" alt="架构"></td>
        <td>
            <a href="https://www.elastic.co/guide/en/beats/filebeat/7.17/filtering-and-enhancing-data.html"  target="_blank">文档</a><br>
        </td>
        <td>
            <a href="https://mirrors.huaweicloud.com/filebeat/"  target="_blank">下载</a><br>
        </td>
        <td>
            <a href="https://www.docker.elastic.co"  target="_blank">docker镜像</a>
        </td>
    </tr>
</table>




[**processors**](https://www.elastic.co/guide/en/beats/filebeat/8.18/filtering-and-enhancing-data.html) 用于日志过滤和日志标签增删改。从功能上我把它理解为*prometheus*或*promtai*l中的`relabel_configs `。从filebeat 自身出发，已经提供了`include_lines` `exclude_lines` `exclude_files` 的过滤功能。但是Processors能够在全局角度提供更加灵活的日志处理方式。包括：`日志过滤`、`元数据添加`、`日志解析`以及`添加额外处理逻辑`。



{{% alert title="processors日志处理逻辑" color="" %}}

多个processor 按照定义顺序执行，建议将`drop_fields`、`rename` 放在最后执行。

```bash
event -> processor 1 -> event1 -> processor 2 -> event2 ...
```

{{% /alert %}}

### processors语法

> 配置文件位置：
>
> + 位于顶级配置段，全局生效
> + 位于指定`input`下，仅在该`input`下生效



{{< tabpane text=true right=false >}}
  {{% tab header="**语法格式**:" disabled=true /%}}
  {{% tab header="格式1" lang="yaml" %}}

```yaml
processors:
  - <processor_name>:  # 定义一个processor 名称，见名知意
      when:
        <condition>   # 定义条件。可选选项
      <parameters>    # 当条件满足时出发的动作

  - <processor_name>:
      when:
        <condition>
      <parameters>
```

  {{% /tab %}}
  {{% tab header="格式2" lang="yaml" %}}

```yaml
processors:
  - if:
      <condition>
    then: 
      - <processor_name>:
          <parameters>
      - <processor_name>:
          <parameters>
      ...
    else: 
      - <processor_name>:
          <parameters>
      - <processor_name>:
          <parameters>
```

  {{% /tab %}}
{{< /tabpane >}}





#### 条件表达式（condition）

- [`equals`](https://www.elastic.co/guide/en/beats/filebeat/8.18/defining-processors.html#condition-equals)

  示例：

  ```bash
  filebeat.inputs:
  - type: filestream
    enabled: true
    paths:
    - /var/log/*.log
    processors:
    - drop_event:
        when:
          equals:
            status: "firing"
  
  output.console:
    pretty: true
  ```

  

  

- [`contains`](https://www.elastic.co/guide/en/beats/filebeat/8.18/defining-processors.html#condition-contains)

  示例：

  ```yaml
  filebeat.inputs:
  - type: filestream
    enabled: true
    paths:
    - /var/log/*.log
    processors:
    - drop_event:
        when:
          contains:
            status: "firing"
  
  output.console:
    pretty: true
  ```

  

  

  

- [`regexp`](https://www.elastic.co/guide/en/beats/filebeat/8.18/defining-processors.html#condition-regexp)

  示例：

  ```yaml
  filebeat.inputs:
  - type: filestream
    enabled: true
    paths:
    - /var/log/*.log
    processors:
    - drop_event:
        when:
          regexp:
            status: "^firing"
  
  output.console:
    pretty: true
  ```

  

- [`range`](https://www.elastic.co/guide/en/beats/filebeat/8.18/defining-processors.html#condition-range)

  > 支持通过`lt`(小于)、 `gt`(大于)、 `lte`(小于等于)、 `gte`(大于等于)符号判断

  示例：

  
  
  ```yaml
  processors:
  - drop_event:
      when:
        range:
          http.response.code:
            lte: 400
  ```
  
  
  
  
  
  ```yaml
  # 200<= http.response.code <=400
  processors:
  - drop_event:
      when:
        range: 
          http.response.code.lte: 400
          http.response.code.gte: 200
  ```
  
  

  
  
- [`network`](https://www.elastic.co/guide/en/beats/filebeat/8.18/defining-processors.html#condition-network)

  > 用于判断*ip*是否在指定的网络范围,有效取值包括：
  >
  > + `loopback` 代表回环地址127.0.0.0/8  、::1/128
  > + `private` ipv4定义的私有地址
  > + 使用 CIDR 表示法

  示例：

  ```yaml
  processors:
  - drop_event:
      when:
        network:
          destination.ip: ['192.168.1.0/24', '10.0.0.0/8', loopback]
  ```

  

- [`has_fields`](https://www.elastic.co/guide/en/beats/filebeat/8.18/defining-processors.html#condition-has_fields)

  示例：

  ```yaml
  processors:
  - drop_event:
      when:
        has_fields: ["kubernetes.labels.filebeat"]
  ```

  

- [`or`](https://www.elastic.co/guide/en/beats/filebeat/8.18/defining-processors.html#condition-or)  和 [`and`](https://www.elastic.co/guide/en/beats/filebeat/8.18/defining-processors.html#condition-and)

  示例：

  ```yaml
  processors:
  - drop_event:
      when:
        or:
        - has_fields: ["kubernetes.labels.filebeat"]
        - network:
            destination.ip: ['192.168.1.0/24', '10.0.0.0/8', loopback]
  ```

  

  

- [`not`](https://www.elastic.co/guide/en/beats/filebeat/8.18/defining-processors.html#condition-not)

  示例：

  ```yaml
  processors:
  - drop_event:
      when:
        not:
          has_fields: ["kubernetes.labels.filebeat"]
  ```

  



#### 当条件满足时出发的动作

- [**`drop_event`**](https://www.elastic.co/guide/en/beats/filebeat/8.18/drop-event.html)丢弃整个事件（通常与条件判断结合）

  ```yaml
  processors:
  # 丢弃开头为^DEBUG的日志
  - drop_event:
      when:
        regexp:
          message: "^DEBUG"
  ```

  

- [`drop_fields`](https://www.elastic.co/guide/en/beats/filebeat/8.18/drop-fields.html)

  ```yaml
  processors:
  # 丢弃开头为^DEBUG的日志
  - drop_event:
      when:
        regexp:
          message: "^DEBUG"
  
  - drop_fields:
      when:
        has_fields: ["kubernetes.labels.filebeat"]
        ignore_missing: true  # 当缺失签时忽略错误
  ```

  

- [**`rename`**](https://www.elastic.co/guide/en/beats/filebeat/8.18/rename-fields.html) 重命名字段

  ```yaml
  processors:
  # 丢弃开头为^DEBUG的日志
  - drop_event:
      when:
        regexp:
          message: "^DEBUG"
  
  - drop_fields:
      when:
        has_fields: ["kubernetes.labels.filebeat"]
        ignore_missing: true  # 当缺失签时忽略错误
        
  - rename:
      ignore_missing: false
      fail_on_error: true
      fields:
      - from: "msg"
        to: "message" 
  ```

  

- [`replace`](https://www.elastic.co/guide/en/beats/filebeat/8.18/replace-fields.html)

  > 替换值，例如把字段`message`的值改为`INFO`

  ```bash
  processors:
  # 丢弃开头为^DEBUG的日志
  - drop_event:
      when:
        regexp:
          message: "^DEBUG"
  
  - drop_fields:
      when:
        has_fields: ["kubernetes.labels.filebeat"]
        ignore_missing: true  # 当缺失签时忽略错误
        
  - rename:
      ignore_missing: false
      fail_on_error: true
      fields:
      - from: "msg"
        to: "message"
        
  - replace:
        fields:
          - field: "message"
            pattern: "^(I|i|info|INFO)"
            replacement: "INFO"
        ignore_missing: false
        fail_on_error: true
  ```

  

- [`add_fields`](https://www.elastic.co/guide/en/beats/filebeat/8.18/add-fields.html)

  ```yaml
  - add_fields:
      fields:
        "kubernetes.labels.filebeat": "true"
        when:
          not:
            has_fields: ["kubernetes.labels.filebeat"] 
  ```

  

  

- [**`add_labels`**](https://www.elastic.co/guide/en/beats/filebeat/8.18/add-labels.html)添加label

  

  ```yaml
  processors:
    - add_fields:
        target: ''
        fields:
          environment: 'uat'
          project: 'my-awesome-app'
  ```

- [add_tags](https://www.elastic.co/guide/en/beats/filebeat/8.18/add-tags.html)

  ```yaml
  processors:
    - add_tags:
        tags: ["web", "production"]
        target: "environment"
  ```

  

- [`add_locale`](https://www.elastic.co/guide/en/beats/filebeat/8.18/add-locale.html)  和 [`timestamp`](https://www.elastic.co/guide/en/beats/filebeat/8.18/processor-timestamp.html)

  ```yaml
  # 配合时间戳处理器使用
  processors:
  - add_locale:
      format: offset
  - timestamp:
      field: log_time
      timezone: '{{event.timezone}}'
  ```

  

- [`add_kubernetes_metadata`](https://www.elastic.co/guide/en/beats/filebeat/8.18/add-kubernetes-metadata.html)

- [`decode_json_fields`](https://www.elastic.co/guide/en/beats/filebeat/8.18/decode-json-fields.html)

  ```bash
  filebeat.inputs:
  - type: filestream
    enabled: true
    paths:
    - /var/log/*.log
  processors:
    - decode_json_fields:
        fields: ["message"]
        process_array: false
        max_depth: 1
        target: ""
        overwrite_keys: false
        add_error_key: true
  
  output.console:
    pretty: true
  ```

  

  

- **`dissect`** / **`grok`**: **非常强大**的处理器，用于**解析**非结构化的日志文本，并将其结构化为多个字段。

  + **Dissect**：使用简单的分隔符匹配，性能极高。
  
    日志格式
  
    ```yaml
    # 日志示例：2023-10-27 12:01:45 [ERROR] Service payment failed.
    ```
  
    ```yaml
    processors:
      - dissect:
          tokenizer: "%{+YYYY-MM-dd} %{+HH:mm:ss} [%{log.level}] Service %{service.name} %{service.status}"
          field: "message"
          target_prefix: ""
    ```
  
    
  
  + **Grok**：使用复杂的正则表达式模式，功能更强大但更耗 CPU。
  
  
  
- [`script`](https://www.elastic.co/guide/en/beats/filebeat/8.18/processor-script.html)

- [`include_fields`](https://www.elastic.co/guide/en/beats/filebeat/8.18/include-fields.html)

- [`syslog`](https://www.elastic.co/guide/en/beats/filebeat/8.18/syslog.html)

  

- [`convert`](https://www.elastic.co/guide/en/beats/filebeat/8.18/convert.html)

- [`copy_fields`](https://www.elastic.co/guide/en/beats/filebeat/8.18/copy-fields.html)

- [`add_process_metadata`](https://www.elastic.co/guide/en/beats/filebeat/8.18/add-process-metadata.html)

- [`add_tags`](https://www.elastic.co/guide/en/beats/filebeat/8.18/add-tags.html)

- [`append`](https://www.elastic.co/guide/en/beats/filebeat/8.18/append.html)

- [`add_id`](https://www.elastic.co/guide/en/beats/filebeat/8.18/add-id.html)



```yaml
processors:
# 对日志行{ "outer": "value", "inner": "{\"data\": \"value\"}" } 解析
- decode_json_fields：
    fields: ["inner"]
# 丢弃开头为^DEBUG的日志
- drop_event:
    when:
      regexp:
        message: "^DEBUG"
# 丢弃来源包含test的日志
- drop_event:
    when:
      contains:
        source: "test"
```





