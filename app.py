from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hifuclub'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ENV'] = 'production'

db = SQLAlchemy(app)

class Zindak(db.Model):
    __table_name__ = 'zindak'
    count = db.Column(db.Integer, primary_key=True)

    def __init__(self, count, **kwargs):
        self.count = count

    def __repr__(self):
        return str(self.count)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/zindak')
def zindak():
    # return render_template('zindak.html', zindak=Zindak.query.all()[0])
    with open('zindak.txt', 'r') as f:
        s = f.read()
    with open('comments.txt', 'r', encoding='utf-8') as f:
        lst = list(f.read().split('@CSP@'))
        for i in range(len(lst)-1):
            raw = list(lst[i].split('@NSP@'))
            lst[i] = {'name':raw[0], 'text':raw[1]}
    return render_template('zindak.html', zindak=s, commlist=lst)

@app.route('/zindak/inc')
def inc():
    # Zindak.query.first().count = Zindak.query.first().count + 1
    # db.session.commit()
    with open('zindak.txt', 'r') as f:
        s = f.read()
    with open('zindak.txt', 'w') as f:
        f.write(str(int(s)+1))
    return redirect(url_for('zindak'))

@app.route('/zindak/post', methods=['POST'])
def post():
    with open('comments.txt', 'a', encoding='utf-8') as f:
        f.write(request.form['name']+'@NSP@'+request.form['text']+'@CSP@\n')
    return redirect(url_for('zindak'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
