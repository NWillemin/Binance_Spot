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
    trades = client.get_my_trades(symbol=symbol)
    last_trade = trades[-1]
    trade_value_usdt = float(last_trade['qty']) * float(last_trade['price'])
    price_info = client.get_symbol_ticker(symbol=symbol)
    price = float(price_info['price'])
    quantity = round(allocation / price, 4)


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
            quantity=float(last_trade['qty'])
        )
        return jsonify({'message': 'Sell order placed', 'order': order})

    return jsonify({'message': 'Invalid action'})

