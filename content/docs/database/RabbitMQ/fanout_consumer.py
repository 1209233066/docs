#!/usr/bin/env python3
import pika

credentials = pika.PlainCredentials('admin', 'admin')
params = pika.ConnectionParameters(
    host='192.168.0.161',
    port=5672,
    virtual_host='/',
    credentials=credentials
)

connection = pika.BlockingConnection(params)
channel = connection.channel()

# 1. 同样声明交换机
channel.exchange_declare(exchange='logs', exchange_type='fanout', durable=False)

# 2. 让服务器生成一个随机、独占、自动删除的队列
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue  # 形如 amq.gen-xxx...

# 3. 把队列绑定到交换机
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

channel.start_consuming()