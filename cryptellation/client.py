from temporalio.client import Client as TemporalClient
import pandas as pd
from datetime import datetime

class Client:
    def __init__(self, address: str, user_agent: str = "python"):
        self.address = address
        self.client = None
        self.user_agent = user_agent

    async def _connect_if_needed(self):
        if self.client is None:
            self.client = await TemporalClient.connect(self.address)

    async def list_candlesticks(self, pair: str, period: str, exchange: str, start: str = None, end: str = None, limit: int = 0):
        await self._connect_if_needed()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        result = await self.client.execute_workflow(
            "ListCandlesticksWorkflow",
            {
                "pair": pair, 
                "period": period,
                "exchange": exchange,
                "start": start,
                "end": end,
                "limit": limit,
            },
            id=f"{self.user_agent}-list-candlesticks-{timestamp}",
            task_queue="CryptellationCandlesticksTaskQueue"
        )
        
        # Convert the result to a pandas DataFrame
        if result and 'List' in result and result['List']:
            df = pd.DataFrame(result['List'])
            # Convert time string to datetime
            df['time'] = pd.to_datetime(df['time'])
            # Set time as index
            df.set_index('time', inplace=True)
            # Sort by time
            df.sort_index(inplace=True)
            return df
        return pd.DataFrame()

    async def list_sma(self, pair: str, period: str, exchange: str, start: str = None, end: str = None, period_number: int = 20, price_type: str = "close"):
        """
        Get Simple Moving Average (SMA) data points.
        
        Args:
            pair (str): Trading pair (e.g., "BTC-USDT")
            period (str): Candlestick period (e.g., "1h", "1d")
            exchange (str): Exchange name (e.g., "binance")
            start (str, optional): Start time in ISO format
            end (str, optional): End time in ISO format
            period_number (int, optional): Number of periods for SMA calculation. Defaults to 20.
            price_type (str, optional): Price type to use for SMA calculation ("open", "high", "low", "close"). Defaults to "close".
        
        Returns:
            pd.DataFrame: DataFrame with time index and SMA values
        """
        await self._connect_if_needed()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        result = await self.client.execute_workflow(
            "ListWorkflow",
            {
                "pair": pair,
                "period": period,
                "exchange": exchange,
                "start": start,
                "end": end,
                "periodNumber": period_number,
                "priceType": price_type
            },
            id=f"{self.user_agent}-list-sma-{timestamp}",
            task_queue="CryptellationSmaTaskQueue"
        )
        
        # Convert the result to a pandas DataFrame
        if result and 'Data' in result and result['Data']:
            df = pd.DataFrame(result['Data'])
            # Convert time string to datetime
            df['Time'] = pd.to_datetime(df['Time'])
            # Set time as index
            df.set_index('Time', inplace=True)
            # Sort by time
            df.sort_index(inplace=True)
            return df
        return pd.DataFrame()