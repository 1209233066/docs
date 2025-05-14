---
title: "fmt"
linkTitle: "fmt"
date: 2025-05-09
toc_hide: false
hide_summary: true
weight: 2
description: >
  fmt|标准库

tags: ["golang","库","fmt"]
categories: ["golang","库"]
url: golang/package/fmt.html
---

+ **printf 格式化输出**

  ```go
  package main
  
  import "fmt"
  
  func main() {
  	// %s %q字符串占位符
  	fmt.Printf("%s\n", "中文") //中文
  	fmt.Printf("%q\n", "中文") //"中文"
  
  	// %d 十进制占位符
  	// %b 二进制占位符
  	// %q 按照assic 码输出字面值
  	fmt.Printf("%d\n", 91) // 91
  	fmt.Printf("%b\n", 91) // 1011011
  	fmt.Printf("%q\n", 91) // '['
  
  	// %f 浮点数占位符
  	fmt.Printf("%.2f\n", 3.141592657) // 3.14
  
  	// %t 布尔型占位符
  	fmt.Printf("%t\n", true) //true
  
  	// %p 指针类型占位符 0x表示16进制
  	Name := "张三"
  	fmt.Printf("%p\n", &Name) //0xc000014270
  
  	// %v 按照值的默认格式输出
  	fmt.Printf("%v %v %v\n", 123, true, "张三") //123 true 张三
  
  	// %+v 按照值的默认格式输出,结构体会添加字段名
  	type Persion struct {
  		Name string
  		Age  int
  	}
  	var p Persion
  	p.Name = "张三"
  	p.Age = 33
  	fmt.Printf("%v\n%+v\n", p, p)
  
  	// %T 数据类型
  	fmt.Printf("%T\n", true) //bool
  
  	// %% 表示一个%
  	fmt.Printf("%.2f%%\n", 3.141592657) //3.14%
  }
  ```

+ **向文件中写入内容**

  `Fprint`,`Fprintf` `Fprintln`

  ```go
  package main
  
  import (
  	"fmt"
  	"os"
  )
  
  func main() {
      // os.OpenFile: 这是Go标准库中os包提供的一个函数，用于打开一个文件，并返回一个文件句柄。
      
      /* os.O_CREATE|os.O_WRONLY|os.O_APPEND：这是文件打开的模式，由几个常量进行位或（|）操作得到:
          os.O_CREATE：如果文件不存在，创建一个新文件。
          os.O_WRONLY：以只写方式打开文件。
          os.O_APPEND：写入文件时，每次写操作都从文件末尾开始，即追加模式。
      */
      
  	f, err := os.OpenFile("./1.txt", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
  	if err != nil {
  		fmt.Println(err)
  	}
  	defer f.Close()
  
  	fmt.Fprintf(f, "%.2f\n", 3.141592657)
  }
  ```

+ **获取输出的字符串**

  ```go
  package main
  
  import "fmt"
  
  func main() {
  	// Sprint Sprintf Sprintln 把输出值赋值给变量
  	name := fmt.Sprint("张三")
  	if name == "张三" {
  		fmt.Println(name)
  	}
  
  }
  ```

+ **键盘输入**

  ```go
  package main
  
  import "fmt"
  
  func main() {
  	// Scan Scanln Scanf
  	var userName, passWord string
  	num, err := fmt.Scan(&userName, &passWord)
  	if err != nil {
  		fmt.Println(num, err)
  	}
  	//  获取变量 userName 和 passWord 的值
  	fmt.Printf("用户名:%s\n密码:%s\n", userName, passWord)
  
  }
  ```

  
  
  ```go
  package main
  
  import "fmt"
  
  func main() {
  	// Scan Scanln Scanf
  	var userName, passWord string
  	num, err := fmt.Scanln(&userName, &passWord)
  	if err != nil {
  		fmt.Println(num, err)
  	}
  	//  获取变量 userName 和 passWord 的值
  	fmt.Printf("用户名:%s\n密码:%s\n", userName, passWord)
  	// root 123
  	// 用户名:root
  	// 密码:123
  }
  ```



+ **自定义错误输出**

  ```go
  package main
  
  import "fmt"
  
  func main() {
  	file := "/etc/hosts"
  	err := fmt.Errorf("%s文件内容为空", file)
  	fmt.Println(err) // /etc/hosts文件内容为空
  }
  ```
  