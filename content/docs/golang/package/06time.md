---
title: "time"
linkTitle: "time"
date: 2025-05-09
toc_hide: false
hide_summary: true
weight: 6
description: >
  time|标准库

tags: ["golang","库","time"]
categories: ["golang","库"]
url: golang/package/time.html
---
#### time 时间操作

+ 获取当前时间、时间格式化、字符串解析

  ```go
  package main
  
  import (
  	"fmt"
  	"time"
  )
  
  func main() {
  	// 获取当前时间
  	now := time.Now()
  	fmt.Println(now) //2024-05-12 16:03:54.379957201 +0800 CST m=+0.000041572
  
  	// 获取指定时间 年 月 日 时 分 秒，纳秒， 时区
  	t1 := time.Date(2024, 5, 12, 16, 07, 19, 0, time.Local)
  	fmt.Println(t1) //2024-05-12 16:07:19 +0800 CST
  
  	// 时间的格式化 Format()
  	t2 := time.Now().Format("2006/01/02 15:04:05 PM")
  	fmt.Println(t2) //2024/05/12 16:21:02 PM
  
  	// 解析 Parse()
  	if t3, err := time.Parse("2006-01-02 15:04:05", "2024-05-12 16:03:54"); err != nil {
  		fmt.Println(err)
  	} else {
  		fmt.Println(t3) //2024-05-12 16:03:54 +0000 UTC
  	}
  
  	// sleep()
  	for i := 1; i < 10; i++ {
  		fmt.Println(i)
  		time.Sleep(10 * time.Second)
  	}
  
  }
  ```