from drive_pdf_extractor import extract_texts_from_folder
from ollama_module import parse_text_with_ollama
from google_calendar_module import add_events_to_calendar
from event_utils import convert_japanese_date, filter_events

# フォルダIDを指定して処理を開始
folder_id = "GoogleDriveフォルダのID"
texts = extract_texts_from_folder(folder_id)

if not texts:
    print("フォルダ内に解析するテキストがありません。")
else:
    for text_content in texts:
        raw_events = parse_text_with_ollama(text_content, model_name='elyza:jp8b')
        print("抽出されたイベント:")
        for event in raw_events:
            print(event)

        # イベントのフィルタリングとフォーマット
        events = filter_events(raw_events)

        print("有効なイベント:")
        for event in events:
            print(event)

        if events:
            add_events_to_calendar(events, calendar_id='primary', token_file='token.json', credentials_file='credentials.json')
        else:
            print("有効なイベントがありません。")
