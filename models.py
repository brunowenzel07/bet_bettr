from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint,ForeignKey, UniqueConstraint, CheckConstraint, Column
from sqlalchemy.types import Float, Unicode, BigInteger, Integer, Boolean, Date, DateTime, Unicode, DECIMAL, String
from sqlalchemy.orm import relationship, backref
import pandas as pd
from datetime import datetime


from app import db

# class Country(db.Model):
#     __tablename__ = "Country"
#     ID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(60))

#     def __init__(self, Name):
#         self.Name = Name


#### GENERAL CLASSES FOR WEB APP

class User(db.Model):
    __tablename__ = "User"
    ID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(120))
    Password = db.Column(db.String(120))
    Name = db.Column(db.String(60))
    Animal = db.Column(db.String(60))
    DateSignedUp = db.Column(db.TIMESTAMP())

    __table_args__ = (UniqueConstraint('Name', 'Animal'),)

    def __init__(self, Email, Password, Name, DateSignedUp, Animal):
        self.Email = Email
        self.Password = Password
        self.Name = Name
        self.DateSignedUp = DateSignedUp
        self.Animal = Animal

# class User_Countries(db.Model):
#     __tablename__ = "User_Countries"
#     ID = db.Column(db.Integer, primary_key=True)
#     Userid = db.Column(db.Integer)
#     Countryid = db.Column(db.Integer)
#     DateStart = db.Column(db.TIMESTAMP())
#     Active = db.Column(db.Boolean)

#     def __init__(self, Userid, Countryid, DateStart, Active):
#         self.Userid = Userid
#         self.Countryid = Countryid
#         self.DateStart = DateStart
#         self.Active = Active

class Racecourses(db.Model):
    __tablename__ = "Racecourses"
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(60), unique=True)

    def __init__(self, Name):
        self.Name = Name

#separate class for Napoleon based on RaceDay

class Selection(db.Model):
    __tablename__ = "Selection" 
    ID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer,ForeignKey('User.ID'))
    RaceID = db.Column(db.Integer, ForeignKey('Race.ID'))
    # Racecourseid = db.Column(db.Integer) 
    # RaceDate = db.Column(db.TIMESTAMP())
    # RaceNumber = db.Column(db.Integer)
    First = db.Column(db.Integer)
    Second = db.Column(db.Integer)
    Third = db.Column(db.Integer)
    Fourth = db.Column(db.Integer)
    SubmittedAt = db.Column(db.DateTime)
    __table_args__ = (UniqueConstraint('UserID', 'RaceID'),)

    def __init__(self, UserID, RaceID, First, Second, Third, Fourth, SubmittedAt):
        self.UserID = UserID
        self.RaceID = RaceID
        # self.RaceDate = RaceDate
        # self.RaceNumber = RaceNumber
        self.First = First
        self.Second = Second
        self.Third = Third
        self.Fourth = Fourth
        self.SubmittedAt = SubmittedAt

### CONVERT TO r TABLES

class RaceDay(db.Model):
    __tablename__ = "RaceDay"
    ID = db.Column(db.Integer, primary_key=True)
    RaceDate = db.Column(db.TIMESTAMP())
    RaceCourseCode = db.Column(db.String(5))
    races = relationship('Race')

    def __init__(self, RaceDate, RaceCourseCode):
        self.RaceDate = RaceDate
        self.RaceCourseCode = RaceCourseCode

# 1Race: Many runners
#BASIC RUNNER MODEL USED FOR SELECTIONS
## BIG RUNNER MODEL RunnerExt
class Runner(db.Model):
    __tablename__ = "Runner"
    ID = db.Column(db.Integer, primary_key=True)
    RaceID = db.Column(db.Integer, ForeignKey('Race.ID'))
    HorseNumber = db.Column(db.Integer)
    HorseCode = db.Column(db.String(10))
    HorseName = db.Column(db.String(60))
    JockeyCode = db.Column(db.String(10))
    TrainerCode = db.Column(db.String(10))
    __table_args__ = (UniqueConstraint('RaceID', 'HorseCode'),)

    def __init__(self, RaceID, HorseNumber, HorseCode, HorseName, JockeyCode, TrainerCode):
        self.RaceID = RaceID 
        self.HorseNumber = HorseNumber 
        self.HorseCode = HorseCode 
        self.HorseName = HorseName 
        self.JockeyCode = JockeyCode 
        self.TrainerCode = TrainerCode

