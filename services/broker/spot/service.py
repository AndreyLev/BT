from app.services.broker.spot.limit_order_processor import LimitOrderProcessor
from app.services.broker.spot.market_order_processor import MarketOrderProcessor
import app.models.spot.spot_order as orders
from app.models.spot.account import Account

class SpotService:
    def __init__(self, account: Account):
        self._market_order_processor = MarketOrderProcessor()
        self._limit_order_processor = LimitOrderProcessor()
        self._account = account

    def place_market_order(self, direction: str, quantity: float):
        order: orders.MarketOrder = orders.MarketOrder(direction=direction,quantity=quantity)
        order.account = self._account
        self._market_order_processor.process_order(order)

    def place_limit_order(self, direction: str, quantity: float, limit_price: float):
        order: orders.LimitOrder = orders.LimitOrder(
            direction=direction,quantity=quantity,limit_price=limit_price)
        order.account = self._account
        self._limit_order_processor.process_order(order)

    def get_base_balance(self) -> float:
        return self._account.base_balance

    def get_quote_balance(self) -> float:
        return self._account.quote_balance
