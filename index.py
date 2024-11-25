from dotenv import load_dotenv
load_dotenv()
import os

from flask import Flask, request, jsonify

import asyncio
import httpx
import urllib.parse

SERVICE_POST = os.environ["SERVICE_POST"]

app = Flask(__name__)

@app.route("/")
def home():
    return "server is up"

def get_content(title, lang):
    print(f"we are here")
    return True

@app.route("/wikipedia/<title>", methods=['GET'])
def handle_get_data(title):
    lang = request.args.get('lang', default='en')

    ans = get_content(title, lang)
    if ans is None:
        return "There was issue with the content"

    return True 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=SERVICE_POST ,debug=True)