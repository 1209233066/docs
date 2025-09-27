---
date: '2025-05-21T15:22:40+08:00'
draft: false
title: 'kubeadm环境搭建'
linkTitle: 'kubeadm环境搭建'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  构建一套高可用、可扩展的kubernetes生态环境
tags: ["kubeadm","kubeaz"]
categories: ["kubernetes"]
url: kubernetes/kubernetes_setup/quitstart.html
author: "wangendao"
---

读取该文档你将了解到：

- [x] 从0到1搭建kubernetes环境
- [x] 基于kubernetes的可观测平台构建
- [x] CI/CD  环境的构建

​	

本示例完全实现下图示例架构,并试图对 `cni/可观测性/cicd` 能力进行扩展。力图构建一套生产环境可用的模型

{{< tabpane text=true right=false >}}
  {{% tab header="架构" lang="en" %}}

<img src="https://kubernetes.io/zh-cn/docs/images/kubeadm-ha-topology-stacked-etcd.svg">
  {{% /tab %}}
  {{% tab header="服务器列表" lang="en" %}}

| hostname    | os        | ipaddress     | roles                                |
| ----------- | --------- | ------------- | ------------------------------------ |
| master01    | centos7.9 | 192.168.0.108 | master、node、keepalived、nginx、nfs |
| master02    | centos7.9 | 192.168.0.140 | master、node、keepalived、nginx      |
| master03    | centos7.9 | 192.168.0.162 | master、node、keepalived、nginx      |
| node01      | centos7.9 |               | node                                 |
| node02      | centos7.9 |               | node                                 |
| virtualhost |           | 192.168.0.144 | vip                                  |

  {{% /tab %}}
{{< /tabpane >}}



*通过自建dns 或 `/etc/hosts` 文件实现对所有主机间的主机名解析. 独立挂载`/var/lib/docker` 、`/var/lib/kubelet` 、`etcd`数据目录*

{{< tabpane text=true right=false >}}
  {{% tab header="**系统优化**:" disabled=true /%}}
  {{% tab header=系统初始化 lang="bash" %}}

```bash
#!/bin/bash

# author: 1209233066@qq.com
# description:
#	init linux env for kuernetes v24-
#   function:
#           1. sethostname 
#           2. turn off swap
#           3. turn off selinux
#           4. turn off firewalld
#           5. turn on kernel for netfilter/ip_nonlocal_bind
#           6. turn on ipvs modle
#           7. modify cgroup driver for docker
#           8. allow bind nonlocal ip
#           
LC_ALL=C
SetEnv(){
	# 设置主机名和时区
	hostnamectl set-hostname "$1"
	timedatectl set-timezone Asia/Shanghai
	# 关闭swap分区 
    swapoff -a 
    sed -i '/swap/s|^|#|g' /etc/fstab
    # 关闭selinux 
    setenforce 0
    sed -i 's|SELINUX=enforcing|SELINUX=disabled|g' /etc/selinux/config
    # 关闭firewalld
    systemctl disable --now firewalld

    # 加载 br_netfilter 模块
    echo br_netfilter >/etc/modules-load.d/br_netfilter.conf
    # 加载ipvs 模块
    ls /usr/lib/modules/$(uname -r)/kernel/net/netfilter/ipvs |awk -F "." '{print $1}' >/etc/modules-load.d/ipvs.conf
    # 加载/etc/modules-load.d 下配置文件
    systemctl restart systemd-modules-load
    
    # 开启 bridge-nf-call-iptables内核功能
    # 开启 bridge-nf-call-ip6tables 内核功能
    # 开启数据包内核转发功能
    sysctl -w net.bridge.bridge-nf-call-iptables=1
    sysctl -w net.bridge.bridge-nf-call-ip6tables=1
    sysctl -w net.ipv4.ip_forward=1
    sysctl -w net.ipv4.ip_nonlocal_bind=1
	echo -e "net.bridge.bridge-nf-call-iptables = 1\nnet.bridge.bridge-nf-call-ip6tables = 1\nnet.ipv4.ip_forward = 1\nnet.ipv4.ip_nonlocal_bind = 1" >/etc/sysctl.d/kubernetes.conf
	# 
	yum install ipvsadm -y
	#
	curl https://get.docker.com|bash -s -- --mirror Aliyun --version 20.10.24 &&\
	mkdir /etc/docker &&\
	echo -e '{\n\t"exec-opts": ["native.cgroupdriver=systemd"]\n}' >/etc/docker/daemon.json
	systemctl daemon-reload
	systemctl enable docker --now
	systemctl status docker
}

SetEnv
```

  {{% /tab %}}
  {{% tab header="LB" lang="en" %}}

