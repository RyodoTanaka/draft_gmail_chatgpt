# draft_gmail_chatgpt
https://user-images.githubusercontent.com/36523448/210385782-616bdf4b-0e62-4a5d-ab3f-d06502248548.mp4

## How to use
### Get chatGPT session token
You need to go browser's coockie page to get a chatgpt session token as shown like following.
1. Go to the [chatGPT page](https://chat.openai.com/chat) and login (or register) 

2. Open coockie page, and get a value of "__Secure-next-auth.session-token".
  ![Screenshot from 2023-01-04 13-10-58](https://user-images.githubusercontent.com/8377208/210483438-6537fd2e-4e92-4606-a8e5-0eaebbda9d03.png)
  ![Screenshot from 2023-01-04 13-11-38](https://user-images.githubusercontent.com/8377208/210483481-cbd7ab04-8fa5-4256-b93c-e6fe20929592.png)

### Set chatGPT session parameters
Create keys directory and params files.  
- `chatgpt_session_token`: copied value from above.
- `gmail_api_sender`: the mail address to login chatGPT.

```bash
$ mkdir keys
$ cd keys
$ vi params.yml
---
chatgpt_session_token: '<chatgpt session token>'
gmail_api_sender: '<gmail sender email address>'
```

### Set Gmail API
You should download secret file from Gmail API and place it under keys directory.  
1. To get an Gmail API, you should follow the process written in [the Qiita page (Japanese)](https://qiita.com/muuuuuwa/items/822c6cffedb9b3c27e21#2020%E5%B9%B46%E6%9C%8814%E6%97%A5%E7%8F%BE%E5%9C%A8%E4%B8%8B%E8%A8%98%E3%81%AE%E6%89%8B%E9%A0%86%E3%81%A7%E3%82%A6%E3%82%A3%E3%82%B6%E3%83%BC%E3%83%89%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B%E3%81%A8%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%8C%E7%99%BA%E7%94%9F%E3%81%99%E3%82%8B%E3%82%88%E3%81%86%E3%81%A7%E3%81%99%E4%B8%8B%E8%A8%98%E6%89%8B%E9%A0%86%E3%81%A7%E5%9B%9E%E9%81%BF%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%97%E3%81%9F).  
2. Then get the secret key as `json` file which should be like `client_secret_**********-g*****************.apps.googleusercontent.com.json`  
3. Finally, rename `client_secret_**********-g*****************.apps.googleusercontent.com.json` to `client_id.json` and place it into the `keys` directory.
4. You should have at least following files.
  ```bash
  $ ls keys
  client_id.json  params.yml
  ```
### Run the code
```bash
$ python3 main.py '以下のEメールについて詳細な返信文を作成して下さい。'
Found an undraft email: {'id': '*********', 'threadId': '*********', 'body': 'ジェダイ株式会社\r\nルーク・スカイウォーカー様\r\n\r\n突然のメール失礼します。\r\n銀河帝国株式会社のダースベイダーと申します。\r\n\r\n現在弊社では、貴社の新製品「ライトセーバー」の導入を検討しております。\r\nそれに伴い、下記の内容について確認したいと存じます。\r\n\r\nライトセーバーの利用方法\r\nライトセーバーの概算お見積\r\n\r\n以上となります。\r\nお手数ですが、ご回答よろしくお願いいたします。\r\n\r\n銀河帝国株式会社\r\nダースベイダー\r\n', 'subject': 'ライトセーバーについて', 'from': '********* <*********@gmail.com>'}
Complete saving a draft email
```
