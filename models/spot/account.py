from dataclasses import dataclass


@dataclass
class Account:
    base_balance: float = 0.0
    quote_balance: float = 0.0
    taker_fee: float = 0.075 / 100.0
    maker_fee: float = 0.04 / 100.0
