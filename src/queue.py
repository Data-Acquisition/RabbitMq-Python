from __future__ import annotations
import json
import time

import pika
from loguru import logger


class RabbitQueue:
    def __init__(self) -> None:
        max_retries = 5
        retries = 0

        while retries < max_retries:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters("localhost"),
                )
                self.channel = self.connection.channel()
                break
            except Exception as e:
                retries += 1
                logger.error(f"Failed to connect to RabbitMQ: {e}")
                if retries < max_retries:
                    logger.warning("Retrying connection in 5 seconds...")
                    time.sleep(5)
                else:
                    logger.error("Max connection retries reached. Exiting.")
                    raise

    def start_connection_queue(self, name_queue: str) -> None:
        self.channel.queue_declare(queue=name_queue)

    def stop_connection_queue(self) -> None:
        self.connection.close()

    def get_count_messages(self, name_queue: str) -> int:
        queue_declare_result = self.channel.queue_declare(queue=name_queue)
        return queue_declare_result.method.message_count

    def add_message_queue(self, name_queue: str, key: str, message_queue: any) -> None:
        self.start_connection_queue(name_queue)

        if isinstance(message_queue, (list, dict)):
            message_queue = json.dumps(message_queue)

        self.channel.basic_publish(exchange="", routing_key=key, body=message_queue)

    def check_queue(self, name_queue: str) -> list[dict] | None:
        self.start_connection_queue(name_queue)
        queue_messages = []
        while True:
            method_frame, header_frame, body = self.channel.basic_get(queue=name_queue)

            if method_frame:
                decoded_body = body.decode("utf-8")
                queue_messages.append(json.loads(decoded_body))

                self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            else:
                break

        if queue_messages:
            return queue_messages
        else:
            return None
