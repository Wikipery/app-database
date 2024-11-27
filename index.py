import os
from dotenv import load_dotenv
load_dotenv()

import gevent
from gevent import monkey
monkey.patch_all()

import httpx
import urllib.parse
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

SERVICE_POST = os.environ["SERVICE_POST"]

app = Flask(__name__)

@app.route("/")
def home():
    return "server is up"

def get_content(title, lang):
    """ 
    Fetching the data content from Wikipedia's open API source.
    Title: (title) refers to the title of the article.
    Language: (lang) refers to the lang we want the content to display.
    """
    
    encoded_title = urllib.parse.quote(title)
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/html/{encoded_title}"

    try:
        with httpx.Client() as client:
            response = client.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"This is the response status: {response.status_code}")

            first_paragraph = soup.find('p')

            print(f"First paragraph: {first_paragraph}")

            return first_paragraph.text if first_paragraph else "No content found."
        else:
            return f"Error: {response.status_code} - {response.text}"

    except httpx.RequestError as e:
        return f"There was a network error: {e}"

@app.route("/wikipedia/<title>", methods=['GET'])
def handle_get_data(title):
    lang = request.args.get('lang', default='en')

    result = get_content(title, lang)
    if 'error' in result:
        return jsonify({"error": result}), 500

    return jsonify({"content": result})

if __name__ == "__main__":
    from gevent.pywsgi import WSGIServer
    # Use Gevent to run Flask as a server handling async operations in the background
    http_server = WSGIServer(('0.0.0.0', int(SERVICE_POST)), app)
    http_server.serve_forever()
