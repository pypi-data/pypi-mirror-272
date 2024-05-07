from datetime import datetime
import requests
import json
import pandas as pd
from pandas import json_normalize


def date_range(start, end):
    calendar_df = pd.DataFrame(columns=['date'])
    start = datetime.strptime(start, "%Y%m%d")
    end =  datetime.strptime(end, "%Y%m%d")
    output = [date.strftime("%Y%m%d") for date in pd.date_range(start, end, freq='D')]
    calendar_df['date'] = sorted(output)

    return calendar_df


def date_merge(calendar_pd, holiday_pd):

    calendar_pd['date'] = pd.to_datetime(calendar_pd['date'], format='%Y%m%d')
    holiday_pd['date'] = pd.to_datetime(holiday_pd['date'], format='%Y%m%d')

    out_pd = pd.merge(calendar_pd, holiday_pd, how='outer', on='date')

    return out_pd


def holiday_collect(year, key):
    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json&numOfRows=50&solYear=' \
          + str(year) + '&ServiceKey=' + str(key)
    response = requests.get(url)

    if response.status_code == 200:
        json_ob = json.loads(response.text)
        holidays_data = json_ob['response']['body']['items']['item']
        dataframe = json_normalize(holidays_data)

    dataframe.rename(columns={"dateName": "description",
                              "isHoliday": "holiday",
                              "locdate": "date"}, inplace=True)
    dataframe.drop(['dateKind', 'seq'], axis=1, inplace=True)

    return dataframe


def weekend_collect(calendar_df):
    calendar_df['day_of_week'] = calendar_df['date'].dt.dayofweek
    calendar_df['weekend'] = calendar_df.day_of_week.apply(lambda x: 1 if x >= 5 else 0)
    calendar_df['holiday'] = (calendar_df['holiday'] == "Y") | (calendar_df['weekend'] == 1)
    calendar_df['holiday'] = calendar_df.holiday.apply(lambda x: 1 if x == True else 0)
    calendar_df.drop(['weekend'], axis=1, inplace=True)

    return calendar_df


def between_collect(calendar_df):
    holiday_list = calendar_df['holiday'].values
    next_day = [0] * len(holiday_list)
    prev_day = [0] * len(holiday_list)

    for i in range(len(holiday_list) - 1):
        if (holiday_list[i] == 1) & (holiday_list[i + 1] == 0):
            next_day[i + 1] = 1

    for i in range(1, len(holiday_list)):
        if (holiday_list[i - 1] == 0) & (holiday_list[i] == 1):
            prev_day[i - 1] = 1

    calendar_df['prev_day'] = prev_day
    calendar_df['next_day'] = next_day

    return calendar_df


def vacation_collect(today_year, start, end):
    vacation_df = pd.DataFrame(columns=['date', "vacation"])

    output = [date.strftime("%Y%m%d")
              for date in pd.date_range(str(today_year)+start,
                                        str(today_year)+end,
                                        freq='D')]
    vacation_df['date'] = sorted(output)
    vacation_df['vacation'] = "1"

    return vacation_df


def select_calender(calender_key, start, end=datetime.today().strftime('%Y%m%d')):
    today_year = datetime.today().year
    start_year = start[0:4]
    end_year = end[0:4]
    if int(end_year)-int(start_year) >= 0 :
        calendar_pd = date_range(start, end)

        for i in range (int(end_year)-int(start_year)+1) :
            vacation_list = [vacation_collect(int(start_year) + i, "0715", "0831"),
                             vacation_collect(int(start_year) + i, "0101", "0228"),
                             vacation_collect(int(start_year) + i, "1215", "1231")]
            vacation_ele = pd.concat(vacation_list, ignore_index=True)
            holiday_ele = holiday_collect(int(start_year) + i, calender_key)

            if i == 0 :
                vacation_pd = vacation_ele
                holiday_pd = holiday_ele
            else :
                vacation_pd = pd.concat([vacation_pd, vacation_ele], ignore_index=True)
                holiday_pd = pd.concat([holiday_pd, holiday_ele], ignore_index=True)

    else :
        print('입력이 정확하지 않습니다.')

    calendar_df = date_merge(calendar_pd, holiday_pd)
    calendar_df = weekend_collect(calendar_df)
    calendar_df = between_collect(calendar_df)
    calendar_df = date_merge(calendar_df, vacation_pd)
    calendar_df = calendar_df[(calendar_df['date'] >= pd.to_datetime(start)) & (calendar_df['date'] <= pd.to_datetime(end))]
    calendar_df['vacation'] = calendar_df['vacation'].fillna(0)

    return calendar_df