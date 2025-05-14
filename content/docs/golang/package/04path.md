---
title: "path"
linkTitle: "path"
date: 2025-05-09
toc_hide: false
hide_summary: true
weight: 4
description: >
  path|标准库

tags: ["golang","库","path"]
categories: ["golang","库"]
url: golang/package/path.html
---

#### **filepath获取文件路径**

```go
package main

import (
	"fmt"
	"path/filepath"
)

func main() {
    // 判断是否为绝对路径
	if filepath.IsAbs("/") {
		fmt.Println("是绝对路径")
	} else {
		fmt.Println("是相对路径")
	}

	// 获取一个文件的绝对路径，如果当前文件是绝对路径则直接输出，否则拼接当前目录并输出
	dirname, err := filepath.Abs("hosts")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(dirname)

	// 获取上一级目录
	fmt.Println(filepath.Join("/etc/hosts", ".."))
}
```