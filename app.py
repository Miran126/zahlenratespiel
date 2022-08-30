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




randomZahl = randrange(0, 100)
versuche = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        name = session["username"]
        if request.method == 'POST':
            newNumber = request.form['number']
            print(randomZahl)
            if newNumber != "":
                newNumber = int(newNumber)
                if newNumber <= 100 and newNumber >= 0:
                    global versuche
                    versuche+=1
                    if newNumber == randomZahl:
                        c.execute(
                        "INSERT INTO user (name, versuche) VALUES(:name,:versuche)", 
                        {'name':name, 'versuche':versuche})
                        res= c.execute("SELECT name, versuche FROM user")
                        print(res.fetchall())
                        altVersuche =versuche
                        versuche = 0
                        conn.commit()
                        print(name)
                        return render_template('index.html', richtig=True, aktuelleZahl=newNumber, versuche=altVersuche, highscore=res.fetchall(), username=name)
                    elif newNumber > randomZahl:
                        return render_template('index.html', tiefer=True, aktuelleZahl=newNumber, versuche=versuche, username=name)
                    elif newNumber < randomZahl:
                        return render_template('index.html', hoeher=True, aktuelleZahl=newNumber, versuche=versuche, username=name)
                else:
                    return render_template('index.html', username=name)
        else:
            return render_template('index.html', username=name)
    return redirect('/login')

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))