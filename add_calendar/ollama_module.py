import requests
import json

def parse_text_with_ollama(text, model_name='elyza:jp8b'):
    """
    Ollamaを使用してテキストから日時とイベントを抽出します。

    Args:
        text (str): 解析するテキスト。
        model_name (str): 使用するOllamaモデルの名前。

    Returns:
        list: 抽出されたイベントのリスト。
    """
    # OllamaのAPIエンドポイント
    ollama_url = 'http://localhost:11434/api/generate'

    # Ollamaに送信するプロンプトを作成
    prompt = f"""
以下の文章から、日付とそれに対応する予定を抽出してください。結果は純粋なJSON形式で、日本語で、"date"と"event"のキーを持つオブジェクトのリストとして返してください。

文章:
{text}

出力例:
[
    {{"date": "2024-10-07", "event": "ペットボトルの準備"}},
    {{"date": "2024-10-25", "event": "準備物の確認"}}
]

重要事項:
- 出力は純粋なJSON形式で、追加のテキストや説明は含めないでください。
- 日付は"YYYY-MM-DD"の形式で出力してください。
- **イベント名が存在しない場合、そのエントリを出力しないでください。**
- イベント名は元の文章から適切に抽出してください。
"""

    payload = {
        'model': model_name,
        'prompt': prompt
    }

    try:
        # ストリーミングレスポンスを取得
        response = requests.post(ollama_url, json=payload, stream=True)
        response.raise_for_status()

        # レスポンスのストリームを処理
        response_text = ''
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                # 各行をJSONとしてパース
                line_json = json.loads(line_str)
                # "response"フィールドを連結
                response_text += line_json.get('response', '')

        print("Ollamaのレスポンス:")
        print(response_text)
    except requests.exceptions.RequestException as e:
        print("Ollamaへのリクエストに失敗しました:", e)
        return []
    except json.JSONDecodeError as e:
        print("レスポンスの解析に失敗しました:", e)
        return []

    # 連結したテキストをJSONとして解析
    try:
        events = json.loads(response_text)
    except json.JSONDecodeError as e:
        print("Ollamaからのレスポンスの解析に失敗しました:", e)
        events = []

    return events
