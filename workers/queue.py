import pika


def init_topic_channel(exchange, queue, routing_key, host_name='localhost'):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host_name))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='topic')
    channel.queue_declare(queue)

    channel.queue_bind(
        exchange=exchange, queue=queue, routing_key=routing_key)

    return channel
