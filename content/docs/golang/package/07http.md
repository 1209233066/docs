---
title: "net/http"
linkTitle: "net/http"
date: 2025-05-09
toc_hide: false
hide_summary: true
weight: 7
description: >
  net/http|标准库

tags: ["golang","库","net/http"]
categories: ["golang","库"]
url: golang/package/http.html
---

### net/http

+ **发送GET请求**

  ```go
  package main
  
  import (
  	"fmt"
  	"io"
  	"net/http"
  )
  
  func main() {
  	// 发送Get 请求
  	response, err := http.Get("http://175.178.65.213:7292")
  	if err != nil {
  		fmt.Println(err)
  	}
  	// 关闭连接
  	defer response.Body.Close()
  	// 读取响应体内容
  	result, err := io.ReadAll(response.Body)
  	if err != nil {
  		fmt.Println(err)
  	}
  	fmt.Println(string(result))
  
  }
  ```

+ **创建http服务**

  ```go
  package main
  
  import (
  	"fmt"
  	"net/http"
  )
  
  func main() {
  
  	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
  		fmt.Printf("接收到%s一个请求\n", r.Method)
  		fmt.Fprintf(w, "你执行了一个%s方法", r.Method)
  
  	})
  	http.ListenAndServe(":8080", nil)
  }
  ```
