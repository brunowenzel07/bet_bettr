##import from CSV into two tables
from datetime import datetime, timedelta, date
import calendar
from collections import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from utilities import *
import os
import csv
import pprint
### SQL ALCHEMY CONNECTION ## 
app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
from models import *

#method 2
FILE_NAME = 'TIPSDATA2015toJULY1.csv'


#if in DB do not import
#how many t_Races are there?
# print db.session.query(func.count(t_Race.id)).one()
if db.session.query(t_Race.id).count() == 0:
	_race=np.genfromtxt(FILE_NAME,dtype=str,delimiter=',',filling_values="None", skiprows=0,usecols=(0,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24))

	for i,r in enumerate(_race):
		if i != 0:
			_racedate, _racecoursecode, _racenumber =  datetime.strptime(r[0][:8], "%Y%m%d"),r[0][8:10],try_int(r[0][10:12])
			#assemble the array manually
			result = r[1]
			winodds = r[2]
			favpos= r[3]
			norunners= r[4]
			market= r[5]
			surface= r[6]
			raceclass= r[7]
			f4= r[8]
			tierce= r[9]
			qtt= r[10]
			dt = r[11]
			tt = r[12]
			ttc= r[13]
			sixup= r[14]
			sixupc  = r[15]
			# print racedate
			# print datetime.strptime(racedate, "%Y%m%d")
			newRace = t_Race( _racedate, _racecoursecode, _racenumber, result, try_float(winodds), try_int(favpos),\
		 	try_int(norunners), market, surface, raceclass, try_float(f4), try_float(tierce), try_float(qtt), try_float(dt), try_float(tt),\
		  	try_float(ttc), try_float(sixup), try_float(sixupc) )
			db.session.add(newRace)
			db.session.commit()
			raceid = t_Race.query.filter_by(racedate=_racedate, racecoursecode=_racecoursecode, racenumber=_racenumber).one()
			# raceid = t_Race.query.get(newRace)
			print raceid.id

#3now put tipster data in



### SYSTEMS ##

s_signup = datetime.strptime("20150101", "%Y%m%d")
lally_quit = datetime.strptime("20150801", "%Y%m%d")
s_names = np.array(['PAUL LALLY', 'CLINT HUTCHINSON', 'BRETT DAVIS', 'ALAN AITKEN', 'ANDREW HAWKINS','PHILLIP WOO','SHANNON','RPONLINE',  'Top 4 Jockeys',\
	'Top 4 Trainers Entries', 'Top 4 PrizeMoney'])
s_animals = np.array(['The Rat', 'The Fox', 'The Hound', 'The Goat', 'The Rabbit', 'The Tiger', 'The Snake', 'The Dragon', 'The Market', 'Jockey Up', 'Trainer Time'\
 'Prizes mean Points' ])

for x,y in zip(s_names, s_animals):
	if x == 'PAUL LALLY':
		newSystem = t_System(Name=x, Animal=y, datestarted=t_signup, datestopped=lally_quit)
	else:
		newSystem = t_System(Name=x, Animal=y, datestarted=t_signup, datestopped=None)
	db.session.add(newSystem)
	db.session.commit()
	systemid = t_Race.query.filter_by(racedate=_racedate, racecoursecode=_racecoursecode, racenumber=_racenumber).one()
	print systemid.id

## DO NOT TOUCH USERS

##make sure system ids are there do count
## 
if db.session.query(t_System.id).count() == 11:
	_tips=np.genfromtxt(FILE_NAME,dtype=str,delimiter=',',filling_values="None", skiprows=0,usecols=(0,1,2,3,4,5,6,7,8,9))
	tips = {defaultdict(list)}
	_systemids = []

	#get system ids
	for s in t_System.query.all():
		_systemids.append(s) #system objects

	pprint.pprint(_systemids)

	for i,t in enumerate(_tips):
		if i !=0:
			#to get raceid
			_racedate, _racecoursecode, _racenumber =  datetime.strptime(t[0][:8], "%Y%m%d"),t[0][8:10],try_int(t[0][10:12])
			try:
				_raceid = t_Race.query.filter_by(racedate=_racedate, racecoursecode=_racecoursecode, racenumber=_racenumber).one()
				_racedate = _raceid.racedate
				_timestamp1 = calendar.timegm(_racedate.timetuple())
				_updated = datetime.utcfromtimestamp(_timestamp1) #midnight this date (which is midight - before the race)
				#convert racedate to time midnight UTC - make sure racetimes are UTC!
				lally= None
				_tips =t[1].split("-")


				## do this at end
				_tips_ct = len(_tips)
				if _tips_ct == 3:
					lally = t_SystemRecords(t_race_id=_raceid, t_system_id=, first=_tips[0], second=_tips[1], third=_tips[3], fourth=None, updated=_updated)
				else:
					lally = t_SystemRecords(t_race_id=, t_system_id=, first=_tips[0], second=_tips[1], third=_tips[3], fourth=_tips[4], updated=_updated)
				#get userid

				# tips['CLINT HUTCHINSON'].append(_raceid, t[2]])
				# tips['BRETT DAVIS'].append(_raceid, t[3]])
				# tips['ALAN AITKEN'].append(_raceid, t[4]])
				# tips['MICHAEL COX'].append(_raceid, t[5]])
				# tips['ANDREW HAWKINS'].append(_raceid, t[6]])
				# tips['PHILLIP WOO'].append(_raceid, t[7]])
				# tips['SHANNON'].append(_raceid, t[8]])
				# tips['RPONLINE'].append(_raceid, t[9]])
			except ValueError:
				continue
	_thesystemid = t_System.query.filter_by(name='PAUL LALLY').one()
	pprint.pprint(tips[str(_thesystemid.id)])