class Race(db.Model):
    __tablename__ = "Race"
    ID = db.Column(db.Integer, primary_key=True)
    RaceDate = db.Column(db.DATE)
    RaceCourseCode = db.Column(db.String(2))
    RaceName = db.Column(db.String(150))
    RaceDayID = db.Column(db.Integer, ForeignKey('RaceDay.ID'))
    RaceNumber = db.Column(db.Integer)
    RaceType = db.Column(db.String(10))  #CLASS ABBFORM 4S 3 HKG1 G1 Gr
    RaceGoing = db.Column(db.String(10)) #GF GY Y 
    RaceRating = db.Column(db.String(10)) #80-60
    RaceSurface = db.Column(db.String(5)) #AWT or C+3 A 
    RaceDistance = db.Column(Integer) # 1000
    UTCRaceTime = db.Column(db.TIMESTAMP()) #exact jump time updatable
    TrackWidth = db.Column(db.Float)
    Result = db.Column(db.String(20))
    R1 = db.Column(db.Integer)
    R2 = db.Column(db.Integer)
    R3 = db.Column(db.Integer)
    R4 = db.Column(db.Integer)
    WinOdds = db.Column(db.Float)
    FavPos = db.Column(db.Integer)
    FavOdds = db.Column(db.Float)
    NoRunners = db.Column(db.Integer) #count runners
    TrioDiv = db.Column(db.Float)
    TierceDiv = db.Column(db.Float)
    F4Div = db.Column(db.Float)
    QuartetDiv = db.Column(db.Float)
    runners = relationship("Runner")

    def __init__(self, RaceDayID, RaceDate, RaceCourseCode, RaceNumber, Result, WinOdds, FavPos, FavOdds, NoRunners, R1, R2, R3, R4):
        self.RaceDayID = RaceDayID
        self.RaceDate = RaceDate
        self.RaceCourseCode = RaceCourseCode
        self.RaceNumber = RaceNumber
        self.Result = Result
        self.WinOdds = WinOdds
        self.FavPos = FavPos
        self.FavOdds = FavOdds
        self.NoRunners = NoRunners
        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.R4 = R4


    # def __init__(self, RaceDate, RaceCourseCode, RaceNumber, Result, WinOdds, FavPos, FavOdds, NoRunners, RaceName=None, RaceType=None, RaceGoing=None, RaceRating=None, \
    #     RaceSurface=None, UTCRaceTime=None, TrackWidth=None, RaceDayID=None, TrioDiv=None, TierceDiv=None, F4Div=None, QuartetDiv=None):
    #     self.RaceDate = RaceDate
    #     self.RaceCourseCode = RaceCourseCode
    #     self.RaceNumber = RaceNumber
    #     self.Result = Result
    #     self.WinOdds = WinOdds
    #     self.FavPos = FavPos
    #     self.FavOdds = FavOdds
    #     self.NoRunners = NoRunners
    #     self.RaceType = RaceType
    #     self.RaceGoing = RaceGoing
    #     self.RaceRating = RaceRating
    #     self.RaceSurface = RaceSurface
    #     self.UTCRaceTime = UTCRaceTime
    #     self.TrackWidth = TrackWidth
    #     self.RaceName = RaceName
    #     self.RaceDayID = RaceDayID
    #     self.TrioDiv = TrioDiv
    #     self.TierceDiv = TierceDiv
    #     self.F4Div = F4Div
    #     self.QuartetDiv = QuartetDiv 

class Naps(db.Model):
    __tablename__ = "Naps"
    ID = Column(BigInteger, primary_key = True, autoincrement = True, nullable = False)
    RaceDayID = db.Column(db.Integer, ForeignKey('RaceDay.ID'))
    RaceNumberSelection = db.Column(db.String(10))
    UserID = db.Column(db.Integer,ForeignKey('User.ID'))
    RaceID = db.Column(db.Integer, ForeignKey('Race.ID'))
    isWin = db.Column(db.Boolean)

    def __init__(self, RaceDayID, RaceNumberSelection, UserID, RaceID, isWin):
        self.RaceDayID = RaceDayID
        self.RaceNumberSelection = RaceNumberSelection
        self.UserID = UserID
        self.RaceID = RaceID
        self.isWin =  isWin

#SELECTIONGGREGATES
#user:user_performances 1:M performance updated after each meeting


##ADD DUMP TABLE FOR CSV IMPORT used to update tupster data as season progresses


