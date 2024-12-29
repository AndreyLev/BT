class DataSource:
    def get_data(self):
        pass

class Strategy:
    def __prepare_data__(self, data: dict[str, object]):
        pass

    def place_market_order(self):
        pass

    def on_next_bar(self, index, bar):
        pass
