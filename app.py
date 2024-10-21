import sqlite3

from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

con = sqlite3.connect('justePrix.db', check_same_thread=False)

app = Flask(__name__)
app.secret_key = 'secret'

article = "B0B928B6BC"

class justePrix(FlaskForm) :
    prix_article = IntegerField('prix_article', validators=[DataRequired()])

@app.route('/')
def justePrixAmazon():
    return render_template('game.html', article=article, nom=getNom(article), image=recupereImageArticle(article))

def recupereImageArticle(article):
    r = requests.get(" http://ws.chez-wam.info/" + article)
    image = r.json()["images"][0]
    return image


def getNom(article):
    o={}

    target_url="https://www.amazon.com/dp/"+article

    headers={"accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}

    resp = requests.get(target_url, headers=headers)

    soup=BeautifulSoup(resp.text,'html.parser')

    try:
        o["title"]=soup.find('h1',{'id':'title'}).text.strip()
    except:
        o["title"]=None

    return o["title"]

print(getNom("B0B928B6BC"))

def creatation_bd():
    try:
        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE Article(id INTEGER PRIMARY KEY, nom_article TEXT, prix_article INTEGER)''')
        conn.commit()
        conn.close()
    except(sqlite3.OperationalError):
        print("La table existe déjà")

creatation_bd()

if __name__ == '__main__':
    app.run()
