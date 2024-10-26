import os
import datetime
import pytz
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
VOICEVOX_API_URL = "http://192.168.1.69:50021"  # VoiceVoxのAPIサーバーURL

def authenticate():
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        return creds
    else:
        print("トークンファイルが見つかりません。認証を実行してください。")
        return None

def get_upcoming_events(creds, days=7):
    service = build('calendar', 'v3', credentials=creds)
    tz = pytz.timezone('Asia/Tokyo')
    now = datetime.datetime.now(tz)
    start_of_week = now - datetime.timedelta(days=now.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=days)
    time_min = now.isoformat()
    time_max = end_of_week.isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    return events

def format_date_with_weekday(date_str):
    """ 日付文字列を「YYYY年M月D日（曜日）」形式に変換します """
    date_obj = datetime.datetime.fromisoformat(date_str)
    # 曜日を日本語で取得
    weekday = date_obj.strftime("%A")
    weekday_dict = {
        "Monday": "月",
        "Tuesday": "火",
        "Wednesday": "水",
        "Thursday": "木",
        "Friday": "金",
        "Saturday": "土",
        "Sunday": "日"
    }
    weekday_jp = weekday_dict.get(weekday, weekday)  # 日本語の曜日に変換
    formatted_date = date_obj.strftime(f"%Y年%m月%d日（{weekday_jp}）")
    return formatted_date
# 音声合成の関数を修正して、生成されたファイル名を返すようにします
def synthesize_speech(text, speaker=1):
    params = {'text': text, 'speaker': speaker}
    response = requests.post(f"{VOICEVOX_API_URL}/audio_query", params=params)
    if response.status_code == 200:
        query_data = response.json()
        synthesis_response = requests.post(f"{VOICEVOX_API_URL}/synthesis", params={'speaker': speaker}, json=query_data)
        if synthesis_response.status_code == 200:
            filename = f"event_voice_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
            with open(filename, "wb") as f:
                f.write(synthesis_response.content)
            print(f"音声ファイルを生成しました: {filename}")
            return filename  # 生成されたファイル名を返す
        else:
            print("音声の生成に失敗しました")
            return None
    else:
        print("クエリの作成に失敗しました")
        return None
