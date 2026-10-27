import math
from dataclasses import dataclass
from typing import Literal


@dataclass
class Order:
    order_id: int
    side: Literal["BUY", "SELL"]
    price: float
    quantity: int
    symbol: str = "CMX/USD"

    def __post_init__(self):
        if type(self.order_id) is not int:
            raise ValueError("Order ID must be an integer")

        if self.order_id <= 0:
            raise ValueError("Order ID must be positive")

        if self.side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")

        if type(self.price) not in (int, float):
            raise ValueError("Price must be a number")

        if not math.isfinite(self.price) or self.price <= 0:
            raise ValueError("Price must be finite and positive")

        if type(self.quantity) is not int:
            raise ValueError("Quantity must be an integer")

        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

        if not isinstance(self.symbol, str) or not self.symbol.strip():
            raise ValueError("Symbol must be a non-empty string")

        self.symbol = self.symbol.strip().upper()