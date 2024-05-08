import re
from typing import Self
from pandas import DataFrame
from httpx import Client, Response, Timeout
from httpx._types import QueryParamTypes
import tomllib
from platformdirs import user_config_path
from pathlib import Path

from ..common.constants import API_VERSION
from ..common.csv_utils import api_csv_string_to_df
from ..common.exceptions import ApiException, ClientException
from .Query import Query

default_url = 'https://api.pvradar.com/v2'


class PvradarSyncClient:
    _token: str
    _base_url: str
    _session: Client | None

    def __init__(
        self,
        token: str = 'pvradar_public',
        base_url: str = default_url,
    ):
        self._token = token
        self._base_url = base_url
        self._session = None

    def make_session(self) -> Client:
        timeout = Timeout(60.0, connect=10.0)
        session = Client(base_url=self._base_url, timeout=timeout)
        session.headers.update({'Authorization': f'Bearer {self._token}'})
        session.headers.update({'Accept-version': API_VERSION})
        return session

    @property
    def session(self) -> Client:
        if not self._session:
            self._session = self.make_session()
        return self._session

    def get(
        self, query: str | Query, params: QueryParamTypes | None = None
    ) -> Response:
        if isinstance(query, str):
            return self.session.get(url=query, params=params)
        return self.session.get(url=query.path, params=query.make_query_params())

    def maybe_raise(self, r: Response):
        if r.status_code >= 400:
            raise ApiException(r.status_code, r.text, r)

    def get_csv(self, query: str | Query, params: QueryParamTypes | None = None) -> str:
        r = self.get(query=query, params=params)
        self.maybe_raise(r)
        return r.text

    def get_df(
        self, query: str | Query, params: QueryParamTypes | None = None
    ) -> DataFrame:
        r = self.get(query=query, params=params)
        self.maybe_raise(r)
        pure_type = re.sub(r';.*$', '', r.headers['content-type']).strip()
        if pure_type in ['text/csv', 'application/csv']:
            return api_csv_string_to_df(r.text)
        raise ClientException(f'unexpected content type: {pure_type}', r)

    @classmethod
    def from_config(cls, config_path_str='') -> Self:
        if not config_path_str:
            config_path = user_config_path('pvradar') / 'sdk.toml'
        else:
            config_path = Path(config_path_str)
        try:
            with config_path.open('rb') as conf_file:
                values = tomllib.load(conf_file)
            return cls(
                token=values['token'],
                base_url=values['base_url'] if 'base_url' in values else default_url,
            )
        except OSError:
            raise ClientException(
                f'CRITICAL: No config found, expected file: {config_path}'
            )
        except tomllib.TOMLDecodeError:
            raise ClientException(
                f'CRITICAL: Invalid config found in file: {config_path}'
            )
        except KeyError as key:
            raise ClientException(
                f'Key:{key} was not found',
            )
