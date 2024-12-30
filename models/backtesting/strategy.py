class Strategy:
    def __bind__api__(self, api):
        self.api = api
    def __bind_data__(self, data):
        self.data = data

    def __prepare_data__(self):
        pass

    def on_next_candle(self, index, candle):
        pass