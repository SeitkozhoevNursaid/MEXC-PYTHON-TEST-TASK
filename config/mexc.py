import hashlib
import json
import time
import requests


def md5(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()


def mexc_crypto(key, obj):
    date_now = str(int(time.time() * 1000))
    g = md5(key + date_now)[7:]
    s = json.dumps(obj, separators=(',', ':'))
    sign = md5(date_now + s + g)
    return {'time': date_now, 'sign': sign}


def place_order(key, obj, url):
    signature = mexc_crypto(key, obj)
    headers = {
        'Content-Type': 'application/json',
        'x-mxc-sign': signature['sign'],
        'x-mxc-nonce': signature['time'],
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'Authorization': key
    }
    response = requests.post(url, headers=headers, json=obj)
    return response.json()


def place_order_with_log(key, order_obj, url):
    """Создаёт ордер и печатает результат"""
    response = place_order(key, order_obj, url)
    if response.get('success'):
        print(f"Ордер успешно создан на аккаунте {key[:5]}...: {response}")
    else:
        print(f"Ошибка создания ордера на аккаунте {key[:5]}...: {response}")
    return response
