# Использование и Работа с RabbitMQ в питоне

- поднятие rabbitmq в докер

`docker run -d --name my-rabbit -p 5672:5672 -p 15672:15672 rabbitmq
`

- /src/queue - основной класс для работы с очередями
- /src/example_use - рабочие примеры как можно использовать очереди в работе