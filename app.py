from flask import Flask, request, jsonify
from binance.client import Client
import time
import hmac
import hashlib
import requests
import os

app = Flask(__name__)

# Binance API keys
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Webhook received: {data}")
    
    symbol = data['ticker']
    action = data['action']
    quantity = data['quantity']



    if action == 'BUY':
        order = client.create_order(
            symbol=symbol,
            side='BUY',
            type='MARKET',
            quantity=quantity
        )
        return jsonify({'message': 'Buy order placed', 'order': order})

    if action == 'SELL':
        order = client.create_order(
            symbol=symbol,
            side='SELL',
            type='MARKET',
            quantity=quantity
        )
        return jsonify({'message': 'Sell order placed', 'order': order})

    return jsonify({'message': 'Invalid action'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
