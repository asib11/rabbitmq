
import json
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


def on_request(ch, method, properties, body):
    request = json.loads(body)

    product_id = request["product_id"]
    quantity = request["quantity"]

    unit_price = 1500
    total_price = unit_price * quantity

    response = {
        "product_id": product_id,
        "total_price": total_price,
    }

    ch.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=json.dumps(response),
    )

    print(f"Request processed: {request}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue="price_requests",
    on_message_callback=on_request,
    auto_ack=False,
)

print("Pricing server waiting for requests...")

channel.start_consuming()