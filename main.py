from bs4 import BeautifulSoup
from flask import Flask, request
from config import TELEGRAM_BOT_TOKEN, LINKEDIN_URL
import requests


app = Flask(__name__)


def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


def pars_data(job_name: str):
    url = f'{LINKEDIN_URL}{job_name.replace(" ", "%20")}'
    request_data = requests.get(url)
    bs = BeautifulSoup(request_data.text, 'html.parser')

    all_links = bs.find_all('a', class_='base-card__full-link')
    return all_links


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        chat_id = request.json["message"]["chat"]["id"]
        if request.json["message"]["text"] == '/start':
            send_message(chat_id, 'hi there')
        else:
            text = request.json["message"]["text"]
            try:
                all_links = pars_data(text)
                for i in range(3):
                    send_message(chat_id, f"{all_links[i].text}{all_links[i]['href']}")
            except:
                send_message(chat_id, 'not a single vacancy')
    return {"ok": True}


if __name__ == '__main__':
    app.run(port=5500, debug=True)