##ADD DATE so that LATEST TIPSTER DATA CAN BE DISPLAYED 
# class UserPerformance(db.Model):
#     __tablename__ = "UserPerformance"
#     ID = Column(BigInteger, primary_key = True, autoincrement = True, nullable = False) # Unique ID
#     RaceDate = db.Column(Date, nullable=False)
#     UserID = db.Column(db.Integer, ForeignKey('User.ID'))
#     Winpc = db.Column(Float, nullable=False)
#     Wins = db.Column(Integer)
#     TotalWinOdds = db.Column(Float)
#     Losses = db.Column(Integer)
#     NonRunners = db.Column(Integer)
#     MaxSeqWin = db.Column(Integer)
#     MaxSeqLose = db.Column(Integer)
#     PresSeqWin = db.Column(Integer)
#     PresSeqLose = db.Column(Integer)
#     MonthRoi = db.Column(Float)
#     SeasonRoi = db.Column(Float)
#     SeasonWins = db.Column(Integer)
#     SeasonLosses = db.Column(Integer)
#     NapsWins = db.Column(Integer)
#     NapsLosses = db.Column(Integer)
#     NapsWinpc = db.Column(Float)
#     NapsMaxSeqWin = db.Column(Integer)
#     NapsMaxSeqLose = db.Column(Integer)
#     NapsPresSeqWin = db.Column(Integer)
#     NapsPresSeqLose = db.Column(Integer)
#     AvgWinOdds = db.Column(Float, nullable=False)
#     Kelly_L200 = db.Column(Float)
#     Kelly_Season = db.Column(Float)
#     Placepc = db.Column(Float, nullable=False)
#     Tiercepc = db.Column(Float)
#     AvgTierceOdds = db.Column(Float)
#     Triopc = db.Column(Float)
#     AvgTrioOdds = db.Column(Float)
#     F4pc = db.Column(Float)
#     QTTpc = db.Column(Float)
#     AvgF4Odds = db.Column(Float)

    #INIT


#ODDS
#THESE 2 TABLES SHOULD EXIST ALREADY - reflect?


################################# t TABLES ##############################################################

'''
All users are also potentially systems - owner_id USER
The systems have names of animals
Users have regular email, name, ...
A system can also stand alone in which case its userid is Metabet
some systems are not users with emails, password
but users can subscribe to systems 

'''

class t_System(db.Model):
    __tablename__ = "t_system"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    animal = db.Column(db.String(60))
    datestarted = db.Column(db.Date)
    datestopped = db.Column(db.Date)
    performances = relationship("t_SystemPerformance") ##I have seen that error before if I forget that ForeignKey() takes the name of a database table-and-field but that relationship() takes the name of an ORM class instead.
    __table_args__ = (UniqueConstraint('name', 'animal'),)

    def __init__(self, name, animal, datestarted, datestopped):
        self.name = name
        self.animal = animal
        self.datestarted = datestarted
        self.datestopped = datestopped


'''
Metadata for race useful for tipsters
use racedate, racecourse racenumber to JOIN to data coming from ODDS (racedate, racecoursecode, racenumber) and r_race = raceresults
and rd_race raceday
'''

class t_Race(db.Model):
    __tablename__  ="t_race"
    id = Column(BigInteger, primary_key = True, autoincrement = True, nullable = False) # Unique ID
    racedate = db.Column(db.Date)
    racecoursecode = db.Column(db.String(2))
    racenumber = db.Column(db.Integer)
    result = db.Column(db.String(40))
    winodds = db.Column(db.Float)
    favpos = db.Column(db.Integer)
    norunners = db.Column(db.Integer)
    marketorder = db.Column(db.String(40))
    surface= db.Column(db.String(10))
    raceclass= db.Column(db.String(6))
    f4 = db.Column(db.Float)
    tierce= db.Column(db.Float)
    qtt = db.Column(db.Float)
    dt = db.Column(db.Float)
    tt = db.Column(db.Float)
    ttc = db.Column(db.Float)
    sixup = db.Column(db.Float)
    sixupc = db.Column(db.Float)
    __table_args__ = (UniqueConstraint('racedate', 'racecoursecode', 'racenumber'),)

    def __init__(self, racedate, racecoursecode, racenumber, results, winodds, favpos, norunners, marketorder, surface, raceclass,\
    f4, tierce, qtt, dt, tt, ttc, sixup, sixupc ):
        self.racedate = racedate
        self.racecoursecode = racecoursecode
        self.racenumber = racenumber
        self.results= results
        self.winodds = winodds
        self.favpos= favpos
        self.norunners = norunners
        self.marketorder = marketorder
        self.surface = surface 
        self.raceclass = raceclass
        self.f4 = f4
        self.tierce = tierce
        self.qtt = qtt
        self.dt = dt
        self.tt  = tt
        self.ttc = ttc
        self.sixup = sixup
        self.sixupc = sixupc
