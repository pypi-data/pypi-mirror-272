import json
from typing import Optional, Self
from json import JSONEncoder
from dataclasses import asdict

from ..common.exceptions import ClientException
from ..common.dd_types import DDPeriod, DDLocation
from httpx._types import QueryParamTypes


def _period_to_str(period: DDPeriod) -> str:
    chunks: list[str] = []
    if period.start is not None:
        chunks.append(str(period.start))
    if period.end is not None:
        chunks.append(str(period.end))
    return '..'.join(chunks)


class Query(JSONEncoder):
    _path: str
    _period: Optional[DDPeriod]
    _location: Optional[DDLocation]

    def __init__(
        self,
        path: str = '',
        period: (int | str | DDPeriod | dict | None) = None,
        location: (str | DDLocation | dict | None) = None,
    ):
        self.set_path(path)
        self.set_period(period)
        self.set_location(location)

    def as_dict(self):
        return {
            'path': self.path,
            'location': None if self._location is None else asdict(self._location),
            'period': None if self._period is None else asdict(self._period),
        }

    def __str__(self):
        return json.dumps(self.__dict__)

    def set_path(self, path: str) -> Self:
        self._path = path
        return self

    @property
    def path(self) -> str:
        return self._path

    def set_location(self, location: str | DDLocation | dict | None) -> Self:
        if isinstance(location, str):
            chunks = location.split(',')
            if len(chunks) != 2:
                raise ClientException(f'unexpected location coordinates: {location}')
            else:
                self._location = DDLocation(
                    lat=float(chunks[0].strip()), lon=float(chunks[1].strip())
                )
        elif isinstance(location, dict):
            self._location = DDLocation(
                lat=float(location['lat']), lon=float(location['lon'])
            )
        elif isinstance(location, DDLocation) or location is None:
            self._location = location
        else:
            raise ClientException(f'unexpected type for location: {type(location)}')
        return self

    def set_period(self, period: int | str | DDPeriod | dict | None) -> Self:
        if isinstance(period, int):
            self._period = DDPeriod(period_type='year-range', start=period, end=period)
        elif isinstance(period, str):
            chunks = period.split('..')
            if len(chunks) == 1:
                self._period = DDPeriod(
                    period_type='year-range', start=int(chunks[0]), end=int(chunks[0])
                )
            else:
                self._period = DDPeriod(
                    period_type='year-range', start=int(chunks[0]), end=int(chunks[1])
                )
        elif isinstance(period, dict):
            if 'year' in period:
                same_year = int(period['year'])
                self._period = DDPeriod(
                    period_type='year-range', start=same_year, end=same_year
                )
            elif 'start' in period and 'end' in period:
                self._period = DDPeriod(
                    period_type='year-range',
                    start=int(period['start']),
                    end=int(period['end']),
                )
            else:
                raise ClientException(
                    f'unexpected keys for period: {list(period.keys())}'
                )
        elif isinstance(period, DDPeriod) or period is None:
            self._period = period
        else:
            raise ClientException(f'unexpected type for period: {type(period)}')
        return self

    def make_query_params(self) -> QueryParamTypes:
        result = {}
        if self._location is not None:
            result['lat'] = str(self._location.lat)
            result['lon'] = str(self._location.lon)
        if self._period is not None:
            result['period'] = _period_to_str(self._period)
        return result
