import pika

def on_message_received(ch, method, properties, body):
    print(f"Received message: {body}")

connection_parameters = pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('user', 'password'))
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.queue_declare(queue='letterbox')
channel.basic_consume(queue='letterbox', on_message_callback=on_message_received, auto_ack=True)
print("Start consuming messages...")
channel.start_consuming()