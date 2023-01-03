# Reference: 
# https://developers.google.com/gmail/api/guides/
# https://qiita.com/muuuuuwa/items/822c6cffedb9b3c27e21
# https://qiita.com/sho0405/items/6b5e9f739917e0a6305f


import base64
import csv
import io
import json
import logging
import os
import os.path
import pickle
from apiclient import errors
from docopt import docopt
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


SCOPES = [
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.modify',
]


def get_credential():
    '''
    アクセストークンの取得

    カレントディレクトリに pickle 形式でトークンを保存し、再利用できるようにする。（雑ですみません。。）
    '''
    creds = None
    if os.path.exists('keys/token.pickle'):
        with open('keys/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('keys/client_id.json', SCOPES)
            # creds = flow.run_local_server()
            creds = flow.run_console()
        with open('keys/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def list_labels(service, user_id):
    '''
    label のリストを取得する
    '''
    labels = []
    response = service.users().labels().list(userId=user_id).execute()
    return response['labels']


def decode_base64url_data(data):
    '''
    base64url のデコード
    '''
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_message = decoded_bytes.decode('UTF-8')
    return decoded_message


def list_message(service, user_id, query, label_ids=[], count=3):
    '''
    メールのリストを取得する

    Parameters
    ----------
    service : googleapiclient.discovery.Resource
        Gmail と通信するためのリソース
    user_id : str
        利用者のID
    query : str
        メールのクエリ文字列。 is:unread など
    label_ids : list
        検索対象のラベルを示すIDのリスト
    count : str
        リターンするメール情報件数の上限

    Returns
    ----------
    messages : list
        id, body, subject, from などのキーを持った辞書データのリスト
    '''
    messages = []
    try:
        message_ids = (
            service.users()
            .messages()
            .list(userId=user_id, maxResults=count, q=query, labelIds=label_ids)
            .execute()
        )

        if message_ids['resultSizeEstimate'] == 0:
            logger.warning('no result data!')
            return []

        # message id を元に、message の内容を確認
        for message_id in message_ids['messages']:
            message_detail = (
                service.users()
                .messages()
                .get(userId='me', id=message_id['id'])
                .execute()
            )
            message = {}
            message['id'] = message_id['id']
            message['threadId'] = message_detail['threadId']
            # 単純なテキストメールの場合
            if 'data' in message_detail['payload']['body']:
                message['body'] = decode_base64url_data(
                    message_detail['payload']['body']['data']
                )
            # html メールの場合、plain/text のパートを使う
            else:
                parts = message_detail['payload']['parts']
                parts = [part for part in parts if part['mimeType'] == 'text/plain']
                message['body'] = decode_base64url_data(
                    parts[0]['body']['data']
                    )
            # payload.headers[name: 'Subject']
            message['subject'] = [
                header['value']
                for header in message_detail['payload']['headers']
                if header['name'] == 'Subject'
            ][0]
            # payload.headers[name: 'From']
            message['from'] = [
                header['value']
                for header in message_detail['payload']['headers']
                if header['name'] == 'From'
            ][0]
            logger.info(message_detail['snippet'])
            messages.append(message)
        return messages

    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_target_emails(service, query='is:unread', tag='INBOX', count=3):
    labels = list_labels(service, 'me')
    target_label_ids = [label['id'] for label in labels if label['name'] == tag]
    messages = list_message(service, 'me', query, target_label_ids, count=count)
    return messages


def create_message(sender, to, subject, message_text, cc=None, thread_id=None, enc='utf-8'):
    message = MIMEText(message_text.encode(enc), _charset=enc)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if cc:
        message['Cc'] = cc
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()  # MIMEText を base64 エンコードする

    message_body = {
        'message': {
            'raw': encoded_message
        }
    }
    if thread_id:
        message_body['message']['threadId'] = thread_id

    return message_body


def gmail_create_draft(service, user_id, message_body):
    try:
        draft = service.users().drafts().create(userId=user_id, body=message_body).execute()
    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None
    return draft


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    query = arguments['<query>']
    tag = arguments['<tag>']
    count = arguments['<count>']
    logging.basicConfig(level=logging.DEBUG)

    creds = get_credential()
    service = build('gmail', 'v1', credentials=creds, cache_discovery=False)

    messages_ = get_target_email(service, query=query, tag=tag, count=count)
    print(messages_)
