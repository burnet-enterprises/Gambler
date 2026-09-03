#!/usr/bin/env python
import re, os, sys, time, shutil, numpy, cgi, cgitb
#Create a class for scenario building
#GScenario = GamblerTimeTradeOff
from BaseModel import *
from peewee import *
import math

#Swinging calculations for Time Trade off mechanism
def factorial(n):
	"""Part of cospoints"""
	if n == 0:
		return 1
	else:
		return n * factorial(n-1)
 
		
def func_cos(x, n):
	"""Part of cospoints"""
	cos_approx = 0
	for i in range(n):
		coef = (-1)**i
		num = x**(2*i)
		denom = factorial(2*i)
		cos_approx += ( coef ) * ( (num)/(denom) )
	return cos_approx


def cospoints(click,points):
#Tradeoff function
	""" Calculate the swinging by clicks for users. """
	decm = round(.1*points,0) #Used to make sure that swings are gradual and within boundaries
	if click <= decm:
		adj = points - 1
	elif click > decm and click < points:
		adj = points - click + decm
	else:
		adj = 0
	g = 90*(adj/points)
	angle_rad = g * 3.141592653589793 / 180
	out =  round(func_cos(angle_rad,8)*5,1)
	out =  round(func_cos(angle_rad,8)*points,1)
	return (int(out))
	
	
#################################################################################
#																				#
#																				#
#																				#
#																				#
#							Time Trade Off Logic 								#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################


#################################################################################
#																				#
#																				#
#																				#
#																				#
#							Life Table Lookups 									#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################

#################################################################################
#Not full representation of Life tables for each race, but this template should allow you to know how to modify it 
class LifeTable(ModelBase):
	"""CDC Life table database lookup template"""
	Age = AutoField()
	Citizen = FloatField() #Generic 
	Male = FloatField()
	Female = FloatField()
	White  = FloatField() #White
	WMale  = FloatField()
	WFemale  = FloatField()
	NAmerican  = FloatField() #Native American
	NAMale  = FloatField()
	NAFemale  = FloatField()
	Asian  = FloatField() #Asian/Pacific Islander
	ASMale  = FloatField()
	ASFemale  = FloatField()
	AA  = FloatField()
	AAMale  = FloatField() #African American
	AAFemale  = FloatField()
	WHispanic  = FloatField() #Hispanic
	WHMale  = FloatField()
	WHFemale  = FloatField()
	class Meta:
			database =db
			#db_table is table for the data.
			db_table = 'LifeTable'
	
#################################################################################
#																				#
#																				#
#																				#
#																				#
#					Time Trade Off Wording Class								#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################

#################################################################################
class GTimeTradeOff:
	def __init__(self):
		self.Scenario_Statement ="This is a scenario statement.\nIt will tell you that you have @#@ pills out of &#& pills.\n"
		self.Scenario_Statement3 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Scenario_Statement4 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Scenario_Statement5 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Scenario_Statement6 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Scenario_Statement7 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Choosing_Statement = "This is the choosing statment.\nIt will ask you if you would want to choose the scenario.  Click Yes for yes and No for no.\n"
		self.Sideeffects_Statement= "This is the side effect statement.\nIt will list the side effects.\n"
		self.Benefits_Statement = "This is the benefits statement.\nIt will list the benefits.\n"
		self.Agreement_Statement_A= "Alternative A" #This is a positive as in yes label
		self.Agreement_Statement_E = "Equal" #This is a neutral as in I don't know or meh label.
		self.Agreement_Statement_B = "Alternative B" #This is a negative as in no label.
		self.Welcome_Statement = "This is a welcoming statement to bring the user comfortably into the decision."

	##Build a secnearion SBuild = Secnario build
	#X is condtion, y is which statement to replace
	def SBuild(self,x,y):
		"""Replaces text with health state for Scenario Statement
		
		:param x: The Health state
		:type x: str	
		:param y: The health state order as it appears on administration page
		:type y: int				
		
		:returns: Statement with health state
		"""

		if y == 3 :
				z = self.Scenario_Statement3.replace("@#@", str(x))
				return z
		elif y == 4 :
				z = self.Scenario_Statement4.replace("@#@", str(x))
				return z
		elif y == 5 :
				z = self.Scenario_Statement5.replace("@#@", str(x))
				return z
		elif y == 6 :
				z = self.Scenario_Statement6.replace("@#@", str(x))
				return z
		elif y == 7 :
				z = self.Scenario_Statement7.replace("@#@", str(x))
				return z
		else:
				z = self.Scenario_Statement.replace("@#@", str(x))
				return z

	##Build a secnearion CBuild = Choosing Statement build
	#X is condtion, y is which statement to replace	
