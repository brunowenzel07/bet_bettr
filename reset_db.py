from flask import Flask
from flask_sqlalchemy import SQLAlchemy

### SQL ALCHEMY CONNECTION ## 
app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
from models import *

db.drop_all()
print "clean all"
db.create_all()
print "created all"