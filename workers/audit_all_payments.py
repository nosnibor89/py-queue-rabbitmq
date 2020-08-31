from workers.queue import init_topic_channel

_exchange_name = 'payment_purchase_topic'
_all_queue_name = '_all_queue_name'

channel = init_topic_channel(_exchange_name, _all_queue_name, 'payment.*')


def callback(ch, method, properties, body):
    print(" [x] We have receive a payment: (%r - %r)" % (method.routing_key, body))


channel.basic_consume(
    queue=_all_queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
