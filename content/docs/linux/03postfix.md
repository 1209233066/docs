---
date: '2025-06-17T16:12:16+08:00'
draft: false
title: 'postfix'
type: blog
toc_hide: false
hide_summary: true
weight: 3
description: >
  centos7 配置 Postfix |linux
tags: ["mail"]
categories: ["linux"]
url: linux/postfix.html
author: "wangendao"
---

![](https://rpic.origz.com/api.php?category=photography)

centos7 配置 Postfix 

```bash
yum install -y postfix mailx  install cyrus-sasl-plain cyrus-sasl-lib
```



1. 检查 /etc/postfix/main.cf 相关配置

```bash
cat >>/etc/postfix/main.cf<<'EOF'
relayhost = [smtp.qq.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_use_tls = yes
smtp_tls_CAfile = /etc/ssl/certs/ca-bundle.crt
inet_protocols = ipv4
EOF
```



2. 检查 /etc/postfix/sasl_passwd 内容

```bash
# [smtp.qq.com]:587 你的QQ邮箱@qq.com:授权码
echo "[smtp.qq.com]:587 810654947@qq.com:kqaexaxpbrbdbajd" >>/etc/postfix/sasl_passwd
```



3. 生成 hash 文件并设置权限

```bash
sudo postmap /etc/postfix/sasl_passwd
sudo chmod 600 /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db
```



4. 重启 Postfix

```bash
sudo systemctl restart postfix
```



5. 测试

```bash
echo "good luck" | mail -s "test" -r 810654947@qq.com 1209233066@qq.com
```



