#!/usr/bin/env python
import re, os, sys, time, shutil, numpy, cgi, cgitb
from BaseModel import * #Get db variable from importing all
from peewee import *

##Condition info and data relating to condtion

class ConditionInfo:
	def __init__(self):
##Mechgamb because of not relying on sessions
		self.mechgamb = ""
	##Conditions 
		self.condOne = ""
		self.condTwo = ""
		self.condThree = ""
		self.condFour = ""
		self.condFive = ""
		self.condSix = ""
		self.condSeven =""
		self.condEight = ""
	##Condition Info
		self.condOneInfo = ""
		self.condTwoInfo = ""
		self.condThreeInfo = ""
		self.condFourInfo = ""
		self.condFiveInfo = ""
		self.condSixInfo = ""
		self.condSevenInfo = ""
		self.condEightInfo = ""
	##Condition Image Names
		self.condOneImage = ""
		self.condTwoImage = ""
		self.condThreeImage = ""
		self.condFourImage = ""
		self.condFiveImage = ""
		self.condSixImage = ""
		self.condSevenImage = ""
		self.condEightImage = ""
	def load(self, titleid):
		"""
		Load health state information, acronyms, image link, and health state name
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str		
		:return: Self loaded data from database
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==titleid)
		db.close()
		self.mechgamb = GamScen.mechgamb
	##Conditions 
		self.condOne = GamScen.conditionOne
		self.condTwo = GamScen.conditionTwo
		self.condThree = GamScen.conditionThree
		self.condFour = GamScen.conditionFour
		self.condFive = GamScen.conditionFive
		self.condSix = GamScen.conditionSix
		self.condSeven = GamScen.conditionSeven
		self.condEight = GamScen.conditionEight
	##Conditions Acronyms
		self.condOneAC = GamScen.conditionOneAC
		self.condTwoAC = GamScen.conditionTwoAC
		self.condThreeAC = GamScen.conditionThreeAC
		self.condFourAC = GamScen.conditionFourAC
		self.condFiveAC = GamScen.conditionFiveAC
		self.condSixAC = GamScen.conditionSixAC
		self.condSevenAC = GamScen.conditionSevenAC
		self.condEightAC = GamScen.conditionEightAC
	##Condition Info
		self.condOneInfo = GamScen.conditionOneInfo
		self.condTwoInfo =  GamScen.conditionTwoInfo
		self.condThreeInfo =  GamScen.conditionThreeInfo
		self.condFourInfo = GamScen.conditionFourInfo
		self.condFiveInfo = GamScen.conditionFiveInfo
		self.condSixInfo =  GamScen.conditionSixInfo
		self.condSevenInfo = GamScen.conditionSevenInfo
		self.condEightInfo = GamScen.conditionEightInfo
	##Condition Image Names
		self.condOneImage = GamScen.imageOnename
		self.condTwoImage = GamScen.imageTwoname
		self.condThreeImage = GamScen.imageThreename
		self.condFourImage = GamScen.imageFourname
		self.condFiveImage = GamScen.imageFivename
		self.condSixImage = GamScen.imageSixname
		self.condSevenImage = GamScen.imageSevenname
		self.condEightImage = GamScen.imageEightname
	def getmech(self, titleid):
		"""
		Load the mechanism in which the Gambler should operate
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str		
		:return: Gambler mechanism data 
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==titleid)
		db.close()
		return GamScen.mechgamb
	def getdemopref(self,titleid):
		"""
		Customizes the demographic page information
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str		
		:return: dict
		"""
		if (db.is_closed()==False):
				db.close()
		db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==titleid)
		db.close()
		return {'SMARTOnFHIR':GamScen.SonFHR, 'GenerateRandomUserID':GamScen.genranduid, 'DisablePatientName':GamScen.disablepatname, 'DisablePatientAge':GamScen.disablepatage, 'DisablePatientRace':GamScen.disablepatrace, 'DisablePatientGender': GamScen.disablepatgender}
	def savemech(self, titleid,mg):
		"""
		Save the mechanism in which the Gambler should operate
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str	
		:param mg: Gambler Mechanism
		:type mg: str			
		:return: Gambler mechanism data 
		"""		
		if (db.is_closed()==False):
			db.close()
		db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==titleid)
		GamScen.mechgamb = mg
		GamScen.save()
		db.close()
		return GamScen.mechgamb
	def getprojecttitle(self, titleid):
		"""
		Retrieves title of project
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str		
		:return: Title of Gambler project (str)
		"""	
		if (db.is_closed()==False):
			db.close()
		db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==titleid)
		db.close()
		return GamScen.otitleid
	def getlang(self,titleid):
		"""
		Retrieves language setting for the project
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str	
		:return: Langauge of project (str) 
		"""	
		if (db.is_closed()==False):
				db.close()
		db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==titleid)
		db.close()
		return GamScen.language
	def getls(self,titleid): #ls = Local Storage
		"""
		Retrieves local storage settings
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str			
		:return: Local storage setting (int)
		"""	
		if (db.is_closed()==False):
				db.close()
		db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==titleid)
		db.close()
		return GamScen.localStorage
