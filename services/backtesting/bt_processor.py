from app.database.models.datasource import DataSource
from app.models.backtesting.strategy import Strategy
from app.services.broker.spot.service import SpotService
from app.api.spot_api import SpotAPI
from app.models.spot.account import Account

class BTProcessor:
    def __init__(self, datasource: DataSource, strategy: Strategy, initial_balance: float = 0.0, market_type: str = 'SPOT'):
        self._datasource = datasource
        self._strategy: Strategy = strategy
        self._api = None
        if initial_balance == 0.0:
            initial_balance = 10000.0
        if market_type == "SPOT":
            account = Account(quote_balance=initial_balance)
            service = SpotService(account=account)
            self._api = SpotAPI(service)
        elif market_type == "FUTURES":
            self._api = None
        self._strategy.__bind__api__(self._api)

    def __calculate_dynamic_candles__(self, data: dict) -> list:
        DynamicCandle = type('DynamicCandle', (object,), {})
        candles = []
        for candle_index in range(len(next(iter(data.values())))):
            # преобразовать в свечу
            candle = DynamicCandle()
            for key in data:
                setattr(candle, key, data[key][candle_index])
            candles.append(candle)
        return candles

    def validate_data(self):
        if not self._datasource:
            raise ValueError("Источник данных не установлен")
        if not self._strategy:
            raise ValueError("Стратегия не установлена")

    def run_backtest(self):
        self.validate_data()
        ohlcv_data = self._datasource.get_ohlcv_data()
        self._strategy.__bind_data__(ohlcv_data)
        self._strategy.__prepare_data__()
        candles = self.__calculate_dynamic_candles__(ohlcv_data)
        for candle_index in range(len(candles)):
            candle = candles[candle_index]
            print(candle.close)
            # прибытие новой свечи
            # разослать подписчикам
