#!/usr/bin/env python
##Build using Bootstrap, Flask, Flask-WTForms
import re, os, sys, time, shutil, numpy, cgi, cgitb, json
from flask_wtf import FlaskForm
import wtforms
#from wtforms import StringField, IntegerField, BooleanField, RadioField, SelectField

from wtforms import validators, ValidationError
##Don't use Self for WTForms
#See: Why doesn't adding fields to self work?
#http://stackoverflow.com/questions/31160781/wtforms-generate-fields-in-constructor

from UserInfo import *
from language_pack import *

##This contains the demographics of the user which can be used to help customize the experience.
##Redundancies are made to ensure the reusability of the package
class Demographics(FlaskForm):
	"""Demographics page class """
###Putting d in front of varibales for clarification for python
	duserid = wtforms.StringField("User ID") #User ID which maybe useful
	dfirstname = wtforms.StringField("Firstname",[validators.DataRequired("Please enter your first name.")])
	dlastname = wtforms.StringField("Lastname",[validators.DataRequired("Please enter your last name.")])
	dage = wtforms.IntegerField("Age", [validators.DataRequired("Please enter your age.")])
	dhld = wtforms.BooleanField('Hispanic/Latino') #Hispanic/Latino designator
	dgender = wtforms.SelectField('Gender', choices = [('F','Female'),('M','Male'), ('O','Non-binary/Other')],default='O')
	drace = wtforms.SelectField('Race', choices = [('blk', 'African/Black American'), ('asn', 'Asian'), ('hpi', 'Hawaiian/Pacific Islander'), ('nam', 'Native/Alsaka American'), ('mna', 'Middle Eastern/North African'), ('wht', 'White')])
	dinstructions = wtforms.BooleanField('Click here to turn off video instructions',default='checked')

	def langload(self,lang="en-US",country="USA"):
		"""Load language for the Demographics page 
		
		:param lang: Language code
		:type: str
		:param country: Country code
		:type: str
		:return: Loaded object into self
		"""	
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		if lang != "en-US":
			LangLoad = LangUserSystemTranslate.get(LangUserSystemTranslate.language == lang)	
			LangGRLoad = LangUserGenderRaceSystemTranslate.get(LangUserGenderRaceSystemTranslate.demographics_language == lang)	
			self.duserid.label.text = LangLoad.Demo_userid_text #User ID which maybe useful
			self.dfirstname.label.text = LangLoad.Demo_firstname_text
			self.dfirstname.validators = [validators.DataRequired(LangLoad.Demo_firstname_warn_text)]
			self.dlastname.label.text = LangLoad.Demo_lastname_text
			self.dlastname.validators = [validators.DataRequired(LangLoad.Demo_lastname_warn_text)]
			self.dage.label.text = LangLoad.Demo_age_text
			self.dage.validators= [validators.DataRequired(LangLoad.Demo_age_warn_text)]
			self.dhld.label.text = LangLoad.Demo_hld_text #Hispanic/Latino designator
			self.dgender.label.text = LangLoad.Demo_gender_text
			gc = json.loads(LangGRLoad.demographics_gender.replace("\'","\""))
			genderchoice = [(key,value) for key,value in gc.items()]
			self.dgender.choices = genderchoice
			self.dgender.default = LangGRLoad.demographics_gender_default
			self.drace.label.text = LangLoad.Demo_race_text
			rc = json.loads(LangGRLoad.demographics_race.replace("\'","\""))
			racechoice = [(key,value) for key,value in rc.items()]
			self.drace.choices = racechoice
			self.drace.default = LangGRLoad.demographics_race_default
			self.dinstructions.label.text = LangLoad.Demo_videoinstructions_text
			db.close()
##We're going to take a hack approach to saving data to the database.
##DEmographics Storage
	def savedemo(self, gtid):
		"""Save Demographic infomration 
		
		:param gtid: Gambler project name/folder
		:type: str
		:return: Gambler database ID 
		"""	
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = UserInfo.select().where(UserInfo.userid==self.duserid.data, UserInfo.titleid==gtid)
		if query.exists():
			return -1
		GamUI = UserInfo(userid=self.duserid.data, firstname=self.dfirstname.data, lastname=self.dlastname.data,hld=int(self.dhld.data == True), age=self.dage.data, gender=self.dgender.data, race=self.drace.data, titleid=gtid)
		GamUI.save()
		w = GamUI.uid
		db.close()
		return w
		

