from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from datetime import datetime, timedelta

app = Flask(__name__)

datapath = path.join(path.abspath('..'), 'data')

app.config['SECRET_KEY'] = 'hifuclub'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+path.join(datapath, 'site.db')
app.config['FLASK_ENV'] = 'production'

db = SQLAlchemy(app)

class Zindak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Zindak('{self.id}', '{self.username}', '{self.content}', '{self.pub_date}')>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/zindak')
def zindak():
    # return render_template('zindak.html', zindak=Zindak.query.all()[0])
    with open(path.join(datapath, 'zindak.txt'), 'r') as f:
        s = f.read()
    # with open(path.join(datapath, 'comments.txt'), 'r', encoding='utf-8') as f:
    #     lst = list(f.read().split('@CSP@'))
    #     for i in range(len(lst)-1):
    #         raw = list(lst[i].split('@NSP@'))
    #         lst[i] = {'name':raw[0], 'text':raw[1]}
    lst = Zindak.query.all()
    for i in lst:
        i.pub_date += timedelta(hours=9)
    return render_template('zindak.html', zindak=s, commlist=list(reversed(lst)))

@app.route('/zindak/inc')
def inc():
    # Zindak.query.first().count = Zindak.query.first().count + 1
    # db.session.commit()
    with open(path.join(datapath, 'zindak.txt'), 'r') as f:
        s = f.read()
    with open(path.join(datapath, 'zindak.txt'), 'w') as f:
        f.write(str(int(s)+1))
    return redirect(url_for('zindak'))

@app.route('/zindak/post', methods=['POST'])
def post():
    db.session.add(Zindak(id = str(Zindak.query.count()+1), username=request.form['name'], content=request.form['text']))
    db.session.commit()
    db.session.close()
    #with open(path.join(datapath, 'comments.txt'), 'a', encoding='utf-8') as f:
    #     f.write(request.form['name']+'@NSP@'+request.form['text']+'@CSP@\n')
    return redirect(url_for('zindak'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
