from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
SERVER_URLS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}

auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE5NDgwNTA0LCJpYXQiOjE3MTk0ODAyMDQsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjE2MzI5ZTJkLTMzODMtNGRlMy04YWEyLWQ0ZTc5ZGY0ODU4OSIsInN1YiI6InByYXRlZWsyMDIxY3NkczA4OEBhYmVzaXQuZWR1LmluIn0sImNvbXBhbnlOYW1lIjoiUGF0cmljayIsImNsaWVudElEIjoiMTYzMjllMmQtMzM4My00ZGUzLThhYTItZDRlNzlkZjQ4NTg5IiwiY2xpZW50U2VjcmV0IjoiS1dhWU9teWZmdHpCRW11USIsIm93bmVyTmFtZSI6IlByYXRlZWsgU2luaGEiLCJvd25lckVtYWlsIjoicHJhdGVlazIwMjFjc2RzMDg4QGFiZXNpdC5lZHUuaW4iLCJyb2xsTm8iOiIyMTAyOTAxNTQwMDgwIn0.xKDA4J-MQtO41wQRqh1BN32Qal6SOKSlsXyqSDZRqDo'
headers = {
    'Authorization': f'Bearer {auth_token}'
}

numbers_storage = []

def fetch_numbers(numberid):
    if numberid not in SERVER_URLS:
        return []
    response = requests.get(SERVER_URLS[numberid], timeout=0.5)
    if response.status_code == 200:
        return response.json().get('numbers', [])
    return []

@app.route('/numbers/<numberid>', methods=['GET'])
def get_numbers(numberid):
    global numbers_storage
    fetched_numbers = fetch_numbers(numberid)
    if not fetched_numbers:
        return jsonify({'error': 'Failed to fetch numbers'}), 500

    # Ensure uniqueness
    numbers_storage = list(set(numbers_storage + fetched_numbers))

    # Maintain window size
    if len(numbers_storage) > WINDOW_SIZE:
        numbers_storage = numbers_storage[-WINDOW_SIZE:]

    avg = sum(numbers_storage) / len(numbers_storage)

    response = {
        'windowPrevState': numbers_storage[:-len(fetched_numbers)] if len(numbers_storage) > len(fetched_numbers) else [],
        'windowCurrState': numbers_storage,
        'numbers': fetched_numbers,
        'avg': round(avg, 2)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=9876)
