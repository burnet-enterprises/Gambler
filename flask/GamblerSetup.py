#!/usr/bin/env python
#GamblerSetup.py
##Build using Bootstrap, Flask, Flask-WTForms
import re, os, sys, time, shutil, numpy, cgi, cgitb
from flask_wtf import FlaskForm
#Importing FileField and require as well as secure_file name from respective package as to allow for upload via special flask WTF format
from flask_wtf.file import FileField, FileRequired
#from wtforms import StringField, IntegerField, BooleanField, TextAreaField as wtforms.StringField, wtforms.IntegerField, wtforms.BooleanField, wtforms.TextAreaField
from BaseModel import *
from wtforms import validators, ValidationError
import wtforms
from werkzeug.utils import secure_filename
##Don't use Self for WTForms
#See: Why doesn't adding fields to self work?
#http://stackoverflow.com/questions/31160781/wtforms-generate-fields-in-constructor
from language_pack import *

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

###Edit Gambler Page
class EditGambler(FlaskForm):
	"""Loads fields for selecting which Gambler project you want to edit"""
	choice = [(0, "Temp")]
	gamblertitle = wtforms.SelectField("Gambler Project Folder", choices = choice, validators=[validators.Optional()])
	gamblerid  = wtforms.StringField("Gambler unique ID", validators=[validators.Optional()])
	prefil = wtforms.SelectField("Previous Gambler Project", choices = choice, validators=[validators.Optional()])


##Select Gambler Page
class SelectGambler(FlaskForm):
	"""Loads fields for selecting a Gambler project"""
	choice = [(0, "Temp")]
	gamblertitle = wtforms.SelectField("Gambler Project Folder", choices = choice, validators=[validators.Optional()])
	
#Select Langauge Page
class SelectLanguage(FlaskForm):
	"""Loads fields for selecting what langauge you want to use"""
	choice = [("en-US", "US English"), ("es-ES", "España Español")]
	languageselect = wtforms.SelectField("Language Selection", choices = choice, validators=[validators.Optional()])

class GamblerImageSetupEdit(FlaskForm):
	"""Creates form that allows users to edit Gambler health state images and general information video fields"""
	xw = ""
	conditionOneimage = FileField("First Health State Image", description="No saved filed")
	conditionTwoimage = FileField("Second Health State Image", description="No saved filed")
	conditionThreeimage = FileField("Third Health State Image", description="No saved filed")
	conditionFourimage = FileField("Fourth Health State Image", description="No saved filed")
	conditionFiveimage = FileField("Fifth Health State Image", description="No saved filed")
	conditionSiximage = FileField("Sixth Health State Image", description="No saved filed")
	conditionSevenimage = FileField("Seventh Health State Image", description="No saved filed")
	conditionEightimage = FileField("Eighth Health State Image", description="No saved filed")
	setSGC = wtforms.BooleanField("Check the box to use include customized Standard Gamble Videos for each intermediate health state", default=False) #Set Standard Gamble Custom
	setTTC= wtforms.BooleanField("Check the box to use include customized Time Trade-off Videos for each intermediate health state", default=False)#Set Time Tradeoff Custom
##General Instructions Video
	conditionORIS= FileField("Ordinal Ranking General Instructions Video", description="No saved filed")
	conditionITIS= FileField("Visual Analog Scale General Instructions Video", description="No saved filed")
	conditionSGIS= FileField("Standard Gamble General Instructions Video", description="No saved filed")
	conditionTTIS= FileField("Time Trade Off Standard Instructions Video", description="No saved filed")
	conditionSIIS= FileField("Health State Description Page Instructions Video", description="No saved filed")
