from datetime import datetime, timedelta
import json
import time
import pandas as pd
import requests
from io import StringIO
import numpy as np

from utils import flomon_url, api_payload, region_name

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# row 생략 없이 출력
pd.set_option('display.max_rows', None)
# col 생략 없이 출력
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:.5f}'.format


def find_sido(input_name, region_dict):
    for key, names in region_dict.items():
        if input_name in names:
            return key
    return "해당 지역을 찾을 수 없습니다."


def filter_by_name(start_str, df=pd.read_json('resource-id-name.json')):
    result_df = df[df['name'].str.startswith(start_str)]
    return result_df.to_json(force_ascii=False)


def load_id_names(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        id_info = json.load(file)
        return {str(ids['id']): ids['name'] for ids in id_info}


def ids_to_names(data, id_name_map):
    named_data = {}
    for region_id, region_data in data.items():
        region_name = id_name_map.get(region_id, "Unknown Region")
        named_data[region_name] = region_data
    return named_data


def date_range(start, end):
    calendar_df = pd.DataFrame(columns=['date'])
    start = datetime.strptime(start, "%Y%m%d")
    end =  datetime.strptime(end, "%Y%m%d")
    output = [date.strftime("%Y%m%d") for date in pd.date_range(start, end, freq='D')]
    calendar_df['date'] = sorted(output)

    return calendar_df


def round_time_and_aggregate(data):
    final_data = {}

    for region_id, categories in data.items():
        final_data[region_id] = {}

        for category, records in categories.items():
            for record in records:
                rounded_time = round(record['time'] / 1000 / 60 / 60) * 60 * 60 * 1000

                if rounded_time not in final_data[region_id]:
                    final_data[region_id][rounded_time] = {}
                if category not in final_data[region_id][rounded_time]:
                    final_data[region_id][rounded_time][category] = record['value']
                else:
                    if not isinstance(final_data[region_id][rounded_time][category], list):
                        final_data[region_id][rounded_time][category] = [final_data[region_id][rounded_time][category]]
                    final_data[region_id][rounded_time][category].append(record['value'])

    return final_data


def kor_time(js):
    rows_list = []
    for district, times in js.items():
        for time, values in times.items():
            row = values.copy()
            row['region'] = district
            row['time'] = time
            rows_list.append(row)

    df = pd.DataFrame(rows_list)
    df['datetime'] = pd.to_datetime(df['time'], unit='ms')
    df['datetime'] = df['datetime'].dt.tz_localize('UTC')
    df['datetime'] = df['datetime'].dt.tz_convert('Asia/Seoul')

    return df


def slice_outter(group, start, end):
    start_date = pd.to_datetime(start, format='%Y%m%d').tz_localize('Asia/Seoul')
    end_date = pd.to_datetime(end, format='%Y%m%d').tz_localize('Asia/Seoul')
    end_date = end_date + pd.DateOffset(days=1, seconds=-1)
    group = group[(group.index >= start_date) & (group.index <= end_date)]

    return group


def region_inter(df, start, end):
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: x[0] if isinstance(x, list) else x)

    df.set_index('datetime', inplace=True)
    results = []
    for name, group in df.groupby('region'):
        full_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='h')
        group = group.reindex(full_index)
        group.interpolate(method='time', inplace=True)
        group['region'] = group['region'].ffill()
        group = slice_outter(group, start, end)
        group = group.reset_index().rename(columns={"index": "datetime"})
        group = group.ffill()
        group = group.bfill()
        results.append(group)

    df = pd.concat(results, ignore_index=True)

    return df


def js_to_dataframe(js, start, end):
    df = kor_time(js)
    df = region_inter(df, start, end)

    required_columns = ['windGust', 'windDirection', 'windSpeed']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[['region', 'datetime', 'time',
             'sunrise', 'sunset', 'temp', 'sensibleTemp',
             'humidity', 'pressure', 'clouds', 'visibility',
             'precipitationIntensity', 'snowfall', 'windGust',
             'windDirection', 'windSpeed', 'weatherCode']]

    return df


def adjust_column_names(cols):
    new_cols = []
    for col in cols:
        if isinstance(col, tuple):
            if col[0] in ['temp', 'sensibleTemp']:
                new_cols.append(f"{col[0]}_{col[1]}")
            else:
                new_cols.append(col[0])
        else:
            new_cols.append(col)
    return new_cols


def hourly_to_daily(df):
    df['date'] = df['datetime'].dt.date

    daily_data = df.groupby(['region', 'date']).agg({
        'sunrise': 'min',
        'sunset': 'max',
        'temp': ['max', 'mean', 'min'],
        'sensibleTemp': ['max', 'mean', 'min'],
        'humidity': 'mean',
        'pressure': 'mean',
        'clouds': 'mean',
        'visibility': 'mean',
        'precipitationIntensity':'sum',
        'snowfall':'sum',
        'windGust': 'max',
        'windDirection': 'mean',
        'windSpeed': 'mean',
        'weatherCode': lambda x: x.mode()[0]
    })

    daily_data.columns = adjust_column_names(daily_data.columns)
    daily_data.reset_index(inplace=True)

    return daily_data


def select_weather(weather_key, weather_url,
                   sido, gungu = "",
                   start = datetime.today().strftime('%Y%m%d'),
                   end = datetime.today().strftime('%Y%m%d'),
                   period="hourly"):

    region_df = pd.read_json('resource-id-name.json')
    id_names = load_id_names("resource-id-name.json")
    specific_sido = find_sido(sido, region_name)
    specific_gungu = specific_sido + gungu

    region_list = filter_by_name(specific_gungu, region_df)
    region_list = pd.read_json(StringIO(region_list))
    region_list = region_list["id"].tolist()
    region_len = len(region_list)
    region_params = ""
    for i in range(len(region_list)):
        region_params += f"resourceIds={region_list[i]}&"

    start_time = (time.mktime(datetime.strptime(start, "%Y%m%d").timetuple()) -1800) *1000
    end_time = (time.mktime(datetime.strptime(end, "%Y%m%d").timetuple()) +86300 +1800) *1000
    limit = (end_time-start_time)//(3600*1000)*3
    if limit == 0 : limit = 24*3

    url = weather_url + flomon_url + f"limit={int(limit)}&" + region_params + f"startTime={int(start_time)}&" + f"endTime={int(end_time)}"
    response = requests.request("GET", url, headers={'Authorization': weather_key}, data=api_payload)

    processed_data = round_time_and_aggregate(response.json())
    named_data = ids_to_names(processed_data, id_names)
    output = js_to_dataframe(named_data, start, end)

    if period == "daily":
        output = hourly_to_daily(output)

    return output