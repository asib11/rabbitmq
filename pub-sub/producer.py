import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('user', 'password'))
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

message = "Hello, I am broadcasting this message to all consumers!"
channel.basic_publish(exchange='pubsub', routing_key='', body=message)
print(f"message Sent successfully")

connection.close()