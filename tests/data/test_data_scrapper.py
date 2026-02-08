from datetime import date

import pandas as pd
import pytest

from alpha_monitor.data.data_scrapper import YahooFinanceDataSource


class DummyTicker:
    """Mock replacement for yfinance.Ticker."""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.info = {"currency": "EUR"}

    def history(self, *args, **kwargs) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Open": [100.0, 101.0],
                "High": [102.0, 103.0],
                "Low": [99.0, 100.0],
                "Close": [101.0, 102.0],
                "Volume": [1_000, 1_200],
                "Dividends": [0.0, 0.0],
                "Stock Splits": [0.0, 0.0],
            },
            index=pd.to_datetime(["2024-01-01", "2024-01-02"]),
        )


def test_get_prices_returns_dataframe(monkeypatch):
    """Basic smoke test: returns a non-empty DataFrame."""

    def mock_ticker(symbol: str):
        return DummyTicker(symbol)

    monkeypatch.setattr("yfinance.Ticker", mock_ticker)

    source = YahooFinanceDataSource()
    df = source.get_prices("RHM.DE")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_get_prices_column_names(monkeypatch):
    """Columns should be normalised to lowercase OHLCV."""

    monkeypatch.setattr("yfinance.Ticker", lambda s: DummyTicker(s))

    df = YahooFinanceDataSource().get_prices("RHM.DE")

    expected_columns = {
        "open",
        "high",
        "low",
        "close",
        "volume",
        "dividends",
        "splits",
    }

    assert set(df.columns) == expected_columns


def test_get_prices_index_is_named_and_sorted(monkeypatch):
    """Index should be datetime, sorted, and named 'date'."""

    monkeypatch.setattr("yfinance.Ticker", lambda s: DummyTicker(s))

    df = YahooFinanceDataSource().get_prices("RHM.DE")

    assert df.index.name == "date"
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.is_monotonic_increasing


def test_get_prices_attaches_metadata(monkeypatch):
    """Currency, symbol, and source should be attached as metadata."""

    monkeypatch.setattr("yfinance.Ticker", lambda s: DummyTicker(s))

    df = YahooFinanceDataSource().get_prices("RHM.DE")

    assert df.attrs["currency"] == "EUR"
    assert df.attrs["symbol"] == "RHM.DE"
    assert df.attrs["source"] == "yahoo"


def test_get_prices_raises_on_empty_data(monkeypatch):
    """Empty Yahoo responses should raise a clear error."""

    class EmptyTicker(DummyTicker):
        def history(self, *args, **kwargs):
            return pd.DataFrame()

    monkeypatch.setattr("yfinance.Ticker", lambda s: EmptyTicker(s))

    source = YahooFinanceDataSource()

    with pytest.raises(ValueError, match="No data returned"):
        source.get_prices("RHM.DE")


def test_get_prices_passes_date_arguments(monkeypatch):
    """Ensure start/end dates are accepted without error."""

    monkeypatch.setattr("yfinance.Ticker", lambda s: DummyTicker(s))

    source = YahooFinanceDataSource()

    df = source.get_prices(
        "RHM.DE",
        start=date(2020, 1, 1),
        end=date(2020, 12, 31),
    )

    assert not df.empty
