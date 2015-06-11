import csv
from datetime import datetime
import re
from models import *

tips_file = "TIPSDATA20150611.csv"
csv_file = csv.DictReader(open(tips_file, 'rU'), delimiter=',')

user_names = [
"PAUL LALLY","CLINT HUTCHINSON","BRETT DAVIS", "ALAN AITKEN", "MICHAEL COX", "ANDREW HAWKINS", 
"PHILLIP WOO",	"SHANNON",	"RPONLINE"]
user_animals = [
"The Fox", "The Rabbit", "The Sloth", "The Eagle", "The Giraffe", "The Vole", "The Wolf", "The Pigeon", "The Bat"
]


for name_, animal_ in zip(user_names, user_animals):
	users = {}
	users["Name"] = name_
	users["Animal"] = animal_
	users["DateSignedUp"] = datetime.strptime('20150611', "%Y%m%d")
	users["Email"] = None
	users["Password"] = None
#create user from user_names and user_animals NO EMAIL! NO PASS NO DateSignedUp
 	user = User(**users)
 	db.session.add(user)
 	db.session.commit()





# selections = {}

# ##create Users from headers
# dbsession = DBSession()





'''
	Selection
    Userid = db.Column(db.Integer)
    Racecourseid = db.Column(db.Integer)
    RaceDate = db.Column(db.TIMESTAMP())
    RaceNumber = db.Column(db.Integer)
    First = db.Column(db.Integer)
    Second = db.Column(db.Integer)
    Third = db.Column(db.Integer)
    Fourth = db.Column(db.Integer)
'''
for row in csv_file:
	for key, value in row.items():
		if key == "RACEDATE|RACECODE|RACENUMBER":
			# print key, value
			if value != '':
				m = re.match(r"^(?P<racedate>\d+)(?P<racecoursecode>HV|ST)(?P<racenumber>\d+)", value)
				racedate_ = datetime.strptime(m.group("racedate"), "%Y%m%d")
				# .strftime("%d%m%y")
				racecoursecode_ = m.group("racecoursecode")
				racenumber_ = int(m.group("racenumber"))
				selections["racedate"] = racedate_
				selections["racecoursecode"] = racecoursecode_
				selections["racenumber"] = racenumber_
				# selections["userid"] = dbsession.query(User.filter_by(name = value).first()
 				print racedate, racecoursecode, racenumber
			# print m.group("racecoursecode")
		##remaining keys