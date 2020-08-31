from workers.queue import init_topic_channel

_exchange_name = 'payment_purchase_topic'
_purchase_order_queue_name = '_purchase_order_queue_name'
_purchase_order_r_key = 'payment.purchase'

channel = init_topic_channel(_exchange_name, _purchase_order_queue_name, _purchase_order_r_key)


def callback(ch, method, properties, body):
    print(" [x] We have receive a purchase order: (%r - %r)" % (method.routing_key, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=_purchase_order_queue_name, on_message_callback=callback)

channel.start_consuming()
