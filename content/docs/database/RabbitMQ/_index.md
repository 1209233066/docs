---
title: ""
linkTitle: "RabbitMQ"
date: 2025-05-17
simple_list: true
weight: 7
type: docs
---



RabbitMQ安装、集群

安全

监控





学习前3章

AMQP advanced message queuing protocol 2004公布协议标准

交换机 exchange

队列 queue

绑定 

虚拟机 vhost： 是一个迷你版的rabbitMQ，可以隔离队列、交换机、绑定以及权限。默认vhost 为 “/“

rabbitmqctl add_vhost test

rabbitmqctl list_vhost test

rabbitmqctl delete_vhost test



消息持久化

+ 交换机和队列同时开启持久化参数durable = true

+ 消息投递时开启持久化参数 delivery_mode=2

  
