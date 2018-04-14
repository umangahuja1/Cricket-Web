from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import calendar
import pytz


def scrape():
    res = requests.get('http://synd.cricbuzz.com/j2me/1.0/sch_calender.xml')

    while(res.status_code != 200):
        res = requests.get('http://synd.cricbuzz.com/j2me/1.0/sch_calender.xml')

    soup = BeautifulSoup(res.content, 'lxml')
    data = soup.find_all('mch')

    return data


def to_indian_time(date, month_year, time):
    hour, minute = int(time.split(':')[0]), int(time.split(':')[1])
    minute = (minute + 30) % 60
    hour = (hour + 5 + int(minute / 60)) % 24

    indian_time = str(hour) + ":"
    if minute < 10:
        indian_time += '0'
    indian_time += str(minute)

    year = month_year.split(',')[1]
    month_word = month_year.split(',')[0]
    month = list(calendar.month_abbr).index(month_word)
    match_time = datetime(int(year), month, int(date.split()[1]), hour, minute)

    return match_time, indian_time, month, year


def Schedule():
    data = scrape()
    result = []

    for item in data[:]:
        if 'Ind' in item['desc']:
            match = item['desc']
            series = item['srs'][5:]
            date = item['ddt']
            month_year = item['mnth_yr']
            time = item['tm']
            match_time, indian_time, month, year = to_indian_time(date, month_year, time)
            india = pytz.timezone('Asia/Kolkata')
            current_time = str(datetime.now(india)).split('+')[0]
            #print(match_time, "....", indian_time, ".....", current_time)

            if(current_time < str(match_time)):

                result.append({
                    'match': match,
                    'series': series,
                    'minutes': int(time.split(':')[1]),
                    'hours': int(time.split(':')[0]),
                    'date': int(date.split()[1]),
                    'month': month,
                    'year': year,
                    'time': match_time,
                    'indian_time': indian_time
                })

    return result[0]


if __name__ == '__main__':

    Schedule()
    # print(Schedule())
