import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/article/<article>')
def recupereImageArticle(article):  # put application's code here
    r = requests.get(" http://ws.chez-wam.info/" + article)
    image = r.json()["images"][0]
    return f"<img width='250px' height='250px' src='{image}'/>"