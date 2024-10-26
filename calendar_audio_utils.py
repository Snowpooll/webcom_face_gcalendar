from calendar_utils import authenticate, get_upcoming_events, synthesize_speech, format_date_with_weekday
from playsound import playsound

def get_weekly_schedule_with_audio(play_audio=False):
    """
    今週の残りの予定を取得し、音声ファイルを生成する関数。
    
    :param play_audio: 予定を音声で再生するかどうか（デフォルトは再生しない）
    :return: 今週の予定をテキスト形式で返すリスト
    """
    creds = authenticate()
    audio_files = []  # 音声ファイルのリスト
    event_texts = []  # 予定のテキストリスト

    if creds:
        events = get_upcoming_events(creds)
        if not events:
            print('今週の残りの予定はありません。')
        else:
            print('今週の残りの予定:')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', '（タイトルなし）')
                formatted_date = format_date_with_weekday(start)
                event_text = f"{formatted_date} - {summary}"
                event_texts.append(event_text)  # テキストをリストに追加
                print(event_text)

                # 音声ファイルを生成
                filename = synthesize_speech(event_text)
                if filename:
                    audio_files.append(filename)  # 生成されたファイル名をリストに追加

        # 音声を再生するオプションがTrueの場合にのみ、音声ファイルを再生
        if play_audio and audio_files:
            # notice.wavを最初に再生
            print("再生中: notice.wav")
            playsound("notice.wav")
            
            # 各予定の音声ファイルを再生
            for audio_file in audio_files:
                print(f"再生中: {audio_file}")
                playsound(audio_file)

    return event_texts
