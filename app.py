from random import randrange
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

app.secret_key = b'Y5^osfE==t[1uo'

conn = sqlite3.connect("highscore.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS 
    user(name text, versuche int)""")

versuche = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        name = session["username"]
        if request.method == 'POST':
            newNumber = request.form['number']
            print(session["randomZahl"])
            if newNumber != "":
                newNumber = int(newNumber)
                global versuche
                versuche+=1

                guess = evaluateInput(input=newNumber)
                match guess:
                    case 0:
                        saveToDb(name=versuche,versuche=versuche)
                        altVersuche =versuche
                        versuche = 0
                        print(name)                   
                        session["randomZahl"] = randrange(0, 100)
                        highscore = getHighscore()
                        return render_template('index.html', richtig=True, aktuelleZahl=newNumber, versuche=altVersuche, highscore=highscore, username=name)
                    case 1:
                        return render_template('index.html', hoeher=True, aktuelleZahl=newNumber, versuche=versuche, username=name)
                    case 2:
                        return render_template('index.html', tiefer=True, aktuelleZahl=newNumber, versuche=versuche, username=name)
              
        else:
            return render_template('index.html', username=name)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session["randomZahl"] = randrange(0, 100)
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

def evaluateInput(input):
    if input <= 100 and input >= 0:
        if input == session["randomZahl"]:
            return 0
        elif input < session["randomZahl"]:
            return 1
        else:
            return 2

def saveToDb(name, versuche):
    c.execute("INSERT INTO user (name, versuche) VALUES(:name,:versuche)", {'name':name, 'versuche':versuche})
    conn.commit()

def getHighscore():
    highscore = c.execute("SELECT name, versuche FROM user ORDER BY versuche ASC LIMIT 10")
    highscore = highscore.fetchall()
    return highscore