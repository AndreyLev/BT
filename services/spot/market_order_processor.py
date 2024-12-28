from app.models.spot.spot_order import MarketOrder
from app.models.spot.account import Account


class MarketOrderProcessor:
    def has_sufficient_funds(self, order: MarketOrder, account: Account) -> bool:
        if order.direction == "BUY":
            if account.quote_balance < order.quantity:
                return False
        elif order.direction == "SELL":
            if account.base_balance < order.quantity:
                return False
        return True

    def validate_order(self, order: MarketOrder, account: Account):
        if self.has_sufficient_funds(order, account):
            raise ValueError("Недостаточно средств для выполнения ордера")

    def process_order(self, order: MarketOrder, account: Account):
        self.validate_order(order, account)
        self.execute_order(order, account)

    def calculate_fee(self, order: MarketOrder, account: Account):
        if order.direction == "BUY":
            order.quote_fee = order.quantity * account.taker_fee
        elif order.direction == "SELL":
            order.quote_fee = (order.quantity * order.execution_price) * account.taker_fee

    def calculate_active_balances(self, order: MarketOrder):
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

    def update_user_balance(self, order: MarketOrder, account: Account):
        if order.direction == "BUY":
            account.base_balance += order.base_balance_change
            account.quote_balance -= order.quote_balance_change
        elif order.direction == "SELL":
            account.base_balance -= order.base_balance_change
            account.quote_balance += order.quote_balance_change

    def execute_order(self, order: MarketOrder, account: Account):
        # исполнение ордера по текущей рыночной цене
        # todo: написать получение текущей цены
        curr_price = None
        order.execution_price = curr_price
        self.calculate_fee(order, account)
        self.calculate_active_balances(order)
        self.update_user_balance(order, account)
        order.status = 'filled'
