# RabbitMQ Producer/Consumer Example

This project demonstrates a simple RabbitMQ message flow built with Python and Docker. It includes a producer that sends messages to a queue and a consumer that receives, processes, and acknowledges each message.

## What this project does

- Starts a RabbitMQ broker using Docker Compose
- Declares a queue named `letterbox`
- Publishes messages from `producer.py`
- Consumes messages from `consumer.py`
- Uses manual acknowledgements (`basic_ack`) so a message is only removed after successful processing
- Simulates work by sleeping for a random duration before acknowledging the message

## Project structure

- `docker-compose.yml` – runs RabbitMQ with the management plugin
- `producer.py` – sends messages to the `letterbox` queue
- `consumer.py` – receives and processes messages from the queue
- `pub-sub/` – demonstrates broadcasting messages with a fanout exchange
- `router/` – demonstrates direct and topic-based message routing
- `consistent-hash-exchange/` – demonstrates distributing messages using the consistent-hash exchange plugin
- `exchange-exchange/` – demonstrates routing a message from one exchange to another
- `header-exchange/` – demonstrates routing messages by message-header values
- `main.py` – placeholder entry point for the sample project
- `pyproject.toml` – Python project metadata and dependencies

## Prerequisites

Before running the project, make sure you have:

- Docker and Docker Compose installed
- Python 3.14 or compatible version
- `uv` (recommended for dependency management) or `pip`

## RabbitMQ credentials

The broker is configured with:

- Username: `user`
- Password: `password`

The RabbitMQ management UI is available at:

- http://localhost:15672

## Start RabbitMQ

From the project root, run:

```bash
docker compose up -d
```

This starts RabbitMQ on port `5672` and exposes the management interface on port `15672`.

## Install Python dependencies

Using `uv`:

```bash
uv sync
```

Or with `pip`:

```bash
pip install pika
```

## Run the producer

Send sample messages into the queue:

```bash
python producer.py
```

This produces messages like:

```text
Message 1
Message 2
...
Message 10
```

## Run the consumer

Start the consumer to read and process messages:

```bash
python consumer.py
```

The consumer will:

1. Connect to RabbitMQ at `localhost`
2. Declare the `letterbox` queue
3. Set `prefetch_count = 1` to process one message at a time
4. Receive each message through `on_message_received`
5. Print the message as received
6. Sleep for a random interval between 1 and 6 seconds
7. Print that it was processed
8. Acknowledge the message with `basic_ack`

## Message flow

The flow is:

```text
producer.py -> RabbitMQ queue: letterbox -> consumer.py
```

The queue is configured without an exchange, so messages are published directly to the queue using the default exchange.

## Example consumer behavior

The consumer does simulated processing work:

```python
print(f"Received: {message}")
time.sleep(random.randint(1, 6))
print(f"Processed: {message}")
ch.basic_ack(delivery_tag=method.delivery_tag)
```

This means no message is marked as done until the processing step finishes successfully.

## Publish/subscribe (fanout exchange)

The `pub-sub/` example broadcasts each message to every consumer with an active
subscription. The producer declares the `pubsub` exchange as `fanout`, and both
consumers create their own temporary, exclusive queues and bind them to that
exchange. The routing key is ignored by a fanout exchange.

Start each consumer in its own terminal:

```bash
python pub-sub/first_consumer.py
python pub-sub/second_consumer.py
```

Then publish a message:

```bash
python pub-sub/producer.py
```

Both running consumers should receive the broadcast. Because the consumer
queues are temporary, messages published while no consumer is subscribed are
not retained for later delivery.

## Message routing

The `router/` examples use exchanges to select queues based on a message's
routing key. Start the relevant consumer scripts in separate terminals before
running the producer so their temporary queues and bindings are in place.

### Direct routing

The scripts in `router/direct/` use the `routing` direct exchange. A direct
exchange delivers a message only to queues bound with an exact matching
routing key:

