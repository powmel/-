import requests
import json
import os
from datetime import datetime

def start_conversation(api_key):
    url = 'http://localhost/v1/chat-messages'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'inputs': {},
        'query': 'Dify_docs_Developing with APIs',
        'response_mode': 'streaming',
        'user': 'abc-123'
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        #ストリーミングレスポンスを処理
        for line in response.iter_lines():
            #print(line)
            if line:
                try:
                    decoded_line = json.loads(line.decode('utf-8').lstrip('data: '))
                    if 'conversation_id' in decoded_line:
                        return decoded_line['conversation_id']
                except json.JSONDecodeError:
                    print("Received non-JSON data:", line.decode('utf-8'))
    else:
        print(f"Failed to start conversation: {response.status_code} {response.text}")
        return None

def send_message_to_chat(api_key, message, conversation_id):
    url = 'http://localhost/v1/chat-messages'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'inputs': {},
        'query': message,
        'response_mode': 'streaming',
        'conversation_id': conversation_id,
        'user': 'abc-123'
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                try:
                    decoded_line = json.loads(line.decode('utf-8').lstrip('data: '))
                    if decoded_line.get('event') == 'message_file' and decoded_line.get('type') == 'image':
                        original_url = decoded_line['url']
                        #URLを修正
                        corrected_url = f"http://localhost{original_url}"
                        print(corrected_url)
                        #画像を保存するパス
                        current_dir = os.path.dirname(__file__)
                        img_dir = os.path.join(current_dir, 'img')
                        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                        save_path = os.path.join(img_dir, f"{timestamp}.jpg")
                        #画像をダウンロードして保存
                        save_image_from_url(corrected_url, save_path)
                        print(f"Image saved to {save_path}")
                except json.JSONDecodeError:
                    print("Received non-JSON data:", line.decode('utf-8'))
    else:
        print(f"Failed to send message: {response.status_code} {response.text}")

def save_image_from_url(url, save_path):
    #保存先のディレクトリを確認し、存在しない場合は作成
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image: {response.status_code}")

#APIキー
api_key = 'XXX' #変更点1：APIキーを入れる

#新しい会話を開始
conversation_id = start_conversation(api_key)
if conversation_id:
    送信するメッセージ
    message = '犬と猫が戯れている' #変更点2：作りたい画像を入れる
    #メッセージを送信して結果を表示
    send_message_to_chat(api_key, message, conversation_id)
else:
    print("Failed to start a new conversation.")
