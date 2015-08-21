from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import csv
### SQL ALCHEMY CONNECTION ## 
app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
from models import *

print "import started"
with open('tipsters.csv', 'rb') as csvfile:
    tipsters = csv.reader(csvfile, delimiter=",", quotechar="'")
    for tipster in tipsters:
    	newTipster = Tipster(tipster[0], tipster[1], tipster[2], tipster[3], tipster[4], tipster[5], tipster[6],
    		 tipster[7], tipster[8], tipster[9], tipster[10], tipster[11], tipster[12], tipster[13])
    	db.session.add(newTipster)
    	print "added tipster ", tipster[0]
    db.session.commit()
print "import ended"