from __future__ import print_function
import os.path
from google.oauth2 import credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# 認証と API クライアントのセットアップ
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Google Drive API に接続し、フォルダを作成または取得します。"""
    creds = None
    # token.json はユーザーのアクセストークンとリフレッシュトークンを保存します。初回実行時に自動的に作成されます。
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # 資格情報がないか、無効または期限切れの場合は再ログインします。
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # ユーザーにブラウザで認証してもらいます。
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # 認証情報を保存します。
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Drive API クライアントを作成
    service = build('drive', 'v3', credentials=creds)

    # 1. "School" フォルダを取得または作成
    school_folder_id = get_or_create_folder(service, 'School', parent_id=None)

    # 2. "Read" フォルダを "School" フォルダ内に作成
    read_folder_id = get_or_create_folder(service, 'Read', parent_id=school_folder_id)

    print('School フォルダの ID: %s' % school_folder_id)
    print('Read フォルダの ID: %s' % read_folder_id)

def get_or_create_folder(service, folder_name, parent_id=None):
    """
    フォルダを取得または作成します。

    Parameters:
        service: Drive API サービス インスタンス。
        folder_name (str): フォルダの名前。
        parent_id (str): 親フォルダの ID（省略可能）。

    Returns:
        str: フォルダの ID。
    """
    # フォルダを検索
    query = "name='{}' and mimeType='application/vnd.google-apps.folder' and trashed=false".format(folder_name)
    if parent_id:
        query += " and '{}' in parents".format(parent_id)

    response = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
    ).execute()
    files = response.get('files', [])

    if files:
        # 既存のフォルダが見つかった場合
        folder_id = files[0]['id']
        print('既存の "{}" フォルダの ID を使用します: {}'.format(folder_name, folder_id))
    else:
        # フォルダが存在しない場合、新規作成
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]

        file = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = file.get('id')
        print('新規に "{}" フォルダを作成しました。ID: {}'.format(folder_name, folder_id))

    return folder_id

if __name__ == '__main__':
    main()
