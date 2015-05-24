from datetime import datetime
import hashlib
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel, gettext
from sqlalchemy import UniqueConstraint
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
babel = Babel(app)
mail = Mail(app)

class Country(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(60))

    def __init__(self, Name):
        self.Name = Name

class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(120))
    Password = db.Column(db.String(120))
    Name = db.Column(db.String(60))
    DateSignedUp = db.Column(db.TIMESTAMP())

    def __init__(self, Email, Password, Name, DateSignedUp):
        self.Email = Email
        self.Password = Password
        self.Name = Name
        self.DateSignedUp = DateSignedUp

class User_Countries(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Userid = db.Column(db.Integer)
    Countryid = db.Column(db.Integer)
    DateStart = db.Column(db.TIMESTAMP())
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
    RaceDate = db.Column(db.TIMESTAMP())
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

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            #add the user to database
            newUser = User(request.form['inputEmail'], generate_password_hash(request.form['inputPassword']), request.form['inputName'], datetime(2001,01,01))
            db.session.add(newUser)
            db.session.commit()

            #generate confirmation link, code:email+hash of email+name
            confirmation_link = app.config['DOMAIN'] + 'confirmemail?email='+request.form['inputEmail']+'&code='+hashlib.md5(request.form['inputEmail']+request.form['inputName']).hexdigest()

            #send email
            msg = Message("Welcome to better app", sender=app.config['DEFAULT_MAIL_SENDER'])
            msg.add_recipient(request.form['inputEmail'])
            msg.body = 'Welcome to the app! Please go to this address to confirm your email: {0}'.format(confirmation_link)
            mail.send(msg)

            return render_template('signup.html', message=gettext('Signed up, please check email for confirmation link!'))
        except:
            return render_template('signup.html', message=gettext('Error, please try again!'))
    return render_template('signup.html', message='')

@app.route('/confirmemail')
def confirm_email():
    try:
        email = request.args.get('email')
        code = request.args.get('code')

        #get the user
        user = User.query.filter_by(Email=email).first()

        #check does the hash match
        if code == hashlib.md5(user.Email+user.Name).hexdigest():
            user.DateSignedUp = datetime.today()
            db.session.commit()
            return render_template('login.html', message=gettext('Success, your email is confirmed, please login below!'))
    except:
        return render_template('login.html', message=gettext('Error, please contact support!'))

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

if __name__ == '__main__':
    app.run()