import csv
from io import StringIO
from pandas import DataFrame, read_csv, to_datetime

def api_csv_string_to_df(csv_str: str) -> DataFrame:
    header = next(csv.reader(StringIO(csv_str)))
    df = read_csv(StringIO(csv_str))

    if header[0] in ['isoDate', 'iso_date']:
        df[header[0]] = to_datetime(df[header[0]])
        index_name = header[0]
        df.set_index(index_name, inplace=True)

    if header[0] == 'month' and len(df) == 12:
        df.set_index(header[0], inplace=True)
    return df

