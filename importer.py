import csv
from datetime import datetime
import re
from models import *
from sqlalchemy import func
import pprint
from querycode import * 

## sqlalchemy 
## USER
## RACEDAY
## RACE
## SELECTION

now = datetime.now()


user_names = [
"PAUL LALLY","CLINT HUTCHINSON","BRETT DAVIS", "ALAN AITKEN", "MICHAEL COX", "ANDREW HAWKINS", 
"PHILLIP WOO",	"SHANNON",	"RPONLINE"]
user_animals = [
"The Fox", "The Rabbit", "The Sloth", "The Eagle", "The Giraffe", "The Vole", "The Wolf", "The Pigeon", "The Bat"
]


# q= db.session.query(User).filter(User.Name == 'PAUL LALLY')
# print q
# if not db.session.query(q.exists()): 
for name_, animal_ in zip(user_names, user_animals):
	users = {}
	users["Name"] = name_
	users["Animal"] = animal_
	users["DateSignedUp"] = now #datetime.strptime('20150612', "%Y%m%d")
	users["Email"] = None
	users["Password"] = None
#create user from user_names and user_animals NO EMAIL! NO PASS NO DateSignedUp
 	user_ = User(**users)
 	u = get_or_create(db.session,User,**users)

assert db.session.query(func.count(User.ID)).first() == (9,)

tips_file = "TIPSDATA20150611.csv"
csv_file = csv.DictReader(open(tips_file, 'rU'), delimiter=',')
for row in csv_file:
	races = {}
	racedays = {}
	for key, value in row.items():
		if key == "RACEDATE|RACECODE|RACENUMBER" and value != '':
			# RACEDAY
			m = re.match(r"^(?P<racedate>\d+)(?P<racecoursecode>HV|ST)(?P<racenumber>\d+)", value)
			racedate_ = datetime.strptime(m.group("racedate"), "%Y%m%d")
			# .strftime("%d%m%y")
			racecoursecode_ = m.group("racecoursecode")
			racenumber_ = int(m.group("racenumber"))
			##LOOK FOR RACEDAYID
			racedays["RaceDate"] = racedate_
			racedays["RaceCourseCode"] = racecoursecode_
			racedayid_ = get_or_create(db.session,RaceDay, **racedays)
			races["RaceDayID"] = racedayid_.ID #RaceDayID
			races["RaceNumber"] = racenumber_
			races["RaceDate"] = racedate_
			races["RaceCourseCode"] = racecoursecode_
		if key == 'RESULT' and value != '':
			races["Result"] = str(value)
			races['R1'] = value.split('-')[0]
			races['R2'] = value.split('-')[1]
			races['R3'] = value.split('-')[2]
			races['R4'] = value.split('-')[3]
		if key == 'WINODDS' and value != '':
			races["WinOdds"] = float(value) 
		if key == 'FAVPOS' and value != '':
			races["FavPos"] = int(value)
		if key == 'NORUNNERS' and value != '':
			races["NoRunners"] = int(value)
		if key == 'FAVODDS' and value != '':
			races["FavOdds"] = float(value)
	# pprint.pprint(races)
	r = get_or_create(db.session,Race, **races)

	# pprint.pprint(races)
nth = {
    1: "First",
    2: "Second",
    3: "Third",
    4: "Fourth"
}

# We have raceday, race and user


csv_file2 = csv.DictReader(open(tips_file, 'rU'), delimiter=',')
# ##ROUND2
record_count = 0
for row in csv_file2:
	# races_ = {}
	selections = {}
	users = {}
	for key, value in row.items():
		record_count +=1
		# pprint.pprint(key)
		# print ">>>>>>>>>>>>>>>>>>>>"
		# pprint.pprint(value)
		if key or value == '':
			pass
		if key == "RACEDATE|RACECODE|RACENUMBER" and value != '' and value != 'NONE':
			# print key, value
			m = re.match(r"^(?P<racedate>\d+)(?P<racecoursecode>HV|ST)(?P<racenumber>\d+)", value)
			racedate_ = datetime.strptime(m.group("racedate"), "%Y%m%d")
			# .strftime("%d%m%y")
			racecoursecode_ = m.group("racecoursecode")
			racenumber_ = int(m.group("racenumber"))
			races["RaceDate"] = racedate_
			races["RaceCourseCode"] = racecoursecode_
			races["RaceNumber"] = racenumber_

			# selections["RaceID"] = get_or_create(db.session,Race, **races_).ID
			# selections["RaceID"] = db.session.query(Race.ID).filter_by(RaceDate = racedate_, RaceCourseCode= racecoursecode_, RaceNumber= racenumber_).first().ID
 		if key in user_names and value != '':
 			# pprint.pprint(key)
 			users["Name"] = key
			# userid_ = db.session.query(User.ID).filter_by(Name = key).first()
			userid_ = get_id(db.session,User, **users)
			selections["UserID"] = userid_
			value = value.replace(' ', '').replace('+', '')
			tips_ = value.split('-')
			selections['First'] = int(tips_[0])
			selections['Second'] = int(tips_[1])
			selections['Third'] = int(tips_[2]) if tips_[2] != '' else None
			selections['Fourth'] = int(tips_[3]) if len(tips_) ==4 and tips_[3] != '' else None
			selections["SubmittedAt"] = now
		pprint.pprint(selections)
		## should: get THIS RACE STATS NOT all race stats
		selections["RaceID"] =  get_id(db.session,Race, RaceDate=racedate_, RaceCourseCode=racecoursecode_, RaceNumber=racenumber_)
		

		if len(selections) >2:
			s = get_or_create(db.session,Selection, **selections)
		# pprint.pprint(races)
		# pprint.pprint(selections)
	
	# pprint.pprint(s)
	# pprint.pprint(record_count)