- `analyticsonly` routes to the analytics consumer.
- `paymentsonly` routes to the payments consumer.
- `both` routes to both consumers.

Start the consumers and then publish the sample message:

```bash
python router/direct/analytices_consumer.py
python router/direct/payment_consumer.py
python router/direct/producer.py
```

The current producer publishes with the `both` key, so both consumers receive
that message.

### Topic routing

The scripts in `router/topic/` use the `topic` exchange. Topic routing keys
are dot-separated words; `*` matches one word and `#` matches zero or more
words. The sample consumers bind these patterns:

- Analytics: `*.europe.*` matches messages about any one-word category in
  Europe.
- Payments: `#.payments` matches routing keys ending in `payments`.
- User: `user.#` matches routing keys beginning with `user`.

Start the consumers and then publish the sample messages:

```bash
python router/topic/analytics_consumer.py
python router/topic/payement_consumer.py
python router/topic/user_consumer.py
python router/topic/producer.py
```

The `user.europe.payments` message matches all three bindings. The
`business.europe.order` message matches only the analytics binding.

The broker started by `docker-compose.yml` uses the `user`/`password`
credentials. Some topic example scripts do not explicitly pass these
credentials in their connection parameters; if a script cannot authenticate,
set its connection credentials to match the broker configuration.

## Consistent-hash exchange

The `consistent-hash-exchange/` example uses RabbitMQ's
`rabbitmq_consistent_hash_exchange` plugin. Enable the plugin on the running
RabbitMQ container:

```bash
docker exec rabbitmq rabbitmq-plugins enable rabbitmq_consistent_hash_exchange
```

The plugin must be installed in the RabbitMQ image before it can be enabled. If
the command reports that the plugin is unknown, use a RabbitMQ image that
includes the plugin or install the matching plugin version for your broker.
Restart RabbitMQ after enabling the plugin if prompted.

The example declares an `x-consistent-hash` exchange named `samplehashing` and
binds two queues, `letterbox1` and `letterbox2`, with binding key `1` (equal
weight). The producer's routing key is hashed by the exchange to choose a
queue; it is not an ordinary exact-match routing key. To try it, first start
the consumer:

```bash
python consistent-hash-exchange/consumer.py
```

Then, in another terminal, publish a message:

```bash
python consistent-hash-exchange/producer.py
```

## Exchange-to-exchange bindings

The `exchange-exchange/` example binds `secondexchange` (a fanout exchange) to
`firstexchange` (a direct exchange). The producer publishes to
`firstexchange` with an empty routing key; the exchange binding forwards the
message to `secondexchange`, which broadcasts it to queues bound to it. The
consumer declares the `letterbox` queue and binds it to `secondexchange`.

Start the consumer, then run the producer in another terminal:

```bash
python exchange-exchange/consumer.py
python exchange-exchange/producer.py
```

## Header exchange

The `header-exchange/` example routes messages by their headers rather than
their routing key. The consumer binds `letterbox` to `headersexchange` with
`x-match: any`, `name: brian`, and `age: 21`. With `any`, a message is delivered
when at least one of the listed header values matches. The producer sends the
`name: brian` header, so the message matches the binding.

Start the consumer, then publish the message:

```bash
python header-exchange/consumer.py
python header-exchange/producer.py
```

## Notes

- This example is intentionally simple and educational
- The queue name used throughout is `letterbox`
- Run the consumer before or while publishing messages if you want to observe live processing
- You can inspect the queue and message flow in the RabbitMQ Management UI at http://localhost:15672

## Useful commands

Check the queue and broker status in the management UI:

```bash
http://localhost:15672
```

Stop the services:

```bash
docker compose down
```

## Summary

This repository is a minimal RabbitMQ example for learning queue-based communication in Python. It shows how to publish messages, consume them, and process them reliably with acknowledgements in a basic producer/consumer pattern.
