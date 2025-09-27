---

date: '2025-05-14T17:24:26+08:00'
draft: false
title: 'ArgoCD'
type: blog

toc_hide: false
hide_summary: true
weight: 1
description: >
 k8s argoCD
tags: ["kubernetes"]
categories: ["kubernetes"]
url: kubernetes/argoCD.html
---

argo CD <sub>v2.13.3</sub> 是一个遵循gitops 理念的持续交付工具,支持对多k8s集群执行部署

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

```bash
[root@master01 ~]# kubectl get pod -n argocd 
NAME                                                READY   STATUS    RESTARTS   AGE
argocd-application-controller-0                     1/1     Running   0          5m14s
argocd-applicationset-controller-7dd8f694d4-zmfbt   1/1     Running   0          5m14s
argocd-dex-server-b5885bb5d-cbw4p                   1/1     Running   0          5m14s
argocd-notifications-controller-564cb78f6f-8qrj9    1/1     Running   0          5m14s
argocd-redis-7857fdd468-b2g8m                       1/1     Running   0          5m14s
argocd-repo-server-5566c77dd9-k55l9                 1/1     Running   0          5m14s
argocd-server-6c44fb8d8-zvpnn                       1/1     Running   0          5m14s
```



查看初始化密码

```bash
kubectl -n argocd get secret  argocd-initial-admin-secret -ojsonpath='{.data.password}'|base64 -d
```

**支持通过ui 界面和argocd 命令操作**

+ **通过argocd 命令操作**

  ```bash
  wget https://github.com/argoproj/argo-cd/releases/download/v2.13.3/argocd-linux-amd64 -O /usr/bin/argocd
  chmod +x /usr/bin/argocd
  ```

  ```bash
  [root@master01 ~]#  kubectl get svc -n argocd argocd-server 
  NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
  argocd-server   NodePort   172.168.227.98   <none>        80:32322/TCP,443:30534/TCP   71m
  ```

  登录argocd

  ```bash
  [root@master01 ~]# argocd login argocd-server
  FATA[0000] dial tcp: lookup argocd-server on 192.168.0.1:53: no such host 
  [root@master01 ~]# argocd login  172.168.227.98
  WARNING: server certificate had error: tls: failed to verify certificate: x509: cannot validate certificate for 172.168.227.98 because it doesn't contain any IP SANs. Proceed insecurely (y/n)? y
  Username: admin
  Password: 
  'admin:login' logged in successfully
  Context '172.168.227.98' updated
  ```

  更新密码

  ```bash
  argocd account update-password
  ```

  



部署一个demo

1. 将名称空间从default 切换到 argocd

   ```bash
   kubectl config set-context --current --namespace=argocd
   ```

2. 部署应用

   > https://github.com/argoproj/argocd-example-apps.git

   ```bash
   argocd app create guestbook \
   --repo https://gitee.com/mingtian66/argocd-example-apps.git   \
   --path guestbook \
   --dest-server https://kubernetes.default.svc \
   --dest-namespace test
   ```

3. 查看app 状态，当前应用并未部署。处于OutOfSync 状态

   ```bash
   argocd app get  guestbook 
   ```

4. 执行部署,该命令从git 仓库获取清单并执行`kubectl apply` 动作

   ```bash
   argocd app sync guestbook
   ```

5. 销毁app

   ```bash
   argocd app delete guestbook
   ```

   

通过ui界面操作

![](https://img2024.cnblogs.com/blog/2108528/202501/2108528-20250126145019694-573427502.png)



### 参考

[docs](https://argo-cd.readthedocs.io/)|[Release](https://github.com/argoproj/argo-cd/releases/tag/v2.13.3)
