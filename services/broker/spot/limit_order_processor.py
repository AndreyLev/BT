from app.models.spot.spot_order import LimitOrder
from app.models.spot.account import Account
from app.models.spot.order_book import OrderBook


class LimitOrderProcessor:
    def __init__(self):
        self._order_book = OrderBook(self)

    def validate_order(self, order: LimitOrder):
        account : Account = order.account
        # todo: получить текущую цену
        curr_price = None

        if order.direction == "BUY":

            if order.limit_price >= curr_price:
                raise ValueError("Limit price >= curr_price")

            if account.quote_balance < order.quantity:
                raise ValueError("Недостаточно средств")

        elif order.direction == "SELL":

            if order.limit_price <= curr_price:
                raise ValueError("Limit price <= curr_price")

            if account.base_balance < order.quantity:
                return ValueError("Недостаточно средств")

        return True

    def reserve_balances(self, order: LimitOrder):
        account: Account = order.account
        if order.direction == "BUY":
            order.reserved_quote = order.quantity
            account.quote_balance -= order.quantity
        elif order.direction == "SELL":
            order.reserved_base = order.quantity
            account.base_balance -= order.quantity

    def calculate_fee(self, order: LimitOrder):
        account: Account = order.account
        if order.direction == "BUY":
            order.quote_fee = order.quantity * account.maker_fee
        elif order.direction == "SELL":
            order.quote_fee = (order.quantity * order.execution_price) * account.maker_fee

    def calculate_active_balances(self, order: LimitOrder):
        base_change, quote_change = 0.0, 0.0
        if order.direction == "BUY":
            quote_trade_sum = order.quantity - order.quote_fee
            base_change = quote_trade_sum / order.execution_price
            quote_change = order.quantity
        elif order.direction == "SELL":
            base_change = order.quantity
            quote_change = order.quantity * order.execution_price - order.quote_fee
        order.base_balance_change = base_change
        order.quote_balance_change = quote_change

    def update_user_balance(self, order: LimitOrder):
        account: Account = order.account
        if order.direction == "BUY":
            account.base_balance += order.base_balance_change
            account.quote_balance -= order.quote_balance_change
        elif order.direction == "SELL":
            account.base_balance -= order.base_balance_change
            account.quote_balance += order.quote_balance_change

    def execute_order(self, order: LimitOrder):
        account: Account = order.account
        # исполнение ордера по лимитной цене
        order.execution_price = order.limit_price
        self.calculate_fee(order, account)
        self.calculate_active_balances(order)
        self.update_user_balance(order, account)
        order.status = 'filled'

    def process_order(self, order: LimitOrder):
        self.validate_order(order)
        self.reserve_balances(order)
        self._order_book.push(order)
