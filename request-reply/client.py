
import json
import uuid
import pika

credentials = pika.PlainCredentials("user", "password")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        "localhost",
        credentials=credentials,
    )
)

channel = connection.channel()

channel.queue_declare(queue="price_requests")

# Temporary queue for receiving the response
result = channel.queue_declare(
    queue="",
    exclusive=True,
)

reply_queue = result.method.queue

correlation_id = str(uuid.uuid4())
response_data = None


def on_response(ch, method, properties, body):
    global response_data

    if properties.correlation_id == correlation_id:
        response_data = json.loads(body)

        print(f"Response received: {response_data}")

        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming()


channel.basic_consume(
    queue=reply_queue,
    on_message_callback=on_response,
    auto_ack=False,
)

request = {
    "product_id": 101,
    "quantity": 3,
}

channel.basic_publish(
    exchange="",
    routing_key="price_requests",
    properties=pika.BasicProperties(
        reply_to=reply_queue,
        correlation_id=correlation_id,
    ),
    body=json.dumps(request),
)

print(f"Request sent: {request}")

# Wait for the matching response
channel.start_consuming()

connection.close()