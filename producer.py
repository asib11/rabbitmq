import pika

connection_parameters = pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('user', 'password'))
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.queue_declare(queue='letterbox')
for i in range(1, 11):
    message = f"Message {i}"

    channel.basic_publish(
        exchange="",
        routing_key="letterbox",
        body=message
    )
    print(f"Message sent: {message}")

channel.basic_publish(exchange='', routing_key='letterbox', body=message)
print(f"message Sent successfully")

connection.close()