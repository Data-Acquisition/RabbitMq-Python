# Использование и Работа с RabbitMQ в питоне

- поднятие rabbitmq в докер

`docker run -p 5672:5672 -p 15672:15672 -d --restart always rabbitmq:3.10.7-management
`

- /src/queue - основной класс для работы с очередями
- /src/example_use - рабочие примеры как можно использовать очереди в работе
