import asyncio
from datetime import datetime, timedelta
import pytest
import pandas as pd

from cryptellation import client

@pytest.mark.asyncio
async def test_candlesticks():
    # Create a new client instance pointing to localhost
    c = client.Client(address="localhost:7233", user_agent="python-e2e")
    
    # Set up test parameters
    pair = "BTC-USDT"    # Trading pair to fetch candlesticks for
    period = "M1"        # 1-minute interval candlesticks
    start = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    end = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Fetch candlesticks
    df = await c.list_candlesticks(pair, period, exchange="binance", start=start, end=end)

    # Verify we got some candlesticks
    assert isinstance(df, pd.DataFrame), "Result should be a pandas DataFrame"
    assert not df.empty, "DataFrame should not be empty"

    # Get the first row
    first_row = df.iloc[0]

    # Verify DataFrame structure
    assert 'open' in df.columns, "DataFrame should have an open column"
    assert 'high' in df.columns, "DataFrame should have a high column"
    assert 'low' in df.columns, "DataFrame should have a low column"
    assert 'close' in df.columns, "DataFrame should have a close column"
    assert 'volume' in df.columns, "DataFrame should have a volume column"

    # Verify data types
    assert isinstance(first_row['open'], (float, int)), "Open should be a float or integer"
    assert isinstance(first_row['high'], (float, int)), "High should be a float or integer"
    assert isinstance(first_row['low'], (float, int)), "Low should be a float or integer"
    assert isinstance(first_row['close'], (float, int)), "Close should be a float or integer"
    assert isinstance(first_row['volume'], (float, int)), "Volume should be a float or integer"

    # Verify price relationships
    assert first_row['high'] >= first_row['open'], "High should be greater than or equal to open"
    assert first_row['high'] >= first_row['close'], "High should be greater than or equal to close"
    assert first_row['low'] <= first_row['open'], "Low should be less than or equal to open"
    assert first_row['low'] <= first_row['close'], "Low should be less than or equal to close"
    assert first_row['volume'] >= 0, "Volume should be non-negative"

    # Verify index is datetime
    assert isinstance(df.index, pd.DatetimeIndex), "Index should be a DatetimeIndex"