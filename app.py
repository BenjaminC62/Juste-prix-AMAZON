import sqlite3
from os.path import exists

from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

con = sqlite3.connect('justePrix.db', check_same_thread=False)

app = Flask(__name__)
app.secret_key = 'secret'

article = "B000I5ZK2U"

class justePrix(FlaskForm) :
    prix_article = IntegerField('prix_article', validators=[DataRequired()])

@app.route('/')
def justePrixAmazon():
    return render_template('game.html', article=article, nom=getNom(article), image=recupereImageArticle(article))

def recupereImageArticle(article):
    r = requests.get(" http://ws.chez-wam.info/" + article)
    image = r.json()["images"][0]
    return image

def get_prix_article(article):
    r = requests.get(" http://ws.chez-wam.info/" + article)
    try:
        price = r.json()["price"][:-1] # récupère le prix de l'article
        for i in price:
            if i == ",":
                price = price.replace(i, ".")
            elif i == " ":
                price = price.replace(i, "")
        result = float(price) # converti la valeur du prix en str -> float
        print(type(result))
    except:
        raise Exception("Prix de l'article n'est pas disponible !")
    return result

print(get_prix_article("B000I5ZK2U"))

def getNom(article):
    r = requests.get(" http://ws.chez-wam.info/" + article)
    try:
        name = r.json()["title"]
    except:
        raise Exception("Nom de l'article n'est pas disponible !")
    return name

print(getNom("B000I5ZK2U"))

def creation_bd():
    try:
        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE ARTICLE(id INTEGER PRIMARY KEY, nom_article TEXT, prix_article FLOAT)''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print("La table existe déjà")


def insertion_bd(article):
    nom_article = getNom(article)
    prix_article = get_prix_article(article)

    conn = sqlite3.connect('justePrix.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO ARTICLE(id,nom_article, prix_article) VALUES(?,?,?)''', (1, nom_article, prix_article))
    conn.commit()
    conn.close()

insertion_bd(article)

if not exists('justePrix.db'):
    creation_bd()

if __name__ == '__main__':
    app.run()
