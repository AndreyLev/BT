from app.services.broker.spot.service import SpotService

class SpotAPI:
    def __init__(self, service: SpotService):
        self._service = service
    def place_market_order(self, direction: str, quantity: float):
        self._service.place_market_order(direction=direction,quantity=quantity)

    def place_limit_order(self, direction: str, quantity: float, limit_price: float):
        self._service.place_limit_order(direction=direction,quantity=quantity,limit_price=limit_price)

    def get_base_balance(self) -> float:
        return self._service.get_base_balance()

    def get_quote_balance(self) -> float:
        return self._service.get_quote_balance()