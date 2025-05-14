---
title: "shortcode"
linkTitle: "shortcode"
date: 2025-05-09

toc_hide: false   #隐藏左侧菜单
hide_summary: true #隐藏描述
weight: 4
description: >
  使用hugo & docsy 构建站点

tags: ["hugo","shortcode"]
categories: ["hugo"]
url: hugo/shortcode.html
---
---

### alert 短代码创建一个 alert 块，可用于显示通知或警告。

> color="" 支持 primary、info、warning

短代码:
```markdown
{{%/* alert title="Info" color="info" */%}}
This is a info.
{{%/* /alert */%}}
```


渲染为：
{{% alert title="Info" color="info" %}}
This is a info.
{{% /alert %}}

短代码:
```markdown
{{%/* alert title="Warning" color="warning" */%}}
This is a warning.
{{%/* /alert */%}}
```
渲染为：
{{% alert title="Warning" color="warning" %}}
This is a warning.
{{% /alert %}}

---


### 选项卡式窗口

短代码:


```markdown
{{</* tabpane text=true right=false */>}}
  {{%/* tab header="**OS**:" disabled=true /*/%}}
  {{%/* tab header="windows" lang="en" */%}}
    可执行文件名*.exe
  {{%/* /tab */%}}
  {{%/* tab header="linux" lang="de" */%}}
    一切皆文件
  {{%/* /tab */%}}
{{</* /tabpane */>}}

```

渲染为：
{{< tabpane text=true right=false >}}
  {{% tab header="**OS**:" disabled=true /%}}
  {{% tab header="windows" lang="en" %}}
    可执行文件名*.exe
  {{% /tab %}}
  {{< tab header="linux" lang="de" >}}
    一切皆文件
  {{< /tab >}}
{{< /tabpane >}}

---


