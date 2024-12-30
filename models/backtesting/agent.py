from dataclasses import dataclass

@dataclass
class Agent:
    net_profit: float = 0.0
    max_drawdown: float = 0.0
    total_closed_trades: int = 0
    percent_profitable: float = 0.0
    profit_factor: float = 0.0
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0