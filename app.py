import atexit
import json

from flask import Flask, jsonify, request

from queue import QueueClient
from model import Payment, PurchaseOder

app = Flask(__name__)

app_queue = QueueClient()

atexit.register(lambda: app_queue.close())


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/purchase-order', methods=['POST'])
def send_purchase_order():
    data = request.get_json()
    purchase_order = PurchaseOder(data['poNumber'], data['amountToPay'], data['companyName'])
    app_queue.send_purchase(json.dumps(purchase_order.__dict__))
    return jsonify(purchase_order.__dict__)


@app.route('/queue-card-payment', methods=['POST'])
def queue_card_payment():
    data = request.get_json()
    card_payment = Payment(data['name'], data['amount'], data['cardnumber'])
    app_queue.send_payment(json.dumps(card_payment.__dict__))
    return jsonify(card_payment.__dict__)


@app.route('/direct-card-payment', methods=['POST'])
def send_card_payment():
    card_payment = request.get_json()
    return jsonify(card_payment)
