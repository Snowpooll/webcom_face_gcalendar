# webcom_face_gcalendar
Perform face identification with OpenCV When the face of the registered person is recognized Get this week's schedule using Google calendar API Generate and read audio with Docker's voicevox


## 動作環境
M1 MacbookAir 16GB で動作しています

Gmail と Google Calendar を操作するためAPIとtoken.jsonが必要になります  
https://developers.google.com/gmail/api/quickstart/python?hl=ja  
を参考にAPIを使用可能にし、token.jsonを取得し同一ディレクトリに設置してください


使用にあたり 
`pip install -r requirements.txt` を実行後

GoogleDrive のフォルダIDが必要になるので
create_folder.py で作業フォルダの作成とIDの取得を行います
add_gdrive_calendar.py
でIDを設定してください

label_gmail.py
でGmail ラベル一覧の取得ができます

add_gmail_calendar.py
で取得するGmailのラベルを設定します

Ollamaでelyza:jp8b’を使用します
```
arch -arm64 brew install git-lfs  
git lfs install  
git clone https://huggingface.co/elyza/Llama-3-ELYZA-JP-8B-GGUF.git
```
でダウンロード

`vim Modelfile`
でファイルを作成

中身を
```
FROM ./Llama-3-ELYZA-JP-8B-q4_k_m.gguf
TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"""
PARAMETER stop "<|start_header_id|>"
PARAMETER stop "<|end_header_id|>"
PARAMETER stop "<|eot_id|>"
PARAMETER stop "<|reserved_special_token"
```
として保存  
` ollama create elyza:jp8b -f Modelfile`
を実行し   
Successとなったら  
`ollama run elyza:jp8b`
で実行します  

これで Ollamaでelyza:jp8bが動作します  

calendar_utils.py  
でDocker VoicevoxマシンのURLを指定していますので  
環境に応じて変更してください  

音声の作成に voicevox の docker が必要になります  
`docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest`   
で取得しています  

動作させるには  
バックグランドでの起動で -d オプションをつけて
 `docker run -d -p '192.168.1.69:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest`
 というように起動させます IPアドレス部分はご自身のマシンのIPに変えてください