> L4负载均衡，在所有master节点执行

```bash
user  nginx;
worker_processes  1;

events {
    worker_connections  1024;
}
stream {
        log_format main '$remote_addr [$time_local] '
             '$protocol $status $bytes_sent $bytes_received '
             '$session_time "$upstream_addr" '
             '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';
        upstream kube_apiserver {
                server 192.168.0.108:6443 weight=1 max_fails=3 fail_timeout=30s;
                server 192.168.0.140:6443 weight=1 max_fails=3 fail_timeout=30s;
                server 192.168.0.162:6443 weight=1 max_fails=3 fail_timeout=30s;
        }
        server {
                listen 192.168.0.144:16443;
                proxy_connect_timeout 2s;
                proxy_timeout 900s;
                proxy_pass kube_apiserver;
                access_log  logs/kubeapiserver.log main;
          }
}
```

  {{% /tab %}}
  {{% tab header="keepalived" lang="en" %}}



三个节点使用相同的` BACKUP` 和 `priority 100` 初始化时拥有对等角色,vrrp初次选举时如果`priority ` 相同则会选择ip较大的节点拥有vip，因此不用担心相同`priority` 脑裂问题。
而`state BACKUP` 是为了让非抢占参数`nopreempt` 能够生效
| 参数              | 赋值 | 作用说明                                                     |
| :---------------- | :--- | :----------------------------------------------------------- |
| router_id         | 不同 | 标识本主机，便于日志区分                                     |
| virtual_router_id | 相同 | VRRP组标识，主备必须一致                                     |
| state BACKUP      | 相同 | 所有节点设置为BACKUP，目的是为了让非抢占参数`nopreempt` 能够生效 |



```bash
cat >/etc/keepalived/keepalived.conf<<'EOF'
! Configuration File for keepalived
####################### main config ########################
global_defs {
   notification_email {
      810654947@qq.com
      1209233066@qq.com
   }
   notification_email_from 810654947@qq.com
   smtp_server smtp.qq.com 587
   smtp_connect_timeout 30
   # 标识本主机，便于日志区分。每个主机不同
   router_id 1921680108
 
   vrrp_garp_master_delay 2
   script_user root
}

vrrp_script check_port {
   script "/etc/keepalived/check_port.sh 16443"
   interval 2
   weight -30
}

################### Vrrp instance config ###################
vrrp_instance VI_1 { 
   # MASTER|BACKUP
   state BACKUP
   priority 100
   interface ens192
   virtual_router_id 51
   advert_int 1
   # 当初始化节点是MASTER时不生效
   nopreempt
   authentication {
      auth_type PASS
      auth_pass 1111
   }
   virtual_ipaddress {
      192.168.0.144/24
   }
    
   track_script {
      check_port
   }
}
EOF
```



健康检查脚本

```bash
cat >/etc/keepalived/check_port.sh<<'EOF'
#!/bin/bash

count=$(ss -lntp|grep -c  "$1")
[ $count -ge 1 ] && exit 0 || pkill keepalived; exit 1
EOF
chmod +x /etc/keepalived/check_port.sh
```

