from flask import Flask, request, jsonify
from binance.client import Client
import time
import hmac
import hashlib
import requests
import os
import math
app = Flask(__name__)

# Binance API keys
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
client = Client(API_KEY, API_SECRET)
position_thresholds = {
    'BTC': 0.00003,
    'ETH': 0.002,
    'SOL': 0.01,
    'AVAX': 0.1,
    'ADA': 1.0,
    'XRP': 1.0,
    'DOT': 0.5
}
tracked_assets = ['BTC', 'ETH', 'DOT', 'SOL', 'AVAX', 'ADA', 'XRP']
def format_quantity(quantity, step_size):
    precision = abs(int(round(math.log10(step_size))))
    rounded_qty = math.floor(quantity / step_size) * step_size
    return f"{rounded_qty:.{precision}f}"
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Webhook received: {data}")
    
    symbol = data['ticker']
    action = data['action']
    # Get all balances from Binance
    account_info = client.get_account(recvWindow=10000)
    all_balances = account_info['balances']
    usdt_balance = next((float(balance['free']) for balance in all_balances if balance['asset'] == 'USDT'), 0)

    # Extract balances for your tracked assets
    filtered_balances = {balance['asset']: float(balance['free']) for balance in all_balances if balance['asset'] in tracked_assets}
    
    remaining_assets = [asset for asset, qty in filtered_balances.items() if qty < position_thresholds[asset]]

    if action == 'BUY':
        if len(remaining_assets) == 0:
            return jsonify({'message': 'No assets remaining to buy'}), 400
        quantity_buy = usdt_balance / len(remaining_assets)
        order = client.create_order(
            symbol=symbol,
            side='BUY',
            type='MARKET',
            quoteOrderQty=quantity_buy,
            recvWindow=10000
        )
        return jsonify({'message': 'Buy order placed', 'order': order})

    if action == 'SELL':
        asset = symbol.replace('USDT', '')
        if asset not in filtered_balances or filtered_balances[asset] <= 0:
            return jsonify({'message': f'Error: No balance found for {asset} or balance is zero.'}), 400
        quantity_sell = filtered_balances[asset]
        symbol_info = client.get_symbol_info(symbol)
        step_size = float([f['stepSize'] for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'][0])

        formatted_quantity = format_quantity(quantity_sell, step_size)
        order = client.create_order(
            symbol=symbol,
            side='SELL',
            type='MARKET',
            quantity=formatted_quantity,
            recvWindow=10000
        )
        return jsonify({'message': 'Sell order placed', 'order': order})

    return jsonify({'message': 'Invalid action'}), 400


