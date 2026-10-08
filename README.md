# RabbitMQ Producer/Consumer Example

This project demonstrates a simple RabbitMQ message flow using Python and Docker. It includes a producer that sends messages into a queue and a consumer that receives, processes, and acknowledges each message.

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