keepalived 启动脚本

```bash
tee /usr/lib/systemd/system/keepalived.service <<EOF
[Unit]
Description = keepalived daemon 
After = network.target

[Service]
Type=forking
ExecStart=/usr/local/sbin/keepalived --log-console -f /etc/keepalived/keepalived.conf
Restart=always
RestartSec=5

User=root

[Install]
WantedBy=multi-user.target
EOF

```

```bash
systemctl daemon-reload
systemctl enable --now keepalived
```

  {{% /tab %}}
{{< /tabpane >}}



### kubeadm 安装



```bash
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```

```bash
yum install -y kubelet-1.23.17-0.x86_64 kubeadm-1.23.17-0.x86_64  kubectl-1.23.17-0.x86_64 
```

#### **初始化集群**

```bash
kubeadm init --control-plane-endpoint "192.168.0.144:16443" \
--image-repository k8s-gcr.m.daocloud.io \
--kubernetes-version 1.23.17 \
--upload-certs \
--pod-network-cidr "10.244.0.0/16" \
--service-cidr "172.168.0.0/16" \
-v5
```

```bash
systemctl enable kubelet --now
```



```bash
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
```

**命令自动补全**

```bash
yum install bash-completion -y
echo 'source <(kubectl completion bash)' >>~/.bashrc
source ~/.bashrc
```





#### **安装基础cni插件flannel**

```bash
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```



#### **安装ingress controller**

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
```



```bash
k8s.gcr.io/ingress-nginx/kube-webhook-certgen:v1.1.1
k8s.gcr.io/ingress-nginx/controller:v1.1.2  
```

```yaml
externalIPs:
  - 192.168.0.236
```





#### **安装dashboard**

```BASH
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.6.2/high-availability-1.21+.yaml
```

```BASH
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/refs/tags/v1.23.2/cluster/addons/dashboard/dashboard.yaml
```



{{% alert title="报错" color="warning" %}}

```bash
x509: cannot validate certificate for 192.168.0.xxx because it doesn't contain any IP SANs
"Failed probe" probe="metric-storage-ready" err="no metrics to serve"
```

解决办法

```bash
--kubelet-insecure-tls
```

{{% /alert %}}





```bash
openssl genrsa -out dashboard.key 2048
openssl req -new -key dashboard.key -out ca.csr -subj "/C=CN/ST=Gd/L=SZ/O=zero-dew.com/CN=dashboard.zero-dew.com"
openssl x509 -req -in ca.csr -out dashboard.crt -signkey  dashboard.key -days 3650
```

```bash
kubectl -n kubernetes-dashboard create secret tls dashboard-tls --cert=dashboard.crt --key=dashboard.key
```



```bash
cat << 'EOF' |kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: dashboard
  namespace: kubernetes-dashboard
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - dashboard.zero-dew.com
    secretName: dashboard-tls
  rules:
  - host: dashboard.zero-dew.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: kubernetes-dashboard
            port:
              number: 443
EOF
```

```bash
192.168.0.236 A dashboard.zero-dew.com
```



```bash
https://dashboard.zero-dew.com
```



```bash
kubectl create sa dashboard-admin -n kubernetes-dashboard

kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kubernetes-dashboard:dashboard-admin 
kubectl describe secret dashboard-admin-token-vm6lm  -n kubernetes-dashboard
```



#### **安装nfs  storage class**



```yaml
# https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner
# https://www.cnblogs.com/punchlinux/p/16552183.html
---
apiVersion: v1
kind: Namespace
metadata:
  name: nfs-storage
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nfs-client-provisioner
  namespace: nfs-storage
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: nfs-client-provisioner
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    verbs: ["get", "list", "watch", "create", "delete"]
  - apiGroups: [""]
    resources: ["persistentvolumeclaims"]
    verbs: ["get", "list", "watch", "update"]
  - apiGroups: ["storage.k8s.io"]
    resources: ["storageclasses"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["create", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: nfs-client-provisioner
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: nfs-client-provisioner
subjects:
- kind: ServiceAccount
  name: nfs-client-provisioner
  namespace: nfs-storage
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: leader-locking-nfs-client-provisioner
  namespace: nfs-storage
rules:
- apiGroups:
  - ""
  resources:
  - endpoints
  verbs:
  - get
  - list
  - watch
  - create
  - update
  - patch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: leader-locking-nfs-client-provisioner
  namespace: nfs-storage
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: leader-locking-nfs-client-provisioner
subjects:
- kind: ServiceAccount
  name: nfs-client-provisioner
  namespace: nfs-storage
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-nfs-storage
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"  # 设置为默认sc
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner
allowVolumeExpansion: true #允许动态扩容，比如kubectl edit pvc
reclaimPolicy: Retain	 #PV的删除策略默认为delete,删除后pv立即删除NFS server的数据
mountOptions:
  #- vers=4.1 #NFS版本，containerd有部分参数异常
  #- noresvport  #告知NFS客户端在重新建立网络连接时，使用新的传输控制协议端口
  - noatime  #访问文件时不更新文件inode中的时间戳，高并发环境可提高性能
parameters:
  #mountOptions: "vers=4.1,noresvport,noatime"
  archiveOnDelete: "true"  #删除pod时保留pod数据，默认为false时不保留数据
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nfs-client-provisioner
  labels:
    app: nfs-client-provisioner
  namespace: nfs-storage
spec:
  replicas: 1
  strategy: #部署策略
    type: Recreate
  selector:
    matchLabels:
      app: nfs-client-provisioner
  template:
    metadata:
      labels:
        app: nfs-client-provisioner
    spec:
      serviceAccountName: nfs-client-provisioner
      containers:
        - name: nfs-client-provisioner
          #image: k8s.gcr.io/sig-storage/nfs-subdir-external-provisioner:v4.0.2 
          image: registry.cn-hangzhou.aliyuncs.com/liangxiaohui/nfs-subdir-external-provisioner:v4.0.2
          volumeMounts:
            - name: nfs-client-root
              mountPath: /persistentvolumes
          env:
            - name: PROVISIONER_NAME
              value: k8s-sigs.io/nfs-subdir-external-provisioner
            - name: NFS_SERVER
              value: 10.4.7.250
            - name: NFS_PATH
              value: /data/volumes
      volumes:
        - name: nfs-client-root
          nfs:
            server: 192.168.0.108
            path: /data/volumes
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-test
  namespace: nfs-storage
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: managed-nfs-storage
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: test
  name: test
  namespace: nfs-storage
spec:
  containers:
  - args:
    - sleep
    - "1000"
    image: busybox
    name: test
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
  volumes:
  - name: dyncmic-pvc
    persistentVolumeClaim:
      claimName: pvc-test

# yum install rpcbind nfs-utils -y
# systemctl enable rpcbind nfs --now 
# systemctl status  rpcbind nfs


# install -d /data/volumes
# echo "/data/volumes  *(rw,sync,no_root_squash)" >/etc/exports
# root@harbor:~# exportfs -r

# showmount -e 192.168.0.108
# mount -t nfs 192.168.0.108:/data/volumes /mnt  
```






#### **安装multus cni插件 + SpiderPool**

![](https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/18630fde0b43e38addb4a83c437c833c39854ffe/docs/images/multus-pod-image.svg)

安装多网卡cni `multus`

```bash
kubectl apply -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset.yml
```



安装ipam  `SpiderPool`

```bash
helm repo add spiderpool https://spidernet-io.github.io/spiderpool
helm fetch spiderpool/spiderpool
```

```bash
helm install spiderpool spiderpool/spiderpool \
--set multus.enableMultusConfig=false \
--set global.imageRegistryOverride=ghcr.m.daocloud.io \
--wait --namespace kube-system 
```

```bash
tee <<EOF|kubectl apply -f -
apiVersion: spiderpool.spidernet.io/v2beta1
kind: SpiderIPPool
metadata:
  name: macvlan-ipv4
spec:
  default: true
  subnet: 192.168.0.0/24
  ips:
  - "192.168.0.213-192.168.0.216"
  - "192.168.0.174-192.168.0.209"
EOF
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: "k8s.cni.cncf.io/v1"
kind: NetworkAttachmentDefinition
metadata:
  name: macvlan1
  namespace: kube-system
spec:
  config: '{
            "cniVersion": "0.3.0",
            "type": "macvlan",
            "master": "ens192",
            "mode": "bridge",
      		"ipam": {
                "type": "spiderpool"
            },
            "promiscuous": true
        }'
EOF
```

测试mcvlan

```bash
cat <<EOF|kubectl apply -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: test
spec:
  selector:
    matchLabels:
      app: test
  template:
    metadata:
      labels:
        app: test
      annotations:
        k8s.v1.cni.cncf.io/networks: macvlan
    spec:
      tolerations:
      - effect: ""
        key: "node-role.kubernetes.io/master"
      containers:
      - name: test
        securityContext:
          privileged: true
        image: quay.io/libpod/alpine:3.10.2
        command: ["sleep","1000"]
EOF
```



#### prometheus监控告警

{{% alert title="目标" color="" %}}
1. 对基础组件的指标采集。`kube-apiserver`、`kube-scheduler`、`kube-controllermanager`、`kubelet`、`kubeproxy`、`etcd`、`coredns`、`cni`、`csi`、`cri`、`node`
2. 通过label 或annotation 通过kubernetes_sd_config 的对业务pod动态发现
3. 完善一个kubernetes基础平台的dashbaord
4. 完善一个kubernetes基础平台的alert 模版和告警规则

{{% /alert %}}

```bash
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      tolerations:
      - key: ""
        operator: "Exists"
      volumes:
      - name: root
        hostPath:
          path: /
      hostNetwork: true
      hostPID: true
      containers:
      - name: node-exporter
        image: quay.io/prometheus/node-exporter:v1.6.1
        args:
        - --path.rootfs=/host
        volumeMounts:
        - mountPath: /host
          name: root
```



```yaml
scrape_configs:
  - job_name: node-exporter
    kubernetes_sd_configs:
    - api_server: https://192.168.0.144:16443
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.crt
        cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
        key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
        # 测试改成false也没问题
        insecure_skip_verify: true
      role: node
    relabel_configs:
    - source_labels: [__address__]
      regex: (.*):(.*)
      replacement: "$1:9100"
      target_label: __address__
      
  - job_name: 'etcd'
    tls_config:
      ca_file: /etc/kubernetes/pki/etcd/ca.crt
      cert_file: /etc/kubernetes/pki/etcd/peer.crt
      key_file: /etc/kubernetes/pki/etcd/peer.key
    scheme: https
    kubernetes_sd_configs:
    - api_server: https://192.168.0.144:16443
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.crt
        cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
        key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
        # 测试改成false也没问题
        insecure_skip_verify: true
      role: node
    relabel_configs:
    - source_labels: [__meta_kubernetes_node_label_kubernetes_io_role]
      regex: "master"
      action: keep
    - source_labels: [__address__]
      regex: (.*):(.*)
      replacement: "$1:2379"
      target_label: __address__
      
  - job_name: kube-apiserver
    honor_timestamps: true
    scrape_interval: 1m
    scrape_timeout: 1m
    metrics_path: /metrics
    scheme: https
    tls_config:
      ca_file: /etc/kubernetes/pki/ca.crt
      cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
      key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
      insecure_skip_verify: false
    follow_redirects: true
    enable_http2: true
    kubernetes_sd_configs:
    - api_server: https://192.168.0.144:16443
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.crt
        cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
        key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
        # 测试改成false也没问题
        insecure_skip_verify: true
      role: node
    relabel_configs:
    - source_labels: [__meta_kubernetes_node_label_kubernetes_io_role]
      regex: "master"
      action: keep
    - source_labels: [__address__]
      regex: (.*):(.*)
      replacement: "$1:6443"
      target_label: __address__
  
  - job_name: kubelet
    honor_timestamps: true
    scrape_interval: 1m
    scrape_timeout: 1m
    metrics_path: /metrics
    scheme: https
    tls_config:
      ca_file: /etc/kubernetes/pki/ca.crt
      cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
      key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
      insecure_skip_verify: true
    follow_redirects: true
    enable_http2: true
    kubernetes_sd_configs:
    - api_server: https://192.168.0.144:16443
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.crt
        cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
        key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
        # 测试改成false也没问题
        insecure_skip_verify: true
      role: node
    relabel_configs:
    - source_labels: [__address__]
      regex: (.*):(.*)
      replacement: "$1:10250"
      target_label: __address__
      

      
  - job_name: kube-state-metrics
    kubernetes_sd_configs:
    - api_server: https://192.168.0.144:16443
      tls_config:
        ca_file: /etc/kubernetes/pki/ca.crt
        cert_file: /etc/kubernetes/pki/apiserver-kubelet-client.crt
        key_file: /etc/kubernetes/pki/apiserver-kubelet-client.key
        # 测试改成false也没问题
        insecure_skip_verify: true
      role: service
    relabel_configs:
    - source_labels: ["__meta_kubernetes_service_name"]
      action: keep
      regex: "kube-state-metrics"
    - source_labels: ["__meta_kubernetes_service_label_prometheus_io_external","__meta_kubernetes_service_label_prometheus_io_ports"]
      regex: ([0-9\.]+);(\d+)
      replacement: $1:$2
      action: replace
      target_label: __address__
```



#### filebeat日志采集

{{% alert title="目标" color="" %}}
1. 采集基础组件：`kube-apiserver`、`kube-scheduler`、`kube-controllermanager`、`kubelet`、`kubeproxy`、`etcd`、`coredns`、`cni`、`csi`、`cri`、`node`
2. 通过label 或annotation 对业务pod动态发现

{{% /alert %}}




{{% details %}}

```bash
kubectl annotation ns kube-system filebeat=true
```



```yaml
filebeat.autodiscover:
  providers:
  - type: kubernetes
    node: ${NODE_NAME}
    templates:
    - condition:
        or:
        - equals:
          kubernetes.labels.filebeat: "true"
        - equals:
          kubernetes.namespace_labels.filebeat: "true"
      config:
      - type: filestream
        id: container-${data.kubernetes.container.id}
        prospector.scanner.symlinks: true
        paths:
        - /var/log/containers/*-${data.kubernetes.container.id}.log
        parsers:
        - container: ~
        - multiline:
            type: pattern
            pattern: '^\['
            negate: true
            match: after
```

{{% /details %}}



#### skywalking



#### **继续添加master节点**

```bash
kubeadm join 192.168.0.144:16443 --token mhnut3.z7xz7l9xzoj8vorg \
--discovery-token-ca-cert-hash sha256:3e77b765acb011d12cfb2649040ba6b51dd07ac6ee1746ce540740fc9d31bea3 \
--control-plane --certificate-key 33bdaf597978b2355117cb742562dbaf4b91a20abb8e3a9f145439122b4eae48 \
-v5
```

```bash
systemctl enable kubelet
```



#### **添加node节点**

```bash
kubeadm join 192.168.0.144:16443 --token mhnut3.z7xz7l9xzoj8vorg \
--discovery-token-ca-cert-hash sha256:3e77b765acb011d12cfb2649040ba6b51dd07ac6ee1746ce540740fc9d31bea3 \
-v5
```

```bash
systemctl enable kubelet
```
