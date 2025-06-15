from temporalio.client import Client as TemporalClient
import pandas as pd
from datetime import datetime

class Client:
    def __init__(self, address: str):
        self.address = address
        self.client = None

    async def _connect_if_needed(self):
        if self.client is None:
            self.client = await TemporalClient.connect(self.address)

    async def list_candlesticks(self, pair: str, period: str, exchange: str, start: str = None, end: str = None, limit: int = 0):
        await self._connect_if_needed()
        result = await self.client.execute_workflow(
            "ListCandlesticksWorkflow",
            {"pair": pair, "period": period, "exchange": exchange, "start": start, "end": end, "limit": limit},
            id="list_candlesticks",
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