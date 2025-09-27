#!/usr/bin/env python3
import pika

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    # 手动 ACK（如需）
    # ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials('admin', 'admin')
    params = pika.ConnectionParameters(
        host='192.168.0.161',
        port=5672,
        virtual_host='/',
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=300
    )

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='hello', durable=False)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_consume(
        queue='hello',
        on_message_callback=callback,
        auto_ack=True        # 若改为手动 ACK，记得在 callback 中 ack
    )

    channel.start_consuming()

if __name__ == '__main__':
    main()