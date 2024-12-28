from functools import cmp_to_key

from app.models.spot.spot_order import LimitOrder
from app.models.spot.account import Account
from app.services.spot.limit_order_processor import LimitOrderProcessor

def bids_comparator(o1, o2):
    if o1.limit_price == o2.limit_price:
        return o2.id - o1.id
    return o1.limit_price - o2.limit_price

def asks_comparator(o1, o2):
    if o1.limit_price == o2.limit_price:
        return o1.id - o2.id
    return o1.limit_price - o2.limit_price

class OrderBook:
    def __init__(self, limit_order_processor: LimitOrderProcessor, account: Account):
        self._processor = limit_order_processor
        self._account = account
        self._bids = []
        self._asks = []

    def push(self, order: LimitOrder):
        if order.direction == "BUY":
            self._bids.append(order)
        elif order.direction == "SELL":
            self._asks.append(order)

    def on_bar_calculated(self, bar):
        # отсортировать биды и аски
        self._bids = sorted(self._bids, key=cmp_to_key(bids_comparator))
        self._asks = sorted(self._asks, key=cmp_to_key(asks_comparator))
        # по bids проход из конца в начало
        # по asks из начала в конец
        for bid in self._bids[::-1]:
            if bar.close < bid.limit_price:
                self._processor.execute_order(bid, self._account)

        for ask in self._asks:
            if bar.close > ask.limit_price:
                self._processor.execute_order(ask, self._account)