# pprint.pprint(tips['ALAN AITKEN'])



	# print racedate, racecode, racenumber, result, winodds, favpos, norunners, market, surface, raceclass, f4, tierce, qtt, dt, tt, ttc, sixup, sixupc
# 	newRace = t_Race(*r)
# 	db.session.add(newRace)
# 	db.session.commit()
# 	raceid = t_Race.query.get(newRace)
# 	print raceid
# #_race has np array of arrays each a race
# usecols=(0,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
# _races=np.genfromtxt(FILE_NAME,dtype=[('|S99')],delimiter=',',filling_values="NO DATA",\
 # names=("RACEDATE|RACECODE|RACENUMBER",), usecols=("RACEDATE|RACECODE|RACENUMBER"), autostrip=True, skip_header=1,defaultfmt="var_%02i")

#each row
# for r in _races:
# 	print r
	#for each row, get number of columns 
	# print r[0]
	# racedate, racecode, racenumber =  r[0][:8],r[0][8:10],r[0][10:12]
	# # print racedate, racecode, racenumber
	# result = r[10]
	# winodds = r[11]
	# favpos= r[12]
	# norunners= r[13]
	# # market= r[14]
	# # print racedate, racecode, racenumber, result, winodds, favpos, norunners, market
	# # surface= r[15]
	# # raceclass= r[16]
	# # f4= r[17]
	# # tierce= r[18]
	# # qtt= r[19]
	# # dt = r[20]
	# # tt = r[21]
	# # ttc= r[22]
	# # sixup= r[23]
	# # sixupc  = r[24]
	# print racedate, racecode, racenumber, result, winodds, favpos, norunners
	# , market, surface, raceclass 
	# print surface, raceclass, f4, tierce, qtt, dt, tt, ttc, sixup, sixupc
	    # newRace = t_Race(racedate, racecode, racenumber, result, winodds, favpos, norunners, market, surface, raceclass, f4, tierce, qtt, dt, tt, ttc, sixup, sixupc)
    	# db.session.add(newRace)
    	# db.session.commit()
    	# raceid = t_Race.query.get(newRace)
    	# print raceid
# races = {}
# print "import of raw data started"
# with open(FILE_NAME, 'rU') as csvfile:
#     tipsters = csv.reader(csvfile, delimiter=",", quotechar="'")
#     for line, tipster in enumerate(tipsters):
#     	#race pass
#     	if line != 0:
#     		data = []
#     		data.append(tipster['RACEDATE|RACECODE|RACENUMBER'])
#     		data.append(tipster[10])
#     		data.append(tipster[11])
#     		data.append(tipster[12])
#     		data.append(tipster[13])
#     		data.append(tipster[14])
#     		races[line] = data
#     	pprint.pprint(races)
    	# if line !=0:
    	# 	# racedatecodenumber = tipster[0]
    	# 	racedate, racecode, racenumber =  tipster[0][:8],tipster[0][8:10],tipster[0][10:12]
    	# 	# print racedate, racecode, racenumber
    	# 	result = tipster[10]
    	# 	winodds = tipster[11]
    	# 	favpos= tipster[12]
    	# 	norunners= tipster[14]
    	# 	market= tipster[15]
    	# 	print racedate, racecode, racenumber, result, winodds, favpos, norunners, market

    	# 	#optional
    	# 	market= tipster[14]
    	# 	surface= tipster[15]
    	# 	raceclass= tipster[16]
    	# 	f4= tipster[17]
    	# 	tierce= tipster[18]
    	# 	qtt= tipster[19]
    	# 	dt = tipster[20]
    	# 	tt = tipster[21]
    	# 	ttc= tipster[22]
    	# 	sixup= tipster[23]
    	# 	sixupc  = tipster[24]
    	# 	# newRace = t_Race(racedate, racecode, racenumber, result, winodds, favpos, norunners, market, surface, raceclass, f4, tierce, qtt, dt, tt, ttc, sixup, sixupc)
    		# db.session.add(newRace)
    		# db.session.commit()
    		# raceid = t_Race.query.get(newRace)
    		# print raceid

    	# newTipster = Tipster(tipster[0], tipster[1], tipster[2], tipster[3], tipster[4], tipster[5], tipster[6],
    	# 	 tipster[7], tipster[9], tipster[10], tipster[11], tipster[12], tipster[13])
    	# db.session.add(newTipster)
    	# print "added tipster ", tipster[0]
    # db.session.commit()
print "import ended"


# for i, data in enumerate(csv_stuff):
#     race = Race()
#     rec.set_stuff(data)
#     session.add(rec)
#     if i % 1000 == 0:
#         session.flush()
# session.commit() # flushes everything remaining + commits