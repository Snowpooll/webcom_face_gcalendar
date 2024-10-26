import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from pdfminer.high_level import extract_text
from io import BytesIO

# Google Drive APIの認証
def authenticate_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    token_path = 'token.json'  # token.jsonのパスを変更
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        print("認証トークンが見つかりません。認証を実行してください。")
        return None
    return build('drive', 'v3', credentials=creds)

# 他の関数も引き続き同様
# フォルダ内のPDFファイルリストを取得
def list_pdf_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/pdf'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

# Google DriveからPDFファイルをダウンロード
def download_pdf_from_drive(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file_data = BytesIO()
    downloader = MediaIoBaseDownload(file_data, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download Progress: {int(status.progress() * 100)}%")
    file_data.seek(0)
    return file_data

# PDFからテキストを抽出
def extract_text_from_pdf(pdf_data):
    text = extract_text(pdf_data)
    return text

# 指定したフォルダ内のすべてのPDFファイルのテキストを抽出
def extract_texts_from_folder(folder_id):
    service = authenticate_drive()
    if not service:
        return []

    pdf_files = list_pdf_files_in_folder(service, folder_id)
    if not pdf_files:
        print("指定されたフォルダにPDFファイルが見つかりません。")
        return []

    texts = []
    for pdf_file in pdf_files:
        print(f"Processing file: {pdf_file['name']}")
        pdf_data = download_pdf_from_drive(service, pdf_file['id'])
        pdf_text = extract_text_from_pdf(pdf_data)
        if pdf_text:
            texts.append(pdf_text)
        else:
            print(f"{pdf_file['name']} からテキストを抽出できませんでした。")
    return texts
