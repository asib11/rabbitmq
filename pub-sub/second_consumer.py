import pika
from pika.exchange_type import ExchangeType

def on_message_received(ch, method, properties, body):
    print(f"Second consumer - Received: {body}")


connection_parameters = pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('user', 'password'))
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)
queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(queue=queue.method.queue, exchange='pubsub')
channel.basic_consume(queue=queue.method.queue, on_message_callback=on_message_received, auto_ack=True)
print("Start consuming messages...")
channel.start_consuming()