#Custom Instructions Video
	conditionTwoSGI = FileField("Second Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionThreeSGI = FileField("Third Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionFourSGI = FileField("Fourth Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionFiveSGI = FileField("Fifth Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionSixSGI = FileField("Sixth Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionSevenSGI = FileField("Seventh Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionTwoTTI = FileField("Second Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionThreeTTI = FileField("Third Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionFourTTI = FileField("Fourth Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionFiveTTI = FileField("Fifth Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionSixTTI = FileField("Sixth Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionSevenTTI = FileField("Seventh Health State Time Trade Off Instructions Video", description="No saved filed")
	def save(self,gid,mv):
		"""Save data about the image/video files and the mechanisms to do it.
		
		:param gid: Project folder name/Database Id
		:type: str / int
		:param mv: Gambler mechansim for projects that will be edited
		:type: int
		"""
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		GambleLoader = GamblerInfo()
		try:
			int(gid)
			GambleLoader = GambleLoader.get(GamblerInfo.gambleid == gid)
		except ValueError:
			GambleLoader = GambleLoader.get(GamblerInfo.titleid == gid)
		a="None"
		b="None"
		c="None"
		d="None"
		e="None"
		f="None"
		g="None"
		h="None"
		if (self.conditionOneimage.data is not None):
			a="image1." + self.conditionOneimage.data.filename[-3:].lower()
		else:
			a = GambleLoader.imageOnename
		if (self.conditionTwoimage.data is not None):
			b="image2." + self.conditionTwoimage.data.filename[-3:].lower()
		else:
			b = GambleLoader.imageTwoname
		if (self.conditionThreeimage.data is not None):
			c="image3." + self.conditionThreeimage.data.filename[-3:].lower()
		else:
			c  = GambleLoader.imageThreename
		if (self.conditionFourimage.data is not None):
			d="image4." + self.conditionFourimage.data.filename[-3:].lower()
		else:
			d =  GambleLoader.imageFourname
		if(self.conditionFiveimage.data is not None):
			e="image5." + self.conditionFiveimage.data.filename[-3:].lower()
		else:
			e = GambleLoader.imageFivename
		if(self.conditionSiximage.data is not None):
			f="image6." + self.conditionSiximage.data.filename[-3:].lower()
		else:
			f = GambleLoader.imageSixname
		if( self.conditionSevenimage.data is not None):
			g="image7." + self.conditionSevenimage.data.filename[-3:].lower()
		else:
			g = GambleLoader.imageSevenname
		if(self.conditionEightimage.data is not None):
			h="image8." + self.conditionEightimage.data.filename[-3:].lower()
		else:
			h = GambleLoader.imageEightname
		if mv > 0:
			xw = GambleLoader.mechgamb
			xw = xw[0:4] + str(mv)
		else:
			xw = GambleLoader.mechgamb
		GamInfo = GamblerInfo(gambleid=GambleLoader.gambleid, mechgamb = xw, imageOnename = a, imageTwoname = b, imageThreename = c, imageFourname = d, imageFivename = e, imageSixname = f, imageSevenname =g, imageEightname = h)
		GamInfo.save()
		db.close()
		
	def load(self,gid):
		"""Save data about the image/video files and the mechanisms to do it.
		
		:param gid: Project folder name/Database Id
		:type: str / int
		:param mv: Gambler mechansim for projects that will be edited
		:type: int
		"""
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==gid)
		self.conditionOneimage.description = GamScen.imageOnename
		self.conditionTwoimage.description = GamScen.imageTwoname
		self.conditionThreeimage.description = GamScen.imageThreename
		if (GamScen.imageFourname is not None):
			self.conditionFourimage.description = GamScen.imageFourname
		if (GamScen.imageFivename is not None):
			self.conditionFiveimage.description = GamScen.imageFivename
		if (GamScen.imageSixname is not None):
			self.conditionSiximage.description = GamScen.imageSixname
		if (GamScen.imageSevenname is not None):
			self.conditionSevenimage.description = GamScen.imageSevenname
		if (GamScen.imageEightname is not None):
			self.conditionEightimage.description = GamScen.imageEightname
		db.close()

class GamblerImageSetup(FlaskForm):
	"""Creates form that allows users to create new slots for  Gambler health state images and general information video fields"""
	xw =""
	conditionOneimage = FileField("First Health State Image", description="No saved filed", validators=[FileRequired()])
	conditionTwoimage = FileField("Second Health State Image", description="No saved filed", validators=[FileRequired()])
	conditionThreeimage = FileField("Third Health State Image", description="No saved filed", validators=[FileRequired()])
	conditionFourimage = FileField("Fourth Health State Image", description="No saved filed")
	conditionFiveimage = FileField("Fifth Health State Image", description="No saved filed")
	conditionSiximage = FileField("Sixth Health State Image", description="No saved filed")
	conditionSevenimage = FileField("Seventh Health State Image", description="No saved filed")
	conditionEightimage = FileField("Eighth Health State Image", description="No saved filed")
	setSGC = wtforms.BooleanField("Check the box to use include customized Standard Gamble Videos for each intermediate health state", default=False) #Set Standard Gamble Custom
	setTTC= wtforms.BooleanField("Check the box to use include customized Time Trade-off Videos for each intermediate health state", default=False)#Set Time Tradeoff Custom
##General Instructions Video
	conditionORIS= FileField("Ordinal Ranking General Instructions Video", description="No saved filed")
	conditionITIS= FileField("Visual Analog Scale General Instructions Video", description="No saved filed")
	conditionSGIS= FileField("Standard Gamble General Instructions Video", description="No saved filed")
	conditionTTIS= FileField("Time Trade Off Standard Instructions Video", description="No saved filed")
	conditionSIIS= FileField("Health State Description Page Instructions Video", description="No saved filed")
#Custom Instructions Video
	conditionTwoSGI = FileField("Second Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionThreeSGI = FileField("Third Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionFourSGI = FileField("Fourth Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionFiveSGI = FileField("Fifth Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionSixSGI = FileField("Sixth Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionSevenSGI = FileField("Seventh Health State Standard Gamble Instructions Video", description="No saved filed")
	conditionTwoTTI = FileField("Second Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionThreeTTI = FileField("Third Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionFourTTI = FileField("Fourth Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionFiveTTI = FileField("Fifth Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionSixTTI = FileField("Sixth Health State Time Trade Off Instructions Video", description="No saved filed")
	conditionSevenTTI = FileField("Seventh Health State Time Trade Off Instructions Video", description="No saved filed")
	def save(self,gid,mv):
		"""Save data about the image/video files and the mechanisms to do it.
		
		:param gid: Project folder name/Database Id
		:type: str / int
		:param mv: Gambler mechansim for projects that will be edited
		:type: int
		"""
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		a="None"
		b="None"
		c="None"
		d="None"
		e="None"
		f="None"
		g="None"
		h="None"
		try:
			a="image1." + self.conditionOneimage.data.filename[-3:].lower()
		except AttributeError:
			a="image1." + self.conditionOneimage.data['filename'][-3:].lower()
		try:
			b="image2." + self.conditionTwoimage.data.filename[-3:].lower()
		except AttributeError:
			b="image2." + self.conditionTwoimage.data['filename'][-3:].lower()
		try:
			c="image3." + self.conditionThreeimage.data.filename[-3:].lower()
		except AttributeError:
			c="image3." + self.conditionThreeimage.data['filename'][-3:].lower()
		if (self.conditionFourimage.data is not None):
				try:
					d="image4." + self.conditionFourimage.data.filename[-3:].lower()
				except AttributeError:
					d="image4." + self.conditionFourimage.data['filename'][-3:].lower()
		if(self.conditionFiveimage.data is not None):
				try:
					e="image5." + self.conditionFiveimage.data.filename[-3:].lower()
				except AttributeError:
					e="image5." + self.conditionFiveimage.data['filename'][-3:].lower()
		if(self.conditionSiximage.data is not None):
				try:
					f="image6." + self.conditionSiximage.data.filename[-3:].lower()
				except AttributeError:
					f="image6." + self.conditionSiximage.data['filename'][-3:].lower()
		if( self.conditionSevenimage.data is not None):
				try:
					g="image7." + self.conditionSevenimage.data.filename[-3:].lower()
				except AttributeError:
					g="image7." + self.conditionSevenimage.data['filename'][-3:].lower()
		if(self.conditionEightimage.data is not None):
				try:
					h="image8." + self.conditionEightimage.data.filename[-3:].lower()
				except AttributeError:
					h="image8." + self.conditionEightimage.data['filename'][-3:].lower()
		GambleLoader = GamblerInfo()
		try:
			int(gid)
			GambleLoader = GambleLoader.get(GamblerInfo.gambleid == gid)
		except ValueError:
			GambleLoader = GambleLoader.get(GamblerInfo.titleid == gid)
		if mv > 0:
			xw = GambleLoader.mechgamb
			xw = xw[0:4] + str(mv)
		else:
			xw = GambleLoader.mechgamb
		GamInfo = GamblerInfo(gambleid=GambleLoader.gambleid, mechgamb = xw, imageOnename = a, imageTwoname = b, imageThreename = c, imageFourname = d, imageFivename = e, imageSixname = f, imageSevenname =g, imageEightname = h)
		GamInfo.save()
		db.close()
		
	def load(self,gid):
		"""Save data about the image/video files and the mechanisms to do it.
		
		:param gid: Project folder name/Database Id
		:type: str / int
		:param mv: Gambler mechansim for projects that will be edited
		:type: int
		"""
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		GamScen = GamblerInfo.get(GamblerInfo.titleid==gid)
		self.conditionOneimage.description = GamScen.imageOnename
		self.conditionTwoimage.description = GamScen.imageTwoname
		self.conditionThreeimage.description = GamScen.imageThreename
		if (GamScen.imageFourname is not None):
			self.conditionFourimage.description = GamScen.imageFourname
		if (GamScen.imageFivename is not None):
			self.conditionFiveimage.description = GamScen.imageFivename
		if (GamScen.imageSixname is not None):
			self.conditionSiximage.description = GamScen.imageSixname
		if (GamScen.imageSevenname is not None):
			self.conditionSevenimage.description = GamScen.imageSevenname
		if (GamScen.imageEightname is not None):
			self.conditionEightimage.description = GamScen.imageEightname
		db.close()
			
##This contains the demographics of the user which can be used to help customize the experience.
class GamblerSetup(FlaskForm):
	"""Creation of a Gambler Project"""
	ogamblertitle = wtforms.StringField("Title of Gambler") #User ID which maybe useful
	gamblertitle = wtforms.StringField("Folder Name to store Gambler project data", [validators.DataRequired("Please enter a value")]) #User ID which maybe useful
	conditionOnetext  = wtforms.StringField("First Health State", [validators.DataRequired("Please enter a value")] )
	conditionTwotext   = wtforms.StringField("Second Health State", [validators.DataRequired("Please enter a value")])
	conditionThreetext   = wtforms.StringField("Third Health State", [validators.DataRequired("Please enter a value")])
	conditionFourtext   = wtforms.StringField("Fourth Health State")
	conditionFivetext   = wtforms.StringField("Fifth Health State")
	conditionSixtext   = wtforms.StringField("Sixth Health State")
	conditionSeventext   = wtforms.StringField("Seventh Health State")
	conditionEighttext   = wtforms.StringField("Eighth Health State")
	conditionOneAC  = wtforms.StringField("First Health State \nAbbreviation", [validators.DataRequired("Please enter a value")] )
	conditionTwoAC   = wtforms.StringField("Second Health State \nAbbreviation", [validators.DataRequired("Please enter a value")])
	conditionThreeAC   = wtforms.StringField("Third Health State \nAbbreviation", [validators.DataRequired("Please enter a value")])
	conditionFourAC   = wtforms.StringField("Fourth Health State \nAbbreviation")
	conditionFiveAC   = wtforms.StringField("Fifth Health State \nAbbreviation")
	conditionSixAC   = wtforms.StringField("Sixth Health State \nAbbreviation")
	conditionSevenAC   = wtforms.StringField("Seventh Health State \nAbbreviation")
	conditionEightAC   = wtforms.StringField("Eighth Health State \nAbbreviation")
	conditionOneInfo  = wtforms.TextAreaField("First Health State Description")
	conditionTwoInfo   = wtforms.TextAreaField("Second Health State Description")
	conditionThreeInfo   = wtforms.TextAreaField("Third Health State Description")
	conditionFourInfo   = wtforms.TextAreaField("Fourth Health State Description")
	conditionFiveInfo   = wtforms.TextAreaField("Fifth Health State Description")
	conditionSixInfo   = wtforms.TextAreaField("Sixth Health State Description")
	conditionSevenInfo   = wtforms.TextAreaField("Seventh Health State Description")
	conditionEightInfo   = wtforms.TextAreaField("Eight Health State Description")
	initgambThresh  = wtforms.IntegerField("Initial Starting Gambler Value (Pills)", default=50)
	posgambThresh  = wtforms.IntegerField("Gambler Large Adjustment (Pills)", default=5)
	maxgambThresh  = wtforms.IntegerField("Maximum Gambler Amount (Pills)", default=100)
	mingambThresh  = wtforms.IntegerField("Minimum Gambler Amount (Pills)", default=0)
	gambScenario   = wtforms.TextAreaField("Describe Second Intermediate Health State Scenario for  User.\nPlease use format\nPlease use format \"you suffer from @#@ \" to designate the place for the health state  " )
	gambChoosing   = wtforms.TextAreaField("Describe Choice for User. Use the following macros for the following:<br/> $#$ : Cure pills <br/>&#& :Total pills <br/>%#% :Dead pills  <br/>@#@ :Intermediate Health state")
	gambBenefits  = wtforms.TextAreaField("Describe Benefits for User", default="Benefits")
	gambWelcome   = wtforms.TextAreaField("Enter General Standard Gamble Instructions for User", default = "INSTRUCTIONS - To determine how you value various health outcomes, it is necessary to ask you a series of questions, which require you to make choices between these states of health. The certain outcome (graphically represented by Figure A below) is the one for which your values are being sought; the gamble (graphically represented by Figure B below) is between the best and worst possible outcomes. You must indicate which of the two alternatives you prefer by clicking on either the Alternative A or Alternative B buttons. Once you have indicated your preference, you may be asked to choose again, but this time the probabilities associated with the gamble are altered. This procedure continues until you show no preference for either choice by clicking the Equal button.  Click the Begin Button to get started.")
	gambSideeffects  = wtforms.StringField("Describe Sideeffects for User", default="Sideeffects")
	gambAgreementA  = wtforms.StringField("Choice A Label", default = "Alternative A")
	gambAgreementE  = wtforms.StringField("Equal Choice Label", default = "Equal")
	gambAgreementB = wtforms.StringField("Choice B Label", default = "Alternative B")
	inittimetThresh  = wtforms.IntegerField("Initial Starting Time Tradeoff Percent", default=50)
	postimetThresh  = wtforms.IntegerField("Time Tradeoff Large Adjustment Percent", default=10)
	maxtimetThresh  = wtforms.IntegerField("Maximum Time Tradeoff Percent", default=100)
	mintimetThresh  = wtforms.IntegerField("Minimum Time Tradeoff Percent", default=0)
	timetScenario   = wtforms.TextAreaField("Describe  Second Intermediate Health State Scenario for User.\nPlease use format \"you suffer from @#@ \" to designate the place for the health state  ")
	timetChoosing   = wtforms.TextAreaField("Describe Choice for User. Use the following macros for the following:<br/> $#$ : Cure time <br/>&#& :Total time <br/>%#% :Dead time  <br/>*#* :Units of Time <br/>@#@ :Intermediate Health state")
	timetBenefits  = wtforms.TextAreaField("Describe Benefits for User", default="Benefits")
	timetWelcome   = wtforms.TextAreaField("Enter General Time Trade off Instructions", default="INSTRUCTIONS - To determine how you value various health outcomes, it is necessary to ask you a series of questions, which require you to make choices between several states of health. The intermediate outcome (graphically represented by Figure A to the left) has a fixed survival (expressed in years) and is the one for which your values are being sought. You will be asked to choose between this and the best outcome (graphically represented by Figure B to the right) which provides a shorter life expectancy, but greater quality of life. You must indicate which of the two alternatives you prefer by clicking on either the buttons for Alternative A or Alternative B. Once you have indicated your preference, you may be asked to choose again, but this time the survival of the best outcome will be varied. This procedure continues until you show no preference for either choice by clicking the Equal button.  A double click on an icon will bring up a secondary window with a more detailed description of that health state. Click the Begin Button to get started.")
	timetSideeffects  = wtforms.StringField("Describe Sideeffects for User", default="Sideeffects")
	timetAgreementA  = wtforms.StringField("Choice A Label", default = "Alternative A")
	timetAgreementE  = wtforms.StringField("Equal Choice Label", default = "Equal")
	timetAgreementB = wtforms.StringField("Choice B Label", default = "Alternative B")
	selectOrdinal = wtforms.BooleanField("Uncheck the box to remove the Ordinal Utility", default=True)
	selectScale= wtforms.BooleanField("Uncheck the box to remove the Visual Analog Scale Utility", default=True)
	selectVideo= wtforms.BooleanField("Check box to enable the viewing of health state video clips", default=False)
	selectGambler = wtforms.BooleanField("Uncheck the box to remove the Gambler Utility", default=True)
	selectTime =wtforms.BooleanField("Uncheck the box to remove the Time Tradeoff Utility", default=True)
	selectAmount = wtforms.SelectField("How many states do you want for your setup",choices=[('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8')], default=3)
	gambScenarioThree   = wtforms.TextAreaField("Describe Third Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \" @#@ \" to designate the place for the health state  " )
	gambScenarioFour   = wtforms.TextAreaField("Describe Fourth Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \" @#@ \" to designate the place for the health state  " )
	gambScenarioFive   = wtforms.TextAreaField("Describe Fifth Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \" @#@ \" to designate the place for the health state  " )
	gambScenarioSix   = wtforms.TextAreaField("Describe Sixth Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \"@#@ \" to designate the place for the health state  " )
	gambScenarioSeven   = wtforms.TextAreaField("Describe Seventh Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \"@#@ \" to designate the place for the health state  " )
	timetScenarioThree   = wtforms.TextAreaField("Describe Third Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \" @#@ \" to designate the place for the health state  " )
	timetScenarioFour   = wtforms.TextAreaField("Describe Fourth Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \" @#@ \" to designate the place for the health state  " )
	timetScenarioFive   = wtforms.TextAreaField("Describe Fifth Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \" @#@ \" to designate the place for the health state  " )
	timetScenarioSix   = wtforms.TextAreaField("Describe Sixth Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \"@#@ \" to designate the place for the health state  " )
	timetScenarioSeven   = wtforms.TextAreaField("Describe Seventh Intermediate Health State Scenario for User.\nPlease use format\nPlease use format \"@#@ \" to designate the place for the health state  " )
	selectLanguage =wtforms.SelectField("Select project language",choices=[(c.language, c.language_name) for c in LangCode.select(LangCode.language, LangCode.language_name)], default='en-US')
	selectSonFHR= wtforms.BooleanField("Deploy Smart on FHR Integration.", default=False)
	selectGenranduid= wtforms.BooleanField("Generate random user ID.", default=False)
	selectDisablepatname = wtforms.BooleanField("Disable patient name identification.", default=False)
	selectDisablepatage= wtforms.BooleanField("Disable patient age.", default=False)
	selectDisablepatrace = wtforms.BooleanField("Disable patient race.", default=False)
	selectDisablepatgender= wtforms.BooleanField("Disable patient gender.", default=False)
	selectlocalStorage= wtforms.BooleanField("Click to store data only locally to the computer.", default=False)
	def save(self):
		"""Saves data to the database

		:return: 0 (int)
		:error: -1 (if project exists)
		"""
		setup=""
		if (self.selectOrdinal.data == True):
			setup+=self.selectAmount.data
		else:
			setup+="0"
		if (self.selectScale.data ==True):
			setup+=self.selectAmount.data
		else:
			setup+="0"
		if (self.selectGambler.data == True):
			setup+=self.selectAmount.data
		else:
			setup+="0"
		if (self.selectTime.data == True):
			setup+=self.selectAmount.data
		else:
			setup+="0"
		if (self.selectVideo.data == True):
			setup+="1"
		else:
			setup+="0"
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		if (self.gambScenarioFour.data is None):
			self.gambScenarioFour.data=self.gambScenario.data
		if(self.gambScenarioFive.data is None):
			self.gambScenarioFive.data=self.gambScenario.data
		if(self.gambScenarioSix.data is None):
			self.gambScenarioSix.data=self.gambScenario.data
		if( self.gambScenarioSeven.data is None):
			self.gambScenarioSeven.data =self.gambScenario.data
		if(self.gambScenarioThree.data is None):
			self.gambScenarioThree.data= self.gambScenario.data
			
		if (self.timetScenarioFour.data is None):
			self.timetScenarioFour.data=self.timetScenario.data
		if(self.timetScenarioFive.data is None):
			self.timetScenarioFive.data=self.timetScenario.data
		if(self.timetScenarioSix.data is None):
			self.timetScenarioSix.data=self.timetScenario.data
		if( self.timetScenarioSeven.data is None):
			self.timetScenarioSeven.data =self.timetScenario.data
		if(self.timetScenarioThree.data is None):
			self.timetScenarioThree.data= self.timetScenario.data
		query = GamblerInfo.select().where(GamblerInfo.titleid==self.gamblertitle.data)
		if query.exists():
			return -1			

		GamInfo = GamblerInfo(titleid=self.gamblertitle.data.replace(" ", "_"), otitleid=self.ogamblertitle.data,mechgamb = setup, conditionOne=self.conditionOnetext.data,conditionTwo=self.conditionTwotext.data, conditionThree=self.conditionThreetext.data,conditionFour=self.conditionFourtext.data, conditionFive=self.conditionFivetext.data,conditionOneInfo=self.conditionOneInfo.data,
		conditionTwoInfo=self.conditionTwoInfo.data,conditionThreeInfo=self.conditionThreeInfo.data,conditionFourInfo=self.conditionFourInfo.data,conditionFiveInfo=self.conditionFiveInfo.data,
		initgambThresh=self.initgambThresh.data,posgambThresh=self.posgambThresh.data,maxgambThresh=self.maxgambThresh.data,mingambThresh=self.mingambThresh.data,gambScenario=self.gambScenario.data, gambChoosing= self.gambChoosing.data,gambBenefits=self.gambBenefits.data,gambWelcome=self.gambWelcome.data,gambSideeffects=self.gambSideeffects.data,
		gambAgreementA=self.gambAgreementA.data,gambAgreementE=self.gambAgreementE.data, gambAgreementB=self.gambAgreementB.data,inittimeThresh=self.inittimetThresh.data,postimetThresh=self.postimetThresh.data,maxtimetThresh=self.maxtimetThresh.data,mintimetThresh=self.mintimetThresh.data,timetScenario=self.timetScenario.data,timetChoosing=self.timetChoosing.data,
		timetBenefits=self.timetBenefits.data,timetWelcome=self.timetWelcome.data,timetSideeffects=self.timetSideeffects.data,timetAgreementA=self.timetAgreementA.data,timetAgreementE=self.timetAgreementE.data,timetAgreementB=self.timetAgreementB.data, 
		conditionSix = self.conditionSixtext.data, conditionSeven=self.conditionSeventext.data, conditionEight=self.conditionEighttext.data, conditionSixInfo=self.conditionSixInfo.data, conditionSevenInfo=self.conditionSevenInfo.data, conditionEightInfo=self.conditionEightInfo.data, conditionOneAC=str(self.conditionOneAC.data).replace(" ", ""),
		conditionTwoAC=str(self.conditionTwoAC.data).replace(" ", ""),conditionThreeAC=str(self.conditionThreeAC.data).replace(" ", ""),conditionFourAC=str(self.conditionFourAC.data).replace(" ", ""),conditionFiveAC=str(self.conditionFiveAC.data).replace(" ", ""),conditionSixAC=str(self.conditionSixAC.data).replace(" ", ""),conditionSevenAC=str(self.conditionSevenAC.data).replace(" ", ""),conditionEightAC=str(self.conditionEightAC.data).replace(" ", ""),
		gambScenarioThree = self.gambScenarioThree.data,gambScenarioFour = self.gambScenarioFour.data,gambScenarioFive = self.gambScenarioFive.data,gambScenarioSix = self.gambScenarioSix.data,
		gambScenarioSeven = self.gambScenarioSeven.data,timetScenarioThree = self.timetScenarioThree.data,timetScenarioFour = self.timetScenarioFour.data,timetScenarioFive = self.timetScenarioFive.data,timetScenarioSix = self.timetScenarioSix.data,timetScenarioSeven = self.timetScenarioSeven.data,
		language=self.selectLanguage.data, SonFHR=self.selectSonFHR.data,genranduid=self.selectGenranduid.data,disablepatname=self.selectDisablepatname.data,disablepatage=self.selectDisablepatage.data,disablepatgender=self.selectDisablepatgender.data,disablepatrace=self.selectDisablepatrace.data, localStorage = self.selectlocalStorage.data)
		GamInfo.save()
		db.close()
		return 0
	def resave(self,gid):
		"""Reaves data to the database

		:param gid: The titleid/folder name of the Gambler project
		:type: str
		:return: 0 (int)
		:error: -1 (if project exists)
		"""
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		GambleLoader = GamblerInfo()
		try:
			int(gid)
			GambleLoader = GambleLoader.get(GamblerInfo.gambleid == gid)
		except ValueError:
			GambleLoader = GambleLoader.get(GamblerInfo.titleid == gid)
		mechcheck = GambleLoader.mechgamb
		setup=""
		if (self.selectOrdinal.data == True):
			setup+=self.selectAmount.data
		else:
			setup+="0"
		if (self.selectScale.data ==True):
			setup+=self.selectAmount.data
		else:
			setup+="0"
		if (self.selectGambler.data == True):
			setup+=self.selectAmount.data
		else:
			setup+="0"
		if (self.selectTime.data == True):
			setup+=self.selectAmount.data
		else:
			setup+="0"
		if (self.selectVideo.data == True):
			if int(mechcheck[len(mechcheck)-1]) > 1:
				setup+=mechcheck[len(mechcheck)-1] 
			else:
				setup+="1"
		else:
			setup+="0"

		if (self.gambScenarioFour.data is None):
			self.gambScenarioFour.data=self.gambScenario.data
		if(self.gambScenarioFive.data is None):
			self.gambScenarioFive.data=self.gambScenario.data
		if(self.gambScenarioSix.data is None):
			self.gambScenarioSix.data=self.gambScenario.data
		if( self.gambScenarioSeven.data is None):
			self.gambScenarioSeven.data =self.gambScenario.data
		if(self.gambScenarioThree.data is None):
			self.gambScenarioThree.data= self.gambScenario.data
			
		if (self.timetScenarioFour.data is None):
			self.timetScenarioFour.data=self.timetScenario.data
		if(self.timetScenarioFive.data is None):
			self.timetScenarioFive.data=self.timetScenario.data
		if(self.timetScenarioSix.data is None):
			self.timetScenarioSix.data=self.timetScenario.data
		if( self.timetScenarioSeven.data is None):
			self.timetScenarioSeven.data =self.timetScenario.data
		if(self.timetScenarioThree.data is None):
			self.timetScenarioThree.data= self.timetScenario.data
			
		GamInfo = GamblerInfo(gambleid=GambleLoader.gambleid, titleid=self.gamblertitle.data, otitleid=self.ogamblertitle.data,mechgamb = setup, conditionOne=self.conditionOnetext.data,conditionTwo=self.conditionTwotext.data, conditionThree=self.conditionThreetext.data,conditionFour=self.conditionFourtext.data, conditionFive=self.conditionFivetext.data,conditionOneInfo=self.conditionOneInfo.data,
		conditionTwoInfo=self.conditionTwoInfo.data,conditionThreeInfo=self.conditionThreeInfo.data,conditionFourInfo=self.conditionFourInfo.data,conditionFiveInfo=self.conditionFiveInfo.data,
		initgambThresh=self.initgambThresh.data,posgambThresh=self.posgambThresh.data,maxgambThresh=self.maxgambThresh.data,mingambThresh=self.mingambThresh.data,gambScenario=self.gambScenario.data, gambChoosing= self.gambChoosing.data,gambBenefits=self.gambBenefits.data,gambWelcome=self.gambWelcome.data,gambSideeffects=self.gambSideeffects.data,
		gambAgreementA=self.gambAgreementA.data,gambAgreementE=self.gambAgreementE.data, gambAgreementB=self.gambAgreementB.data,inittimeThresh=self.inittimetThresh.data,postimetThresh=self.postimetThresh.data,maxtimetThresh=self.maxtimetThresh.data,mintimetThresh=self.mintimetThresh.data,timetScenario=self.timetScenario.data,timetChoosing=self.timetChoosing.data,
		timetBenefits=self.timetBenefits.data,timetWelcome=self.timetWelcome.data,timetSideeffects=self.timetSideeffects.data,timetAgreementA=self.timetAgreementA.data,timetAgreementE=self.timetAgreementE.data,timetAgreementB=self.timetAgreementB.data,
		conditionSix = self.conditionSixtext.data, conditionSeven=self.conditionSeventext.data, conditionEight=self.conditionEighttext.data, conditionSixInfo=self.conditionSixInfo.data, conditionSevenInfo=self.conditionSevenInfo.data, conditionEightInfo=self.conditionEightInfo.data, conditionOneAC=str(self.conditionOneAC.data).replace(" ", ""),
		conditionTwoAC=str(self.conditionTwoAC.data).replace(" ", ""),conditionThreeAC=str(self.conditionThreeAC.data).replace(" ", ""),conditionFourAC=str(self.conditionFourAC.data).replace(" ", ""),conditionFiveAC=str(self.conditionFiveAC.data).replace(" ", ""),conditionSixAC=str(self.conditionSixAC.data).replace(" ", ""),conditionSevenAC=str(self.conditionSevenAC.data).replace(" ", ""),conditionEightAC=str(self.conditionEightAC.data).replace(" ", ""),
		gambScenarioThree = self.gambScenarioThree.data,gambScenarioFour = self.gambScenarioFour.data,gambScenarioFive = self.gambScenarioFive.data,gambScenarioSix = self.gambScenarioSix.data,
		gambScenarioSeven = self.gambScenarioSeven.data,timetScenarioThree = self.timetScenarioThree.data,timetScenarioFour = self.timetScenarioFour.data,timetScenarioFive = self.timetScenarioFive.data,timetScenarioSix = self.timetScenarioSix.data,timetScenarioSeven = self.timetScenarioSeven.data,
		language=self.selectLanguage.data, SonFHR=self.selectSonFHR.data,genranduid=self.selectGenranduid.data,disablepatname=self.selectDisablepatname.data,disablepatage=self.selectDisablepatage.data,disablepatgender=self.selectDisablepatgender.data,disablepatrace=self.selectDisablepatrace.data, localStorage= self.selectlocalStorage.data)
		GamInfo.save()
		db.close()
		return 0
		
	def populate_obj(self,obj):
		"""Populates object for editing.

		:param obj: Object containing projet information
		:type: Object/GamblerSetup data
		:return: 0 (int)
		:error: -1 (if project exists)
		"""
		self.gamblertitle.data = obj.titleid
		self.gamblertitle.render_kw={'readonly': True}
		self.ogamblertitle.data = obj.otitleid
		self.conditionOnetext.data = obj.conditionOne
		self.conditionTwotext.data = obj.conditionTwo
		self.conditionThreetext.data = obj.conditionThree
		self.conditionFourtext.data = obj.conditionFour
		self.conditionFivetext.data = obj.conditionFive
		self.conditionSixtext.data = obj.conditionSix
		self.conditionSeventext.data = obj.conditionSeven
		self.conditionEighttext.data = obj.conditionEight
		self.conditionOneAC.data = obj.conditionOneAC
		self.conditionTwoAC.data = obj.conditionTwoAC
		self.conditionThreeAC.data = obj.conditionThreeAC
		self.conditionFourAC.data = obj.conditionFourAC
		self.conditionFiveAC.data = obj.conditionFiveAC
		self.conditionSixAC.data = obj.conditionSixAC
		self.conditionSevenAC.data = obj.conditionSevenAC
		self.conditionEightAC.data = obj.conditionEightAC
		self.conditionOneInfo.data = obj.conditionOneInfo
		self.conditionTwoInfo.data = obj.conditionTwoInfo
		self.conditionThreeInfo.data = obj.conditionThreeInfo
		self.conditionFourInfo.data = obj.conditionFourInfo
		self.conditionFiveInfo.data = obj.conditionFiveInfo
		self.conditionSixInfo.data = obj.conditionSixInfo
		self.conditionSevenInfo.data = obj.conditionSevenInfo
		self.conditionEightInfo.data = obj.conditionEightInfo
		self.initgambThresh.data = obj.initgambThresh
		self.posgambThresh.data = obj.posgambThresh
		self.maxgambThresh.data = obj.maxgambThresh
		self.mingambThresh.data = obj.mingambThresh
		self.gambScenario.data = obj.gambScenario
		self.gambChoosing.data = obj.gambChoosing
		self.gambBenefits.data = obj.gambBenefits
		self.gambWelcome.data = obj.gambWelcome
		self.gambSideeffects.data = obj.gambSideeffects
		self.gambAgreementA.data = obj.gambAgreementA
		self.gambAgreementE.data = obj.gambAgreementE
		self.gambAgreementB.data  = obj.gambAgreementB
		self.gambScenarioThree.data = obj.gambScenarioThree 
		self.gambScenarioFour.data = obj.gambScenarioFour
		self.gambScenarioFive.data = obj.gambScenarioFive
		self.gambScenarioSix.data = obj.gambScenarioSix
		self.gambScenarioSeven.data = obj.gambScenarioSeven
		self.inittimetThresh.data = obj.inittimeThresh
		self.postimetThresh.data = obj.postimetThresh
		self.maxtimetThresh.data = obj.maxtimetThresh
		self.mintimetThresh.data = obj.mintimetThresh
		self.timetScenario.data = obj.timetScenario
		self.timetChoosing.data = obj.timetChoosing
		self.timetBenefits.data = obj.timetBenefits
		self.timetWelcome.data = obj.timetWelcome
		self.timetSideeffects.data = obj.timetSideeffects
		self.timetAgreementA.data = obj.timetAgreementA
		self.timetAgreementE.data = obj.timetAgreementE
		self.timetAgreementB.data  = obj.timetAgreementB
		self.timetScenarioThree.data = obj.timetScenarioThree
		self.timetScenarioFour.data = obj.timetScenarioFour
		self.timetScenarioFive.data = obj.timetScenarioFive
		self.timetScenarioSix.data = obj.timetScenarioSix
		self.timetScenarioSeven.data = obj.timetScenarioSeven
		self.selectLanguage.data=obj.language
		self.selectSonFHR.data=obj.SonFHR
		self.selectGenranduid.data=obj.genranduid
		self.selectDisablepatname.data=obj.disablepatname
		self.selectDisablepatage.data=obj.disablepatage
		self.selectDisablepatrace.data=obj.disablepatrace
		self.selectDisablepatgender.data=obj.disablepatgender
		self.selectlocalStorage.data=obj.localStorage
		mg = obj.mechgamb
		mg1 = [tx for tx in mg]
		if mg1[0] == "0":
			self.selectOrdinal.process_data(False)
		if mg1[1] == "0":
			self.selectScale.process_data(False)
		if mg1[2]  == "0":
			self.selectGamble.process_data(False)
		if mg1[3] == "0":
			self.selectTime.process_data(False)	
		if int(mg1[4]) >= 1:
			self.selectVideo.process_data(True)	
		for i in mg1:
			if int(i) >0:
				self.selectAmount.process_data(i)
				break
		super(GamblerSetup, self).populate_obj(obj)
	def delete(self,gid):
		"""
		Delete information from the Gambler
		
		:param gid: The titleid (foldername) of the Gambler project
		:type gid: str		
		:return: Self loaded data from database
		"""
		rstatus = 0
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		GambleLoader = GamblerInfo()
		try:
			int(gid)
			GambleLoader = GambleLoader.select().where(GamblerInfo.gambleid == gid)
			if GambleLoader.exists():
				GambleLoader = GamblerInfo()
				GambleLoader = GambleLoader.get(GamblerInfo.gambleid == gid)
				rstatus =  GambleLoader.titleid
				GambleLoader.delete_instance()
			else:
				rstatus = 1
		except ValueError:
			GambleLoader = GambleLoader.select().where(GamblerInfo.titleid == gid)
			if GambleLoader.exists():
				GambleLoader = GamblerInfo()
				GambleLoader = GambleLoader.get(GamblerInfo.titleid == gid)
				rstatus =GambleLoader.titleid
				GambleLoader.delete_instance()
			else:
				rstatus = 1
		db.close()
		return rstatus

class LanguageTranslation(FlaskForm):
	"""Demographics page class """
###Putting d in front of varibales for clarification for python
	dlanguage = wtforms.StringField("Language Code", [validators.length(max=5)])
	dlanguage_name = wtforms.StringField("Language Name")
	dGreeting_Text 	 = wtforms.StringField("Hello")
	dContinue_Button 	 = wtforms.StringField("Continue")
	dShow_Less_Text	 = wtforms.StringField("Show less information ")
	dShow_More_Text	 = wtforms.StringField("Show more information ")
	dTitle_Title_Program 	 = wtforms.StringField("The Gambler ")
	dTitle_Project_Name 	 = wtforms.StringField("Leave Blank")
	dTitle_Status_Text	 = wtforms.StringField("'Welcome, press start to begin.' ")
	dTitle_Start_Button 	 = wtforms.StringField("Start")
	dSInfo_Icon_Text 	 = wtforms.StringField("Icon")
	dSInfo_HS_Text 	 = wtforms.StringField("Health State")
	dSInfo_HSA_Text 	 = wtforms.StringField("Health State Abbreviations ")
	dSInfo_Status_Info	 = wtforms.StringField("'Here are the following health states, their icons, their abbreviations, and their information.' ")
	dSInfo_Information_Text 	 = wtforms.StringField("Information")
	dSInfo_Instruction_Text 	 = wtforms.StringField("Double click on a health state icon to see a video clip description of the health state. ")
	dOR_Instruction_Text	 = wtforms.StringField("Each of the images that represents health states are drag and droppable.Please drag each image into the empty box ordering them from best to worst state (top to bottom) ")
	dOR_Video_Instruction_Text 	 = wtforms.StringField("Video Instructions")
	dOR_Incorrect_Function_Text 	 = wtforms.StringField("'Sorry, you may have forgotten to order the states.<br/>Please drag each image into the empty box ordering them from best to worst state (top to bottom).' ")
	dVAS_Instruction_Text	 = wtforms.StringField("Click and drag the icon on the sliders to show your values for each health state. ")
	dVAS_Alert_Selection_Text 	 = wtforms.StringField("'Sorry, you may have forgotten to click and drag the sliders.<br/>Click and drag the icon on the sliders to show your values for each health state.' ")
	dVAS_Video_Instruction_Text 	 = wtforms.StringField("Video Instructions ")
	dSG_Video_Instruction_Text 	 = wtforms.StringField("Performing General Standard Gamble Video Instructions ")
	dSG_HS_Video_Instruction_Text	 = wtforms.StringField("Performing Standard Gamble for {{MainCondition}} Video Instructions ")
	dTTO_Video_Instruction_Text 	 = wtforms.StringField("Performing General Time Trade off Video Instructions ")
	dTTO_HS_Video_Instruction_Text	 = wtforms.StringField("Performing Time Trade off for {{MainCondition}} Video Instructions ")
	dEnd_HS_Text	 = wtforms.StringField("Health State ")
	dEnd_OR_Text 	 = wtforms.StringField("Ordinal Scale ")
	dEnd_VAS_Text	 = wtforms.StringField("Visual Analog Scale ")
	dEnd_SG_Text 	 = wtforms.StringField("Standard Gamble ")
	dEnd_TTO_Text 	 = wtforms.StringField("Time Trade off ")
	dEnd_CSV_Export_Button 	 = wtforms.StringField("CSV Export")
	dEnd_Finish_Button 	 = wtforms.StringField("Finish")
	dEnd_Greeting_Text 	 = wtforms.StringField("Thank you for completing the assessement {{FirstName}}.Here are the results:")
	dDemo_userid_text 	 = wtforms.StringField("User ID")
	dDemo_firstname_text 	 = wtforms.StringField("First name")
	dDemo_lastname_text 	 = wtforms.StringField("Last name")
	dDemo_age_text 	 = wtforms.StringField("Age ")
	dDemo_hld_text 	 = wtforms.StringField("Hispanic/Latino ")
	dDemo_gender_text 	 = wtforms.StringField("Gender ")
	dDemo_race_text 	 = wtforms.StringField("Race ")
	dDemo_videoinstructions_text 	 = wtforms.StringField("Click here to turn off video instructions ")
	dDemo_firstname_warn_text	 = wtforms.StringField("Please enter your first name. ")
	dDemo_lastname_warn_text	 = wtforms.StringField("Please enter your last name. ")
	dDemo_age_warn_text 	 = wtforms.StringField("Please enter your age. ")
	dDemo_Information_Text	 = wtforms.StringField("Please enter your information.")
	dSG_Shake_Button 	 = wtforms.StringField("Shake")
	dSG_Pill_Text 	 = wtforms.StringField("Pill(s)")
	dTTO_Month_Text 	 = wtforms.StringField("Month(s)")
	dTTO_Year_Text 	 = wtforms.StringField("Years")
	ddemographics_gender = wtforms.StringField("Gender in JSON format, eg ({'O': 'Non-binary/Other'} )")
	ddemographics_gender_default = wtforms.StringField("Type in the 1 letter gender code (eg. O for other)", [validators.length(max=1)])
	ddemographics_race= wtforms.StringField("Race in JSON format, eg ({'blk': 'Africana/Afroamericana'} )")
	ddemographics_race_default = wtforms.StringField("Type in the 3 letter race code (eg. blk)", [validators.length(max=3)])
	
	def save(self,resave):
		"""Save data about Langauge.
		
		:param resave: Indication of saving or resaving content  0 = Original 1 = Resaving
		:type: int
		"""
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		LangTranslator = LangUserSystemTranslate()
		if resave == 0: 
			LangTranslator = LangUserSystemTranslate(language = self.dlanguage.data, Greeting_Text  = self.dGreeting_Text.data,Continue_Button  = self.dContinue_Button.data,Show_Less_Text = self.dShow_Less_Text.data,Show_More_Text = self.dShow_More_Text.data,Title_Title_Program  = self.dTitle_Title_Program.data,Title_Project_Name  = self.dTitle_Project_Name.data,Title_Status_Text = self.dTitle_Status_Text.data,Title_Start_Button  = self.dTitle_Start_Button.data,SInfo_Icon_Text  = self.dSInfo_Icon_Text.data,SInfo_HS_Text  = self.dSInfo_HS_Text.data,SInfo_HSA_Text  = self.dSInfo_HSA_Text.data,SInfo_Status_Info = self.dSInfo_Status_Info.data,SInfo_Information_Text  = self.dSInfo_Information_Text.data,
				SInfo_Instruction_Text  = self.dSInfo_Instruction_Text.data,OR_Instruction_Text = self.dOR_Instruction_Text.data,OR_Video_Instruction_Text  = self.dOR_Video_Instruction_Text.data,OR_Incorrect_Function_Text  = self.dOR_Incorrect_Function_Text.data,VAS_Instruction_Text = self.dVAS_Instruction_Text.data,VAS_Alert_Selection_Text  = self.dVAS_Alert_Selection_Text.data,VAS_Video_Instruction_Text  = self.dVAS_Video_Instruction_Text.data,SG_Video_Instruction_Text  = self.dSG_Video_Instruction_Text.data,SG_HS_Video_Instruction_Text = self.dSG_HS_Video_Instruction_Text.data,TTO_Video_Instruction_Text  = self.dTTO_Video_Instruction_Text.data,
				TTO_HS_Video_Instruction_Text = self.dTTO_HS_Video_Instruction_Text.data,End_HS_Text = self.dEnd_HS_Text.data,End_OR_Text  = self.dEnd_OR_Text.data,End_VAS_Text = self.dEnd_VAS_Text.data,End_SG_Text  = self.dEnd_SG_Text.data,End_TTO_Text  = self.dEnd_TTO_Text.data,End_CSV_Export_Button  = self.dEnd_CSV_Export_Button.data,
				End_Finish_Button  = self.dEnd_Finish_Button.data,End_Greeting_Text  = self.dEnd_Greeting_Text.data,Demo_userid_text  = self.dDemo_userid_text.data,Demo_firstname_text  = self.dDemo_firstname_text.data,Demo_lastname_text  = self.dDemo_lastname_text.data,Demo_age_text  = self.dDemo_age_text.data,Demo_hld_text  = self.dDemo_hld_text.data,Demo_gender_text  = self.dDemo_gender_text.data,Demo_race_text  = self.dDemo_race_text.data,Demo_videoinstructions_text  = self.dDemo_videoinstructions_text.data,Demo_firstname_warn_text = self.dDemo_firstname_warn_text.data,Demo_lastname_warn_text = self.dDemo_lastname_warn_text.data,Demo_age_warn_text  = self.dDemo_age_warn_text.data,
				Demo_Information_Text = self.dDemo_Information_Text.data,SG_Shake_Button  = self.dSG_Shake_Button.data,SG_Pill_Text  = self.dSG_Pill_Text.data,TTO_Month_Text  = self.dTTO_Month_Text.data,TTO_Year_Text  = self.dTTO_Year_Text.data)
			LangTranslator.save()
			LangDemoTranslator = LangUserGenderRaceSystemTranslate(demographics_language = self.dlanguage.data,  demographics_gender = self.ddemographics_gender.data,demographics_gender_default = self.ddemographics_gender_default.data, demographics_race = self.ddemographics_race.data,demographics_race_default = self.ddemographics_race_default.data)
			LangDemoTranslator.save()
			LangCodeSave = LangCode( language  = self.dlanguage.data,language_name = self.dlanguage_name.data )
			LangCodeSave.save()
			db.close()
		else:
			LangTranslator = LangUserSystemTranslate.update(Greeting_Text  = self.dGreeting_Text.data,Continue_Button  = self.dContinue_Button.data,Show_Less_Text = self.dShow_Less_Text.data,Show_More_Text = self.dShow_More_Text.data,Title_Title_Program  = self.dTitle_Title_Program.data,Title_Project_Name  = self.dTitle_Project_Name.data,Title_Status_Text = self.dTitle_Status_Text.data,Title_Start_Button  = self.dTitle_Start_Button.data,SInfo_Icon_Text  = self.dSInfo_Icon_Text.data,SInfo_HS_Text  = self.dSInfo_HS_Text.data,SInfo_HSA_Text  = self.dSInfo_HSA_Text.data,SInfo_Status_Info = self.dSInfo_Status_Info.data,SInfo_Information_Text  = self.dSInfo_Information_Text.data,
				SInfo_Instruction_Text  = self.dSInfo_Instruction_Text.data,OR_Instruction_Text = self.dOR_Instruction_Text.data,OR_Video_Instruction_Text  = self.dOR_Video_Instruction_Text.data,OR_Incorrect_Function_Text  = self.dOR_Incorrect_Function_Text.data,VAS_Instruction_Text = self.dVAS_Instruction_Text.data,VAS_Alert_Selection_Text  = self.dVAS_Alert_Selection_Text.data,VAS_Video_Instruction_Text  = self.dVAS_Video_Instruction_Text.data,SG_Video_Instruction_Text  = self.dSG_Video_Instruction_Text.data,SG_HS_Video_Instruction_Text = self.dSG_HS_Video_Instruction_Text.data,TTO_Video_Instruction_Text  = self.dTTO_Video_Instruction_Text.data,
				TTO_HS_Video_Instruction_Text = self.dTTO_HS_Video_Instruction_Text.data,End_HS_Text = self.dEnd_HS_Text.data,End_OR_Text  = self.dEnd_OR_Text.data,End_VAS_Text = self.dEnd_VAS_Text.data,End_SG_Text  = self.dEnd_SG_Text.data,End_TTO_Text  = self.dEnd_TTO_Text.data,End_CSV_Export_Button  = self.dEnd_CSV_Export_Button.data,
				End_Finish_Button  = self.dEnd_Finish_Button.data,End_Greeting_Text  = self.dEnd_Greeting_Text.data,Demo_userid_text  = self.dDemo_userid_text.data,Demo_firstname_text  = self.dDemo_firstname_text.data,Demo_lastname_text  = self.dDemo_lastname_text.data,Demo_age_text  = self.dDemo_age_text.data,Demo_hld_text  = self.dDemo_hld_text.data,Demo_gender_text  = self.dDemo_gender_text.data,Demo_race_text  = self.dDemo_race_text.data,Demo_videoinstructions_text  = self.dDemo_videoinstructions_text.data,Demo_firstname_warn_text = self.dDemo_firstname_warn_text.data,Demo_lastname_warn_text = self.dDemo_lastname_warn_text.data,Demo_age_warn_text  = self.dDemo_age_warn_text.data,
				Demo_Information_Text = self.dDemo_Information_Text.data,SG_Shake_Button  = self.dSG_Shake_Button.data,SG_Pill_Text  = self.dSG_Pill_Text.data,TTO_Month_Text  = self.dTTO_Month_Text.data,TTO_Year_Text  = self.dTTO_Year_Text.data, language = self.dlanguage.data).where(LangUserSystemTranslate.language == self.dlanguage.data)
			LangTranslator.execute()
			LangDemoTranslator = LangUserGenderRaceSystemTranslate.update(demographics_language = self.dlanguage.data, demographics_gender = self.ddemographics_gender.data,demographics_gender_default = self.ddemographics_gender_default.data, demographics_race = self.ddemographics_race.data,demographics_race_default = self.ddemographics_race_default.data).where(LangUserGenderRaceSystemTranslate.demographics_language == self.dlanguage.data)
			LangDemoTranslator.execute()
			LangCodeSave = LangCode.update( language  = self.dlanguage.data,language_name = self.dlanguage_name.data ).where(LangCode.language  == self.dlanguage.data)
			LangCodeSave.execute()
			db.close()
		

	def populate_obj(self,obj):
		"""Load data about Langauge.
		
		:param obj: Object
		:type: Peewee executed query object 
		"""
		#These are specially accessed.  Peewee does the joins, but pushes them in a descending tree from 0 to nth table joined
		self.dlanguage.data = obj.language
		self.dlanguage_name.data = obj.langusergenderracesystemtranslate.langcode.language_name 
		self.ddemographics_gender.data = obj.langusergenderracesystemtranslate.demographics_gender
		self.ddemographics_gender_default.data = obj.langusergenderracesystemtranslate.demographics_gender_default
		self.ddemographics_race.data = obj.langusergenderracesystemtranslate.demographics_race
		self.ddemographics_race_default.data = obj.langusergenderracesystemtranslate.demographics_race_default
		##Next ones are normal access
		self.dGreeting_Text.data = 	obj.Greeting_Text
		self.dContinue_Button.data = 	obj.Continue_Button
		self.dShow_Less_Text.data = 	obj.Show_Less_Text
		self.dShow_More_Text.data = 	obj.Show_More_Text
		self.dTitle_Title_Program.data = 	obj.Title_Title_Program
		self.dTitle_Project_Name.data = 	obj.Title_Project_Name
		self.dTitle_Status_Text.data = 	obj.Title_Status_Text
		self.dTitle_Start_Button.data = 	obj.Title_Start_Button
		self.dSInfo_Icon_Text.data = 	obj.SInfo_Icon_Text
		self.dSInfo_HS_Text.data = 	obj.SInfo_HS_Text
		self.dSInfo_HSA_Text.data = 	obj.SInfo_HSA_Text
		self.dSInfo_Status_Info.data = 	obj.SInfo_Status_Info
		self.dSInfo_Information_Text.data = 	obj.SInfo_Information_Text
		self.dSInfo_Instruction_Text.data = 	obj.SInfo_Instruction_Text
		self.dOR_Instruction_Text.data = 	obj.OR_Instruction_Text
		self.dOR_Video_Instruction_Text.data = 	obj.OR_Video_Instruction_Text
		self.dOR_Incorrect_Function_Text.data = 	obj.OR_Incorrect_Function_Text
		self.dVAS_Instruction_Text.data = 	obj.VAS_Instruction_Text
		self.dVAS_Alert_Selection_Text.data = 	obj.VAS_Alert_Selection_Text
		self.dVAS_Video_Instruction_Text.data = 	obj.VAS_Video_Instruction_Text
		self.dSG_Video_Instruction_Text.data = 	obj.SG_Video_Instruction_Text
		self.dSG_HS_Video_Instruction_Text.data = 	obj.SG_HS_Video_Instruction_Text
		self.dTTO_Video_Instruction_Text.data = 	obj.TTO_Video_Instruction_Text
		self.dTTO_HS_Video_Instruction_Text.data = 	obj.TTO_HS_Video_Instruction_Text
		self.dEnd_HS_Text.data = 	obj.End_HS_Text
		self.dEnd_OR_Text.data = 	obj.End_OR_Text
		self.dEnd_VAS_Text.data = 	obj.End_VAS_Text
		self.dEnd_SG_Text.data = 	obj.End_SG_Text
		self.dEnd_TTO_Text.data = 	obj.End_TTO_Text
		self.dEnd_CSV_Export_Button.data = 	obj.End_CSV_Export_Button
		self.dEnd_Finish_Button.data = 	obj.End_Finish_Button
		self.dlanguage.data = 	obj.language
		self.dEnd_Greeting_Text.data = 	obj.End_Greeting_Text
		self.dDemo_userid_text.data = 	obj.Demo_userid_text
		self.dDemo_firstname_text.data = 	obj.Demo_firstname_text
		self.dDemo_lastname_text.data = 	obj.Demo_lastname_text
		self.dDemo_age_text.data = 	obj.Demo_age_text
		self.dDemo_hld_text.data = 	obj.Demo_hld_text
		self.dDemo_gender_text.data = 	obj.Demo_gender_text
		self.dDemo_race_text.data = 	obj.Demo_race_text
		self.dDemo_videoinstructions_text.data = 	obj.Demo_videoinstructions_text
		self.dDemo_firstname_warn_text.data = 	obj.Demo_firstname_warn_text
		self.dDemo_lastname_warn_text.data = 	obj.Demo_lastname_warn_text
		self.dDemo_age_warn_text.data = 	obj.Demo_age_warn_text
		self.dDemo_Information_Text.data = 	obj.Demo_Information_Text
		self.dSG_Shake_Button.data = 	obj.SG_Shake_Button
		self.dSG_Pill_Text.data = 	obj.SG_Pill_Text
		self.dTTO_Month_Text.data = 	obj.TTO_Month_Text
		self.dTTO_Year_Text.data = 	obj.TTO_Year_Text
		super(LanguageTranslation, self).populate_obj(obj)
