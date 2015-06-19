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
	# db.session.add(user)
	 	# db.session.commit()

#check if users are OK (should be 9)
# print db.session.query(func.count(User.ID)).first()
assert db.session.query(func.count(User.ID)).first() == (9,)
# assert Selections.query.filter_by(Userid=user.ID,Racecourseid=race.RaceCourseCode).first()








### create races
# for row in csv_file:
# 	racedays = {}
# 	for key, value in row.items():
# 		if key == "RACEDATE|RACECODE|RACENUMBER" and value != '':
# 			# RACEDAY
# 			m = re.match(r"^(?P<racedate>\d+)(?P<racecoursecode>HV|ST)(?P<racenumber>\d+)", value)
# 			racedate_ = datetime.strptime(m.group("racedate"), "%Y%m%d")
# 			# .strftime("%d%m%y")
# 			racecoursecode_ = m.group("racecoursecode")
# 			racenumber_ = int(m.group("racenumber"))
# 			racedays["RaceDate"] = racedate_
# 			racedays["RaceCourseCode"] = racecoursecode_
# 			# racedays["RaceNumber"] = racenumber_
# 	rd =get_or_create(db.session,RaceDay, **racedays)

##RACES NEED RACEDAY ID

# with open(tips_file, 'rU') as csvfile:
# 	reader = csv.DictReader(csvfile)
# 	for row in reader:
# 		races = {}
# 		racedays = {}
# 		selections = {}
# 		#each row is a dictionary key(header): value
# 		#get keys for race, create race get id
# 		raceinfo_ = row['RACEDATE|RACECODE|RACENUMBER']
# 		if raceinfo_ != '' or raceinfo_ is not None:
# 			m = re.match(r"^(?P<racedate>\d+)(?P<racecoursecode>HV|ST)(?P<racenumber>\d+)", raceinfo_)
# 			racedate_ = datetime.strptime(m.group("racedate"), "%Y%m%d")
# 			racecoursecode_ = m.group("racecoursecode")
# 			racenumber_ = int(m.group("racenumber"))
# 			racedays["RaceDate"] = racedate_
# 			racedays["RaceCourseCode"] = racecoursecode_
# 			racedayid_ = get_or_create(db.session,RaceDay, **racedays)
# 		#get k for User get id
# 			races["RaceDayID"] = racedayid_.ID #RaceDayID
# 			races["RaceNumber"] = racenumber_
# 			races["Result"] = row['RESULT']
# 			races["WinOdds"] = row['WINODDS']
# 			races['FavPos'] = row['FAVPOS']
# 			races['NoRunners'] = row['NORUNNERS']
# 			races['FavOdds'] = row['FAVODDS']
# 			r = get_or_create(db.session,Race, **races)

### RACEDAYS AND RACES
##THIS WORKS DONT CHANGE IT!!
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
		if key == "RACEDATE|RACECODE|RACENUMBER" and value != '':
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
			###GET
			selections["RaceID"] =  get_id(db.session,Race, **races)
			# selections["RaceID"] = db.session.query(Race.ID).filter_by(RaceDate = racedate_, RaceCourseCode= racecoursecode_, RaceNumber= racenumber_).first().ID
 		if key in user_names and value != '':
 			# pprint.pprint(key)
 			users["Name"] = key
			# userid_ = db.session.query(User.ID).filter_by(Name = key).first()
			userid_ = get_id(db.session,User, **users)
			selections["UserID"] = userid_
			# selections["tipster"] = key
			# selections["tips"] = value
			tips_ = value.split('-')
			selections['First'] = int(tips_[0])
			selections['Second'] = int(tips_[1])
			selections['Third'] = int(tips_[2])
			selections['Fourth'] = int(tips_[3]) if len(tips_) ==4 else None
			selections["SubmittedAt"] = now
		pprint.pprint(selections)
		if len(selections) >0:
			s = get_or_create(db.session,Selection, **selections)
		# pprint.pprint(races)
		# pprint.pprint(selections)
	
	# pprint.pprint(s)
	# pprint.pprint(record_count)

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


##SELECTIONS GET USERID RACEID

# for row in csv_file:
# 	selections = {}
# 	for key, value in row.items():
# 		if key == "RACEDATE|RACECODE|RACENUMBER":
# 			# print key, value
# 			if value != '':
# 				m = re.match(r"^(?P<racedate>\d+)(?P<racecoursecode>HV|ST)(?P<racenumber>\d+)", value)
# 				racedate_ = datetime.strptime(m.group("racedate"), "%Y%m%d")
# 				# .strftime("%d%m%y")
# 				racecoursecode_ = m.group("racecoursecode")
# 				racenumber_ = int(m.group("racenumber"))
# 				selections["racedate"] = racedate_
# 				selections["racecoursecode"] = racecoursecode_
# 				selections["racenumber"] = racenumber_
# 				# selections["userid"] = dbsession.query(User.filter_by(name = value).first()
#  		if key in user_names and value != '':
# 			userid_ = db.session.query(User.ID).filter_by(Name = str(key)).first()
# 			selections["userid"] = userid_
# 			selections["tipster"] = key
# 			selections["tips"] = value
# 			# tips_ = value.split('-')
# 			# for i,t in enumerate(tips_):
# 			# 	selections[nth[i+1]] = t

# 		if key == 'RESULT' and value != '':
# 			selections["result"] = value

# 		if key == 'WINODDS' and value != '':
# 			selections['winodds'] 
# 		# 	res_ = value.split('-')
# 		# 	for j,r in enumerate(res_):
# 		# 		selections['res_' + nth[j]] = r
# 	pprint.pprint(selections)
			# print m.group("racecoursecode")
		##remaining keys