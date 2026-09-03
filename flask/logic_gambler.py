#!/usr/bin/env python
import re, os, sys, time, shutil, numpy, cgi, cgitb
from BaseModel import * #Get db variable from importing all
from peewee import *
from math import *
#Create a class for scenario building
#GScenario = GamblerScenario
#Base this class off of the BaseModel

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
	""" Calculate the swinging by clicks for users. """
	decm = (.1*points)
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
#							Standard Gamble Logic								#
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
#							Standard Gamble Setup								#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################
#################################################################################

class GScenario:
	def __init__(self):
		self.Scenario_Statement ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Scenario_Statement3 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Scenario_Statement4 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Scenario_Statement5 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Scenario_Statement6 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Scenario_Statement7 ="This is a scenario statement.\nIt wil tell you about the condition of @#@\n"
		self.Choosing_Statement = "This is the choosing statment.\nIt will ask you if you would want to choose the scenario.  It will tell you that you have @#@ pills out of &#& pills.\n"
		self.Sideeffects_Statement= "This is the side effect statement.\nIt will list the side effects.\n"
		self.Benefits_Statement = "This is the benefits statement.\nIt will list the benefits.\n"
		self.Agreement_Statement_A= "Alternative A" #This is a positive as in yes label
		self.Agreement_Statement_E = "Equal" #This is a neutral as in I don't know or meh label.
		self.Agreement_Statement_B = "Alternative B" #This is a negative as in no label.
		self.Welcome_Statement = "This is a welcoming statement to bring the user comfortably into the decision."
	#Database loading of the information
	def load(self, titleid,x=None):
		""" 
		Load information for Standard Gamble page
		
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
		:param Benefits_Statement: This statement explains part of the Gamble that's beneficial to users
		:type Scenario_Statement: str
		:param Sideeffects_Statement: This statement explains the negative effects of taking the Gamble to users
		:type Scenario_Statement: str		
		:param Agreement_Statement_A: Left side button normally used to choose the health state
		:type Agreement_Statement_A: str		
		:param Agreement_Statement_E: Middle button normally to end the Gamble
		:type Agreement_Statement_E: str		
		:param Agreement_Statement_B: Right side button normally used to choose The Gamble
		:type Agreement_Statement_B: str	
		:param Welcome_Statement: The introduction statement used to welcome patients to the Standard Gamble screen
		:type Welcome_Statement: str				
		
		:returns: Loaded information to self

		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==titleid)
		db.close()
		self.Scenario_Statement = GamScen.gambScenario
		self.Scenario_Statement3 = GamScen.gambScenarioThree
		self.Scenario_Statement4 = GamScen.gambScenarioFour
		self.Scenario_Statement5 = GamScen.gambScenarioFive
		self.Scenario_Statement6 = GamScen.gambScenarioSix
		self.Scenario_Statement7 = GamScen.gambScenarioSeven
		self.Choosing_Statement = GamScen.gambChoosing
		self.Sideeffects_Statement= GamScen.gambSideeffects
		self.Benefits_Statement = GamScen.gambBenefits
		self.Agreement_Statement_A= GamScen.gambAgreementA
		self.Agreement_Statement_E= GamScen.gambAgreementE
		self.Agreement_Statement_B= GamScen.gambAgreementB
		self.Welcome_Statement = GamScen.gambWelcome
	##Build a secnearion SBuild = Secnario build
	#X is new threshold, y is total amount or percentage

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
#Builds the choosing decision information 
	def CBuild(self, x, y,w):
		"""Builds choosing statement for Gambler
		
		:param x: The amount of cure pills that would be in the bottle
		:type x: int	
		:param y: The total amount of pills in pill bottle
		:type y: int				
		:param w: The intermediate health state (health state being evaluated against the Gamble)
		:type w: int
				
		:returns: Statement with health state
		"""
##  $#$ <- Live pills &#& <-Total pills %#% <-Dead pills @#@ <-Intermediate Health state
		z = self.Choosing_Statement.replace("$#$", str(int(x)))
		z = z.replace("&#&", str(int(y)))
		z = z.replace("@#@", str(w))
		z = z.replace("%#%", str(int(y-x)))
		return z

#Creating a class for the Gambler so that values are accessible as an object
#By doing this class setup now, it should be easy to import values
#More importantly, it should make for cleaner code

#################################################################################
#																				#
#																				#
#																				#
#																				#
#							Gambler Calculations 								#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################
class Gambler:
	#When speaking of iterative that means you iterate or update values 
	#
	"""Gambler class that holds the mechanism to perform standard gamble """
	def __init__ (self):
		self.threshold = 50  #Starting and iterative threshold
		self.thresh_step_high = 10 #High increment of stepping for best value
		self.thresh_step_low = 5 #Low decrement of stepping for best value
		self.thresh_step_refine = 1 #Refining stepping for best value
		self.threshold_max = 100 #Ceiling value
		self.threshold_min = 0 #Floor value

	def load(self, titleid):
		"""
		Load information to the Gambler
		
		:param titleid: The titleid (foldername) of the Gambler project
		:type titleid: str		
		:return: Self loaded data from database
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		GamLog = GamblerInfo.get(GamblerInfo.titleid==titleid)
		self.threshold = GamLog.initgambThresh
		self.thresh_step_high = GamLog.posgambThresh #High increment of stepping for best value
		self.thresh_step_refine = 1 #Refining stepping for best value
		self.threshold_max = GamLog.maxgambThresh #Low decrement of stepping for best value
		self.threshold_min = GamLog.mingambThresh #Low decrement of stepping for best value
		db.close()


	def refine_threshold(self, user_input, count, th):
		"""
		Calculates the increment of the tradeoff percentage and returns new value
		
		:param user_input: The user input/button press a person has done for either Alternative A or B
		:type user_input: int
		:param count: How many times a person has clicked either Alternative A or B
		:type count: int
		:param th: Current pill amount
		:type th: int
				
		:return: int
		"""	

		fvalue = 0
		if (abs(user_input) == 1):
			fvalue =  th + user_input*self.thresh_step_high	
		else:
			fvalue = th + round(user_input/2)*cospoints(count,self.thresh_step_high)
		if (fvalue >= self.threshold_max):
			return self.threshold_max
		elif (fvalue  <= self.threshold_min):
			return self.threshold_min
		elif (fvalue == th):
			fvalue = fvalue + (user_input/abs(user_input))
			return fvalue
		else:
			return fvalue
		
