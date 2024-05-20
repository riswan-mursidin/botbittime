import requests
import time
import hmac
import hashlib

BASE_URL = "https://api.bittime.com"
API_KEY = "31659620dd5aad2967b005dc2ed50daa3080e1ecae6101194dbc5eb96309c80a"
SECRET_KEY = "d16661def613d4c350592e945ba40324471c9c68fe3ad1bdd1da1c07a5c39da6"

def create_signature(query_string, secret_key):
    return hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def get_order_book(symbol, limit=100):
    url = f"{BASE_URL}/api/v1/depth"
    params = {'symbol': symbol, 'limit': limit}
    response = requests.get(url, params=params)
    return response.json()

def place_order(symbol, side, quantity, price):
    url = f"{BASE_URL}/api/v1/order"
    timestamp = int(time.time() * 1000)
    query_string = f"symbol={symbol}&side={side}&type=LIMIT&quantity={quantity}&price={price}&timeInForce=GTC&timestamp={timestamp}"
    signature = create_signature(query_string, SECRET_KEY)

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    params = {
        'symbol': symbol,
        'side': side,
        'type': 'LIMIT',
        'quantity': quantity,
        'price': price,
        'timeInForce': 'GTC',
        'timestamp': timestamp,
        'signature': signature
    }

    response = requests.post(url, headers=headers, params=params)
    return response.json()

def main():
    symbol = "CUANIDR"

    while True:
        order_book = get_order_book(symbol)
        bids = order_book['bids']
        asks = order_book['asks']

        best_bid = float(bids[0][0])
        best_ask = float(asks[0][0])

        # Beli di best bid dan jual di best ask menggunakan harga pasar real-time
        place_order(symbol, "BUY", 1, best_bid)
        place_order(symbol, "SELL", 1, best_ask)

        time.sleep(10)

if __name__ == "__main__":
    main()