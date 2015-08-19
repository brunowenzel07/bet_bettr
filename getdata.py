
## SQL Alchemy functions for data retrieval go here ##
## INITIALLY RUN AS FILE

#THIS SHOULD ALSO GET from app import db and session
from models import *
from sqlalchemy import func
import numpy as np
from StringIO import StringIO
from numpy import isnan

from datetime import datetime
import re
import pprint
from querycode import * 
import random

import difflib
from itertools import *
import pickle

# pprint(db.session.query(func.count(User.ID)).first())
# assert db.session.query(func.count(User.ID)).first() == (9,)

tipsters = np.array(["LALLY","HUTCH", "DAVIS", "AITKEN", "MICHAEL", "ANDREW", "WOO", "SHANNON", "RPONLINE"])
# testdata = np.array(["4-1-2", "13-2-4","2-3-5","12-7-3-4", "2-3-9-4",	"5-2-9-3",	"4-3-2-13",	"2-4-5-9", "3-2-12-7"])
# result = np.array(["12-2-4-13"])

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

f_name =  "TIPSDATA2015toJULY1.csv"

###use this to get snapshots
def gettipsterdata_bydate(tipsteridx, racedate):
	#which rows to skip?
	dates = np.genfromtxt(fname=f_name,delimiter=",", autostrip=True, skip_header=1, usecols=(0), dtype="S35")
	itemindex = numpy.amax(numpy.where(dates==racedate))
	# headers = ["racedate", "tips", "result", "winodds", "favpos"]
	tipster_data = np.genfromtxt(fname=f_name,delimiter=",", autostrip=True, skip_header=itemindex, usecols=(0,tipsteridx,10,11,12), 
		names=True, dtype=("S35, S25, S25, float, int"))
	 # dtype={'names':['raceinfo', 'tips', 'result', 'winodds', 'favpos', 'favodds'], 'formats': ['StringIO', 
	 # 'StringIO', 'StringIO','StringIO','StringIO','StringIO'] }, delimiter=",", autostrip=True, skip_header=1, usecols=(0,idx,10,11,12))
	return tipster_data


def gettipsterdata(tipsteridx):
	headers = ["racedate", "tips", "result", "winodds", "favpos"]
	tipster_data = np.genfromtxt(fname=f_name,delimiter=",", autostrip=True, skip_header=1, usecols=(0,tipsteridx,10,11,12), 
		names=True, dtype=("S35, S25, S25, float, int"))
	 # dtype={'names':['raceinfo', 'tips', 'result', 'winodds', 'favpos', 'favodds'], 'formats': ['StringIO', 
	 # 'StringIO', 'StringIO','StringIO','StringIO','StringIO'] }, delimiter=",", autostrip=True, skip_header=1, usecols=(0,idx,10,11,12))
	return tipster_data


##LOOK UP race, return horsenumbers in market order 
##return srting "2-6-7-8" of horses in order of finishing position by winodds asc
def getspmarketorder(raceinfo):
	pass

##does weighting
def f(x,y,i):
	# print x,y,i
	return (x==y)*i

##each line has raceinfo, tip, result, winodds, favpos
#SMC computes adapted similarity
# winners weighted by 12, followed by 6,4,2
# benchmark is market order
#  

def currentconsecutiveprofit():
	pass

#consecutive losses

def getmaxminlosingstreak(res_str):
		return len(min(re.compile("(L+L)").findall(res_str))), len(max(re.compile("(L+L)").findall(res_str)))

def getcurrentstreak(res_str):
	pass


def getmaxminwinningstreak(res_str):
	return len(min(re.compile("(W+W)").findall(res_str))), len(max(re.compile("(W+W)").findall(res_str)))


def compare(tips, res,winodds, favpos):
	matches = 0
	favorites = 0
	winnings = 0.0
	score,winners,seconds, thirds, fourths=0.0,0,0,0,0
	num = 0.0
	wts = [12,6,4,2]
	totalwts_4 = 12+6+4+2
	totalwts_3 = totalwts_4-2
	len_tips = len(tips)
	for i,t in enumerate(tips):
		if t == res[i]:
			if i == 0:
				winners +=1
				# print "winner!"
				score+=12
				if not isnan(winodds):
					winnings = float(winodds)
				if favpos == '1':
					favorites +=1
			if i ==1:
				seconds +=1
				score+=6
			if i ==2:
				thirds +=1
				score+=4
			if i ==3:
				fourths +=1
				score+=2
			matches +=1
			num += f(tips[i], res[i], wts[i])
	if len_tips == 3:
		return round(float(score/totalwts_3),2),winners,seconds, thirds, fourths,winnings, favorites
	else:
		return round(float(score/totalwts_4),2),winners,seconds, thirds, fourths,winnings, favorites

