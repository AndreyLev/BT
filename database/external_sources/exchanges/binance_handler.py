import ccxt
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Binance:
    def __init__(self):
        self._exchange = ccxt.binance({
            'enableRateLimit': True
        })

    def fetch_ohlcv_data(self, symbol, timeframe, start_date, end_date=None):
        if end_date is None:
            end_date = datetime.now()

        start_timestamp = int(start_date.timestamp() * 1000)
        end_timestamp = int(end_date.timestamp() * 1000)

        all_candles = []
        current_timestamp = start_timestamp

        while current_timestamp <= end_timestamp:
            try:
                candles = self._exchange.fetch_ohlcv(
                    symbol=symbol,
                    timeframe=timeframe,
                    since=current_timestamp,
                    limit=1000
                )

                if not candles:
                    break

                all_candles.extend(candles)

                current_timestamp = candles[-1][0] + 1
            except Exception as e:
                print(f'Ошибка при получении данных: {e}')
                break

        df = pd.DataFrame(
            all_candles,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df


# тест
binance = Binance()
end_date = datetime.now()
start_date = end_date - relativedelta(months=12)
print(binance.fetch_ohlcv_data("ETHUSDT", '1d', start_date, end_date))
