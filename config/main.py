import threading
from pymexc import futures

from mexc import place_order_with_log
from constants import MASTER_ACCOUNT, COPIER_ACCOUNTS, CREATE_ORDER_URL


processed_orders = set()


def handle_master_order(msg):
    """
    Этот колбэк вызывается при создании нового ордера на основном аккаунте
    """

    data = msg.get('data')
    order_id = data.get('orderId')
    channel = msg.get('channel')
    if not data:
        return

    if channel != "push.personal.order" and channel != "push.personal.order.deal":
        print(f"Игнорируем событие {channel}")
        return

    print("Открылся ордер на основном аккаунте детальная информация:", msg)

    if order_id in processed_orders:
        return
    processed_orders.add(order_id)

    symbol = data.get('symbol')
    side = 1 if data.get('side') == "buy" else 2
    vol = float(data.get('vol', 1))
    price = float(data.get('price', 0))
    leverage = int(data.get('leverage', 5))

    order_obj = {
        "symbol": symbol,
        "side": side,
        "openType": 1,
        "type": 1,
        "vol": vol,
        "leverage": leverage,
        "price": price,
    }

    for acc in COPIER_ACCOUNTS:
        threading.Thread(target=place_order_with_log, args=(acc['api_key'], order_obj, CREATE_ORDER_URL)).start()


def run_master_ws():
    """
    Подключение по протоколу websocket к основному аккаунту для отслеживания открытия ордеров
    """
    futures.WebSocket(
        api_key=MASTER_ACCOUNT['api_key'],
        api_secret=MASTER_ACCOUNT['api_secret'],
        personal_callback=handle_master_order,
    )
    print("Подключено к WS мастера, слушаем новые ордера...")

    threading.Event().wait()


if __name__ == "__main__":
    run_master_ws()