'''
Measures cross performance based on perf_seq for 2 or more systems  
the combination is a string code SYSTEM1ID|SYSTEM2ID| (SYSTEM3ID) 
add other metrics to this table later
'''
class t_SystemCrossPerformance(db.Model):
    __tablename__ = "t_systemcrossperformance"
    id = db.Column(db.Integer, primary_key=True)
    combination =db.Column(db.String(40))
    similarity= db.Column(db.Float)
    updated = db.Column(db.TIMESTAMP)
    updated_date = db.Column(db.Date)

    def __init__(self, combination, similarity, updated= datetime.utcnow()):
        self.combination = combination
        self.similarity = twowaysimilarity
        self.updated = updated
        self.updated_date = updated.date()

'''
Contains aggregate data for tipsters based on the updated/_date.
Thus can be updated at any time pre post race 
select latest always
'''
class t_SystemPerformance(db.Model):
    __tablename__ = "t_systemperformance"
    id = db.Column(db.Integer, primary_key=True)
    t_system_id= db.Column(db.Integer, ForeignKey('t_system.id'))
    tipsterscore = db.Column(db.Float) 
    winners = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
    thirds = db.Column(db.Integer)
    fourths = db.Column(db.Integer)
    totalraces = db.Column(db.Integer)
    winsr = db.Column(db.Float)
    favorites = db.Column(db.Integer)
    perf_seq = db.Column(db.TEXT())
    maxlosingstreak = db.Column(db.Integer)
    maxwinningstreak = db.Column(db.Integer)
    last10 = db.Column(db.String(40))
    updated = db.Column(db.TIMESTAMP)
    updated_date = db.Column(db.Date)

    def __init__(self, t_system_id, tipsterscore, winners, seconds, thirds, fourths, totalraces, winsr, favorites,
        perf_seq, maxlosingstreak, maxwinningstreak, last10, updated=datetime.utcnow()):
        self.t_system_id = t_system_id
        self.tipsterscore = tipsterscore
        self.winners = winners
        self.seconds = seconds
        self.thirds = thirds
        self.fourths = fourths
        self.totalraces = totalraces
        self.winsr = winsr
        self.favorites = favorites
        self.perf_seq = perf_seq
        self.maxlosingstreak = maxlosingstreak
        self.maxwinningstreak = maxwinningstreak
        self.last10 = last10
        self.updated = updated
        self.updated_date = updated.date()

'''
Contains the raw tips per tipster (system)
for system non tipsters - calculate from formfactors/jockeys/etc to output 1st-2nd-3rd-4th string and update
can only tip once per race
'''
class t_SystemRecords(db.Model):
    __tablename__ = "t_systemrecords"
    id = Column(BigInteger, primary_key = True, autoincrement = True, nullable = False) # Unique ID
    t_race_id = db.Column(db.Integer, ForeignKey('t_race.id'))
    t_system_id= db.Column(db.Integer, ForeignKey('t_system.id'))
    first = db.Column(db.Integer)
    second = db.Column(db.Integer)
    third = db.Column(db.Integer)
    fourth = db.Column(db.Integer)
    updated = db.Column(db.TIMESTAMP)
    updated_date = db.Column(db.Date)
    __table_args__ = (UniqueConstraint('t_race_id', 't_system_id'),)

    def __init__(self,t_race_id, t_system_id, first, second, third, fourth, updated=datetime.utcnow()):
        self.t_race_id= t_race_id
        self.t_system_id=t_system_id
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
        self.updated = updated
        self.updated_date = updated.date()

#################################################################################################################


### convert to o_ redo oddsmodel

class HKOddsModel(db.Model):
    __tablename__ = "hk_odds"
    id = Column(BigInteger, primary_key = True, autoincrement = True, nullable = False) # Unique ID
    race_date = Column("racedate", Date, nullable = False) # Race date.
    race_course_code = Column("racecoursecode", Unicode(2)) # Race course code.
    race_number = Column("racenumber", Integer) # Race number.
    horse_number = Column("horsenumber", Integer, nullable = False) # Horse number.
    update_date_time = Column("updatedate", DateTime, nullable = False) # Date and time of last update.
    win_odds = Column("winodds", DECIMAL(10,2)) # Odds of win. It's not float! Float for money is not acceptable!
    is_win_fav = Column("isWinFav", Integer) # Some times this parameter can takes value 2 and more.
    place_odds = Column("placeodds", DECIMAL(10,2)) # The same as Win odds.
    is_place_fav = Column("isPlaceFav", Integer) # The same as is_win_fav.
    pool = Column("pool", BigInteger) # Pool number.
    is_reserve = Column("isReserve", Boolean) # Reserve data.
    is_scratched = Column("isScratched", Boolean) # Scratched data.

    def __init__(self, race_date, race_course_code, race_number, horse_number, update_date_time, win_odds, is_win_fav, place_odds, is_place_fav, pool, is_reserve = False, is_scratched = False):
        self.race_date = race_date
        self.race_course_code = race_course_code
        self.race_number = race_number
        self.horse_number = horse_number
        self.update_date_time = update_date_time
        self.win_odds = win_odds
        self.is_win_fav = is_win_fav
        self.place_odds = place_odds
        self.is_place_fav = is_place_fav
        self.pool = pool
        self.is_reserve = is_reserve
        self.is_scratched = is_scratched