#	Describe Choice for User. \"$#$ *#*  out of &#& for The Life Time with *#* being time units and %#% *#* out of &#& *#* for The Dead Time  with *#* being time units.\" to describe the choice and \" or suffer from $#$ \". to designate the place for the health state
## @#@ <- Live Time &#& <-Total Time %#% <-Dead Time @#@ <-Intermediate Health state  *#* <-Timetrade units
	def CBuild(self, q, x, y,w):
		"""Replaces text with health state for Scenario Statement
		
		:param x: The Health state
		:type x: str	
		:param y: The health state order as it appears on administration page
		:type y: int				
		
		:returns: Statement with health state
		"""

		z = self.Choosing_Statement.replace("$#$", str(int(x)))
		z = z.replace("&#&", str(int(y)))
		z = z.replace("@#@", str(w))
		z = z.replace("*#*", str(q))
		z = z.replace("%#%", str(int(y-x)))
		return z
		
	def load(self, titleid):
		""" 
		Load information for Time Trade off page
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str	
		:param Scenario_Statement: The scenario statement that includes the second health state as ordered in the admin page
		:type Scenario_Statement: str
		:param Scenario_Statement3: The scenario statement that includes the third health state as ordered in the admin page
		:type Scenario_Statement3: str
		:param Scenario_Statement4: The scenario statement that includes the fourth health state as ordered in the admin page
		:type Scenario_Statement4: str
		:param Scenario_Statement5: The scenario statement that includes the fifth health state as ordered in the admin page
		:type Scenario_Statement5: str
		:param Scenario_Statement6: The scenario statement that includes the sixth health state as ordered in the admin page
		:type Scenario_Statement6: str
		:param Scenario_Statement7: The scenario statement that includes the seventh health state as ordered in the admin page
		:type Scenario_Statement7: str		
		:param Choosing_Statement: This statement explains to users to make the choices in the Gambler health state
		:type Choosing_Statement: str
		:param Benefits_Statement: This statement explains part of the Tradeoff that's beneficial to users
		:type Scenario_Statement: str
		:param Sideeffects_Statement: This statement explains the negative effects of taking the Tradeoff to users
		:type Scenario_Statement: str		
		:param Agreement_Statement_A: Left side button normally used to choose the health state
		:type Agreement_Statement_A: str		
		:param Agreement_Statement_E: Middle button normally to end the Tradeoff
		:type Agreement_Statement_E: str		
		:param Agreement_Statement_B: Right side button normally used to choose The Tradeoff
		:type Agreement_Statement_B: str	
		:param Welcome_Statement: The introduction statement used to welcome patients to the Time Trade off screen
		:type Welcome_Statement: str				
		
		:returns: Loaded information to self

		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		TimeScen = GamblerInfo.get(GamblerInfo.titleid==titleid)
		db.close()
		self.Scenario_Statement = TimeScen.timetScenario
		self.Scenario_Statement3 = TimeScen.timetScenarioThree
		self.Scenario_Statement4 = TimeScen.timetScenarioFour
		self.Scenario_Statement5 = TimeScen.timetScenarioFive
		self.Scenario_Statement6 = TimeScen.timetScenarioSix
		self.Scenario_Statement7 = TimeScen.timetScenarioSeven

		self.Choosing_Statement = TimeScen.timetChoosing
		self.Sideeffects_Statement= TimeScen.timetSideeffects
		self.Benefits_Statement = TimeScen.timetBenefits
		self.Agreement_Statement_A= TimeScen.timetAgreementA
		self.Agreement_Statement_E= TimeScen.timetAgreementE
		self.Agreement_Statement_B= TimeScen.timetAgreementB
		self.Welcome_Statement = TimeScen.timetWelcome

#################################################################################
#																				#
#																				#
#																				#
#																				#
#							Time Trade Off Calculations							#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################

#################################################################################
#Creating a class for the Time Tradeoff so that values are accessible as an object
#By doing this class setup now, it should be easy to import values
#More importantly, it should make for cleaner code
#TimeTradeOff has 
class TimeTradeOff:
	#When speaking of iterative that means you iterate or update values 
	#
	def __init__ (self):
		self.threshold = 40  #Starting and iterative time threshold
		self.thresh_step_high = 2 #High increment of stepping for best value
		self.threshold_max = 100 #math.ceiling value
		self.threshold_min = 0 #math.floor value
		self.thresh_step_refine = 1 #Small increment refinement
#################################################################################
#Load Information
	def load(self, titleid,a,r,h,g):
		"""
		Load information to the Gambler for Time trade off
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str	
		:param a: Age of user
		:type a: int	
		:param r: Race of user
		:type r: str	
		:param h: Hispanic/Latino designation
		:type h: int	
		:param g: Gender of user
		:type g: str
				
		:return: Value of whether to do the Time trade off in years (0) or months (1)
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		TimeTLog = GamblerInfo.get(GamblerInfo.titleid==titleid)
		db.close()
		z = self.aqle(a,r,h,g)
		self.threshold = round(z*(TimeTLog.inittimeThresh/100.0))
		self.thresh_step_high = (TimeTLog.postimetThresh) #High increment of stepping for best value
		self.thresh_step_refine = (0.01) #Refining stepping for best value
		self.threshold_max = z
		##POsisble bug, figure out how to do min time trhesh
		self.threshold_min = TimeTLog.mintimetThresh  #math.floor valu  	
		if (z < 5.0):
			self.threshold = self.threshold *12.0
			self.threshold_max = z *12.0 #math.ceiling value
			self.threshold_min = TimeTLog.mintimetThresh*12.0  #math.floor valuue
			self.thresh_step_refine = 1 
			return 1
		return 0
