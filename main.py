#!/usr/bin/env python
# coding: utf-8

import sys
import time
import yaml
from googleapiclient.discovery import build
from lib.gmail_api_exampls import get_credential, get_target_emails, create_message, gmail_create_draft
from pyChatGPT import ChatGPT


def main():
    args = sys.argv
    cfgs = yaml.load(open('keys/params.yml'), Loader=yaml.SafeLoader)

    creds = get_credential()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    chatgpt_order = args[1]
    gmail_query = args[2] if len(args) > 2 else 'is:unread'
    gmail_tag = args[3] if len(args) > 3 else 'INBOX'

    chat_gpt_api = ChatGPT(cfgs['chatgpt_session_token'], verbose=False)  # auth with session token
    chat_gpt_api.reset_conversation()
    chat_gpt_api.clear_conversations()

    drafted_email_list = []
    while True:
        emails = get_target_emails(service, gmail_query, gmail_tag, count=3)
        for email in emails:
            if not email['id'] in drafted_email_list:
                print('Found an undraft email:', email)
                drafted_email_list.append(email['id'])

                send_data = chatgpt_order + '\n\n' + email['body']
                resp = chat_gpt_api.send_message(send_data)
                message_text = resp['message']

                message = create_message(
                    cfgs['gmail_api_sender'], email['from'], email['subject'], message_text, thread_id=email['threadId'])
                gmail_create_draft(service, "me", message)

                print('Complete saving a draft email')
        time.sleep(60)

if __name__ == '__main__':
    main()
