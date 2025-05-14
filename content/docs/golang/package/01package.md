---
title: "包管理"
linkTitle: "包管理"
date: 2025-05-09
toc_hide: false
hide_summary: true
weight: 1
description: >
 库|golang

tags: ["golang","库"]
categories: ["golang"]
url: golang/package/package.html
---


**包的声明:**

+ 同一目录下的文件必须属于同一个包
+ package 声明的包名应该和所在目录名称一致。允许不一致
+ 包可以嵌套
+ 同包下的函数不需要导入和直接使用
+ init() 函数和 main() 函数是golang 保留函数，不能有参数和返回值。init() 可以在任意包中，并且一个包下允许存在多个init()函数main() 函数只能被定义在main包中。

**包的导入格式：**

{{< tabpane text=true right=true >}}
  {{% tab header="**导包方法**:" disabled=true /%}}
  {{% tab header="标准导入" lang="en" %}}
  ```go
  package main
  
  import "fmt"
  
  func main() {
    fmt.Println("hello world")
  }
  ```
  {{% /tab %}}

  {{% tab header="自定义别名" lang="en" %}}
  ```go
  package main
  
  import f "fmt"
  
  func main() {
    f.Println("hello world")
  }
  ```
  {{% /tab %}}

  {{% tab header="省略导入格式" lang="en" %}}
  ```go
  package main
  
  import . "fmt"
  
  func main() {
    Println("hello world")
  }
  ```
  {{% /tab %}}


  {{% tab header="匿名导入" lang="en" %}}
  ```go
  初始化函数通常在这个包执行main()前执行初始化动作，一个包可以包含0或多个init()函数
  ```
  {{% /tab %}}
{{< /tabpane >}}


### 常见库

| 库名                                  | 类型                 | 功能                                                  |
| ------------------------------------- | -------------------- | ----------------------------------------------------- |
| `fmt`                                 | 格式化 I/O           | 提供格式化输入输出函数（如 `Printf`、`Scanf` 等）     |
| `os`                                  | 系统交互             | 操作系统功能接口（文件、进程、环境变量等）            |
| `filepath`                            | 文件路径处理         | 跨平台路径操作（路径拼接、分析、规范化等）            |
| `io`                                  | 基础 I/O             | 定义 `Reader`/`Writer` 接口及流式数据操作             |
| `bufio`                               | 缓冲 I/O             | 带缓冲的读写操作（纠正自 `iobufer`，原库名无效）      |
| `time`                                | 时间处理             | 时间获取、格式化、计算与时区转换                      |
| `strings`                             | 字符串处理           | 字符串分割、替换、查找等操作                          |
| `log`                                 | 日志管理             | 基础日志记录（支持输出到文件、终端等）                |
| `encoding/json`                       | 数据序列化           | JSON 编码与解码                                       |
| `gopkg.in/yaml.v3`                    | 数据序列化（第三方） | YAML 解析与生成（需手动导入第三方库）                 |
| `net/http`                            | 网络通信             | HTTP 客户端/服务端实现（构建 Web 应用）               |
| `flag`                                | 命令行工具           | 解析命令行参数与选项                                  |
| `context`                             | 并发控制             | 跨协程传递请求上下文（超时、取消信号等）              |
| `sync`                                | 并发控制             | 互斥锁、条件变量、并发安全工具（`Mutex`/`WaitGroup`） |
| `runtime`                             | 系统交互             | 访问 Go 运行时信息（GC、协程监控等）                  |
| `syscall`                             | 系统交互             | 直接调用操作系统底层接口                              |
| `path/filepath`                       | 文件路径处理         | 跨平台文件路径解析（已补全标准写法）                  |
| `net`                                 | 网络通信             | 底层网络协议（TCP/UDP）与 DNS 解析                    |
| `net/http/pprof`                      | 性能监控             | 集成性能分析工具（CPU/内存/协程分析）                 |
| `reflect`                             | 元编程               | 运行时类型反射与动态操作                              |
| `testing`                             | 测试框架             | 单元测试与基准测试                                    |
| `errors`                              | 错误处理             | 错误包装与自定义错误类型                              |
| `compress/gzip`                       | 压缩解压             | GZIP 格式压缩与解压                                   |
| `github.com/spf13/cobra`              | 命令行工具（第三方） | 强大的 CLI 应用框架（替代 `flag` 的高级选择）         |
| `github.com/spf13/viper`              | 配置管理（第三方）   | 多格式配置读取（JSON/YAML/ENV 等）                    |
| `github.com/sirupsen/logrus`          | 日志管理（第三方）   | 结构化日志记录（支持 Hook 和多种输出格式）            |
| `github.com/gin-gonic/gin`            | Web 框架（第三方）   | 高性能 HTTP Web 框架（路由、中间件等）                |
| `github.com/gorilla/websocket`        | 网络通信（第三方）   | WebSocket 协议实现（客户端/服务端）                   |
| `github.com/go-redis/redis`           | 数据存储（第三方）   | Redis 客户端库                                        |
| `github.com/stretchr/testify`         | 测试工具（第三方）   | 断言库与 Mock 工具（增强 `testing` 功能）             |
| `github.com/prometheus/client_golang` | 监控（第三方）       | Prometheus 指标暴露与收集（运维监控必备）             |
| `github.com/docker/docker`            | 容器交互（第三方）   | Docker 引擎 API 客户端（容器管理）                    |
| `gorm.io/gorm`                        | ORM 框架（第三方）   | 数据库 ORM 操作（支持 MySQL/PostgreSQL 等）           |

