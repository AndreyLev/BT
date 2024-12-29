from app.models.backtesting.engine import DataSource, Strategy

class BTProcessor:
    # данные будут из postgres

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

    def run_backtest(self):
        pass

