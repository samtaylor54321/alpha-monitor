from __future__ import annotations

from datetime import date
from typing import Optional

import pandas as pd
import yfinance as yf


class YahooFinanceDataSource:
    def get_prices(
        self,
        symbol: str,
        start: Optional[date] = None,
        end: Optional[date] = None,
        interval: str = "1d",
    ) -> pd.DataFrame:
        ticker = yf.Ticker(symbol)

        df = ticker.history(
            start=start,
            end=end,
            interval=interval,
            auto_adjust=False,
        )

        if df.empty:
            raise ValueError(f"No data returned for symbol '{symbol}'")

        df = df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
                "Dividends": "dividends",
                "Stock Splits": "splits",
            }
        )

        df.index.name = "date"
        df = df.sort_index()

        # 🔑 Add metadata
        currency = ticker.info.get("currency")
        df.attrs["symbol"] = symbol
        df.attrs["currency"] = currency
        df.attrs["source"] = "yahoo"

        return df
