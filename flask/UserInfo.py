import peewee
from peewee import *
#Centralizies database model
from BaseModel import ModelBase, db
"""This script is the pewee database model for UserData. """
##CReates Database for User Data.
class UserInfo(ModelBase):
	"""Databaase model for user information including demographics and health utilities."""
	uid = AutoField()
	userid = CharField()
	titleid=CharField()
	firstname = CharField()
	lastname = CharField()
	age = IntegerField()
	hld = IntegerField()
	gender = CharField()
	race = CharField()
	finalconditionIntensityOne =IntegerField()                   
	finalconditionIntensityTwo =IntegerField()                   
	finalconditionIntensityThree =IntegerField()                 
	finalconditionIntensityFour =IntegerField()                  
	finalconditionIntensityFive =IntegerField()
	finalconditionIntensitySix =IntegerField()                 
	finalconditionIntensitySeven =IntegerField()                  
	finalconditionIntensityEight =IntegerField()                      
	finalconditionTimeTOne    =IntegerField()                   
	finalconditionTimeTTwo    =IntegerField()                   
	finalconditionTimeTThree  =IntegerField()                   
	finalconditionTimeTFour   =IntegerField()                   
	finalconditionTimeTFive   =IntegerField() 
	finalconditionTimeTSix  =IntegerField()                   
	finalconditionTimeTSeven   =IntegerField()                   
	finalconditionTimeTEight  =IntegerField()                   
	finalconditionGambOne     =IntegerField()                   
	finalconditionGambTwo     =IntegerField()                   
	finalconditionGambThree   =IntegerField()                   
	finalconditionGambFour    =IntegerField()                   
	finalconditionGambFive  =IntegerField()
	finalconditionGambSix  =IntegerField()                   
	finalconditionGambSeven    =IntegerField()                   
	finalconditionGambEight  =IntegerField()
	finalconditionOrderOne   = CharField()          
	finalconditionOrderTwo   = CharField()     
	finalconditionOrderThree = CharField()        
	finalconditionOrderFour   = CharField()        
	finalconditionOrderFive = CharField()
	finalconditionOrderSix = CharField()        
	finalconditionOrderSeven   = CharField()        
	finalconditionOrderEight = CharField()
	class Meta:
			database =db
			#table_name is table for the data.
			table_name = 'UserInfo'

#Create Class for meta data.
class UserMetaData(ModelBase):
	"""Database model for user meta data including the project and what they clicked on."""
	entryid = AutoField()
	userid = CharField()
	titleid=CharField()
	gambleid = IntegerField()
	currentPage = CharField()
	buttonPress = CharField()
	totalTime = IntegerField()
	conditionOneTime = DoubleField()
	conditionTwoTime = DoubleField()
	conditionThreeTime = DoubleField()
	conditionFourTime = DoubleField()
	conditionFiveTime = DoubleField()
	conditionSixTime = DoubleField()
	conditionSevenTime = DoubleField()
	conditionEightTime = DoubleField()
	conditionOneVideoTime = DoubleField()
	conditionTwoVideoTime = DoubleField()
	conditionThreeVideoTime = DoubleField()
	conditionFourVideoTime = DoubleField()
	conditionFiveVideoTime = DoubleField()
	conditionSixVideoTime = DoubleField()
	conditionSevenVideoTime = DoubleField()
	conditionEightVideoTime = DoubleField()
	class Meta:
			database =db
			#table_name is table for the data.
			table_name = 'UserMetaData'
