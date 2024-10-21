import sqlite3
from os.path import exists

from flask import Flask, render_template
import requests
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

import random

con = sqlite3.connect('justePrix.db', check_same_thread=False)

app = Flask(__name__)
app.secret_key = 'secret'

image = ""
prix = 0
nom = ""

class justePrix(FlaskForm) :
    prix_article = IntegerField('Prix de larticle' , validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def justePrixAmazon():
    global image
    global prix
    global nom

    form = justePrix()

    if form.validate_on_submit():
        if form.prix_article.data == prix:
            return "Bravo, vous avez trouvé le juste prix !"
        elif form.prix_article.data > prix:
            return "Le prix est trop grand"
        else:
            return "Le prix est trop petit"
    return render_template('game.html', form=form, prix=prix, nom=nom)

def choisirArticle():
    global image
    global prix
    global nom

    conn = sqlite3.connect('justePrix.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ARTICLE")
    nb_article = cursor.fetchone()[0]
    conn.commit()
    item_random = random.randint(1, nb_article)
    cursor.execute("SELECT * FROM ARTICLE WHERE id = %d" % item_random)
    article = cursor.fetchone()
    conn.commit()
    conn.close()
    print(article)

    nom = article[1]
    prix = article[2]


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

def getNom(article):
    r = requests.get(" http://ws.chez-wam.info/" + article)
    try:
        name = r.json()["title"]
    except:
        raise Exception("Nom de l'article n'est pas disponible !")
    return name

def creation_bd():
    try:
        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE ARTICLE(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nom_article TEXT, prix_article FLOAT)''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print("La table existe déjà")

def insertion_bd():
    liste_article = ["B000I5ZK2U", "B0B5X5KBYG", "B0CN3C6G1M", "B0BPS5392V"]
    conn = sqlite3.connect('justePrix.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM ARTICLE''')
    conn.commit()
    for i in range(len(liste_article)):
        nom_article = getNom(liste_article[i])
        prix_article = get_prix_article(liste_article[i])
        cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article) VALUES(?,?)''', (nom_article, prix_article))
    conn.commit()
    conn.close()

insertion_bd()


if not exists('justePrix.db'):
    creation_bd()

if __name__ == '__main__':
    app.run()
