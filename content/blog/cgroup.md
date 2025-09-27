---
date: '2025-05-25T15:04:12+08:00'
draft: false
title: 'Cgroup'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  k8s cgroup
tags: ["kubernetes"]
categories: ["kubernetes"]
url: 2025-05-25/cgroup.html
author: "wangendao"
---





任务：
- [x] 通过cgroupfs 限制cpu/memory/diskio
- [x] 通过systemd 限制cpu/memory/diskio
- [x] 通过cgroupfs 限制kubernetes 容器的cpu/memory/diskio



---

cgroups 由 Google 工程师于 2006 年提出，并在 2007 年被合并到 Linux 2.6.24 内核。虽然目前有两个版本的 cgroups，但大多数发行版和机制都使用v1版本。





在linux中一切皆文件的宗旨下，cgroup通过文件结构来实现对进程的控制和限制，目录结构：

{{< tabpane text=true right=false >}}
  {{% tab header="**目录结构**:" disabled=true /%}}
  {{% tab header="" lang="en" %}}
![](https://www.redhat.com/rhdc/managed-files/styles/wysiwyg_full_width/private/sysadmin/2020-09/CGroup_Diagram.png.webp?itok=eaJUZX0z)
  {{% /tab %}}
  {{% tab header="" lang="en" %}}

```bash
/sys/fs/cgroup/
├── blkio					# 限制进程对硬盘的读写速率
├── cpu -> cpu,cpuacct
├── cpuacct -> cpu,cpuacct
├── cpu,cpuacct			    # 限制和监控进程的CPU消耗
├── cpuset					# 绑定进程到特定CPU核心或内存节点（NUMA 架构）
├── devices					# 控制进程对设备文件（如 /dev/sda）的访问权限（读/写/创建设备）
├── freezer					# 暂停/恢复 进程组中的所有进程
├── hugetlb					# 限制大页内存的使用量。
├── memory					# 控制内存用量 和 Swap 交换空间
├── net_cls -> net_cls,net_prio
├── net_cls,net_prio
├── net_prio -> net_cls,net_prio
├── perf_event				# 允许性能监控工具（如 perf）追踪 CGroup 内进程的性能事件
├── pids					# 限制 CGroup 内允许的 最大进程数量
└── systemd
```

  {{% /tab %}}
{{< /tabpane >}}



### 管理cgroup

cgroup作为linux内核的一部分，在用户层面centos提供了三种管理cgroup的工具，分别为：*libcgroup* *cgroupfs*  *systemd* 
{{% alert title="" color="" %}}

+ *libcgroup（已经弃用）* 是一个用户空间的 cgroup 管理库和工具集，提供了命令行工具（如 cgcreate、cgexec、cgclassify 等）和 C 语言 API。
+ *cgroupfs* 不是一个单独的工具，而是指 Linux 内核通过挂载 cgroup 文件系统，暴露出来的接口。通过操作 /sys/fs/cgroup 目录，用户和程序通过直接操作 cgroup（如创建目录、写入参数文件）来管理资源。
+   *systemd* 是现代 Linux 的初始化系统和服务管理器，它内置了对 cgroup 的原生支持

{{% /alert %}}

**任务一：通过cgroupfs 限制cpu/memory/diskio**

{{< tabpane text=true right=false >}}
  {{% tab header="**cgroupfs管理cgroup**:" disabled=true /%}}
  {{% tab header="管理cpu" lang="bash" %}}

1. 创建新的cpu 子系统

   ```bash
   mkdir /sys/fs/cgroup/cpu,cpuacct/m
   ```

2. 找到所有进程及子进程

   ```bash
   [root@seagullcore01-uat-s2 ~]# ps -ef|grep /usr/bin/m
   root      65787  61380 99 16:46 pts/1    00:02:07 /usr/bin/m
   root      65850  63340  0 16:47 pts/2    00:00:00 grep --color=auto /usr/bin/m
   [root@seagullcore01-uat-s2 ~]# pstree -p 65787
   m(65787)─┬─{m}(65788)
            ├─{m}(65789)
            ├─{m}(65790)
            └─{m}(65791)
   ```

3. 配额cpu限额

   ```bash
   for pid in 65787 65788 65789 65790 65791; do echo $pid >/sys/fs/cgroup/cpu,cpuacct/m/tasks;done
   echo 200000 >/sys/fs/cgroup/cpu,cpuacct/m/cpu.cfs_quota_us # 在一个周期内允许使用的 CPU 时间（μs）,默认-1不限制
   echo 100000 >/sys/fs/cgroup/cpu,cpuacct/m/cpu.cfs_period_us # 调度周期，单位为微秒（μs），通常设为 100000（即 100ms）
   ```

4. 验证是否生效，使用 `top` 或查看 `cpu.stat ` 

   ```bash
   [root@seagullcore01-uat-s2 ~]# cat  /sys/fs/cgroup/cpu,cpuacct/m/cpu.stat 
   nr_periods 3083 			# 自创建以来经历了多少个调度周期
   nr_throttled 2716   		# 因为达到cgroup限制而中断的次数（中断后等待下一次调度）
   throttled_time 521614106629 # 因达到cgroup限制中断停止的时长（纳秒）
   ```

5. 清理子cgroup

   ```bash
   [root@seagullcore01-uat-s2 ~]# rmdir /sys/fs/cgroup/cpu,cpuacct/m
   rmdir: failed to remove ‘/sys/fs/cgroup/cpu,cpuacct/m’: Device or resource busy
   [root@seagullcore01-uat-s2 ~]# cat /sys/fs/cgroup/cpu,cpuacct/m/cgroup.procs 
   65787
   [root@seagullcore01-uat-s2 ~]# echo 65787 >/sys/fs/cgroup/cpu,cpuacct/cgroup.procs 
   [root@seagullcore01-uat-s2 ~]# cat /sys/fs/cgroup/cpu,cpuacct/m/cgroup.procs 
   [root@seagullcore01-uat-s2 ~]# rmdir /sys/fs/cgroup/cpu,cpuacct/m
   ```


  {{% /tab %}}
  {{% tab header="管理内存" lang="en" %}}
1. 创建新的内存子系统
   ```bash
   mkdir /sys/fs/cgroup/memory/m
   ```
2. 找到所有进程及子进程

   ```bash
   [root@seagullcore01-uat-s2 ~]# ps -ef|grep /usr/bin/m
   root      65787  61380 99 16:46 pts/1    00:02:07 /usr/bin/m
   root      65850  63340  0 16:47 pts/2    00:00:00 grep --color=auto /usr/bin/m
   [root@seagullcore01-uat-s2 ~]# pstree -p 65787
   m(65787)─┬─{m}(65788)
            ├─{m}(65789)
            ├─{m}(65790)
            └─{m}(65791)
   ```
3. 配额内存限额

   ```bash
   for pid in 65787 65788 65789 65790 65791; do echo $pid >/sys/fs/cgroup/memory/m/cgroup.procs;done
   echo 1g >/sys/fs/cgroup/memory/m/memory.limit_in_bytes
   ```

  {{% /tab %}}
  {{% tab header="管理磁盘io" lang="en" %}}

  {{% /tab %}}
{{< /tabpane >}}



{{< tabpane text=true right=false >}}
  {{% tab header="**systemd管理cgroup**:" disabled=true /%}}
  {{% tab header="方式一" lang="en" %}}

```bash
# 动态设置进程不超过2个cpu
~]# systemctl set-property m.service CPUQuota=200%
```

```bash
# 使用命令行设置进程不超过2G
~]# systemctl set-property m.service  MemoryLimit=2G
```

 

  {{% /tab %}}
  {{% tab header="方式二" lang="en" %}}

```bash
tee >/usr/lib/systemd/system/m.service <<'EOF'
[Unit]
Description=A demo for load cpu

[Service]
ExecStart=/usr/bin/m
# 限制2核心cpu
CPUQuota=200%

EOF
```

```bash
tee >/usr/lib/systemd/system/m.service <<'EOF'
[Unit]
Description=A demo for load memory

[Service]
ExecStart=/usr/bin/m
# 限制2G 内存
MemoryLimit=2G

EOF
```

  {{% /tab %}}
{{< /tabpane >}}

**任务二：通过cgroupfs 调整kubernetes容器的限制**


```bash
cat <<EOF | kubectl apply -f - 
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: cgrouptest
  name: cgrouptest
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cgrouptest
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: cgrouptest
    spec:
      containers:
      - image: harbor.pytc.com/library/m:latest
        name: m
        resources:
          limits:
            cpu: 1000m
            memory: 128Mi
      - image: harbor.pytc.com/library/m:latest
        name: m2
        resources:
          limits:
            cpu: 2000m
            memory: 128Mi
EOF
```

获取pod uid

```bash
[root@master-01 ~]# kubectl get pod -l app=cgrouptest -ojsonpath='{.items[0].metadata.uid}{"\n"}'|tr "-" "_"
5dba196d_897b_4ebb_865e_0e43b612575d
```

获取pod中容器的containerID

```bash
[root@master-01 ~]# kubectl get pod -l app=cgrouptest -ojsonpath='{range .items[0].status.containerStatuses[*] } {.name}{"\t"}{.containerID}{"\n"}{end}'
 m      containerd://05d994653b88f6fe97254c206efba6dc34f6e03a0ede108be081d71a0e1c6857
 m2     containerd://3f06542e87e0fb80b38c86181b8fdd48580c258969770c56466cd68498deb2a5
```

查看容器的限制

```bash
[root@master-01 kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice]# cat /sys/fs/cgroup/cpu/kubepods.slice/kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice/cri-containerd-05d994653b88f6fe97254c206efba6dc34f6e03a0ede108be081d71a0e1c6857.scope/cpu.cfs_quota_us 
100000
```

```bash
[root@master-01 kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice]#  cat /sys/fs/cgroup/cpu/kubepods.slice/kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice/cri-containerd-3f06542e87e0fb80b38c86181b8fdd48580c258969770c56466cd68498deb2a5.scope/cpu.cfs_quota_us
200000
```

修改容器的限制，并观察变化

{{% alert title="" color="warning" %}}

**报错：**

```bash
[root@master-01 kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice]# echo 400000 >/sys/fs/cgroup/cpu/kubepods.slice/kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice/cri-containerd-05d994653b88f6fe97254c206efba6dc34f6e03a0ede108be081d71a0e1c6857.scope/cpu.cfs_quota_us 
-bash: echo: write error: Invalid argument
```
**排查和解决:**

设置问题：由于容器上一层pod 中 `cpu.cfs_quota_us `的值为300000（即两个容器的资源限制总和不会超过3个核心），在cgroup中子系统受父级限制。因此最大设置不能超过 300000。

资源限制问题： 同时对于该示例中一个pod包含两个容器，即使两个容器`cpu.cfs_quota_us `的值都设置为300000。操作系统也不会分配6个cpu。原因是cgroup中子系统受父级限制。因此两个容器合计最大可以使用3个核心。

突破限制： 首先修改父级`cpu.cfs_quota_us` 限制，其次修改容器限制



```bash
[root@master-01 kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice]# cat  /sys/fs/cgroup/cpu/kubepods.slice/kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice/cpu.cfs_quota_us 
300000
```

```bash
[root@master-01 kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice]# echo 300000 >/sys/fs/cgroup/cpu/kubepods.slice/kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice/cri-containerd-05d994653b88f6fe97254c206efba6dc34f6e03a0ede108be081d71a0e1c6857.scope/cpu.cfs_quota_us 
```



```bash
[root@master-01 kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice]# echo  500000 >/sys/fs/cgroup/cpu/kubepods.slice/kubepods-pod5dba196d_897b_4ebb_865e_0e43b612575d.slice/cpu.cfs_quota_us 
```



{{% /alert %}}







### 故障处理

{{% alert title="" color="warning" %}}
使用 `umount -a` 后 cgroup文件系统被卸载，以下为重新挂载 cgroup 文件系统的步骤。
{{% /alert %}}



**重建基础结构**

```bash
mount -t tmpfs tmpfs /sys/fs/cgroup
```
{{< tabpane text=true right=false >}}
  {{% tab header="**挂载 cgroup v2**" lang="bash" %}}

```bash
mkdir /sys/fs/cgroup/unified
mount -t cgroup2 none /sys/fs/cgroup/unified
```


  {{% /tab %}}
  {{% tab header="**挂载 cgroup v1**" lang="bash" %}}

```bash
controllers=(blkio  cpu,cpuacct  cpuset  devices  freezer  hugetlb  memory   net_cls,net_prio  perf_event  pids systemd )
for ctrl in "${controllers[@]}"; do
   mkdir -p /sys/fs/cgroup/$ctrl
   mount -t cgroup -o $ctrl cgroup /sys/fs/cgroup/$ctrl
done
# 特别处理 systemd 控制器
umount /sys/fs/cgroup/systemd
mount -t cgroup -o none,name=systemd systemd /sys/fs/cgroup/systemd
# 创建符号链接
cd  /sys/fs/cgroup/
ln -sv  cpu,cpuacct cpuacct
ln -sv  cpu,cpuacct cpu
ln -sv  net_cls,net_prio net_cls 
ln -sv  net_cls,net_prio net_prio
```
  {{% /tab %}}
{{< /tabpane >}}

### 示例代码

cpu 压测代码{{% details %}}
  ```go
  package main
  
  import (
  	"runtime"
  	"sync/atomic"
  )
  
  // 定义全局变量阻止编译器优化
  var counter uint64
  
  func main() {
  	// 获取逻辑 CPU 核心数 (如 4 核 8 线程则返回 8)
  	// numCPU := runtime.NumCPU()
  	numCPU := 4
  	// 设置 Go 运行时使用的最大 CPU 核数
  	runtime.GOMAXPROCS(numCPU)
  
  	// 为每个逻辑 CPU 核心启动一个满载 goroutine
  	for i := 0; i < numCPU; i++ {
  		go worker()
  	}
  
  	// 阻塞主线程防止退出
  	select {}
  }
  
  // CPU 密集型任务函数
  func worker() {
  	// 原子操作循环 (避免循环被 Go 编译器优化)
  	for {
  		atomic.AddUint64(&counter, 1)
  	}
  }
  ```
{{% /details %}}

内存压测代码{{% details %}}
  ```go
  package main
  
  import (
  	"fmt"
  	"runtime"
  	"time"
  )
  
  const targetMem = 2 * 1024 * 1024 * 1024 // 2GB
  
  func main() {
  	// 创建内存池避免被GC回收
  	var memoryHolder [][]byte
  
  	// 分块分配更贴近真实场景
  	blockSize := 100 * 1024 * 1024 // 每次分配100MB
  	for allocated := 0; allocated < targetMem; allocated += blockSize {
  		block := make([]byte, blockSize)
  		memoryHolder = append(memoryHolder, block)
  
  		// 读取内存数据防止优化
  		for i := 0; i < len(block); i += 4096 {
  			block[i] = byte(i % 256)
  		}
  
  		// 打印当前分配状态
  		printMemUsage()
  	}
  
  	fmt.Println("\n📊 内存分配完成，持续占用中...")
  	fmt.Println("✅ 可使用以下命令监控：")
  	fmt.Println("   top -p $(pgrep your_program_name)")
  	fmt.Println("   watch -n 1 'ps -eo pid,rss,comm | grep your_program_name'")
  
  	// 保持程序运行直到kill
  	ticker := time.NewTicker(30 * time.Second)
  	defer ticker.Stop()
  
  	for range ticker.C {
  		printMemUsage()
  	}
  }
  
  func printMemUsage() {
  	var m runtime.MemStats
  	runtime.ReadMemStats(&m)
  	fmt.Printf("➤ 系统视角内存: %.2fGB | Alloc=%.2fMB | Sys=%.2fMB\n",
  		float64(m.HeapSys)/1024/1024/1024,
  		float64(m.HeapAlloc)/1024/1024,
  		float64(m.Sys)/1024/1024)
  }
  
  ```
{{% /details %}}






https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/7/html/resource_management_guide/chap-introduction_to_control_groups
https://segmentfault.com/a/1190000009732550

https://www.redhat.com/sysadmin/cgroups-part-one

https://www.redhat.com/sysadmin/cgroups-part-two

https://www.redhat.com/sysadmin/cgroups-part-three

https://www.redhat.com/sysadmin/cgroups-part-four

https://www.redhat.com/en/services/training/do080-deploying-containerized-applications-technical-overview?intcmp=701f20000012ngPAAQ

https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/resource_management_guide/index

https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/resource_management_guide/chap-introduction_to_control_groups

https://isovalent.com/blog/post/demystifying-cni/

https://zhuanlan.zhihu.com/p/346050404

https://systemd-by-example.com/

https://www.ibm.com/support/pages/node/6393890?mhsrc=ibmsearch_a&mhq=cgroup

https://www.redhat.com/en/services/training/do080-deploying-containerized-applications-technical-overview?intcmp=701f20000012ngPAAQ&section=overview

https://www.redhat.com/sysadmin/cgroups-part-three

https://zhuanlan.zhihu.com/p/346050404

https://blog.csdn.net/qq_37041791/article/details/126031351