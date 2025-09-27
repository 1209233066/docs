---
date: '2025-05-20T21:44:02+08:00'
draft: false
title: 'gitlab'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  gitlab||devops
tags: ["gitlab"]
categories: ["devops"]
url: devops/gitlab.html
author: "wangendao"
---

*基于Ruby 的 rails框架开发，主要组件：nginx postgreSQL redis sidekiq*

版本： gitlab-ee（企业版） gitlab-ce（社区版） 极狐（面向中国的版本）

8c 16G centons7

https://docs.gitlab.com/

https://www.kancloud.cn/apachecn/gitlab-doc-zh/1948588



### 安装部署

使用docker安装

```bash
export GITLAB_HOME=/home/gitlab
sudo docker run --detach \
  --hostname gitlab.example.com \
  --publish 443:443 --publish 80:80 --publish 122:22 \
  --name gitlab \
  --restart always \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  --shm-size 256m \
  -m 4g\
  gitlab-jh.tencentcloudcr.com/omnibus/gitlab-jh:latest
```



1. 创建数据目录
    ```bash
    pvcreate /dev/sdb 
    vgextend centos /dev/sdb
    lvcreate -L +199G -n gitlab centos
    mkfs.ext4 /dev/mapper/centos-gitlab 
    ```
    ```bash
    # 默认数据放在/opt/gitlab,如何修改这个路径
    
    mkdir /opt/gitlab
    echo /dev/mapper/centos-gitlab  /opt/gitlab  ext4 defaults 0 0 >>/etc/fstab
    mount -a 
    
    df -hT /gitlab
    ```

2. 离线rpm包安装
   ```bash
   wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-15.0.1-ce.0.el7.x86_64.rpm
   yum localinstall gitlab-ce-15.0.1-ce.0.el7.x86_64.rpm -y
   ```

3. 修改配置文件
   ```bash
   vi /etc/gitlab/gitlab.rb
    修改下面这一行
    external_url 'http://192.168.0.247'
   ```

4. 启动服务
   ```bash
   gitlab-ctl reconfigure
   ```
   日后重启服务
   ```bash
   gitlab-ctl start gitaly
   gitlab-ctl start gitlab-kas
   gitlab-ctl start gitlab-workhorse
   gitlab-ctl start logrotate
   gitlab-ctl start nginx
   gitlab-ctl start postgresql
   gitlab-ctl start puma
   gitlab-ctl start redis
   gitlab-ctl start sidekiq
   ```
