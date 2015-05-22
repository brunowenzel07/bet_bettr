from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)

class Country(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(60))

    def __init__(self, Name):
        self.Name = Name

class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(120))
    Name = db.Column(db.String(60))
    DateSignedUp = db.Column(db.DateTime)

    def __init__(self, Email, Name, DateSignedUp):
        self.Email = Email
        self.Name = Name
        self.DateSignedUp = DateSignedUp

class User_Countries(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Userid = db.Column(db.Integer)
    Countryid = db.Column(db.Integer)
    DateStart = db.Column(db.DateTime)
    Active = db.Column(db.Boolean)

    def __init__(self, Userid, Countryid, DateStart, Active):
        self.Userid = Userid
        self.Countryid = Countryid
        self.DateStart = DateStart
        self.Active = Active

class Racecourses(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(60), unique=True)

    def __init__(self, Name):
        self.Name = Name

class Selections(db.Model): 
    ID = db.Column(db.Integer, primary_key=True)
    Userid = db.Column(db.Integer)
    Racecourseid = db.Column(db.Integer)
    RaceDate = db.Column(db.DateTime)
    RaceNumber = db.Column(db.Integer)
    HorseNumber = db.Column(db.Integer)
    __table_args__ = (UniqueConstraint('Userid', 'Racecourseid', 'RaceDate', 'RaceNumber', 'HorseNumber'),
                     )

    def __init__(self, Userid, Racecourseid, RaceDate, RaceNumber, HorseNumber):
        self.Userid = Userid
        self.Racecourseid = Racecourseid
        self.RaceDate = RaceDate
        self.RaceNumber = RaceNumber
        self.HorseNumber = HorseNumber

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()