##per line
def smc(tipline):
	# print tipline
	raceinfo = tipline[0]
	# tips = 
	tips = tipline[1].split('-')
	res = tipline[2].split('-')
	winodds = tipline[3]
	favpos = tipline[4]
	# print favpos
	score = 0
	# winners,seconds, thirds, fourths, races= 0,0,0,0,0
	races = 0
	## are equal length
	tips_l = len(tips)
	if tips_l == len(res):
		##
		score,winners,seconds, thirds, fourths,winnings,favorites=compare(tips, res,winodds,favpos)
		# c=np.intersect1d(t,res[0])
		# print(c)
	else:
		res = res[:-1]
		# print tips, res
		score,winners,seconds, thirds, fourths,winnings,favorites= compare(tips, res,winodds,favpos)
	return score,winners,seconds, thirds, fourths,winnings,favorites
		#iterate to the min size
		

def round_up(x,n):
	return round(x,n)

def getfullresults(tipsterindex,tipster):
	tipster_score = 0
	res_seq = ""
	winners,seconds, thirds, fourths, races,winnings,favorites= 0,0,0,0,0,0.0,0
	t_data = gettipsterdata(tipsterindex)
	races = t_data.size

	# print(t_data)
	for l in t_data:
		if l[2] != '':
			all_r = smc(l)
			tipster_score += all_r[0]
			winners += all_r[1]
			seconds += all_r[2]
			thirds += all_r[3]
			fourths += all_r[4]
			winnings += all_r[5]
			favorites += all_r[6]
			if all_r[1] != 0:
				res_seq +='W'
			if all_r[1] == 0:
				res_seq +='L'
	# print winning_count
	##get max number of consecutive wins, losses, and current losingstreak, winningstreak

	return tipster, round_up(tipster_score,2),winners,seconds, thirds, fourths,races,round_up(winners/float(races)*100.0,2),\
	 round_up(winnings-float(races),2), \
	favorites,res_seq, getmaxminlosingstreak(res_seq)[1], getmaxminwinningstreak(res_seq)[1], res_seq[-10:]
# smc(davis_tips)

# print(getfullresults(3,'DAVIS'))






#later use market order from DB
def randompunter():
	tipster_score = 0
	#get number of runners for each race
	results = gettipsterdata(10)
	favpos = gettipsterdata(12)
	norunners = gettipsterdata(14)

	# if favpos in [1,2,3,4]:

## TIPSTER DATA 
'''
PERSIST THIS TABLE to DB
'''
# t_f = file("tmp.bin","wb")
output = open('data.pkl', 'wb')

def testdriver():
	d = {}
	for i,n in enumerate(tipsters):
		# print i+1,n
		# headers = ["score", "tipster", "winners", "seconds", "3", "4", "races"]
		d[i] = np.array(getfullresults(i+1,n), dtype=[('tipster', 'S35'),('b',float), 
			('c',int),('d',int),('e',int),('f',int),('g',int), ('winsr', float),
			('levelprofit', float),('j', int),('k', 'S500'),('l', int),('m', int),('n', 'S20')])
		# pprint.pprint(d[i])
		# np.save(t_f, res)
	# pprint.pprint(d)
	# print(np.sort(res))
	res = pickle.dump(d, output)
	output.close()
		# pickle.dump(res, output)
	
		# print(smc(tip, result[0]))

testdriver()
# testdriver()


def getsequencesimilarity(s1,s2):
#COMPARE sequences to see which are more complimentary
	s = difflib.SequenceMatcher(lambda x: x == " ", str(s1), str(s2))
	return round(s.ratio(), 3)


def getsimilarity():
	## get res
	# res = np.load(t_f)
	pkl_file = open('data.pkl', 'rb')
	res = pickle.load(pkl_file)
	pprint.pprint(res[0]['levelprofit'].item())
	for a, b in combinations(res, 2):
		pprint.pprint(res[a]['tipster'].item() + " " + repr(res[a]['levelprofit'].item()))
		pprint.pprint(" versus " + res[b]['tipster'].item() + " " + repr(res[b]['levelprofit'].item()))
		pprint.pprint(getsequencesimilarity(res[a]['k'].item(),res[b]['k'].item()))
		print "-----------------------END------------------------"

getsimilarity()