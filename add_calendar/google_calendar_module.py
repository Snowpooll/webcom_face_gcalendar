import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

def add_events_to_calendar(events, calendar_id='primary', token_file='token.json', credentials_file='credentials.json'):
    """
    抽出されたイベントをGoogleカレンダーに追加します。

    Args:
        events (list): イベントのリスト。
        calendar_id (str): イベントを追加するカレンダーのID。
        token_file (str): 認証トークンファイルのパス。
        credentials_file (str): クライアント認証情報のファイルパス。
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    else:
        if os.path.exists(credentials_file):
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        else:
            print(f"{credentials_file} が見つかりません。認証情報を取得してください。")
            return

    # トークンが無効または期限切れの場合は更新
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("認証情報が無効です。再度認証を行ってください。")
            return

    service = build('calendar', 'v3', credentials=creds)

    for event in events:
        # 日付の形式を確認し、必要に応じて変換
        try:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
        except ValueError:
            print(f"無効な日付形式: {event['date']}")
            continue

        event_body = {
            'summary': event['event'],
            'start': {
                'date': event_date.strftime('%Y-%m-%d'),
                'timeZone': 'Asia/Tokyo',
            },
            'end': {
                'date': (event_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                'timeZone': 'Asia/Tokyo',
            },
        }

        try:
            # イベントをカレンダーに追加
            created_event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
            print(f"イベントが作成されました: {created_event.get('htmlLink')}")
        except Exception as e:
            print(f"イベントの作成中にエラーが発生しました: {e}")
