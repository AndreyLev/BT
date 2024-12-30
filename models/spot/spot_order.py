from dataclasses import dataclass, field
from itertools import count
from app.models.spot.account import Account

id_counter = count(1)

@dataclass
class Order:
    acc: Account
    status: str
    id: int = field(default_factory=lambda: next(id_counter))

@dataclass
class MarketOrder:
    direction: str
    quantity: float
    execution_price: float = None
    base_balance_change: float = None
    quote_balance_change: float = None
    quote_fee: float = None

@dataclass
class LimitOrder:
    direction: str
    quantity: float
    limit_price: float
    execution_price: float = None
    reserved_base: float = None
    reserved_quote: float = None

    base_balance_change: float = None
    quote_balance_change: float = None
    quote_fee: float = None




