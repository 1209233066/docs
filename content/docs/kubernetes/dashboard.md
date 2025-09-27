---
date: '2025-05-21T15:22:40+08:00'
draft: false
title: 'dashboard'
type: blog
toc_hide: false
hide_summary: true
weight: 99
description: >
  dashboard|k8s
tags: ["dashboard"]
categories: ["kubernetes"]
url: kubernetes/dashboard.html
author: "wangendao"
---

![](https://rpic.origz.com/api.php?category=photography)

### 开源软件对比

| 功能                                | kuboard（v3.3.0）            | KubeSphere(v3.1.1)           | rancher(v2.5.10)             | dashboard(v2.0.1)                                  |
| ----------------------------------- | ---------------------------- | ---------------------------- | ---------------------------- | -------------------------------------------------- |
| k8s集群部署                         | /                            | 支持                         | 支持                         | 不支持                                             |
| 多集群管理                          | 支持                         | 支持                         | 支持                         | 不支持                                             |
| 资源管理                            | 可以监视、管理和部署应用程序 | 可以监视、管理和部署应用程序 | 可以监视、管理和部署应用程序 | 仅支持deploy,dasemonset,statefustset等内置资源管理 |
| 集群证书有效期展示                  | 支持                         | /                            | /                            | /                                                  |
| 认证和权限                          | 支持RBAC和AD/LDAP集成        | 支持RBAC和AD/LDAP集成        | 支持RBAC和AD/LDAP集成        | 支持RBAC                                           |
| 开源协议                            | /                            | Apache2.0                    | Apache2.0                    | Apache2.0                                          |
| 主要维护者                          | /                            | 青云                         | SUSE                         | 属于kubernetes项目                                 |
| 编程语言                            | javascript                   | go                           | go                           | go                                                 |
| 活跃度                              | 18.2k                        | 12.7k                        | 21.1k                        | 12.6k                                              |
| 部署难度                            | 一般                         | 较复杂                       | 较复杂                       | 一般                                               |
| 应用市场 (关联helm仓库快速部署服务) | 支持                         | /                            | 支持                         | /                                                  |

### 介绍

Rancher Server 由认证代理（Authentication Proxy）、Rancher API Server、集群控制器（Cluster Controller）、etcd 节点和集群 Agent（Cluster Agent） 组成。除了集群 Agent 以外，其他组件都运行在 Rancher Server 中。

**主要功能：**

1. 创建k8s集群（rancher成为RKE）
2. 支持管理已有集群
3. 可以集成elk，prometheus、alertmanager功能



![](https://docs.rancher.cn/assets/images/rancher-architecture-rancher-api-server-2743dae746c64cd2ad66711908be4108.svg)

### 安装

##### 准备TLS版本离线镜像

> `docker run -d --restart=unless-stopped -p 80:80 -p 443:443 --privileged rancher/rancher:stable`
>
> ```bash
> rancher/rancher-agent:v2.10.3
> rancher/rancher:v2.10.3
> rancher/rancher-webhook:v0.6.4
> ```

| 版本                                                         | 容器镜像                                              |
| ------------------------------------------------------------ | ----------------------------------------------------- |
| [v2.10](https://github.com/rancher/rancher/releases/tag/v2.10.3) | `rancher/rancher:v2.10.3`    `rancher/rancher:stable` |
| v2.9                                                         | `rancher/rancher:v2.9.3`                              |
| v2.8                                                         | `rancher/rancher:v2.8.5`                              |

*离线镜像下载并推送到内网仓库*

| Release 文件             | 描述                                                         |
| ------------------------ | ------------------------------------------------------------ |
| `rancher-images.txt`     | 此文件包含安装 Rancher、创建集群和运行 Rancher 工具所需的镜像列表。 |
| `rancher-save-images.sh` | 这个脚本会从 DockerHub 中拉取在文件`rancher-images.txt`中描述的所有镜像，并将它们保存为文件`rancher-images.tar.gz`。 |
| `rancher-load-images.sh` | 这个脚本会载入文件`rancher-images.tar.gz`中的镜像，并将它们推送到你自己的私有镜像库。 |

```bash
# https://github.com/rancher/rancher/releases/download/v2.10.3/rancher-save-images.sh
chmod +x rancher-save-images.sh rancher-load-images.sh
./rancher-save-images.sh --image-list ./rancher-images.txt 
./rancher-load-images.sh --image-list ./rancher-images.txt --registry <REGISTRY.YOURDOMAIN.COM:PORT>
```





##### 准备离线YAML

1. 添加helm仓库

   ```bash
   helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
   helm repo update
   ```

   

2. 获取对应版本

   > `rancher.zero-dew.com` rancher的访问域名
   >
   > `registry.zero-dew.com` 私有仓库地址
   >
   > `privateCA=true` 指明使用自签CA 
   
   ```bash
   helm template rancher rancher-stable/rancher \
   --version 2.10.3 --output-dir ./ \
   --no-hooks \
   --namespace rancher \
   --set hostname=rancher.zero-dew.com \
   --set ingress.tls.source=secret \
   --set privateCA=true \
   --set rancherImage=registry.zero-dew.com/rancher \
   --set systemDefaultRegistry=registry.zero-dew.com \
   --set useBundledSystemChart=true \
   --kube-version 1.31.2 
   ```
   
   

   

3. 自签https证书

   

   *生成 CA 证书*

   ```bash
   openssl genrsa -out ca.key 2048
   openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt -subj "/C=CN/ST=GD/L=SZ/O=zero-dew.com/CN=zero-dew.com"
   ```

   

   *创建 SAN 配置文件*

   ```bash
   cat >san.cnf <<'EOF'
   [req]
   default_bits = 2048
   prompt = no
   default_md = sha256
   req_extensions = req_ext
   distinguished_name = dn
   
   [dn]
   C = CN
   ST = Gd
   L = SZ
   O = zero-dew.com
   CN = rancher.zero-dew.com
   
   [req_ext]
   subjectAltName = @alt_names
   
   [alt_names]
   DNS.1 = rancher.zero-dew.com
   EOF
   ```

   *生成服务端私钥和 CSR*

   ```bash
   openssl genrsa -out rancher.key 2048
   openssl req -new -key rancher.key -out rancher.csr -config san.cnf
   ```

   *用 CA 签发服务端证书（带 SAN）*

   ```bash
   openssl x509 -req -in rancher.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
   -out rancher.crt -days 3650 -sha256 -extensions req_ext -extfile san.cnf
   ```

   

4. 部署

   ```bash
   kubectl create ns rancher
   # ingress tls证书
   kubectl -n rancher create secret tls tls-rancher-ingress --cert=./rancher.crt --key=./rancher.key
   # 该ca会被传递到agent端用于访问https://rancher.zero-dew.com
   kubectl -n rancher create secret generic  tls-ca --from-file=cacerts.pem=./ca.crt
   kubectl -n rancher apply -f rancher/templates
   ```

   

   



### 使用

登录和修改密码

![](/docs/kubernetes/rancher01.png)

选择导入已有集群

![](/docs/kubernetes/rancher05.png)



![](/docs/kubernetes/rancher07.png)



### 卸载

```bash
kubectl -n rancher delete -f rancher/templates
```