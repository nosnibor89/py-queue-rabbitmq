import pika

_exchange_name = 'payment_purchase_topic'
_card_payment_queue_name = '_card_payment_queue_name'

_payment_card_r_key = 'payment.card'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=_exchange_name, exchange_type='topic')

result = channel.queue_declare(_card_payment_queue_name)

channel.queue_bind(
    exchange=_exchange_name, queue=_card_payment_queue_name, routing_key=_payment_card_r_key)


def callback(ch, method, properties, body):
    print(" [x] We have receive a card payment: (%r - %r)" % (method.routing_key, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=_card_payment_queue_name, on_message_callback=callback)

channel.start_consuming()
