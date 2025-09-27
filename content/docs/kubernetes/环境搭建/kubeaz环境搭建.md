---
date: '2025-05-21T15:22:40+08:00'
draft: false
title: 'kubeaz环境搭建'
linkTitle: 'kubeaz环境搭建'
type: blog
toc_hide: false
hide_summary: true
weight: 2
description: >
  构建一套高可用、可扩展的kubernetes生态环境
tags: ["kubeadm","kubeaz"]
categories: ["kubernetes"]
url: kubernetes/kubernetes_setup/kubeaz.html
author: "wangendao"
---



```bash
git clone  https://github.com/easzlab/kubeasz.git
```



环境

| 主机     | ip            | 资源        | kernel       |
| -------- | ------------- | ----------- | ------------ |
| master01 | 192.168.0.243 | 2c 4g 100GB | centos7 3.10 |
| master02 | 192.168.0.244 | 2c 4g 100GB | centos7 3.10 |
| master03 | 192.168.0.245 | 2c 4g 100GB | centos7 3.10 |



1. 时间同步

   `chrony` 是一个优秀的 `NTP` 实现，性能比ntp好，且配置管理方便；它既可作时间服务器服务端，也可作客户端。

   **安装chronyd服务**:	` yum install chrony`

   **配置时间服务器地址**:

   ```
   # server <时间服务器>  <客户端向服务端发起时间同步的最小间隔，示例中4 表示 2^4=64s> <客户端向服务端发起时间同步的最大间隔，示例中10表示 2^10=1024s> 
   server ntp.aliyun.com minpoll 4 maxpoll 10 iburst
   server ntp1.aliyun.com minpoll 4 maxpoll 10 iburst
   server ntp2.aliyun.com minpoll 4 maxpoll 10 iburst
   server ntp3.aliyun.com minpoll 4 maxpoll 10 iburst
   server ntp4.aliyun.com minpoll 4 maxpoll 10 iburst
   server ntp5.aliyun.com minpoll 4 maxpoll 10 iburst
   server ntp6.aliyun.com minpoll 4 maxpoll 10 iburst
   server 192.168.0.251 minpoll 4 maxpoll 10 iburst
   ```

   **作为服务端时，允许连接的客户端**: 

   ```
   allow 192.168.0.0/16
   ```

   **启动守护进程：** 

   > 客户端监听本机的323/udp 端口，服务端监听 123/udp

   ```bash
   systemctl enable chronyd --now
   systemctl status chronyd 
   ```

   **chronyc 作为客户端命令 查看配置的时间服务器**

   ![](https://img2024.cnblogs.com/blog/2108528/202502/2108528-20250213144507664-645070835.png)

   **追踪查看时间同步的详细信息**

   ![](https://img2024.cnblogs.com/blog/2108528/202502/2108528-20250213144524152-429284700.png)

   **作为服务端，查看当前连接过来的客户端**

   ![](https://img2024.cnblogs.com/blog/2108528/202502/2108528-20250213144538920-686752789.png)

2. 关闭firewalld

3. 关闭 selinux

4. [使用kubeasz](https://github.com/easzlab/kubeasz/blob/3.1.1/docs/setup/00-planning_and_overall_intro.md)

```bash
deploy ~]# yum install ansible -y
deploy ~]# ansible --version
ansible 2.9.27
# 秘钥认证
ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa
#
for host in 192.168.0.251 192.168.0.252 192.168.0.253;do
	sshpass -p pytc@2024 ssh-copy-id $host
done
```

```bash
git clone  https://github.com/easzlab/kubeasz.git
cd kubeasz/
git checkout 3.6.5

/etc/kubeasz/ezctl new cluster01 
```



```bash
# 是bash 脚本
wget https://github.com/easzlab/kubeasz/releases/download/3.1.1/ezdown

# 下载 kubeasz代码、二进制、离线镜像 到/etc/kubeasz
bash ezdown -D

# 在/etc/kubeasz/clusters/k8s-01/ 下生成集群配置文件和ansible主机模板 k8s-01 是集群名称
cd /etc/kubeasz
deploy kubeasz]# ./ezctl new k8s-01
```

```bash
# 集群名称 k8s-01 
# 可以但组件安装./ezctl setup k8s-01 01
# 也可以 ./ezctl setup k8s-01 all  全部安装
deploy kubeasz]# ./ezctl setup k8s-01 all 
```



kubelete 无法启动，通过docker info 查看得知 kubelet 启动配置 和docker  的cgroup-driver 不一致。修改kubelete 的启动文件后正常

````bash
  --cgroup-driver=cgroupfs
````



```bash
[root@ceph-deploy kubeasz]# kubectl version
Client Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.0", GitCommit:"cb303e613a121a29364f75cc67d3d580833a7479", GitTreeState:"clean", BuildDate:"2021-04-08T16:31:21Z", GoVersion:"go1.16.1", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.0", GitCommit:"cb303e613a121a29364f75cc67d3d580833a7479", GitTreeState:"clean", BuildDate:"2021-04-08T16:25:06Z", GoVersion:"go1.16.1", Compiler:"gc", Platform:"linux/amd64"}
```



后面的增删该都是通过 `./ezctl `



集群升级

1. 创建两套完整的集群。
2. 一台一台先升级master，master 升级完。在升级node 