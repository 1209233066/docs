#!/usr/bin/env python3
import pika, sys

credentials = pika.PlainCredentials('admin', 'admin')
params = pika.ConnectionParameters(
    host='192.168.0.161',
    port=5672,
    virtual_host='/',
    credentials=credentials
)

connection = pika.BlockingConnection(params)
channel = connection.channel()

# 1. 声明 fanout 交换机（不存在则自动创建）
channel.exchange_declare(exchange='logs', exchange_type='fanout', durable=False)

message = ' '.join(sys.argv[1:]) or 'Hello Fanout!'
channel.basic_publish(
    exchange='logs',   # 指定交换机
    routing_key='',    # fanout 忽略 routing_key
    body=message
)
print(f" [x] Sent '{message}'")
connection.close()