import yfinance as yf
from abc import ABC, abstractmethod

# 1. The Abstract Base Class (Blueprint)
# This MUST come before any class that uses it.
class MarketDataProvider(ABC):
    @abstractmethod
    def get_realtime_price(self, symbol: str) -> float:
        pass

    @abstractmethod
    def validate_symbol(self, symbol: str) -> bool:
        pass

# 2. The Concrete Implementation
class YFinanceProvider(MarketDataProvider):
    def get_realtime_price(self, symbol: str) -> float:
        try:
            ticker = yf.Ticker(symbol)
            # Try fast access first
            price = ticker.fast_info['last_price']
            return float(price)
        except (KeyError, TypeError):
            # Fallback to history if fast_info fails
            history = ticker.history(period="1d")
            if not history.empty:
                return history['Close'].iloc[-1]
            raise ValueError(f"Price unavailable for {symbol}")

    def validate_symbol(self, symbol: str) -> bool:
        try:
            ticker = yf.Ticker(symbol)
            _ = ticker.fast_info['timezone']
            return True
        except:
            return False