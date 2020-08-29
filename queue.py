import pika

_exchange_name = 'payment_purchase_topic'
_purchase_order_queue_name = '_purchase_order_queue_name'
_card_payment_queue_name = '_card_payment_queue_name'
_all_queue_name = '_all_queue_name'

_payment_card_r_key = 'payment.card'
_purchase_order_r_key = 'payment.purchase'


class QueueClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        # Declare Queue platform
        self.channel.exchange_declare(exchange=_exchange_name, exchange_type='topic')
        self.channel.queue_declare(_purchase_order_queue_name)
        self.channel.queue_declare(_card_payment_queue_name)
        self.channel.queue_declare(_all_queue_name)

        # Bind queue platform
        self.channel.queue_bind(
            exchange=_exchange_name, queue=_purchase_order_queue_name, routing_key=_purchase_order_r_key)
        self.channel.queue_bind(
            exchange=_exchange_name, queue=_card_payment_queue_name, routing_key=_payment_card_r_key)
        self.channel.queue_bind(
            exchange=_exchange_name, queue=_all_queue_name, routing_key='payment.*')

    def send_payment(self, payment: str):
        self.channel.basic_publish(
            exchange=_exchange_name, routing_key=_payment_card_r_key, body=payment
        )

    def send_purchase(self, purchase: str):
        self.channel.basic_publish(
            exchange=_exchange_name, routing_key=_purchase_order_r_key, body=purchase
        )

    def close(self):
        self.connection.close()
