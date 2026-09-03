import os
import peewee
from peewee import *

#Must modify this information before production
#Password must be modified.  

#db = MySQLDatabase(os.getenv('DB_NAME', 'Gambler'), user=os.getenv('DB_USER', 'user'), passwd=os.getenv('DB_PW', 'passwd'))
from playhouse.sqlite_ext import SqliteExtDatabase

# PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'configfiles'))
PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', ''))
# db = SqliteDatabase('../configfiles/Gambler.db', pragmas={'journal_mode': 'wal'})
db = SqliteExtDatabase(PROJECT_PATH + '/Gambler.db', regexp_function=True, timeout=3,
                       pragmas={'journal_mode': 'wal'})
class ModelBase(peewee.Model):
	"""Generic model database for Peewee"""
	class Meta:
		database = db

class GamblerInfo(ModelBase):
	"""Database model for Gambler project information"""
	gambleid = AutoField()
	otitleid =TextField()
	titleid=CharField(unique=True)
	mechgamb =CharField()
	conditionOne=TextField()
	conditionTwo=TextField()
	conditionThree=TextField()
	conditionFour=TextField()
	conditionFive=TextField()
	conditionSix=TextField()
	conditionSeven=TextField()
	conditionEight=TextField()
	conditionOneAC=TextField()
	conditionTwoAC=TextField()
	conditionThreeAC=TextField()
	conditionFourAC=TextField()
	conditionFiveAC=TextField()
	conditionSixAC=TextField()
	conditionSevenAC=TextField()
	conditionEightAC=TextField()
	conditionOneInfo=TextField()
	conditionTwoInfo=TextField()
	conditionThreeInfo=TextField()
	conditionFourInfo=TextField()
	conditionFiveInfo=TextField()
	conditionSixInfo=TextField()
	conditionSevenInfo=TextField()
	conditionEightInfo=TextField()
	imageOnename = TextField()
	imageTwoname = TextField()
	imageThreename= TextField()
	imageFourname = TextField()
	imageFivename = TextField()
	imageSixname= TextField()
	imageSevenname = TextField()
	imageEightname = TextField()
	initgambThresh =IntegerField()
	maxgambThresh = IntegerField()
	mingambThresh = IntegerField()
	posgambThresh =IntegerField()
	neggambThresh =IntegerField()
	gambChoosing =TextField()
	gambScenario =TextField()
	gambScenarioThree =TextField()
	gambScenarioFour =TextField()
	gambScenarioFive =TextField()
	gambScenarioSix =TextField()
	gambScenarioSeven =TextField()
	gambBenefits=TextField()
	gambSideeffects = TextField()
	gambWelcome =TextField()
	gambAgreementA=TextField()
	gambAgreementE=TextField()
	gambAgreementB=TextField()
	inittimeThresh =IntegerField()
	postimetThresh =IntegerField()
	negtimetThresh =IntegerField()
	maxtimetThresh = IntegerField()
	mintimetThresh = IntegerField()
	timetScenario = TextField()
	timetScenarioThree = TextField()
	timetScenarioFour = TextField()
	timetScenarioFive = TextField()
	timetScenarioSix = TextField()
	timetScenarioSeven = TextField()
	timetChoosing=TextField()
	timetBenefits=TextField()
	timetSideeffects=TextField()
	timetWelcome=TextField()
	timetAgreementA=TextField()
	timetAgreementE=TextField()
	timetAgreementB=TextField()
	language=CharField()
	SonFHR=IntegerField() 
	genranduid=IntegerField()
	disablepatname=IntegerField()
	disablepatage=IntegerField()
	disablepatgender=IntegerField()
	disablepatrace=IntegerField()
	localStorage=IntegerField()
	class Meta:
		database =db
			#table_name is table for the data.
		table_name = 'GamblerInfo'
