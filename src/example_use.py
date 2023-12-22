import json
import uuid
import random

from src.queue import RabbitQueue
from loguru import logger


def predict_data(data: any):
    # обрабатываем данные как необходимо

    list_example = [data]
    rabbit_queue = RabbitQueue()
    name_queue = "any_lalal_queue"

    rabbit_queue.add_message_queue(name_queue, name_queue, list_example)
    # обработали данные и положили их в другую очередь если необходимо


class RabbitCallback(RabbitQueue):
    @staticmethod
    def callback(ch, method, properties, body) -> None:
        message = body.decode("utf-8")
        message_content = json.loads(message)
        logger.info(message_content)

        predict_data(message_content)

    def fetch_messages(self, name_queue: str) -> None:
        self.channel.queue_declare(queue=name_queue)
        self.channel.basic_consume(queue=name_queue, on_message_callback=self.callback, auto_ack=True)

        logger.info("Waiting messages")
        self.channel.start_consuming()


def run_example_1():
    rabbit_queue = RabbitCallback()
    name_queue = "input_stream_data"

    event_game = ['break', "jump", 'shot']
    for _ in range(100):
        game_content = {
            'id': str(uuid.uuid4()),
            'event': random.choice(event_game)
        }

        rabbit_queue.add_message_queue(name_queue, name_queue, game_content)


def run_example_2():
    rabbit_queue = RabbitCallback()
    name_queue = "input_stream_data"

    event_game = ['break', "jump", 'shot']
    for _ in range(100):
        game_content = {
            'id': str(uuid.uuid4()),
            'event': random.choice(event_game)
        }

        rabbit_queue.add_message_queue(name_queue, name_queue, game_content)

    if rabbit_queue.get_count_messages(name_queue) != 0:
        messages = rabbit_queue.check_queue(name_queue)
        logger.info(messages)


def run_example_3():
    rabbit_queue = RabbitCallback()
    name_queue = "input_stream_data"

    event_game = ['break', "jump", 'shot']
    for _ in range(100):
        game_content = {
            'id': str(uuid.uuid4()),
            'event': random.choice(event_game)
        }

        rabbit_queue.add_message_queue(name_queue, name_queue, game_content)

    rabbit_queue.fetch_messages(name_queue)


def run_example_4():
    rabbit_queue = RabbitCallback()
    name_queue = "input_stream_data"

    rabbit_queue.fetch_messages(name_queue)


if __name__ == "__main__":
    run_example_1()  # просто кладем данные в названную очередь
    run_example_2()  # кладем данные в очередь, проверяем не пустая ли очередь и получаем выходные данные в виде списка
    run_example_3()  # кладем данные в очередь, запускаем callback manager на прослушку
    run_example_4()  # запускаем callback manager отдельно
