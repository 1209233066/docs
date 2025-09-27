---
date: '2025-09-17T16:12:16+08:00'
draft: false
title: 'rsyslog'
type: blog
toc_hide: false
hide_summary: true
weight: 6
description: >
  centos7 配置 rsyslog|linux
tags: ["log"]
categories: ["linux"]
url: linux/rsyslog.html
author: "wangendao"
---



```bash
yum install rsyslog 
```

```bash
[root@zabbix ~]# grep -Ev '^$|^#' /etc/rsyslog.conf 

#开启udp/tcp 514 接收日志
$ModLoad imudp
$UDPServerRun 514
$ModLoad imtcp
$InputTCPServerRun 514
#默认的日志格式模板，无需定义
$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
#屏蔽本机的日志
:fromhost-ip,!isequal,"127.0.0.1" ?RSYSLOG_TraditionalFileFormat
#所有类型.所以级别				: :ommysql:主机,库名,用户名,密码
*.*                          @filebeat:端口

#检查语法rsyslog.conf 
[root@Nagios ~]# rsyslogd -f /etc/rsyslog.conf -N1
[root@Nagios ~]# /etc/init.d/rsyslog restart
```

客户端配置

```bash
H3C 配置
sys
info-center loghost 168.204.37.50
linux配置
*.* 	@168.204.37.50  # tcp
*.* 	@@168.204.37.50  ## udp
```



rsyslog.conf 

rsyslog中的数据库支持是通过可加载的插件模块集成的。要使用数据库功能，必须在使用第一个数据库表操作之前在配置文件中启用数据库插件。这是通过放置

$ModLoad ommysql

接下来，我们需要告诉rsyslogd将数据写入数据库。由于使用默认架构，因此无需为此定义模板。我们可以使用硬编码的代码（rsyslogd处理正确的模板链接）。因此，对于MySQL，我们需要做的就是在/etc/rsyslog.conf中添加一个简单的选择器行：

*.*    :ommysql:database-server,database-name,database-userid,database-password

例如，如果您仅对来自邮件子系统的消息感兴趣，则可以使用以下选择器行：

mail.*    :ommysql:127.0.0.1,syslog,syslogwriter,topsecret

 

如果您要转发多个服务器，则可以很快完成。Rsyslog对操作的数量或类型没有限制，因此您可以定义任意多个目标。然而，重要的是要知道，全套指令构成了一个动作。因此，您不能简单地添加（仅）第二条转发规则，而还需要复制规则配置。请注意，对于第二个操作，请使用不同的队列文件名，否则将使系统混乱。

转发到两个主机的示例如下所示：

$ ModLoad imuxsock ＃本地消息接收 

$ WorkDirectory / rsyslog / work ＃工作（假脱机）文件的默认位置

## ***\*记录系统日志消息的优先级\****[***\*¶\****](#recording-the-priority-of-syslog-messages)

 

 

 

 

＃开始转发规则1 

$ ActionQueueType LinkedList ＃使用异步处理 

$ ActionQueueFileName srvrfwd1 ＃设置文件名，还启用磁盘模式 

$ ActionResumeRetryCount -1 ＃插入失败时无限重试 

$ ActionQueueSaveOnShutdown on ＃如果rsyslog关闭，则保存内存数据

*.* @@ server1：端口

＃结束转发规则1

 

＃开始转发规则2 

$ ActionQueueType LinkedList ＃使用异步处理 

$ ActionQueueFileName srvrfwd2 ＃设置文件名，还启用磁盘模式 

$ ActionResumeRetryCount -1 ＃插入失败时无限重试 

$ ActionQueueSaveOnShutdown on ＃如果rsyslog关闭，则保存内存数据

*.* @@ server2

＃结束转发规则2

 

 

配置日志模板： $template 模板名称,

"%timegenerated% %HOSTNAME% %syslogtag%%msg%0

$template RemoteLogs,"/tmp/rsyslog/%$YEAR%-%$MONTH%/%fromhost-ip%/%fromhost-ip%_%$YEAR%-%$MONTH%-%$DAY%.log"
