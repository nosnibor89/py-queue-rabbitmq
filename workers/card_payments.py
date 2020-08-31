from workers.queue import init_topic_channel

_exchange_name = 'payment_purchase_topic'
_card_payment_queue_name = '_card_payment_queue_name'
_payment_card_r_key = 'payment.card'

channel = init_topic_channel(_exchange_name, _card_payment_queue_name, _payment_card_r_key)


def callback(ch, method, properties, body):
    print(" [x] We have receive a card payment: (%r - %r)" % (method.routing_key, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=_card_payment_queue_name, on_message_callback=callback)

channel.start_consuming()
