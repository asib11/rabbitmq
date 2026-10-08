import pika
import time
import random

def on_message_received(ch, method, properties, body):
    message = body
    print(f"Received: {message}")
    time.sleep(random.randint(1, 6))
    print(f"Processed: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('finish processing message')


connection_parameters = pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('user', 'password'))
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.queue_declare(queue='letterbox')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='letterbox', on_message_callback=on_message_received, auto_ack=False)
print("Start consuming messages...")
channel.start_consuming()