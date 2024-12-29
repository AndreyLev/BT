from app.database.models.datasource import DataSource
from app.models.backtesting.strategy import Strategy

class BTProcessor:
    # добавить источник данных
    # добавить стратегию
    # базовая мысль следующая:
    # источник данных выдает словарь со свечами
    # в стратегии добавляются необходимые индикаторы
    # далее происходят вычисления на каждой свече
    # агент собирает статистику

    # источниками данных могут быть
    # postgres sql, exchanges(напр. binance, bybit и т.д.)
    # csv, txt
    # datasource это singleton, который один раз считывает данных
    # и возвращает их в виде словаря со значениями ohlcv
    def __init__(self, datasource: DataSource, strategy: Strategy):
        self._datasource = datasource
        self._strategy = strategy

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
        candles = self.__calculate_dynamic_candles__()
        for candle_index in range(len(candles)):
            candle = candles[candle_index]
            # прибытие новой свечи
            # разослать подписчикам
