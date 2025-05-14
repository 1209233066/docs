---
title: "flag"
linkTitle: "flag"
date: 2025-05-09
toc_hide: false
hide_summary: true
weight: 8
description: >
  flag|标准库

tags: ["golang","库","flag"]
categories: ["golang","库"]
url: golang/package/flag.html
---

```go
package main

/*
功能：
	通过flag,实现用户传参
	通过os/exec，实现调用操作系统命令
*/

import (
	"flag"
	"fmt"
	"os/exec"
)

var (
	ip   = flag.String("ip", "127.0.0.1", "--ip <ip地址>")
	port = flag.Int("port", 80, "--port <端口>")
	ssl  = flag.Bool("ssl", false, "--ssl <true|false>")
)

func GenerateUrl() string {
	var url string
	if *ssl {
		// Sprintf() 实现字符串格式化
		url = fmt.Sprintf("https://%s:%d", *ip, *port)
	} else {
		url = fmt.Sprintf("http://%s:%d", *ip, *port)
	}
	return url
}

func main() {
	// 解析flag定义参数
	flag.Parse()
	url := GenerateUrl()

	cmd := exec.Command("curl", url)
	output, _ := cmd.CombinedOutput()
	fmt.Print(string(output))
}
```