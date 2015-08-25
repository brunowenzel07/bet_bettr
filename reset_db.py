from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

### SQL ALCHEMY CONNECTION ## 
app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
from models import *

table_sql='''SELECT table_name FROM information_schema.tables
 WHERE table_schema='public' AND table_type != 'VIEW' AND table_name NOT LIKE 'pg_ts_%%'
'''
for table in [name for (name, ) in db.engine.execute(text(table_sql))]:
	try:
		db.engine.execute(text('DROP TABLE %s CASCADE' % table))
	except SQLAlchemyError, e:
		print e


# db.reflect_all()
db.drop_all()
print "clean all"
db.create_all()
print "created all"