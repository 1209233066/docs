#!/bin/python3

import pika,sys

# 连接RabbitMQ
credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.161', 5672, '/', credentials))
channel = connection.channel()

# 声明交换机
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# 发送消息
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='topic_logs', routing_key='topic_logs', body=message)
print(" [x] Sent %r" % message)




# 关闭连接
connection.close()