from flask import Flask, request, jsonify
from binance.client import Client
import time
import hmac
import hashlib
import requests

app = Flask(__name__)

# Binance API keys
API_KEY = "NNaai2QQeFzftcWSicIzTmSBtVW7kVaW0W9zr5DKx4kWAT0luyM71pHF0wwJWlaa"
API_SECRET = "ZtEk57bRIaeTEQK5i15MKkLvvBBUpE1jVqAzzMDb1ZPSjjGTgqqcyn9B4GdZNBbT"

client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Webhook received: {data}")
    
    symbol = data['ticker']
    action = data['action']
    quantity = data['quantity']
    # Example: Fixed $300 per trade
    usdt_amount = 300



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
