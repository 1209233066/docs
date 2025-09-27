---
date: '2025-07-15T15:22:40+08:00'
draft: false
title: 'kubeadm工具'
linkTitle: 'kubeadm tools'
type: blog
toc_hide: false
weight: 3
description: >
  介绍kubeadm工具的使用。搭建集群/节点扩容/版本升级
tags: ["kubeadm"]
categories: ["kubernetes"]
url: kubernetes/kubernetes_setup/kubeadm.html
author: "wangendao"
---

---

**任务：**

- [ ] 什么是bootstraptoken,在kubernetes中的应用
- [ ] kube-apiserver 的认证方式有哪些，输出最佳实践
- [ ] kubeadm 配置文件结构体，支持哪些配置和字段

authentication  认证

authorization   授权

---














执行kubeadm init 阶段将`ClusterConfiguration` 配置上传到kube-system名称空间下` kubeadm-config ` configmap中，

执行`kubeadm join`、`kubeadm reset`、 `kubeadm upgrade` 时读取该配置

`kubeadm config migrate` 来转换旧配置文件

`kubeadm config validate` 可用于验证配置文件

`kubeadm config images list` 

`kubeadm config images pull`

`kubeadm config print`

`kubeadm token create`

配置文件包含5中类型：

```bash
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration

apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration

apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration

apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration

apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
```

```bash
kubeadm config print init-defaults
kubeadm config print join-defaults
```



```bash
kubeadm config print init-defaults \
--component-configs KubeProxyConfiguration \
--component-configs KubeletConfiguration
```

`kubeadm/app/apis/kubeadm/types.go`



```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
localAPIEndpoint:
  advertiseAddress: 192.168.0.161
  bindPort: 6443
nodeRegistration:
  criSocket: /var/run/dockershim.sock
  imagePullPolicy: IfNotPresent
  name: seagullcore01-uat-s2
  taints: null
dryRun: false
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
imageRepository: k8s-gcr.m.daocloud.io
kubernetesVersion: 1.23.17
apiServer:
  timeoutForControlPlane: 4m0s
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns: {}
etcd:
  local:
    dataDir: /var/lib/etcd
networking:
  dnsDomain: cluster.local
  serviceSubnet: 172.168.0.0/16
scheduler: {}
```

`kubeadm/app/apis/config/types.go`

```yaml
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
bindAddress: 0.0.0.0            # kube-proxy 监听的地址
healthzBindAddress: ""          # /healthz 默认 0.0.0.0:10256
metricsBindAddress: ""          # /metrics 默认 0.0.0.0:10249
hostnameOverride: ""        # kube-proxy 实例的名称，默认 `hostname`
bindAddressHardFail: false  # 当为true,kube-proxy监听ip和端口失败，报致命错误并退出
enableProfiling: false          # 允许 /debug/pprof
clientConnection:                       # 连接apiserver的配置
  kubeconfig: /var/lib/kube-proxy/kubeconfig.conf
  acceptContentTypes: ""
  burst: 0
  contentType: ""
  qps: 0
mode: "ipvs"
ipvs:
  scheduler: "rr"
clusterCIDR: "172.168.0.0/16"
configSyncPeriod: 0s
oomScoreAdj: -1000
portRange: "20000-65535"
```

```yaml
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
bindAddress: 0.0.0.0            # kube-proxy 监听的地址
healthzBindAddress: ""          # /healthz 默认 0.0.0.0:10256
metricsBindAddress: ""          # /metrics 默认 0.0.0.0:10249
hostnameOverride: ""        # kube-proxy 实例的名称，默认 `hostname`
bindAddressHardFail: false  # 当为true,kube-proxy监听ip和端口失败，报致命错误并退出
enableProfiling: false          # 允许 /debug/pprof
clientConnection:                       # 连接apiserver的配置
  kubeconfig: /var/lib/kube-proxy/kubeconfig.conf
  acceptContentTypes: ""
  burst: 0
  contentType: ""
  qps: 0
mode: "ipvs"
ipvs:
  scheduler: "rr"
clusterCIDR: "172.168.0.0/16"
configSyncPeriod: 0s
oomScoreAdj: -1000
portRange: "20000-65535"
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  anonymous:
    enabled: false
  webhook:
    cacheTTL: 0s
    enabled: true
  x509:
    clientCAFile: /etc/kubernetes/pki/ca.crt
authorization:
  mode: Webhook
  webhook:
    cacheAuthorizedTTL: 0s
    cacheUnauthorizedTTL: 0s
cgroupDriver: cgroupfs
clusterDNS:
- 172.168.0.2
clusterDomain: cluster.local
cpuManagerReconcilePeriod: 0s
evictionPressureTransitionPeriod: 0s
fileCheckFrequency: 0s
healthzBindAddress: 0.0.0.0
healthzPort: 10248
httpCheckFrequency: 0s
imageMinimumGCAge: 0s
logging:
  flushFrequency: 0
  options:
    json:
      infoBufferSize: "0"
  verbosity: 0
memorySwap: {}
nodeStatusReportFrequency: 0s
nodeStatusUpdateFrequency: 0s
rotateCertificates: true
runtimeRequestTimeout: 0s
shutdownGracePeriod: 0s
shutdownGracePeriodCriticalPods: 0s
staticPodPath: /etc/kubernetes/manifests
streamingConnectionIdleTimeout: 0s
syncFrequency: 0s
volumeStatsAggPeriod: 0s
```



```bash
kubeadm config print join-defaults
```



```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
caCertPath: /etc/kubernetes/pki/ca.crt
discovery:
  bootstrapToken:
    apiServerEndpoint: kube-apiserver:6443
    token: abcdef.0123456789abcdef
    unsafeSkipCAVerification: true
  timeout: 5m0s
  tlsBootstrapToken: abcdef.0123456789abcdef
nodeRegistration:
  criSocket: /var/run/dockershim.sock
  imagePullPolicy: IfNotPresent
  name: master01
  taints: null
```







[Kubeadm | Kubernetes](https://kubernetes.io/zh-cn/docs/reference/setup-tools/kubeadm/)

[使用 kubeadm 引导集群 | Kubernetes](https://kubernetes.io/zh-cn/docs/setup/production-environment/tools/kubeadm/)

[Kubeadm | Kubernetes](https://kubernetes.io/zh-cn/docs/reference/setup-tools/kubeadm/)

[kubeadm 配置（v1beta3） | Kubernetes](https://kubernetes.io/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/)

控制平面与 kubelet 之间可以存在**一个**次要版本的偏差，但 kubelet 的版本不可以超过 API 服务器的版本。 例如，1.7.0 版本的 kubelet 可以完全兼容 1.8.0 版本的 API 服务器，反之则不可以。

[版本偏差策略 | Kubernetes](https://kubernetes.io/zh-cn/releases/version-skew-policy/)

[使用 kubeadm 创建集群 | Kubernetes](https://kubernetes.io/zh-cn/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#version-skew-policy)

