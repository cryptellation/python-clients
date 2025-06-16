import asyncio
from datetime import datetime, timedelta
import pytest
import pandas as pd

from cryptellation import client

@pytest.mark.asyncio
async def test_sma():
    # Create a new client instance pointing to localhost
    c = client.Client(address="localhost:7233", user_agent="python-e2e")
    
    # Set up test parameters
    pair = "ETH-USDT"    # Trading pair to fetch SMA for
    period = "M1"        # 1-minute interval
    start = "2023-02-26T12:00:00Z"
    end = "2023-02-26T13:00:00Z"
    
    # Fetch SMA data
    df = await c.list_sma(
        exchange="binance",
        pair=pair,
        period=period,
        start=start,
        end=end,
        period_number=3,
        price_type="close"
    )

    # Verify we got some data
    assert isinstance(df, pd.DataFrame), "Result should be a pandas DataFrame"
    assert not df.empty, "DataFrame should not be empty"

    # Get the first row
    first_row = df.iloc[0]

    # Verify DataFrame structure
    assert 'Value' in df.columns, "DataFrame should have a Value column"

    # Verify data types
    assert isinstance(first_row['Value'], (float, int)), "Value should be a float or integer"
    assert first_row['Value'] > 0, "SMA value should be positive"

    # Verify index is datetime
    assert isinstance(df.index, pd.DatetimeIndex), "Index should be a DatetimeIndex"

    # Verify time range
    assert df.index.min() >= pd.Timestamp(start), "First timestamp should be after start time"
    assert df.index.max() <= pd.Timestamp(end), "Last timestamp should be before end time"

    # Verify data continuity
    time_diff = df.index.to_series().diff()
    expected_diff = pd.Timedelta(minutes=1)  # For M1 period
    assert all(time_diff[1:] == expected_diff), "Data points should be 1 minute apart"

@pytest.mark.asyncio
async def test_sma_different_periods():
    # Create a new client instance pointing to localhost
    c = client.Client(address="localhost:7233", user_agent="python-e2e")
    
    # Set up test parameters
    pair = "ETH-USDT"
    start = "2023-02-26T12:00:00Z"
    end = "2023-02-26T13:00:00Z"
    
    # Test different periods
    periods = ["M1", "M5", "M15", "H1"]
    for period in periods:
        df = await c.list_sma(
            exchange="binance",
            pair=pair,
            period=period,
            start=start,
            end=end,
            period_number=3,
            price_type="close"
        )
        
        assert isinstance(df, pd.DataFrame), f"Result should be a DataFrame for period {period}"
        assert not df.empty, f"DataFrame should not be empty for period {period}"
        
        # Verify period-specific time differences
        time_diff = df.index.to_series().diff()
        if period == "M1":
            expected_diff = pd.Timedelta(minutes=1)
        elif period == "M5":
            expected_diff = pd.Timedelta(minutes=5)
        elif period == "M15":
            expected_diff = pd.Timedelta(minutes=15)
        elif period == "H1":
            expected_diff = pd.Timedelta(hours=1)
            
        assert all(time_diff[1:] == expected_diff), f"Data points should be {period} apart"

@pytest.mark.asyncio
async def test_sma_different_price_types():
    # Create a new client instance pointing to localhost
    c = client.Client(address="localhost:7233", user_agent="python-e2e")
    
    # Set up test parameters
    pair = "ETH-USDT"
    period = "M1"
    start = "2023-02-26T12:00:00Z"
    end = "2023-02-26T13:00:00Z"
    
    # Test different price types
    price_types = ["open", "high", "low", "close"]
    for price_type in price_types:
        df = await c.list_sma(
            exchange="binance",
            pair=pair,
            period=period,
            start=start,
            end=end,
            period_number=3,
            price_type=price_type
        )
        
        assert isinstance(df, pd.DataFrame), f"Result should be a DataFrame for price type {price_type}"
        assert not df.empty, f"DataFrame should not be empty for price type {price_type}"
        assert all(df['Value'] > 0), f"SMA values should be positive for price type {price_type}"