##Create table For Aggregate Data (waiting for results to do analysis) - do CSV to remote database

##ODDS
class HKOddsDisplayModel(db.Model):
    __tablename__ = "hk_odds_display"
    ID = db.Column(db.Integer, primary_key=True)
    RaceDate = db.Column(db.TIMESTAMP())
    RaceCourseCode = db.Column(db.String(2))
    RaceNumber = db.Column(db.Integer)
    HorseNumber = db.Column(db.Integer)
    OpWin = db.Column(db.Float)
    OpWinRank = db.Column(db.Integer)
    Win12am = db.Column(Float)
    Win6am  = db.Column(Float)
    Win8am = db.Column(Float)
    Win3pm = db.Column(Float)
    Win5mins = db.Column(Float)
    WinNow = db.Column(Float)
    WinNowRank = db.Column(db.Integer)
    WinNowOPDiff = db.Column(Float)
    WinNowL5minsDiff = db.Column(Float)
    WinNowBettingLine = db.Column(Float)
    WinSp = db.Column(Float)
    WinSpRank = db.Column(db.Integer)

    def __init__(self,RaceDate,RaceCourseCode,RaceNumber,HorseNumber,OpWin,OpWinRank,Win12am,Win6am,Win8am,Win3pm,WinL5mins,WinNow,WinNowRank,WinSp,WinSpRank):
        self.RaceDate = RaceDate
        self.RaceCourseCode = RaceCourseCode
        self.RaceNumber = RaceNumber
        self.HorseNumber = HorseNumber
        self.OpWin = OpWin
        self.OpWinRank = OpWinRank
        self.Win12am = Win12am
        self.Win6am = Win6am
        self.Win8am = Win8am
        self.Win3pm = Win3pm
        self.WinL5mins = WinL5mins
        self.WinNow = WinNow
        self.WinNowRank = WinNowRank
        self.WinSp = WinSp
        self.WinSpRank= WinSpRank
        self.WinNowOPDiff = WinNowOPDiff
        self.WinNow5minsDiff = WinNow5minsDiff
        self.WinNowBettingLine = WinNowBettingLine

## ADD VALIDASOF DATE HERE and DISPLAYED BASED ON FILTERED BY THIS DATE
class Tipster(db.Model):
    __tablename__ = "TipsterPerformance"
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(40))
    TipsterScore = db.Column(db.Float) 
    NumberWinners = db.Column(db.Integer)
    Seconds = db.Column(db.Integer)
    Thirds = db.Column(db.Integer)
    Fourths = db.Column(db.Integer)
    TotalRaces = db.Column(db.Integer)
    WinStrikeRate = db.Column(db.Float)
    NumberFavorites = db.Column(db.Integer)
    PerformanceSequence = db.Column(db.TEXT())
    MaxLosingStreak = db.Column(db.Integer)
    MinWinningStreak = db.Column(db.Integer)
    Last10 = db.Column(db.String(40))

    def __init__(self, Name, TipsterScore, NumberWinners, Seconds, Thirds, Fourths, TotalRaces, WinStrikeRate, NumberFavorites,
        PerformanceSequence, MaxLosingStreak, MinWinningStreak, Last10):
        self.Name = Name
        self.TipsterScore = TipsterScore
        self.NumberWinners = NumberWinners
        self.Seconds = Seconds
        self.Thirds = Thirds
        self.Fourths = Fourths
        self.TotalRaces = TotalRaces
        self.WinStrikeRate = WinStrikeRate
        self.NumberFavorites = NumberFavorites
        self.PerformanceSequence = PerformanceSequence
        self.MaxLosingStreak = MaxLosingStreak
        self.MinWinningStreak = MinWinningStreak
        self.Last10 = Last10
        