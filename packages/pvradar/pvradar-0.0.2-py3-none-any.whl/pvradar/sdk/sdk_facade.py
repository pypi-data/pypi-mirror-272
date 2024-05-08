from typing import Optional
from pandas import DataFrame
from .client.SyncClient import PvradarSyncClient
from .client.Query import Query


class _SdkFacade:
    _client: Optional[PvradarSyncClient] = None

    def _get_client(self):
        if self._client is None:
            self._client = PvradarSyncClient()
        return self._client

    def _get_soiling_ratio(self, part: str, query_dict: dict) -> DataFrame:
        query = Query(
            path=f'standard-soiling/{part}/csv',
            location=query_dict['location'],
            period=query_dict['period'],
        )
        return self._get_client().get_df(query=query)

    def get_soiling_ratio(self, query_dict: dict) -> DataFrame:
        return self._get_soiling_ratio('monthly', query_dict)

    def get_soiling_ratio_monthly(self, query_dict: dict) -> DataFrame:
        return self._get_soiling_ratio('monthly', query_dict)

    def get_soiling_ratio_daily(self, query_dict: dict) -> DataFrame:
        return self._get_soiling_ratio('daily', query_dict)

    def get_soiling_level_monthly(self, location: dict, period: dict) -> DataFrame:
        raise Exception('whoops, not implemented')


sdk_facade = _SdkFacade()