5. [卸载](https://docs.gitlab.com/omnibus/installation/)
   ```bash
   sudo gitlab-ctl stop && sudo gitlab-ctl remove-accounts
   
   sudo systemctl stop gitlab-runsvdir
   sudo systemctl disable gitlab-runsvdir
   sudo rm /usr/lib/systemd/system/gitlab-runsvdir.service
   sudo systemctl daemon-reload
   sudo systemctl reset-failed
   sudo gitlab-ctl uninstall
   
   sudo gitlab-ctl cleanse && sudo rm -r /opt/gitlab
   yum remove gitlab-ce
   ```
### 使用
1. 默认用户`root`,密码 `cat /etc/gitlab/initial_root_password`
![alt text](/docs/devops/gitlab/img/image.png)
2. 登录后首页
![alt text](/docs/devops/gitlab/img/image-1.png)
3. 基础设置
  + 修改root密码
    ![alt text](/docs/devops/gitlab/img/image-2.png)
    ![alt text](/docs/devops/gitlab/img/image-3.png)
  + 基本页面，amdin是后台管理页面
    ![alt text](/docs/devops/gitlab/img/image-5.png)
  + 关闭注册
  + 中文显示
  + 邮箱配置

    Docs: https://docs.gitlab.com/omnibus/settings/smtp.html
    {{% alert title="ERROR" color="warning" %}}
```bash
    irb(main):001:0> Notify.test_email('1209233066@qq.com','test','gitlab test').deliver_now
Delivered mail 6683e6c0128bc_1e1d45d83bd@gitlab.mail (35089.4ms)
Traceback (most recent call last):
        1: from (irb):1
EOFError (end of file reached)
```
    {{% /alert %}}



    vi /etc/gitlab/gitlab.rb
    ```ruby
    ### GitLab email server settings
    ###! Docs: https://docs.gitlab.com/omnibus/settings/smtp.html
    ###! **Use smtp instead of sendmail/postfix.**
    
    gitlab_rails['smtp_enable'] = true
    gitlab_rails['smtp_address'] = "smtp.qq.com"
    gitlab_rails['smtp_port'] = 465
    gitlab_rails['smtp_user_name'] = "810654947@qq.com"
    gitlab_rails['smtp_password'] = "kqaexaxpbrbdbajd"
    gitlab_rails['smtp_domain'] = "smtp.qq.com"
    gitlab_rails['smtp_authentication'] = "login"
    gitlab_rails['smtp_enable_starttls_auto'] = false
    gitlab_rails['smtp_tls'] = true
    # gitlab_rails['smtp_pool'] = false
    
    ### Email Settings
    
    gitlab_rails['gitlab_email_enabled'] = true
    
    ##! If your SMTP server does not like the default 'From: gitlab@gitlab.example.com'
    ##! can change the 'From' with this setting.
    gitlab_rails['gitlab_email_from'] = '810654947@qq.com'
    gitlab_rails['gitlab_email_display_name'] = 'gitlabAdmin'
    # gitlab_rails['gitlab_email_reply_to'] = 'noreply@example.com'
    # gitlab_rails['gitlab_email_subject_suffix'] = ''
    # gitlab_rails['gitlab_email_smime_enabled'] = false
    # gitlab_rails['gitlab_email_smime_key_file'] = '/etc/gitlab/ssl/gitlab_smime.key'
    # gitlab_rails['gitlab_email_smime_cert_file'] = '/etc/gitlab/ssl/gitlab_smime.crt'
    # gitlab_rails['gitlab_email_smime_ca_certs_file'] = '/etc/gitlab/ssl/gitlab_smime_cas.crt'
    ```
    ```bash
    gitlab-ctl stop 
    gitlab-ctl reconfigure
    gitlab-ctl start 
    gitlab-rails console
    ```
    ```bash
    Notify.test_email('1209233066@qq.com', 'Message Subject', 'Message Body').deliver_now
    ```
    ![alt text](/docs/devops/gitlab/img/image-14.png)

4. 组织配置
+ namespace 用于逻辑隔离，可以分为用户名称空间，组名称空间，子组名称空间。
  + user namespace 
  + group namespace
    ![alt text](/docs/devops/gitlab/img/image-13.png)
  + subgroup namespace

    创建子组
    ![alt text](/docs/devops/gitlab/img/image-4.png)
    ![alt text](/docs/devops/gitlab/img/image-11.png)
    ![alt text](/docs/devops/gitlab/img/image-12.png)

+ 用户管理
  + 添加成员
  + 加入组
  + 分配角色

+ groups 用户管理一个或多个项目

5. 项目管理
  + 创建项目、导入项目
  + 

6. 版本升级
   不要跨越大版本，直接下载rpm包更新

1. 创建一个pytc的组
   ![alt text](/docs/devops/gitlab/img/image-6.png)
2. 创建一个项目seagull，隶属于pytc 的组
3. 添加dev01/dev02 属于该组织


### 触发jienkins构建
> 路径： 找到对应项目 > setting > Webhooks 
![alt text](/docs/devops/gitlab/img/image-7.png)

选择对应触发事件进行测试

![alt text](/docs/devops/gitlab/img/image-8.png)
![alt text](/docs/devops/gitlab/img/image-9.png)



### 忘记root密码
https://blog.csdn.net/qq_21017997/article/details/131420935