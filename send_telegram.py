#!/usr/bin/env python3
import os
import sys
import requests

def send_telegram(message: str):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID 環境變數未設定", file=sys.stderr)
        sys.exit(1)

    # Telegram 單則訊息上限 4096 字元，超過則拆分發送
    max_length = 4000
    chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]

    for i, chunk in enumerate(chunks):
        response = requests.post(
            f'https://api.telegram.org/bot{token}/sendMessage',
            json={'chat_id': chat_id, 'text': chunk},
            timeout=30
        )
        if not response.ok:
            print(f"Telegram API 錯誤: {response.status_code} {response.text}", file=sys.stderr)
            sys.exit(1)

    print(f"✅ 已發送到 Telegram（共 {len(chunks)} 則）")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            message = f.read()
    else:
        message = sys.stdin.read()

    send_telegram(message)
