from datetime import datetime
import re

def convert_japanese_date(japanese_date):
    pattern = r"令和(\d+)年(\d+)月(\d+)日"
    match = re.match(pattern, japanese_date)
    if match:
        year = int(match.group(1)) + 2018  # 令和元年は2019年に相当
        month = int(match.group(2))
        day = int(match.group(3))
        return f"{year}-{month:02d}-{day:02d}"
    # ISO形式のチェック
    try:
        datetime.strptime(japanese_date, '%Y-%m-%d')
        return japanese_date
    except ValueError:
        return None  # 無効な日付形式

def filter_events(events):
    valid_events = []
    for event in events:
        date = convert_japanese_date(event['date'])
        if date and event['event']:
            valid_events.append({'date': date, 'event': event['event']})
        else:
            print(f"無効な日付形式: {event['date']}")
    return valid_events
