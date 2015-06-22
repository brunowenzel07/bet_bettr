from datetime import datetime, timedelta
import hashlib
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel, gettext
import os
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.sql' #os.environ['DATABASE_URL']
db = SQLAlchemy(app)
from models import *
babel = Babel(app)
mail = Mail(app)

try:
    db.drop_all()
    db.create_all()
except Exception, e:
    print str(e)

@app.route('/')
def index():
    if 'username' in session:
        try:
            user = User.query.filter_by(Email=session['username']).first()
            return render_template('dashboard.html', user=user)
        except:
            return redirect('/logout')
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = User.query.filter_by(Email=request.form['inputEmail']).first()
            if check_password_hash(user.Password, request.form['inputPassword']):
                #check if user is active
                if user.DateSignedUp == datetime(2001,01,01):
                   return render_template('login.html', message=gettext('Your account is not activated yet, please check your email for activation link!'))
                session['username'] = user.Email
                return redirect('/')
            print("passmismatch")
            return render_template('login.html', message=gettext('Please try again!'))
        except Exception, e:
            print str(e)
            return render_template('login.html', message=gettext('Please try again!'))
    return render_template('login.html')

@app.route('/show')
def show():
    if 'username' in session:
        try:
            user = User.query.filter_by(Email=session['username']).first()
            racecourse = Racecourses.query.subquery()
            selections = db.session.query(Selections, racecourse.c.RaceDate, racecourse.c.RaceCourseCode, racecourse.c.RaceNumber, racecourse.c.Result, racecourse.c.WinOdds, racecourse.c.FavPos, racecourse.c.FavOdds, racecourse.c.NoRunners).filter(Selections.Userid==user.ID).outerjoin(racecourse, Selections.Racecourseid == racecourse.c.ID)
            return render_template('show.html', user=user, selections = selections)
        except:
            return redirect('/logout')
    else:
        return render_template('index.html')

@app.route('/racedaycourse', methods=['GET', 'POST'])
def racedaycourse():
    if 'username' in session:
        try:
            user = User.query.filter_by(Email=session['username']).first()
            if request.method == 'POST':
                racedate_min = datetime.strptime(request.form['date'], "%m/%d/%Y") + timedelta(seconds=-1)
            else:
                racedate_min = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d") + timedelta(seconds=-1)
            racedate_max = racedate_min + timedelta(days=1)
            races = Race.query.filter(Race.RaceDate>=racedate_min,Race.RaceDate<=racedate_max).all()

            #get the selections user already made
            selections = {}
            sels = Selections.query.filter_by(Userid=user.ID).all()
            for s in sels:
                selections[s.Racecourseid] = [s.First, s.Second, s.Third, s.Fourth]
            return render_template('racedaycourse.html', user = user, races = races, selections=selections,current_date=racedate_max.strftime("%m/%d/%Y"))
        except Exception, e:
            return str(e)
            # return redirect('/logout')
    else:
        return render_template('index.html')

@app.route('/updateselection', methods=['POST'])
def updateselection():
    if 'username' in session:
        try:
            user = User.query.filter_by(Email=session['username']).first()
            race = Race.query.filter_by(ID=request.form['race_id']).first()
            try:
                first = request.form['race_first']
            except:
                first = 0
            try:
                second = request.form['race_second']
            except:
                second = 0
            try:
                third = request.form['race_third']
            except:
                third = 0
            try:
                fourth = request.form['race_fourth']
            except:
                fourth = 0

            #check is there a selection for this user and this racecourse code already made, if so remove it
            oldSelection = Selections.query.filter_by(Userid=user.ID,Racecourseid=race.RaceCourseCode).first()
            if oldSelection:
                db.session.delete(oldSelection)
                db.session.commit()
            newSelection = Selections(user.ID, race.RaceCourseCode, race.RaceDate, race.RaceNumber, first, second, third, fourth, 0, 0, 0, 12)
            db.session.add(newSelection)
            db.session.commit()
            return "1"
        except Exception, e:
            print str(e)
            # return "0"
    else:
        return "0"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

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
        except Exception, e:
            print str(e)
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
    except Exception, e:
        print str(e)
        return render_template('login.html', message=gettext('Error, please contact support!'))

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

if __name__ == '__main__':
    app.run()