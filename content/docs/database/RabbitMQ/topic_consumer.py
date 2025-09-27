#!/bin/python3

import pika

# 连接RabbitMQ
credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.161', 5672, '/', credentials))
channel = connection.channel()

# 声明交换机
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# 声明队列
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 绑定队列到交换机
channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key='topic_logs')


# 定义回调函数
def callback(ch, method, properties, body):
    print(" [x] %r" % body)

# 消费消息
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# 开始消费
channel.start_consuming()



