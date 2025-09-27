# producer_safe.py
import pika, sys

def main():
    credentials = pika.PlainCredentials('admin', 'admin')
    params = pika.ConnectionParameters(
        host='192.168.0.161',
        port=5672,
        virtual_host='/',
        credentials=credentials,
        socket_timeout=5
    )

    try:
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
    except Exception as e:
        print("连接失败：", e)
        sys.exit(1)

    # 先检查队列是否存在；如果不存在再创建
    try:
        ch.queue_declare(queue='hello', passive=True)
    except pika.exceptions.ChannelClosedByBroker as e:
        if e.reply_code == 404:   # 队列不存在
            ch = conn.channel()   # 重新打开通道
            ch.queue_declare(queue='hello', durable=False)
        else:
            raise

    try:
        ch.basic_publish(
            exchange='',
            routing_key='hello',
            body='Hello from safe producer'
        )
        print(" [x] Sent")
    except Exception as e:
        print("发送失败：", e)

    conn.close()

if __name__ == '__main__':
    main()