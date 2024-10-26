from gmail_utils import gmail_init, gmail_get_latest_unread_message_body
from ollama_module import parse_text_with_ollama
from google_calendar_module import add_events_to_calendar
from event_utils import filter_events

# Gmail APIの初期化
service = gmail_init()

# 最新の未読メッセージの本文を取得
label_id = ''  # 取得するラベルID
message_body = gmail_get_latest_unread_message_body(service, label_id)

if message_body != "No unread messages found.":
    print("メール本文:")
    print(message_body)
    
    # Ollamaでメール本文を解析
    raw_events = parse_text_with_ollama(message_body, model_name='elyza:jp8b')
    
    # 抽出されたイベントを表示
    print("抽出されたイベント:")
    for event in raw_events:
        print(event)

    # イベントのフィルタリングとフォーマット
    events = filter_events(raw_events)

    # 有効なイベントを表示
    print("有効なイベント:")
    for event in events:
        print(event)

    # 有効なイベントがある場合のみGoogleカレンダーに追加
    if events:
        add_events_to_calendar(events, calendar_id='primary', token_file='token.json', credentials_file='credentials.json')
    else:
        print("有効なイベントがありません。")
else:
    print("未読メッセージが見つかりませんでした。")
