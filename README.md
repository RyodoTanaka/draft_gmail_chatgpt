# draft_gmail_chatgpt
https://user-images.githubusercontent.com/36523448/210385782-616bdf4b-0e62-4a5d-ab3f-d06502248548.mp4

## How to use
- Create keys directory and params files.

```bash
$ mkdir keys
$ cd keys
$ vi params.yml
---
chatgpt_session_token: '<chatgpt session token>'
gmail_api_sender: '<gmail sender email address>'
```

- You should download secret file from Gmail API and place it under keys directory.
  - client_secret_**********-g*****************.apps.googleusercontent.com.json

```bash
$ ls keys
client_id.json  params.yml
```

- run.
```bash
$ python3 main.py '以下のEメールについて詳細な返信文を作成して下さい。'
Found an undraft email: {'id': '*********', 'threadId': '*********', 'body': 'ジェダイ株式会社\r\nルーク・スカイウォーカー様\r\n\r\n突然のメール失礼します。\r\n銀河帝国株式会社のダースベイダーと申します。\r\n\r\n現在弊社では、貴社の新製品「ライトセーバー」の導入を検討しております。\r\nそれに伴い、下記の内容について確認したいと存じます。\r\n\r\nライトセーバーの利用方法\r\nライトセーバーの概算お見積\r\n\r\n以上となります。\r\nお手数ですが、ご回答よろしくお願いいたします。\r\n\r\n銀河帝国株式会社\r\nダースベイダー\r\n', 'subject': 'ライトセーバーについて', 'from': '********* <*********@gmail.com>'}
Complete saving a draft email
```
