"""Generic way to send a RabbitMQ message."""

# Python modules
import json
import os

# 3rd Party libraries
import pika
from dotenv import load_dotenv

current_directory = os.getcwd()
dotenv_path = os.path.join(current_directory, '.env')

load_dotenv(dotenv_path)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_VIRTUAL_HOST = os.getenv("RABBITMQ_VIRTUAL_HOST")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

RABBITMQ_EXCHANGE_PARSER_QUEUE = os.getenv("RABBITMQ_EXCHANGE_PARSER_QUEUE")

def send_message(body, routing_key="") -> bool:
    """Send a message to RabbitMQ."""
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host=RABBITMQ_VIRTUAL_HOST,
        credentials=credentials,
        connection_attempts=5,
        retry_delay=1,
    )

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE_PARSER_QUEUE, routing_key=routing_key, body=json.dumps(body)
        )

        connection.close()

        return True
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error sending message to {RABBITMQ_EXCHANGE_PARSER_QUEUE}")

    return False