#################################################################################
#Aquire the life expectancy
	def aqle(self,a,r,h,g):
		"""
		Aquire life expectancy for users 
		:param a: Age of user
		:type a: int	
		:param r: Race of user
		:type r: str	
		:param h: Hispanic/Latino designation
		:type h: int	
		:param g: Gender of user
		:type g: str
				
		:return: Life expectancy of user (int)
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		q = LifeTable.get(LifeTable.Age ==a)	
		db.close()		
		if r == 'blk': #African American/Black Patients
			if g =="M":
				return round(q.AAMale)			
			elif g=="F":
				return round(q.AAFemale)		
			else:
				return round(q.AA)
		elif r =='asn': #ASIAN Paitnets
			if h ==1:
				if g =="M":
					return round(q.ASMale)		
				elif g=="F":
					return round(q.ASFemale)		
				else:
					return round(q.Asian)
		elif r =='hpi': #Pacific Islander Patients
			if g =="M":
				return round(q.ASMale)		
			elif g=="F":
				return round(q.ASFemale)		
			else:
				return round(q.Asian)
		elif r =='NAmerican':
			if g =="M":#Native/Alaskan Indigenous  Patients
				return round(q.NAMale)		
			elif g=="F":
				return round(q.NAFemale)		
			else:
				return round(q.NAmerican)	
		elif r =='wht': #White Patients
			if h ==1:
				if g =="M":
					return round(q.WHMale)		
				elif g=="F":
					return round(q.WHFemale)		
				else:
					return round(q.WHispanic)
			else:
				if g =="M":
					return round(q.WMale)		
				elif g=="F":
					return round(q.WFemale)		
				else:
					return round(q.White)		
		else: #Generic Infromation
			if g =="M":
				return round(q.Male)		
			elif g =="F":
				return round(q.Female)		

			else:
				return round(q.Citizen)		

#################################################################################
#Calculating the time trade off		
	def refine_threshold(self, user_input, count, th,mys=0): 	#mys = months year switch
		"""
		Calculates the increment of the tradeoff percentage and returns new value
		
		:param user_input: The user input/button press a person has done for either Alternative A or B
		:type user_input: int
		:param count: How many times a person has clicked either Alternative A or B
		:type count: int
		:param th: Current years/months in the trade off
		:type th: int
		:param mys: Months or years state for user
		:type mys: int
						
		:return: int
		"""	
		fvalue = 0
		
		if (abs(user_input) == 1):
			fvalue =  th + user_input*round(self.threshold_max*(self.thresh_step_high/100.0))
		else:
			#We're going to make an estimation that noone's going to want to swing more than 25% of the years when refining.
			#Create a holder
			thr =(round(user_input/2)*cospoints(count,round(self.threshold_max*0.25)))
			if (abs(thr) < 1):
				thr = round(user_input/2)*1 #We're going to make an educated guess that the next number jump will be 1 if the value of thr is 0 This is optimum for < 100 afterwards, it doesn't really matter
			fvalue = th + thr
		if (fvalue >= self.threshold_max):
			fvalue= self.threshold_max
		elif (fvalue  <= self.threshold_min):
			fvalue = self.threshold_min
			
#This rounds to either full months if calculating by fraction of years if calculating by years
		if (mys == 1):
			fvalue =  round(fvalue)
		else:
			fvalue =  round(fvalue,1)		

		return fvalue
