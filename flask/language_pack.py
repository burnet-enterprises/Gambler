#!/usr/bin/env python3
import peewee
from peewee import *
from BaseModel import ModelBase,db

#Must modify this information before production
#Password must me modified.  

class LangCode(ModelBase):
	""" 
	Retrieves the language and language id from the database
	"""
	language_id = AutoField()
	language = CharField()
	language_name = CharField()

	class Meta:
			database =db
			#table_name is table for the data.
			table_name = 'LangCode'

class LangUserSystemTranslate(ModelBase):
	""" 
	Retrieves the language translation of the Gambler
	"""
	language_id = AutoField()
	language = CharField()
	Greeting_Text  = TextField()
	Continue_Button = TextField()
	Show_Less_Text = TextField()
	Show_More_Text  = TextField()
	Title_Title_Program = TextField()
	Title_Project_Name = TextField()
	Title_Status_Text = TextField()
	Title_Start_Button = TextField()
	SInfo_Icon_Text = TextField()
	SInfo_HS_Text = TextField()
	SInfo_HSA_Text = TextField()
	SInfo_Status_Info = TextField()
	SInfo_Information_Text = TextField()
	SInfo_Instruction_Text = TextField()
	OR_Instruction_Text = TextField()
	OR_Video_Instruction_Text = TextField()
	OR_Incorrect_Function_Text = TextField()
	VAS_Instruction_Text = TextField()
	VAS_Alert_Selection_Text = TextField()
	VAS_Video_Instruction_Text = TextField()
	SG_Video_Instruction_Text = TextField()
	SG_HS_Video_Instruction_Text = TextField()
	SG_Shake_Button = TextField()
	TTO_Video_Instruction_Text = TextField()
	TTO_HS_Video_Instruction_Text = TextField()
	End_Greeting_Text = TextField()
	End_HS_Text = TextField()
	End_OR_Text = TextField()
	End_VAS_Text = TextField()
	End_SG_Text = TextField()
	End_TTO_Text = TextField()
	End_CSV_Export_Button = TextField()
	End_Finish_Button = TextField()
	Demo_userid_text  = TextField()
	Demo_firstname_text  = TextField()
	Demo_lastname_text  = TextField()
	Demo_age_text  = TextField()
	Demo_hld_text  = TextField()
	Demo_gender_text  = TextField()
	Demo_race_text  = TextField()
	Demo_videoinstructions_text  = TextField()
	Demo_firstname_warn_text  = TextField()
	Demo_lastname_warn_text  = TextField()
	Demo_age_warn_text  = TextField()
	Demo_Information_Text = TextField()
	SG_Pill_Text =  TextField()
	TTO_Month_Text = TextField()
	TTO_Year_Text = TextField()
	class Meta:
			database =db
			#table_name is table for the data.
			table_name = 'LangUserSystemTranslate'

class LangUserGenderRaceSystemTranslate(ModelBase):
	""" 
	Retrieves the language translation of demographic information
	"""
	language_id = AutoField()
	demographics_language= CharField()
	demographics_country  = CharField()
	demographics_gender = TextField()
	demographics_gender_default = CharField()
	demographics_race = TextField()
	demographics_race_default = CharField()
	class Meta:
			database =db
			#table_name is table for the data.
			table_name = 'LangUserGenderRaceSystemTranslate'
