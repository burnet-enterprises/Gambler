#!/usr/local/bin/ python3

#################################################################################
#																				#
#																				#
#																				#
#																				#
#				General Data Protection Regulation (GDPR) Functions				#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################


#Libraries 
import json, errno
from flask import *
import csv
try:
	from StringIO import StringIO #Python2->3
except ImportError:
	from io import StringIO
from werkzeug.utils import secure_filename
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
##Packages defined by AJ Adejare
from UserInfo import *
from BaseModel import db
from ReverseProxy import *
from ConditionInfo import *
from language_pack import *
from logic_gambler import *
from demographics import *
from logic_timetradeoff import *
from GamblerSetup import *
from ConditionInfo import * 
from UserData import *
from VideoSetup import *
from ReverseProxy import *
mainud = UserData()
gthold1 = 0

gdpr = Blueprint('gdpr', 'gdpr', url_prefix='/gdpr',static_folder='static')
"""See mainapp.py for function comments as they parallel GDPR."""
#All flask applicaiton relative to directory: https://stackoverflow.com/questions/21303198/relative-paths-in-flask
#Index route
@gdpr.route('/', methods = ['GET', 'POST'])
@gdpr.route('', methods = ['GET', 'POST'])
def gdprindexgdpr():
	GamEditor = SelectGambler()
	gdpr = True
	if (db.is_closed()==False):
		db.close()
	db.connect()
	GambleLoader = GamblerInfo()
	GamblerList = GambleLoader.select(GamblerInfo.titleid, GamblerInfo.otitleid, GamblerInfo.language)
	choice = [(c.titleid, c.otitleid) for c in GamblerList if c.language != "en-US"]
	GamEditor.gamblertitle.choices = choice
	if request.method == 'POST':
		if GamEditor.gamblertitle.data == None and GamEditor.gamblerid.data == None:
			flash('You must fill in at least one field are required, or press the New Gambler Project Button to start a new project')
			return render_template('index.html', form = GamEditor)
		else:
			if GamEditor.gamblertitle.data == None:
				return redirect("gdpr/" + str(GamEditor.gamblerid.data) + "/")
			else:
				return redirect("gdpr/" + str(GamEditor.gamblertitle.data) + "/")
	else:
		return render_template('index.html', form = GamEditor,gdpr = gdpr)

#@babel.localeselector
#def gdprget_locale():
#	return 'en'
@gdpr.route('/language/', methods = ['GET', 'POST'])
@gdpr.route('/language', methods = ['GET', 'POST'])
def gdprlanguageselect():
	if (db.is_closed()==False):
		db.close()
	db.connect()
	GamEditor = SelectLanguage()
	GamEditor.languageselect.choices = [(c.language, c.language_name) for c in LangCode.select(LangCode.language, LangCode.language_name)]
	db.close()
	if request.method == "POST":
		session['language'] = GamEditor.languageselect.data
		if request.form['docreferal'] != "outside":
			chkdf = request.form['docreferal'].split("/")
			chkdf.pop(0)
			if gdpr.config["APPLICATION_ROOT"] == ("/" + chkdf[0]):
				chkdf.pop(0)
			return redirect("gdpr/" + "/".join(chkdf))
				
		else:
                        return redirect("gdpr/" + "")
	return render_template('language.html', form = GamEditor)
		

#################################################################################
#																				#
#																				#
#																				#
#																				#
#								Documentation									#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################

#################################################################################
@gdpr.route('/docs/<path:filename>',methods = ['GET', 'POST'])
@gdpr.route('/docs',methods = ['GET', 'POST'])
@gdpr.route('/docs/',methods = ['GET', 'POST'])
#@gdpr.route('/docs/<path:filename>',methods = ['GET', 'POST'])
def gdprdocumentation(filename="index.html"):
    return send_from_directory('/home/ubuntu/Flask/docs/build/html',filename)

@gdpr.route('/about/<path:filename>',methods = ['GET', 'POST'])
@gdpr.route('/about',methods = ['GET', 'POST'])
@gdpr.route('/about/',methods = ['GET', 'POST'])
def gdpraboutpage(filename="about.html"):
    return render_template(filename)

@gdpr.route('/contact/<path:filename>',methods = ['GET', 'POST'])
@gdpr.route('/contact',methods = ['GET', 'POST'])
@gdpr.route('/contact/',methods = ['GET', 'POST'])
def gdprcontactpage(filename="contact.html"):
    return render_template(filename)

#################################################################################
#																				#
#																				#
#																				#
#																				#
#					Introduction and User Setup									#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################

#################################################################################
#Introduction Page
@gdpr.route('/<titleid>/', methods=['GET','POST'])
@gdpr.route('/<titleid>/intro', methods=['GET','POST'])
def gdprintroduction(titleid):
	maincond = ConditionInfo()
	Title_Program = "The Gambler"
	Project_Name = ""
	Status_Text = "Welcome, press start to begin."
	Start_Button = "Start"
	##Get the mechanics for how many statuses are in the Gambler
	if maincond.getls(titleid) == True:
		session['local'] = True
	if 'language' not in session:
		session['language'] = maincond.getlang(titleid)
	else:
		if  session['language'] != maincond.getlang(titleid):
			session['language'] = maincond.getlang(titleid)
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystem = LangUserSystemTranslate()
		UserSysData = LangUserSystemTranslate.get(LangUserSystemTranslate.language == session['language'])
		db.close()
		Title_Program = UserSysData.Title_Title_Program
		Status_Text = UserSysData.Title_Status_Text
		Start_Button = UserSysData.Title_Start_Button
		
	try:	
		session['mechgamb'] = maincond.getmech(titleid)
	except Exception as e:
		return render_template('error.html', Error_Info = "This Gambler project does not exist.  Please check to see if the Gambler project exists.",Error_Statement = e)
	if request.method == 'GET':
		Project_Name = maincond.getprojecttitle(titleid)
		if (Title_Program is None or Title_Program == ""):
			Project_Name = "Gambler"
		return render_template('intro.html',Project_Name = Project_Name, Title_Program = Title_Program , Status_Text = Status_Text, Start_Button=Start_Button, slug=titleid)
	if request.method == 'POST':
		maincond = ConditionInfo()
		session['mechgamb'] = maincond.getmech(titleid)
		return redirect("gdpr/" + titleid + "/demographics")
#################################################################################
#Status conditions
@gdpr.route('/<titleid>/<username>/statusinfo', methods=['GET','POST'])
def gdprstatusinfo(titleid,username):
	Instruction_Text = "Double click on a health state icon to see a video clip description of the health state."
	Icon_Text = "Icon"
	HS_Text = "Health State"
	HSA_Text = "Health State Abbreviations"
	Status_Info = "Here are the following health states, their icons, their abbreviations, and their information."
	Information_Text = "Information"
	Instruction_Text = "Double click on a health state icon to see a video clip description of the health state."
	Next_Button = "Next"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Status_Info = LangLoad.SInfo_Status_Info
		Icon_Text = LangLoad.SInfo_Icon_Text
		HS_Text = LangLoad.SInfo_HS_Text
		HSA_Text = LangLoad.SInfo_HSA_Text
		Information_Text = LangLoad.SInfo_Information_Text
		Instruction_Text = LangLoad.SInfo_Instruction_Text
		Next_Button = LangLoad.Continue_Button
	maincond = ConditionInfo()
	maincond.load(titleid)
	w=0
	wt = 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	
	for q in session['mechgamb']:
		if int(q) > 0:
			w = int(q)
			break;
	if request.method == 'GET':
		Title_Program = maincond.getprojecttitle(titleid)
		if (Title_Program is None or Title_Program == ""):
			Title_Program = "Gambler"
		return render_template('status_info.html', Next_Button = Next_Button, Status_Info = Status_Info,Information_Text=Information_Text, Instruction_Text = Instruction_Text, Icon_Text = Icon_Text, HS_Text=HS_Text, HSA_Text= HSA_Text, Title_Program = Title_Program, video = wt, setup=w, VideoOne =  VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt),  VideoTwo =  VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt), VideoThree =  VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt), VideoFour=  VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt), VideoFive =  VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt), VideoSix =  VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt), VideoSeven =  VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt),  VideoEight =  VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt),First_ConditionAC = maincond.condOneAC,Second_ConditionAC = maincond.condTwoAC,Third_ConditionAC = maincond.condThreeAC,Fourth_ConditionAC = maincond.condFourAC,Fifth_ConditionAC = maincond.condFiveAC,Sixth_ConditionAC = maincond.condSixAC,Seventh_ConditionAC = maincond.condSevenAC,Eighth_ConditionAC = maincond.condEightAC,First_Condition = maincond.condOne, First_Condition_Info = maincond.condOneInfo, First_Condition_Image = maincond.condOneImage,Second_Condition = maincond.condTwo, Second_Condition_Info = maincond.condTwoInfo, Second_Condition_Image = maincond.condTwoImage,Third_Condition = maincond.condThree, Third_Condition_Info = maincond.condThreeInfo, Third_Condition_Image = maincond.condThreeImage,Fourth_Condition = maincond.condFour, Fourth_Condition_Info = maincond.condFourInfo, Fourth_Condition_Image = maincond.condFourImage,slug=titleid, Fifth_Condition = maincond.condFive, Fifth_Condition_Info = maincond.condFiveInfo, Fifth_Condition_Image = maincond.condFiveImage, Sixth_Condition = maincond.condSix, Sixth_Condition_Info = maincond.condSixInfo, Sixth_Condition_Image = maincond.condSixImage, Seventh_Condition = maincond.condSeven, Seventh_Condition_Info = maincond.condSevenInfo, Seventh_Condition_Image = maincond.condSevenImage, Eighth_Condition = maincond.condEight, Eighth_Condition_Info = maincond.condEightInfo, Eighth_Condition_Image = maincond.condEightImage) 
	if request.method == 'POST':
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="Health State Info", buttonPress = "Submit", totalTime = int(totaltime) )
		db.close()
		
		if (int(session['mechgamb'][0]) > 0):
			return redirect("gdpr/" + titleid + "/" +  username  + "/order")
		elif (int(session['mechgamb'][1]) > 0):
			return redirect("gdpr/" + titleid + "/" +  username  + "/intensity")
		elif (int(session['mechgamb'][2]) > 0):
			return redirect("gdpr/" + titleid + "/" +  username  + "/scenario/1")
		elif (int(session['mechgamb'][3]) > 0):
			return redirect("gdpr/" + titleid + "/" +  username  + '/timetrade/1')
		else:
			return redirect("gdpr/" + titleid + "/" +  username  + '/finish')
##############################################################
#User Demographic Data

#Production Code
@gdpr.route('/<titleid>/demographics', methods = ['GET', 'POST'])
def gdprdemoform(titleid):
##This is where WTFforms must work from as it wants to be right as you're implemnting it.
	maindemo = Demographics(request.form)
	session['name'] = "Temp"
	session['counter'] = 0
	session['flag'] = 0
	session['th'] = 0
	session['age'] = 70
	session['race'] = "blk"
	session['hld'] = 0
	session['gender'] = "O"	
	session['instructions'] = 0	
	session['userid'] = "Temp"	
	Information_Text = "Please enter your information."
	Continue_Button = "Continue"
	maincond = ConditionInfo()
	maincond.load(titleid)		
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	if session['language'] != "en-US":
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Title_Program = LangLoad.Title_Title_Program
		Continue_Button = LangLoad.Continue_Button
		Information_Text = LangLoad.Demo_Information_Text
		maindemo.langload(session['language'])
	#if statement for anonymous goes here
	demopref = maincond.getdemopref(titleid)
	if demopref['GenerateRandomUserID'] == True:
		import uuid
		maindemo.duserid.data = uuid.uuid4().hex
	if demopref['DisablePatientName'] == True:
		maindemo.dfirstname.data = "Unknown"
		maindemo.dlastname.data = "Unknown"
	if demopref['DisablePatientAge'] == True:
		maindemo.dage.data = 70
	if demopref['DisablePatientRace'] == True:
		maindemo.drace.data = 'blk'
	if demopref['DisablePatientGender'] == True:
		maindemo.dgender.data = 'O'
	if request.method == 'POST':
		g = maindemo.savedemo(titleid)
		if maindemo.validate() == False:
			flash('All fields are required.')
			return render_template('demographics.html', Title_Program = Title_Program, Information_Text=Information_Text, Continue_Button = Continue_Button,GRUID = demopref['GenerateRandomUserID'],DPN=demopref['DisablePatientName'],DPA=demopref['DisablePatientAge'],DPR=demopref['DisablePatientRace'],DPG=demopref['DisablePatientGender'],form = maindemo)
		if g == -1:
			maindemo.duserid.errors.append("Username taken for this project please enter another one")
			return render_template('demographics.html', Title_Program = Title_Program, Information_Text=Information_Text, Continue_Button = Continue_Button,GRUID = demopref['GenerateRandomUserID'],DPN=demopref['DisablePatientName'],DPA=demopref['DisablePatientAge'],DPR=demopref['DisablePatientRace'],DPG=demopref['DisablePatientGender'],form = maindemo)
		else:
		#NEEd to use and modify for data
		#https://stackoverflow.com/questions/39261260/flask-session-variable-not-persisting-between-requests 
			a = session['name']
			b= session['gender'] 
			e = session['age'] 
			f =session['race'] 
			x = session['hld']
			weerd = session['userid']
#Hack to get patient name everywhere
			session['name'] = maindemo.dfirstname.data
			session['lname'] = maindemo.dlastname.data
			session['age'] = maindemo.dage.data
			session['race'] = maindemo.drace.data
			session['gender'] = maindemo.dgender.data
			session['instructions'] = int(maindemo.dinstructions.data == True)
			session['userid'] = maindemo.duserid.data
			totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
			session.modified = True 
			if session['name'] == "Unknown" or session['lname'] == "Unknown":
				session['name'] = ""
				session['lname'] = ""
#This saves Demographic data to the database
#This locally saves Demographic Data
			mainud = UserData()
			mainud.demosave(maindemo.duserid.data,titleid, maindemo.dfirstname.data, maindemo.dlastname.data, maindemo.dage.data, int(maindemo.dhld.data == True), maindemo.dgender.data, maindemo.drace.data, g)
			if (db.is_closed()==False):
				db.close()
			db.connect()
			HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="Demographics", buttonPress = "Submit", totalTime = int(totaltime) )
			db.close()
			return redirect("gdpr/" + titleid + "/" + str(g) + "/statusinfo")
	elif request.method == 'GET':
		return render_template('demographics.html', Title_Program = Title_Program, Information_Text=Information_Text, Continue_Button = Continue_Button, GRUID = demopref['GenerateRandomUserID'],DPN=demopref['DisablePatientName'],DPA=demopref['DisablePatientAge'],DPR=demopref['DisablePatientRace'],DPG=demopref['DisablePatientGender'],form = maindemo)


#################################################################################
#																				#
#																				#
#																				#
#																				#
#					Order and Visual Analog Scale								#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################

#Production
@gdpr.route('/<titleid>/<username>/order', methods=['GET','POST'])
def gdprorderinfo(titleid, username):
	mainscen = GScenario()
	Greeting_Text = "Hello"
	patientname=""
	Continue_Button = "Continue"
	Instruction_Text = "Each of the images that represents health states are drag and droppable.  Please drag each image into the empty box ordering them from best to worst state (top to bottom)."
	Video_Instruction_Text = "Video Instructions"
	Incorrect_Function_Text = "Sorry, you may have forgotten to order the states.<br/>Please drag each image into the empty box ordering them from best to worst state (top to bottom)."
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Continue_Button = LangLoad.Continue_Button
		Instruction_Text = LangLoad.OR_Instruction_Text
		Video_Instruction_Text = LangLoad.OR_Video_Instruction_Text
		Incorrect_Function_Text = LangLoad.OR_Incorrect_Function_Text
	maincond = ConditionInfo()
	mainscen.load(titleid)
	maincond.load(titleid)
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	y = 0
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if request.method =='GET':
		return render_template('order_info.html', Greeting_Text=Greeting_Text, Continue_Button=Continue_Button,Instruction_Text = Instruction_Text, Incorrect_Function_Text = Incorrect_Function_Text, Video_Instruction_Text = Video_Instruction_Text, ce = 0, video = wt, First_ConditionAC = maincond.condOneAC,Second_ConditionAC = maincond.condTwoAC,Third_ConditionAC = maincond.condThreeAC,Fourth_ConditionAC = maincond.condFourAC,Fifth_ConditionAC = maincond.condFiveAC,Sixth_ConditionAC = maincond.condSixAC,Seventh_ConditionAC = maincond.condSevenAC,Eighth_ConditionAC = maincond.condEightAC, VideoOne =  VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt),  VideoTwo =  VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt), VideoThree =  VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt), VideoFour=  VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt), VideoFive =  VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt), VideoSix =  VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt), VideoSeven =  VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt),  VideoEight =  VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt),instructions = session['instructions'], patientname=patientname,  Title_Program = Title_Program, First_Image=maincond.condOneImage, Second_Image=maincond.condTwoImage, Third_Image=maincond.condThreeImage, Fourth_Image=maincond.condFourImage, Fifth_Image=maincond.condFiveImage, Sixth_Image = maincond.condSixImage, Seventh_Image =maincond.condSevenImage, Eighth_Image = maincond.condEightImage, Info_Condition1 = maincond.condOneInfo, Info_Condition2=maincond.condTwoInfo, Info_Condition3=maincond.condThreeInfo, Info_Condition4 = maincond.condFourInfo, Info_Condition5 = maincond.condFiveInfo,Info_Condition6 = maincond.condSixInfo,Info_Condition7 = maincond.condSevenInfo,Info_Condition8 = maincond.condEightInfo, Condition1_Title=maincond.condOne, Condition2_Title=maincond.condTwo, Condition3_Title=maincond.condThree, Condition4_Title=maincond.condFour,Condition5_Title=maincond.condFive, Condition6_Title=maincond.condSix,Condition7_Title=maincond.condSeven, Condition8_Title=maincond.condEight, slug=titleid, setup=int(session['mechgamb'][0]))
	if request.method == 'POST':
	  #ce = check empty
#return render_template('index.html', Title_Program= "Gambler")
		order_info = request.form['orderinfo']
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
##There's an issue with a trailing comma at the bottom so we're going to search through it and 
##then remove it before sorting info.
		x = [q.strip() for q in order_info.split(",")]
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		if len(x) < int(session['mechgamb'][0]): 
			return render_template('order_info.html', Greeting_Text=Greeting_Text, Continue_Button=Continue_Button,Instruction_Text = Instruction_Text, Incorrect_Function_Text = Incorrect_Function_Text, Video_Instruction_Text = Video_Instruction_Text,  ce = 1, video = wt, First_ConditionAC = maincond.condOneAC,Second_ConditionAC = maincond.condTwoAC,Third_ConditionAC = maincond.condThreeAC,Fourth_ConditionAC = maincond.condFourAC,Fifth_ConditionAC = maincond.condFiveAC,Sixth_ConditionAC = maincond.condSixAC,Seventh_ConditionAC = maincond.condSevenAC,Eighth_ConditionAC = maincond.condEightAC, VideoOne =  VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt),  VideoTwo =  VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt), VideoThree =  VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt), VideoFour=  VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt), VideoFive =  VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt), VideoSix =  VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt), VideoSeven =  VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt),  VideoEight =  VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt),instructions = session['instructions'], patientname=patientname,  Title_Program = Title_Program, First_Image=maincond.condOneImage, Second_Image=maincond.condTwoImage, Third_Image=maincond.condThreeImage, Fourth_Image=maincond.condFourImage, Fifth_Image=maincond.condFiveImage, Sixth_Image = maincond.condSixImage, Seventh_Image =maincond.condSevenImage, Eighth_Image = maincond.condEightImage, Info_Condition1 = maincond.condOneInfo, Info_Condition2=maincond.condTwoInfo, Info_Condition3=maincond.condThreeInfo, Info_Condition4 = maincond.condFourInfo, Info_Condition5 = maincond.condFiveInfo,Info_Condition6 = maincond.condSixInfo,Info_Condition7 = maincond.condSevenInfo,Info_Condition8 = maincond.condEightInfo, Condition1_Title=maincond.condOne, Condition2_Title=maincond.condTwo, Condition3_Title=maincond.condThree, Condition4_Title=maincond.condFour,Condition5_Title=maincond.condFive, Condition6_Title=maincond.condSix,Condition7_Title=maincond.condSeven, Condition8_Title=maincond.condEight, slug=titleid, setup=int(session['mechgamb'][0]))
		session['order'] = x
		if(int(session['mechgamb'][0]) ==4):
			mainud.ordersave(str(x.index(maincond.condOneAC)+1),str(x.index(maincond.condTwoAC)+1),str(x.index(maincond.condThreeAC)+1),str(x.index(maincond.condFourAC)+1),"","","","")
			mainud.orderdbsave(username,x.index(maincond.condOneAC)+1,x.index(maincond.condTwoAC)+1,x.index(maincond.condThreeAC)+1,x.index(maincond.condFourAC)+1,-1,-1,-1,-1)
		elif(int(session['mechgamb'][0]) ==5):
			mainud.ordersave(str(x.index(maincond.condOneAC)+1),str(x.index(maincond.condTwoAC)+1),str(x.index(maincond.condThreeAC)+1),str(x.index(maincond.condFourAC)+1),str(x.index(maincond.condFiveAC)+1),"","","")
			mainud.orderdbsave(username,x.index(maincond.condOneAC)+1,x.index(maincond.condTwoAC)+1,x.index(maincond.condThreeAC)+1,x.index(maincond.condFourAC)+1,x.index(maincond.condFiveAC)+1 ,-1,-1,-1)
		elif(int(session['mechgamb'][0]) ==6):
			mainud.ordersave(str(x.index(maincond.condOneAC)+1),str(x.index(maincond.condTwoAC)+1),str(x.index(maincond.condThreeAC)+1),str(x.index(maincond.condFourAC)+1),str(x.index(maincond.condFiveAC)+1),str(x.index(maincond.condSixAC)+1),"","")
			mainud.orderdbsave(username,x.index(maincond.condOneAC)+1,x.index(maincond.condTwoAC)+1,x.index(maincond.condThreeAC)+1,x.index(maincond.condFourAC)+1,x.index(maincond.condFiveAC)+1 ,x.index(maincond.condSixAC)+1,-1,-1)
		elif(int(session['mechgamb'][0]) ==7):
			mainud.ordersave(str(x.index(maincond.condOneAC)+1),str(x.index(maincond.condTwoAC)+1),str(x.index(maincond.condThreeAC)+1),str(x.index(maincond.condFourAC)+1),str(x.index(maincond.condFiveAC)+1),str(x.index(maincond.condSixAC)+1),str(x.index(maincond.condSevenAC)+1),"")
			mainud.orderdbsave(username,x.index(maincond.condOneAC)+1,x.index(maincond.condTwoAC)+1,x.index(maincond.condThreeAC)+1,x.index(maincond.condFourAC)+1,x.index(maincond.condFiveAC)+1 ,x.index(maincond.condSixAC)+1,x.index(maincond.condSevenAC)+1,-1)
		elif(int(session['mechgamb'][0]) ==8):
			mainud.ordersave(str(x.index(maincond.condOneAC)+1),str(x.index(maincond.condTwoAC)+1),str(x.index(maincond.condThreeAC)+1),str(x.index(maincond.condFourAC)+1),str(x.index(maincond.condFiveAC)+1),str(x.index(maincond.condSixAC)+1),str(x.index(maincond.condSevenAC)+1),str(x.index(maincond.condEightAC)+1))
			mainud.orderdbsave(username,x.index(maincond.condOneAC)+1,x.index(maincond.condTwoAC)+1,x.index(maincond.condThreeAC)+1,x.index(maincond.condFourAC)+1,x.index(maincond.condFiveAC)+1,x.index(maincond.condSixAC)+1,x.index(maincond.condSevenAC)+1,x.index(maincond.condEightAC)+1)
		else:
			mainud.ordersave(str(x.index(maincond.condOneAC)+1),str(x.index(maincond.condTwoAC)+1),str(x.index(maincond.condThreeAC)+1),"","","","","")
			mainud.orderdbsave(username,x.index(maincond.condOneAC)+1,x.index(maincond.condTwoAC)+1,x.index(maincond.condThreeAC)+1,-1, -1,-1,-1,-1)

		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="orderinfo", buttonPress = "Submit", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()
			####Now for direction	
		if (int(session['mechgamb'][1]) > 0):
			return redirect("gdpr/" + titleid + "/" + username + "/intensity")
		elif (int(session['mechgamb'][2]) > 0):
			return redirect("gdpr/" + titleid + "/" + username + "/scenario/1")
		elif (int(session['mechgamb'][3]) > 0):
			return redirect("gdpr/" + titleid + "/" + username + '/timetrade/1')
		else:
			return redirect("gdpr/" + titleid + "/" + username + '/finish')
@gdpr.route('/<titleid>/<username>/intensity', methods=['GET','POST'])
def gdprintensityinfo(titleid, username):
	wt= 0
	Instruction_Text = "Click and drag the icon on the sliders to show your values for each health state."
	Greeting_Text = "Hello"
	Alert_Selection_Text = "Sorry, you may have forgotten to click and drag the sliders.<br/>Click and drag the icon on the sliders to show your values for each health state."
	Video_Instruction_Text = "Video Instructions"
	Continue_Button = "Continue"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Instruction_Text = LangLoad.VAS_Instruction_Text
		Alert_Selection_Text = LangLoad.VAS_Alert_Selection_Text
		Video_Instruction_Text = LangLoad.VAS_Video_Instruction_Text
		Continue_Button = LangLoad.Continue_Button
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	patientname = ""
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	maincond = ConditionInfo()
	maincond.load(titleid)
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	if 'order' not in session:
		if int(session['mechgamb'][1]) != 0:
			mech_h = int(session['mechgamb'][1])
		elif int(session['mechgamb'][2]) != 0:
			mech_h = int(session['mechgamb'][2])
		else:
			mech_h = int(session['mechgamb'][3])
		order_hd=[]
		order_hd.append(maincond.condOneAC)
		order_hd.append(maincond.condTwoAC)
		order_hd.append(maincond.condThreeAC)
		if mech_h >= 4:
			order_hd.append(maincond.condFourAC)
		if mech_h >= 5:
			order_hd.append(maincond.condFiveAC)
		if mech_h >= 6:
			order_hd.append(maincond.condSixAC)
		if mech_h >= 7:
			order_hd.append(maincond.condSevenAC)
		if mech_h >= 8:
			order_hd.append(maincond.condEightAC)
		session['order'] = order_hd
		del order_hd
	y = session['order']
	if request.method =='GET':  #ce = check empty
		return render_template('intensity_info.html',Greeting_Text =Greeting_Text,  Instruction_Text = Instruction_Text, Continue_Button=Continue_Button, Alert_Selection_Text= Alert_Selection_Text, Video_Instruction_Text = Video_Instruction_Text, ce = 0, video = wt,instructions = session['instructions'], order=y, patientname=patientname,  VideoOne =  VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt),  VideoTwo =  VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt), VideoThree =  VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt), VideoFour=  VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt), VideoFive =  VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt), VideoSix =  VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt), VideoSeven =  VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt),  VideoEight =  VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt), First_ConditionAC = maincond.condOneAC,Second_ConditionAC = maincond.condTwoAC,Third_ConditionAC = maincond.condThreeAC,Fourth_ConditionAC = maincond.condFourAC,Fifth_ConditionAC = maincond.condFiveAC,Sixth_ConditionAC = maincond.condSixAC,Seventh_ConditionAC = maincond.condSevenAC,Eighth_ConditionAC = maincond.condEightAC, Title_Program = Title_Program,ConditionOne=maincond.condOne, ConditionOneInfo =maincond.condOneInfo, ConditionTwo=maincond.condTwo, ConditionTwoInfo=maincond.condTwoInfo, ConditionThree=maincond.condThree, ConditionThreeInfo=maincond.condThreeInfo, ConditionFour=maincond.condFour, ConditionFourInfo=maincond.condFourInfo, First_Image=maincond.condOneImage, Second_Image=maincond.condTwoImage, Third_Image=maincond.condThreeImage, Fourth_Image=maincond.condFourImage, ConditionFive=maincond.condFive, ConditionFiveInfo =maincond.condFiveInfo, Fifth_Image=maincond.condFiveImage, ConditionSix=maincond.condSix, ConditionSixInfo =maincond.condSixInfo, Sixth_Image=maincond.condSixImage, ConditionSeven=maincond.condSeven, ConditionSevenInfo =maincond.condSevenInfo, Seventh_Image=maincond.condSevenImage, ConditionEight=maincond.condEight, ConditionEightInfo =maincond.condEightInfo, Eighth_Image=maincond.condEightImage, slug=titleid, setup=int(session['mechgamb'][1]))
	if request.method == 'POST':
# 		if not request.data:
# 			return render_template('jsonreturn.html', data=request.content_type)
# #return render_template('index.html', Title_Program= "Gambler")
# 	else:
		if request.form['intensityinfo'] is None or request.form['intensityinfo'] == "":
			return render_template('intensity_info.html', Greeting_Text =Greeting_Text,  Instruction_Text = Instruction_Text, Continue_Button=Continue_Button, Alert_Selection_Text= Alert_Selection_Text, Video_Instruction_Text = Video_Instruction_Text, ce = 1, video = wt,instructions = session['instructions'], order=y, patientname=patientname,  VideoOne =  VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt),  VideoTwo =  VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt), VideoThree =  VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt), VideoFour=  VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt), VideoFive =  VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt), VideoSix =  VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt), VideoSeven =  VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt),  VideoEight =  VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt),First_ConditionAC = maincond.condOneAC,Second_ConditionAC = maincond.condTwoAC,Third_ConditionAC = maincond.condThreeAC,Fourth_ConditionAC = maincond.condFourAC,Fifth_ConditionAC = maincond.condFiveAC,Sixth_ConditionAC = maincond.condSixAC,Seventh_ConditionAC = maincond.condSevenAC,Eighth_ConditionAC = maincond.condEightAC, Title_Program = Title_Program,ConditionOne=maincond.condOne, ConditionOneInfo =maincond.condOneInfo, ConditionTwo=maincond.condTwo, ConditionTwoInfo=maincond.condTwoInfo, ConditionThree=maincond.condThree, ConditionThreeInfo=maincond.condThreeInfo, ConditionFour=maincond.condFour, ConditionFourInfo=maincond.condFourInfo, First_Image=maincond.condOneImage, Second_Image=maincond.condTwoImage, Third_Image=maincond.condThreeImage, Fourth_Image=maincond.condFourImage, ConditionFive=maincond.condFive, ConditionFiveInfo =maincond.condFiveInfo, Fifth_Image=maincond.condFiveImage, ConditionSix=maincond.condSix, ConditionSixInfo =maincond.condSixInfo, Sixth_Image=maincond.condSixImage, ConditionSeven=maincond.condSeven, ConditionSevenInfo =maincond.condSevenInfo, Seventh_Image=maincond.condSevenImage, ConditionEight=maincond.condEight, ConditionEightInfo =maincond.condEightInfo, Eighth_Image=maincond.condEightImage, slug=titleid, setup=int(session['mechgamb'][1]))
		intensity_info = request.form['intensityinfo']
		z = [float(q) for q in intensity_info.split(",")]
		x = [-1,-1,-1,-1,-1,-1,-1,-1]
		#Rearranges values
		for t in range(0,len(y)):
			if (y[t] == maincond.condOneAC):
				x[0] = z[t]		
			if (y[t] == maincond.condTwoAC):
				x[1] = z[t]		
			if (y[t] == maincond.condThreeAC):
				x[2] = z[t]			
			elif (y[t] == maincond.condFourAC):
				x[3] = z[t]
			elif (y[t] == maincond.condFiveAC):
				x[4] = z[t]
			elif (y[t] == maincond.condSixAC):
				x[5] = z[t]
			elif (y[t] == maincond.condSevenAC):
				x[6] = z[t]
			else:
				x[7] = z[t]
		mainud = UserData()
	##Peewee doens't recgonize 0 as an integer so we go with -1
		if(int(session['mechgamb'][1]) ==4):
			mainud.intensave(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
			mainud.intendbsave(username,int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),int(x[5]),int(x[6]),int(x[7]))
		elif(int(session['mechgamb'][1]) ==5):
			mainud.intensave(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
			mainud.intendbsave(username,int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),int(x[5]),int(x[6]),int(x[7]))
		elif(int(session['mechgamb'][1]) ==6):
			mainud.intensave(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
			mainud.intendbsave(username,int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),int(x[5]),int(x[6]),int(x[7]))
		elif(int(session['mechgamb'][1]) ==7):
			mainud.intensave(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
			mainud.intendbsave(username,int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),int(x[5]),int(x[6]),int(x[7]))
		elif(int(session['mechgamb'][1]) ==8):
			mainud.intensave(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
			mainud.intendbsave(username,int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),int(x[5]),int(x[6]),int(x[7]))
		else:
			mainud.intensave(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
			mainud.intendbsave(username,int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),int(x[5]),int(x[6]),int(x[7]))

		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="VASinfo", buttonPress = "Submit", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()		###Now for direction
		if (int(session['mechgamb'][2]) > 0):
			return redirect("gdpr/" + titleid + "/" + username + "/scenario/1")
		elif (int(session['mechgamb'][3]) > 0):
			return redirect("gdpr/" + titleid + "/" + username + '/timetrade/1')
		else:
			return redirect("gdpr/" + titleid + "/" + username + '/finish')
	#                return json.dumps({'success': intensity_info}), 200, {'ContentType': 'application/json'}



#################################################################################
#																				#
#																				#
#																				#
#																				#
#								Time Trade Off 									#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################

#Production
@gdpr.route('/<titleid>/<username>/timetrade/1', methods=['GET','POST'])
def gdprtimetrade_information_one(titleid, username):
	maintime = GTimeTradeOff()
	maintimetradeoff = TimeTradeOff()
	patientname=""
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Time Trade off Video Instructions"
	HS_Video_Instruction_Text = "Performing Time Trade off for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Month_Text = "Month(s)"
	Year_Text = "Years"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.TTO_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.TTO_HS_Video_Instruction_Text
		Month_Text = LangLoad.TTO_Month_Text
		Year_Text = LangLoad.TTO_Year_Text
		
	maincond = ConditionInfo()
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	maintimetradeoff = TimeTradeOff()
	#mys = month year switch
	mys = maintimetradeoff.load(titleid,session['age'],session['race'],session['hld'], session['gender'])
	maintime.load(titleid)
	maincond.load(titleid)
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	if 'order' not in session:
		if int(session['mechgamb'][1]) != 0:
			mech_h = int(session['mechgamb'][1])
		elif int(session['mechgamb'][2]) != 0:
			mech_h = int(session['mechgamb'][2])
		else:
			mech_h = int(session['mechgamb'][3])
		order_hd=[]
		order_hd.append(maincond.condOneAC)
		order_hd.append(maincond.condTwoAC)
		order_hd.append(maincond.condThreeAC)
		if mech_h >= 4:
			order_hd.append(maincond.condFourAC)
		if mech_h >= 5:
			order_hd.append(maincond.condFiveAC)
		if mech_h >= 6:
			order_hd.append(maincond.condSixAC)
		if mech_h >= 7:
			order_hd.append(maincond.condSevenAC)
		if mech_h >= 8:
			order_hd.append(maincond.condEightAC)
		session['order'] = order_hd
		del order_hd
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	##Change Units with Timetrade units
	timetrade_units="Years"
	insvidtag = "" ##instructionsvideotag
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][3]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][3]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][3]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][3]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][3]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	if (session['order'][1] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement= 3
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][1] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainStatusInfo = maincond.condFourInfo
		MainScenStatement= 4
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][1] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement= 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][1] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement= 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][1] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement= 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	session['TTStart'] = maintimetradeoff.threshold
	if (wt <= 2):
		insvidtag = ""
	if  (mys == 1):
		timetrade_units=Month_Text
	else:
		timetrade_units=Year_Text
	if request.method == 'GET':
		return render_template('timetrade_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt, InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, instructions = session['instructions'],  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, maintimetradeoff.threshold, maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E, timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid,  Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min, Slider_Value=maintimetradeoff.threshold)
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][1], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()		
		###Now for direction
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['flag'] -= 1
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (abs(session['flag']),session['counter'],session['th'],mys)
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'], InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units,InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid,Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][1], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):	
			if (session['counter'] != 0):
				session['counter'] = 0
				session['flag'] +=1	
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('timetrade_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],   InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement = maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	else:
	
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][1], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['th'] = maintimetradeoff.threshold
		if (session['order'][1] == maincond.condThreeAC):
			session['timecon3'] = session['th']			
		elif (session['order'][1] == maincond.condFourAC):
			session['timecon4'] = session['th']
		elif (session['order'][1] == maincond.condFiveAC):
			session['timecon5'] = session['th']
		elif (session['order'][1] == maincond.condSixAC):
			session['timecon6'] = session['th']
		elif (session['order'][1] == maincond.condSevenAC):
			session['timecon7'] = session['th']
		else:
			session['timecon2'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][3]) <4):
				mainud = UserData()
				mainud.timetsave((maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max,(session['timecon2']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1,-1,-1,-1,-1)
				mainud.timetdbsave(username,( maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max,(session['timecon2']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1,-1,-1,-1,-1)
				return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else:
			return redirect("gdpr/" + titleid + "/" + username + "/timetrade/2")

@gdpr.route('/<titleid>/<username>/timetrade/2', methods=['GET','POST'])
def gdprtimetrade_information_two(titleid, username):
	maintime = GTimeTradeOff()
	maintimetradeoff = TimeTradeOff()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Time Trade off Video Instructions"
	HS_Video_Instruction_Text = "Performing Time Trade off for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Month_Text = "Month(s)"
	Year_Text = "Years"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.TTO_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.TTO_HS_Video_Instruction_Text
		Month_Text = LangLoad.TTO_Month_Text
		Year_Text = LangLoad.TTO_Year_Text
	maincond = ConditionInfo()
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	maintimetradeoff = TimeTradeOff()
	mys = maintimetradeoff.load(titleid,session['age'],session['race'],session['hld'], session['gender'])
	maintime.load(titleid)
	maincond.load(titleid)
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	##Change units here.
	timetrade_units="Years"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	insvidtag = ""
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][3]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][3]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][3]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][3]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][3]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	if (session['order'][2] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement= 3
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][2] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainStatusInfo = maincond.condFourInfo
		MainScenStatement= 4
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][2] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement= 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][2] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement= 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][2] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement= 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	maintimetradeoff.threshold = session['TTStart'] 
	if (wt <= 2):
		insvidtag = ""
	if  (mys == 1):
		timetrade_units=Month_Text
	else:
		timetrade_units=Year_Text
	if request.method == 'GET':
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, maintimetradeoff.threshold, maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E, timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min, Slider_Value=maintimetradeoff.threshold)
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][2], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['flag'] -= 1
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (abs(session['flag']),session['counter'],session['th'],mys)
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][2], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['counter'] = 0
				session['flag'] +=1	
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('timetrade_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'], InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units,  InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid,  Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][2], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['th'] = maintimetradeoff.threshold
		if (session['order'][2] == maincond.condThreeAC):
			session['timecon3'] = session['th']			
		elif (session['order'][2] == maincond.condFourAC):
			session['timecon4'] = session['th']
		elif (session['order'][2] == maincond.condFiveAC):
			session['timecon5'] = session['th']
		elif (session['order'][2] == maincond.condSixAC):
			session['timecon6'] = session['th']
		elif (session['order'][2] == maincond.condSevenAC):
			session['timecon7'] = session['th']
		else:
			session['timecon2'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][3]) <5):
			mainud = UserData()
			mainud.timetsave((maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max,(session['timecon3']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1,-1,-1,-1)
			mainud.timetdbsave(username, (maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max,(session['timecon3']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1,-1,-1,-1)
			return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else: 
			return redirect("gdpr/" + titleid + "/" + username + '/timetrade/3')
			

@gdpr.route('/<titleid>/<username>/timetrade/3', methods=['GET','POST'])
def gdprtimetrade_information_three(titleid, username):
	maintime = GTimeTradeOff()
	maintimetradeoff = TimeTradeOff()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Time Trade off Video Instructions"
	HS_Video_Instruction_Text = "Performing Time Trade off for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Month_Text = "Month(s)"
	Year_Text = "Years"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.TTO_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.TTO_HS_Video_Instruction_Text
		Month_Text = LangLoad.TTO_Month_Text
		Year_Text = LangLoad.TTO_Year_Text
	maincond = ConditionInfo()
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	maintimetradeoff = TimeTradeOff()
	mys = maintimetradeoff.load(titleid,session['age'],session['race'],session['hld'], session['gender'])
	maintime.load(titleid)
	maincond.load(titleid)
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	##Change units here.
	timetrade_units="Years"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	insvidtag = ""
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][3]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][3]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][3]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][3]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][3]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	if (session['order'][3] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement= 3
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][3] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainStatusInfo = maincond.condFourInfo
		MainScenStatement= 4
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][3] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement= 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][3] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement= 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][3] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement= 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	maintimetradeoff.threshold = session['TTStart'] 
	if (wt <= 2):
		insvidtag = ""
	if  (mys == 1):
		timetrade_units=Month_Text
	else:
		timetrade_units=Year_Text
	if request.method == 'GET':
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, maintimetradeoff.threshold, maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E, timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min, Slider_Value=maintimetradeoff.threshold)
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][3], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['flag'] -=1
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (abs(session['flag']),session['counter'],session['th'],mys)
		return render_template('timetrade_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo,  LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][3], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['counter'] = 0
				session['flag'] +=1	
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('timetrade_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units,  InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid,  Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][3], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['th'] = maintimetradeoff.threshold
		if (session['order'][3] == maincond.condThreeAC):
			session['timecon3'] = session['th']			
		elif (session['order'][3] == maincond.condFourAC):
			session['timecon4'] = session['th']
		elif (session['order'][3] == maincond.condFiveAC):
			session['timecon5'] = session['th']
		elif (session['order'][3] == maincond.condSixAC):
			session['timecon6'] = session['th']
		elif (session['order'][3] == maincond.condSevenAC):
			session['timecon7'] = session['th']
		else:
			session['timecon2'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][3]) <6):
			mainud = UserData()
			mainud.timetsave((maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max, (session['timecon3']*100.0)/maintimetradeoff.threshold_max,(session['timecon4']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1,-1,-1)
			mainud.timetdbsave(username,(maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max, (session['timecon3']*100.0)/maintimetradeoff.threshold_max,(session['timecon4']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1,-1,-1)
			return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else: 
			return redirect("gdpr/" + titleid + "/" + username + '/timetrade/4')

@gdpr.route('/<titleid>/<username>/timetrade/4', methods=['GET','POST'])
def gdprtimetrade_information_four(titleid, username):
	maintime = GTimeTradeOff()
	maintimetradeoff = TimeTradeOff()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Time Trade off Video Instructions"
	HS_Video_Instruction_Text = "Performing Time Trade off for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Month_Text = "Month(s)"
	Year_Text = "Years"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.TTO_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.TTO_HS_Video_Instruction_Text
		Month_Text = LangLoad.TTO_Month_Text
		Year_Text = LangLoad.TTO_Year_Text
	maincond = ConditionInfo()
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	mys = maintimetradeoff.load(titleid,session['age'],session['race'],session['hld'], session['gender'])
	maintime.load(titleid)
	maincond.load(titleid)
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	##Change units here.
	timetrade_units="Years"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	insvidtag = ""
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][3]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][3]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][3]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][3]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][3]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	if (session['order'][4] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement= 3
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][4] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainStatusInfo = maincond.condFourInfo
		MainScenStatement= 4
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][4] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement= 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][4] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement= 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][4] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement= 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	maintimetradeoff.threshold = session['TTStart']
	if (wt <= 2):
		insvidtag = "" 
	if  (mys == 1):
		timetrade_units=Month_Text
	else:
		timetrade_units=Year_Text
	if request.method == 'GET':
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, maintimetradeoff.threshold, maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E, timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min, Slider_Value=maintimetradeoff.threshold)
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][4], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['counter'] = 0
				session['flag'] -=1	
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (abs(session['flag']),session['counter'],session['th'],mys)
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][4], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['counter'] = 0
				session['flag'] +=1	
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units,  InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid,  Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][4], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['th'] = maintimetradeoff.threshold
		if (session['order'][4] == maincond.condThreeAC):
			session['timecon3'] = session['th']			
		elif (session['order'][4] == maincond.condFourAC):
			session['timecon4'] = session['th']
		elif (session['order'][4] == maincond.condFiveAC):
			session['timecon5'] = session['th']
		elif (session['order'][4] == maincond.condSixAC):
			session['timecon6'] = session['th']
		elif (session['order'][4] == maincond.condSevenAC):
			session['timecon7'] = session['th']
		else:
			session['timecon2'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][2]) < 7):
			mainud = UserData()
			mainud.timetsave((maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max, (session['timecon3']*100.0)/maintimetradeoff.threshold_max,(session['timecon4']*100.0)/maintimetradeoff.threshold_max, (session['timecon5']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1,-1)
			mainud.timetdbsave(username, (maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max, (session['timecon3']*100.0)/maintimetradeoff.threshold_max,(session['timecon4']*100.0)/maintimetradeoff.threshold_max, (session['timecon5']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1,-1)
			return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else: 
			return redirect("gdpr/" + titleid + "/" + username + '/timetrade/5')

@gdpr.route('/<titleid>/<username>/timetrade/5', methods=['GET','POST'])
def gdprtimetrade_information_five(titleid, username):
	maintime = GTimeTradeOff()
	maintimetradeoff = TimeTradeOff()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Time Trade off Video Instructions"
	HS_Video_Instruction_Text = "Performing Time Trade off for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Month_Text = "Month(s)"
	Year_Text = "Years"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.TTO_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.TTO_HS_Video_Instruction_Text
		Month_Text = LangLoad.TTO_Month_Text
		Year_Text = LangLoad.TTO_Year_Text
	maincond = ConditionInfo()
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	mys = maintimetradeoff.load(titleid,session['age'],session['race'],session['hld'], session['gender'])
	maintime.load(titleid)
	maincond.load(titleid)
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	##Change units here.
	timetrade_units="Years"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	insvidtag = "Five"
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][3]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][3]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][3]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][3]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][3]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	if (session['order'][5] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement= 3
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][5] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainStatusInfo = maincond.condFourInfo
		MainScenStatement= 4
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][5] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement= 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][5] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement= 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][5] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement= 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if (wt <= 2):
		insvidtag = ""
	maintimetradeoff.threshold = session['TTStart'] 
	if  (mys == 1):
		timetrade_units=Month_Text
	else:
		timetrade_units=Year_Text
	if request.method == 'GET':
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt, instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, maintimetradeoff.threshold, maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E, timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min, Slider_Value=maintimetradeoff.threshold)
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][5], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['counter'] = 0
				session['flag'] -=1	
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (abs(session['flag']),session['counter'],session['th'],mys)
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][4], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['counter'] = 0
				session['flag'] +=1	
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('timetrade_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'], InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo,  LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units,  InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid,  Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][4], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['th'] = maintimetradeoff.threshold
		if (session['order'][5] == maincond.condThreeAC):
			session['timecon3'] = session['th']			
		elif (session['order'][5] == maincond.condFourAC):
			session['timecon4'] = session['th']
		elif (session['order'][5] == maincond.condFiveAC):
			session['timecon5'] = session['th']
		elif (session['order'][5] == maincond.condSixAC):
			session['timecon6'] = session['th']
		elif (session['order'][5] == maincond.condSevenAC):
			session['timecon7'] = session['th']
		else:
			session['timecon2'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][3]) <8):
			mainud = UserData()
			mainud.timetsave((maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max, (session['timecon3']*100.0)/maintimetradeoff.threshold_max,(session['timecon4']*100.0)/maintimetradeoff.threshold_max, (session['timecon5']*100.0)/maintimetradeoff.threshold_max,(session['timecon6']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1)
			mainud.timetdbsave(username, (maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max, (session['timecon3']*100.0)/maintimetradeoff.threshold_max, (session['timecon4']*100.0)/maintimetradeoff.threshold_max, (session['timecon5']*100.0)/maintimetradeoff.threshold_max,(session['timecon6']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max,-1)
			return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else: 
			return redirect("gdpr/" + titleid + "/" + username + '/timetrade/6')
@gdpr.route('/<titleid>/<username>/timetrade/6', methods=['GET','POST'])
def gdprtimetrade_information_six(titleid, username):
	maintime = GTimeTradeOff()
	maintimetradeoff = TimeTradeOff()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Time Trade off Video Instructions"
	HS_Video_Instruction_Text = "Performing Time Trade off for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Month_Text = "Month(s)"
	Year_Text = "Years"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.TTO_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.TTO_HS_Video_Instruction_Text
		Month_Text = LangLoad.TTO_Month_Text
		Year_Text = LangLoad.TTO_Year_Text
	maincond = ConditionInfo()
	mys = maintimetradeoff.load(titleid,session['age'],session['race'],session['hld'], session['gender'])
	maintime.load(titleid)
	maincond.load(titleid)
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	##Change units here.
	timetrade_units="Years"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][3]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][3]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][3]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][3]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][3]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	if (session['order'][6] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement= 3
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][6] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainStatusInfo = maincond.condFourInfo
		MainScenStatement= 4
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][6] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement= 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][6] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement= 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][6] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement= 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement= 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	maintimetradeoff.threshold =session['TTStart'] 
	if (wt <= 2):
		insvidtag = ""
	if  (mys == 1):
		timetrade_units=Month_Text
	else:
		timetrade_units=Year_Text
	if request.method == 'GET':
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, maintimetradeoff.threshold, maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E, timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min, Slider_Value=maintimetradeoff.threshold)
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][6], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['counter'] = 0
				session['flag'] -=1	
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (abs(session['flag']),session['counter'],session['th'],mys)
		return render_template('timetrade_decision.html',Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units, InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid, Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][6], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maintimetradeoff.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['counter'] = 0
				session['flag'] +=1	
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maintimetradeoff.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('timetrade_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text,insvidtag = insvidtag, video = wt,  instructions=0,  Welcome_Statement=maintime.Welcome_Statement,flag = session['flag'],  InterVideo=MainVideo, LifeVideo=LifeVideo,DeathVideo=DeathVideo, LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][3],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=maintime.SBuild(MainCondition,MainScenStatement), Choosing_Statement=maintime.CBuild(timetrade_units, session['th'], maintimetradeoff.threshold_max, MainCondition),Agreement_Statement_A=maintime.Agreement_Statement_A, Agreement_Statement_B=maintime.Agreement_Statement_B, Agreement_Statement_E = maintime.Agreement_Statement_E,  Slider_Value=session['th'], timetrade_units=timetrade_units,  InterStatusInfo=MainStatusInfo, InterConditionStatus=MainCondition,InterImage=MainImage, slug=titleid,  Max_Time = maintimetradeoff.threshold_max, Min_Time=maintimetradeoff.threshold_min)
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="TTO" + session['order'][6], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['th'] = maintimetradeoff.threshold
		if (session['order'][6] == maincond.condThreeAC):
			session['timecon3'] = session['th']			
		elif (session['order'][6] == maincond.condFourAC):
			session['timecon4'] = session['th']
		elif (session['order'][6] == maincond.condFiveAC):
			session['timecon5'] = session['th']
		elif (session['order'][6] == maincond.condSixAC):
			session['timecon6'] = session['th']
		elif (session['order'][6] == maincond.condSevenAC):
			session['timecon7'] = session['th']
		else:
			session['timecon2'] = session['th']
		mainud = UserData()
		mainud.timetsave((maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max, (session['timecon3']*100.0)/maintimetradeoff.threshold_max,(session['timecon4']*100.0)/maintimetradeoff.threshold_max, (session['timecon5']*100.0)/maintimetradeoff.threshold_max,(session['timecon6']*100.0)/maintimetradeoff.threshold_max,(session['timecon7']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max)
		mainud.timetdbsave(username,(maintimetradeoff.threshold_max*100.0)/maintimetradeoff.threshold_max, (session['timecon2']*100.0)/maintimetradeoff.threshold_max, (session['timecon3']*100.0)/maintimetradeoff.threshold_max,(session['timecon4']*100.0)/maintimetradeoff.threshold_max, (session['timecon5']*100.0)/maintimetradeoff.threshold_max,(session['timecon6']*100.0)/maintimetradeoff.threshold_max,(session['timecon7']*100.0)/maintimetradeoff.threshold_max,(maintimetradeoff.threshold_min*100.0)/maintimetradeoff.threshold_max)
		return redirect("gdpr/" + titleid + "/" + username + '/finish')

#################################################################################
#																				#
#																				#
#																				#
#																				#
#									Standard Gamble								#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################


#Production
@gdpr.route('/<titleid>/<username>/scenario/1', methods=['GET','POST'])
def gdprscenario_informationone(titleid, username):
	mainscen = GScenario()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Standard Gamble Video Instructions"
	HS_Video_Instruction_Text = "Performing Standard Gamble for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Shake_Button = "Shake"
	Pill_Text = "Pill(s)"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.SG_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.SG_HS_Video_Instruction_Text
		Shake_Button = LangLoad.SG_Shake_Button
		Pill_Text = LangLoad.SG_Pill_Text
	flag = 0
	counter=0
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	if 'order' not in session:
		if int(session['mechgamb'][1]) != 0:
			mech_h = int(session['mechgamb'][1])
		elif int(session['mechgamb'][2]) != 0:
			mech_h = int(session['mechgamb'][2])
		else:
			mech_h = int(session['mechgamb'][3])
		order_hd=[]
		order_hd.append(maincond.condOneAC)
		order_hd.append(maincond.condTwoAC)
		order_hd.append(maincond.condThreeAC)
		if mech_h >= 4:
			order_hd.append(maincond.condFourAC)
		if mech_h >= 5:
			order_hd.append(maincond.condFiveAC)
		if mech_h >= 6:
			order_hd.append(maincond.condSixAC)
		if mech_h >= 7:
			order_hd.append(maincond.condSevenAC)
		if mech_h >= 8:
			order_hd.append(maincond.condEightAC)
		session['order'] = order_hd
		del order_hd
	maingamble = Gambler()
	maingamble.load(titleid)
	maincond = ConditionInfo()
	mainscen.load(titleid)
	maincond.load(titleid)
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	if session['name'] is None:
		patientname = "Temp"
	if session['counter'] is None:
		session['counter'] = 0
	if session['flag'] is None:
		session['flag'] = 0
	else:
		patientname=session['name']
	if (int(session['mechgamb'][2]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][2]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][2]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][2]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][2]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	session['PVStart'] = maingamble.threshold
	if (session['order'][1] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement = 3 #Use number to dictate which statement
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][1] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainScenStatement = 4
		MainStatusInfo = maincond.condFourInfo
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][1] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement = 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][1] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement = 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][1] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement = 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if (wt <= 2):
		insvidtag = ""
	if request.method == 'GET':
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = session['instructions'],  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value =maingamble.threshold,  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(maingamble.threshold, maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][1], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maingamble.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['flag'] -=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][1], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maingamble.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['flag'] +=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'],count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][1], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['th'] = maingamble.threshold
		if (session['order'][1] == maincond.condTwoAC):
			session['valcon2'] = session['th']
		if (session['order'][1] == maincond.condThreeAC):
			session['valcon3'] = session['th']
		if (session['order'][1] == maincond.condFourAC):
			session['valcon4'] = session['th']
		if (session['order'][1] == maincond.condFiveAC):
			session['valcon5'] = session['th']
		if (session['order'][1] == maincond.condSixAC):
			session['valcon6'] = session['th']
		else:		
			session['valcon7'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][2]) < 4):
			mainud = UserData()
			mainud.gambsave((maingamble.threshold_max*100)/maingamble.threshold_max, ((session['valcon2'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1,-1,-1,-1,-1)
			mainud.gambdbsave(username, (maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1,-1,-1,-1,-1)
			if (int(session['mechgamb'][3]) > 0):
				return redirect("gdpr/" + titleid + "/" + username + '/timetrade/1')
			else:
				return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else:
			return redirect("gdpr/" + titleid + "/" + username + '/scenario/2')

@gdpr.route('/<titleid>/<username>/scenario/2', methods=['GET','POST'])
def gdprscenario_informationtwo(titleid, username):
	mainscen = GScenario()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Standard Gamble Video Instructions"
	HS_Video_Instruction_Text = "Performing Standard Gamble for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Shake_Button = "Shake"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.SG_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.SG_HS_Video_Instruction_Text
		Shake_Button = LangLoad.SG_Shake_Button
		Pill_Text = LangLoad.SG_Pill_Text
	flag = 0
	counter=0
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	maingamble = Gambler()
	maingamble.load(titleid)
	maincond = ConditionInfo()
	mainscen.load(titleid)
	maincond.load(titleid)
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	maingamble.threshold =session['PVStart']
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][2]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][2]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][2]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][2]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][2]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	session['PVStart'] = maingamble.threshold
	if (session['order'][2] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement = 3 #Use number to dictate which statement
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][2] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainScenStatement = 4
		MainStatusInfo = maincond.condFourInfo
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][2] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement = 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][2] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement = 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][2] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement = 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if (wt <= 2):
		insvidtag = ""
	if request.method == 'GET':
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value =maingamble.threshold,  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(maingamble.threshold, maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][2], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maingamble.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['flag'] -=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][2], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maingamble.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['flag'] +=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'],count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][2], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['th'] = maingamble.threshold
		if (session['order'][2] == maincond.condTwoAC):
			session['valcon2'] = session['th']
		if (session['order'][2] == maincond.condThreeAC):
			session['valcon3'] = session['th']
		if (session['order'][2] == maincond.condFourAC):
			session['valcon4'] = session['th']
		if (session['order'][2] == maincond.condFiveAC):
			session['valcon5'] = session['th']
		if (session['order'][2] == maincond.condSixAC):
			session['valcon6'] = session['th']
		else:		
			session['valcon7'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][2]) < 5):
			mainud = UserData()
			mainud.gambsave((maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1,-1,-1,-1)
			mainud.gambdbsave(username,(maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1,-1,-1,-1)
			if (int(session['mechgamb'][3]) > 0):
				return redirect("gdpr/" + titleid + "/" + username + '/timetrade/1')
			else:
				return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else:
			return redirect("gdpr/" + titleid + "/" + username + '/scenario/3')


@gdpr.route('/<titleid>/<username>/scenario/3', methods=['GET','POST'])
def gdprscenario_informationthree(titleid, username):
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	mainscen = GScenario()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Standard Gamble Video Instructions"
	HS_Video_Instruction_Text = "Performing Standard Gamble for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Shake_Button = "Shake"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.SG_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.SG_HS_Video_Instruction_Text
		Shake_Button = LangLoad.SG_Shake_Button
		Pill_Text = LangLoad.SG_Pill_Text
	flag = 0
	counter=0
	maingamble = Gambler()
	maingamble.load(titleid)
	maincond = ConditionInfo()
	mainscen.load(titleid)
	maincond.load(titleid)
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	maingamble.threshold =session['PVStart']
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][2]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][2]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][2]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][2]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][2]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	session['PVStart'] = maingamble.threshold
	if (session['order'][3] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement = 3 #Use number to dictate which statement
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][3] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainScenStatement = 4
		MainStatusInfo = maincond.condFourInfo
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][3] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement = 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][3] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement = 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][3] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement = 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if (wt <= 2):
		insvidtag = ""
	if request.method == 'GET':
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value =maingamble.threshold,  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(maingamble.threshold, maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][3], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maingamble.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['flag'] -=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][3], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maingamble.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['flag'] +=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'],count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][3], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['th'] = maingamble.threshold
		if (session['order'][3] == maincond.condTwoAC):
			session['valcon2'] = session['th']
		if (session['order'][3] == maincond.condThreeAC):
			session['valcon3'] = session['th']
		if (session['order'][3] == maincond.condFourAC):
			session['valcon4'] = session['th']
		if (session['order'][3] == maincond.condFiveAC):
			session['valcon5'] = session['th']
		if (session['order'][3] == maincond.condSixAC):
			session['valcon6'] = session['th']
		else:		
			session['valcon7'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][2]) < 6):
			mainud = UserData()
			mainud.gambsave((maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,((session['valcon4'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1,-1,-1)
			mainud.gambdbsave(username,(maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,((session['valcon4'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1,-1,-1)
			if (int(session['mechgamb'][3]) > 0):
				return redirect("gdpr/" + titleid + "/" + username + '/timetrade/1')
			else:
				return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else:
			return redirect("gdpr/" + titleid + "/" + username + '/scenario/4')
			
@gdpr.route('/<titleid>/<username>/scenario/4', methods=['GET','POST'])
def gdprscenario_informationfour(titleid, username):
	mainscen = GScenario()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Standard Gamble Video Instructions"
	HS_Video_Instruction_Text = "Performing Standard Gamble for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Shake_Button = "Shake"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.SG_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.SG_HS_Video_Instruction_Text
		Shake_Button = LangLoad.SG_Shake_Button
		Pill_Text = LangLoad.SG_Pill_Text
	flag = 0
	counter=0
	maingamble = Gambler()
	maingamble.load(titleid)
	maincond = ConditionInfo()
	mainscen.load(titleid)
	maincond.load(titleid)
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	maingamble.threshold =session['PVStart']
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][2]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][2]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][2]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][2]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][2]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	session['PVStart'] = maingamble.threshold
	if (session['order'][4] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement = 3 #Use number to dictate which statement
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][4] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainScenStatement = 4
		MainStatusInfo = maincond.condFourInfo
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][4] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement = 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][4] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement = 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][4] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement = 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if (wt <= 2):
		insvidtag = ""
	if request.method == 'GET':
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value =maingamble.threshold,  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(maingamble.threshold, maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][4], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maingamble.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['flag'] -=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][4], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maingamble.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['flag'] +=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'],count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][1], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['th'] = maingamble.threshold
		if (session['order'][4] == maincond.condTwoAC):
			session['valcon2'] = session['th']
		if (session['order'][4] == maincond.condThreeAC):
			session['valcon3'] = session['th']
		if (session['order'][4] == maincond.condFourAC):
			session['valcon4'] = session['th']
		if (session['order'][4] == maincond.condFiveAC):
			session['valcon5'] = session['th']
		if (session['order'][4] == maincond.condSixAC):
			session['valcon6'] = session['th']
		else:		
			session['valcon7'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][2]) < 7):
			mainud = UserData()
			mainud.gambsave((maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,((session['valcon4'])*100)/maingamble.threshold_max,((session['valcon5'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1,-1)
			mainud.gambdbsave(username,(maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,((session['valcon4'])*100)/maingamble.threshold_max,((session['valcon5'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1,-1)
			if (int(session['mechgamb'][3]) > 0):
				return redirect("gdpr/" + titleid + "/" + username + '/timetrade/1')
			else:
				return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else:
			return redirect("gdpr/" + titleid + "/" + username + '/scenario/5')
			
@gdpr.route('/<titleid>/<username>/scenario/5', methods=['GET','POST'])
def gdprscenario_informationfive(titleid, username):
	mainscen = GScenario()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Standard Gamble Video Instructions"
	HS_Video_Instruction_Text = "Performing Standard Gamble for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Shake_Button = "Shake"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.SG_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.SG_HS_Video_Instruction_Text
		Shake_Button = LangLoad.SG_Shake_Button
		Pill_Text = LangLoad.SG_Pill_Text
	flag = 0
	counter=0
	maingamble = Gambler()
	maingamble.load(titleid)
	maincond = ConditionInfo()
	mainscen.load(titleid)
	maincond.load(titleid)
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][2]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][2]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][2]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][2]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][2]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	if (session['order'][5] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement = 3 #Use number to dictate which statement
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][5] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainScenStatement = 4
		MainStatusInfo = maincond.condFourInfo
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][5] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement = 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][5] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement = 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][5] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement = 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if (wt <= 2):
		insvidtag = ""
	if request.method == 'GET':
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value =maingamble.threshold,  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(maingamble.threshold, maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][5], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maingamble.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['flag'] -=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][5], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maingamble.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['flag'] +=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt,  MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'],count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][5], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['th'] = maingamble.threshold
		if (session['order'][5] == maincond.condTwoAC):
			session['valcon2'] = session['th']
		if (session['order'][5] == maincond.condThreeAC):
			session['valcon3'] = session['th']
		if (session['order'][5] == maincond.condFourAC):
			session['valcon4'] = session['th']
		if (session['order'][5] == maincond.condFiveAC):
			session['valcon5'] = session['th']
		if (session['order'][5] == maincond.condSixAC):
			session['valcon6'] = session['th']
		else:		
			session['valcon7'] = session['th']
		session['flag'] = 0
		session['counter'] = 0
		if (int(session['mechgamb'][2]) < 8):
			mainud = UserData()
			mainud.gambsave((maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,((session['valcon4'])*100)/maingamble.threshold_max,((session['valcon5'])*100)/maingamble.threshold_max,((session['valcon6'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1)
			mainud.gambdbsave(username,(maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,((session['valcon4'])*100)/maingamble.threshold_max,((session['valcon5'])*100)/maingamble.threshold_max,((session['valcon6'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max,-1)
			if (int(session['mechgamb'][3]) > 0):
				return redirect("gdpr/" + titleid + "/" + username + '/timetrade/1')
			else:
				return redirect("gdpr/" + titleid + "/" + username + '/finish')
		else:
			return redirect("gdpr/" + titleid + "/" + username + '/scenario/6')
			
@gdpr.route('/<titleid>/<username>/scenario/6', methods=['GET','POST'])
def gdprscenario_informationsix(titleid, username):
	mainscen = GScenario()
	patientname=""
	insvidtag = "" ##instructionsvideotag
	Show_Less_Text = "Show less information"
	Show_More_Text = "Show more information"
	Video_Instruction_Text = "Performing General Standard Gamble Video Instructions"
	HS_Video_Instruction_Text = "Performing Standard Gamble for {{MainCondition}} Video Instructions"
	Greeting_Text = "Hello"
	Shake_Button = "Shake"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.Greeting_Text
		Show_Less_Text = LangLoad.Show_Less_Text
		Show_More_Text = LangLoad.Show_More_Text
		Video_Instruction_Text = LangLoad.SG_Video_Instruction_Text
		HS_Video_Instruction_Text = LangLoad.SG_HS_Video_Instruction_Text
		Shake_Button = LangLoad.SG_Shake_Button
		Pill_Text = LangLoad.SG_Pill_Text
	flag = 0
	counter=0
	maingamble = Gambler()
	maingamble.load(titleid)
	maincond = ConditionInfo()
	mainscen.load(titleid)
	maincond.load(titleid)
	wt= 0
	try:
		wt = int(session['mechgamb'][4])
	except:
		wt = 0
	Title_Program = maincond.getprojecttitle(titleid)
	if (Title_Program is None or Title_Program == ""):
		Title_Program = "Gambler"
	DeathCondition = None
	DeathImage = None
	DeathStatusInfo = None
	LifeCondition = maincond.condOne
	LifeImage = maincond.condOneImage
	LifeStatusInfo = maincond.condOneInfo
	LifeVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],1,wt)
	session['th'] = session['PVStart']
	maingamble.threshold =session['PVStart']
	if session['name'] is None:
		patientname = "Temp"
	else:
		patientname=session['name']
	if (int(session['mechgamb'][2]) == 3):
		DeathCondition = maincond.condThree
		DeathImage = maincond.condThreeImage
		DeathStatusInfo = maincond.condThreeInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
	elif (int(session['mechgamb'][2]) == 4):
		DeathCondition = maincond.condFour
		DeathImage = maincond.condFourImage
		DeathStatusInfo = maincond.condFourInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
	elif (int(session['mechgamb'][2]) == 5):
		DeathCondition = maincond.condFive
		DeathImage = maincond.condFiveImage
		DeathStatusInfo = maincond.condFiveInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
	elif (int(session['mechgamb'][2]) == 6):
		DeathCondition = maincond.condSix
		DeathImage = maincond.condSixImage
		DeathStatusInfo = maincond.condSixInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
	elif (int(session['mechgamb'][2]) == 7):
		DeathCondition = maincond.condSeven
		DeathImage = maincond.condSevenImage
		DeathStatusInfo = maincond.condSevenInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
	else:
		DeathCondition = maincond.condEight
		DeathImage = maincond.condEightImage
		DeathStatusInfo = maincond.condEightInfo
		DeathVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],8,wt)
	if (session['order'][6] == maincond.condThreeAC):
		MainCondition = maincond.condThree
		MainImage = maincond.condThreeImage
		MainStatusInfo = maincond.condThreeInfo
		MainScenStatement = 3 #Use number to dictate which statement
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],3,wt)
		insvidtag = "Three"
	elif (session['order'][6] == maincond.condFourAC):
		MainCondition = maincond.condFour
		MainImage = maincond.condFourImage
		MainScenStatement = 4
		MainStatusInfo = maincond.condFourInfo
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],4,wt)
		insvidtag = "Four"
	elif (session['order'][6] == maincond.condFiveAC):
		MainCondition = maincond.condFive
		MainImage = maincond.condFiveImage
		MainStatusInfo = maincond.condFiveInfo
		MainScenStatement = 5
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],5,wt)
		insvidtag = "Five"
	elif (session['order'][6] == maincond.condSixAC):
		MainCondition = maincond.condSix
		MainImage = maincond.condSixImage
		MainStatusInfo = maincond.condSixInfo
		MainScenStatement = 6
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],6,wt)
		insvidtag = "Six"
	elif (session['order'][6] == maincond.condSevenAC):
		MainCondition = maincond.condSeven
		MainImage = maincond.condSevenImage
		MainStatusInfo = maincond.condSevenInfo
		MainScenStatement = 7
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],7,wt)
		insvidtag = "Seven"
	else:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if not session['order']:
		MainCondition = maincond.condTwo
		MainImage = maincond.condTwoImage
		MainStatusInfo = maincond.condTwoInfo
		MainScenStatement = 2
		MainVideo = VideoUrlBuild(session['race'], session['gender'],session['age'],2,wt)
		insvidtag = "Two"
	if (wt <= 2):
		insvidtag = ""
	if request.method == 'GET':
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value =maingamble.threshold,  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(maingamble.threshold, maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_A' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][6], buttonPress = "Agreement_Box_A", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] == 0):
			session['flag'] = 1
			session['th'] = maingamble.threshold
		if (session['flag'] >= 1 or abs(session['flag']) >=2):
			if (session['flag'] != abs(session['flag'])):
				session['flag'] = abs(session['flag'])
				session['counter'] = 0
			else:
				session['counter']+=1
		if (session['flag'] <= -1):
			if (session['counter'] != 0):
				session['flag'] -=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt, MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'], count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	if 'Agreement_Box_B' in request.form:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else "" 
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][6], buttonPress = "Agreement_Box_B", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['flag'] = -1
			session['th'] = maingamble.threshold
		if (session['flag'] <=-1 or -abs(session['flag']) <=-2):
			if (session['flag'] != -abs(session['flag'])):
				session['counter']=0
				session['flag'] = -abs(session['flag']) 
			else:
				session['counter']+=1
		if (session['flag'] >=1 ):
			if (session['counter'] != 0):
				session['flag'] +=1	
				session['counter'] = 0
			else:
				session['counter']+=1
			session['flag'] *=-1	
		session['th'] = maingamble.refine_threshold (-abs(session['flag']),session['counter'],session['th'])
		return render_template('scenario_decision.html', Greeting_Text = Greeting_Text, Show_Less_Text = Show_Less_Text, Show_More_Text = Show_More_Text,Video_Instruction_Text = Video_Instruction_Text,HS_Video_Instruction_Text = HS_Video_Instruction_Text, Shake_Button = Shake_Button, Pill_Text = Pill_Text,insvidtag = insvidtag, video = wt,  MainVideo = MainVideo, DeathVideo=DeathVideo, LifeVideo=LifeVideo, instructions = 0,  Welcome_Statement=mainscen.Welcome_Statement, flag = session['flag'],count =session['counter'], LifeCondition = LifeCondition,LifeImage = LifeImage,LifeStatusInfo = LifeStatusInfo,DeathCondition = DeathCondition,DeathImage = DeathImage,DeathStatusInfo = DeathStatusInfo,setup=session['mechgamb'][2], Total_Pills =  maingamble.threshold_max, Pill_Value = session['th'],  Title_Program = Title_Program, patientname=patientname, Scenario_Statement=mainscen.SBuild(MainCondition,MainScenStatement), Choosing_Statement=mainscen.CBuild(session['th'], maingamble.threshold_max, MainCondition),Agreement_Statement_A=mainscen.Agreement_Statement_A, Agreement_Statement_B=mainscen.Agreement_Statement_B, Agreement_Statement_E = mainscen.Agreement_Statement_E, MainStatusInfo=MainStatusInfo,MainCondition=MainCondition, slug=titleid, Main_Image = MainImage )
	else:
		healthtime = request.form['timinginfo'] if request.form['totaltiminginfo'] is not None else ""
		totaltime = request.form['totaltiminginfo'] if request.form['totaltiminginfo'] is not None else 0
		healthtime = healthtime.strip("undefined")
		hts = [float(q.strip()) for q in healthtime.split(",") if healthtime != ""]
		for uphst in range(0, 8-len(hts)):
			hts.append(0.0)

		if (db.is_closed()==False):
			db.close()
		db.connect()
		HSave = UserMetaData.create(userid = session['userid'], titleid= titleid, currentPage ="SG" + session['order'][1], buttonPress = "Agreement_Box_E", totalTime = int(totaltime),	conditionOneTime = hts[0], 	conditionTwoTime = hts[1],conditionThreeTime = hts[2], conditionFourTime = hts[3],	conditionFiveTime = hts[4],  conditionSixTime = hts[5], conditionSevenTime = hts[6], conditionEightTime = hts[7])
		db.close()	
		if (session['flag'] ==0):
			session['th'] = maingamble.threshold
		if (session['order'][6] == maincond.condTwoAC):
			session['valcon2'] = session['th']
		if (session['order'][6] == maincond.condThreeAC):
			session['valcon3'] = session['th']
		if (session['order'][6] == maincond.condFourAC):
			session['valcon4'] = session['th']
		if (session['order'][6] == maincond.condFiveAC):
			session['valcon5'] = session['th']
		if (session['order'][6] == maincond.condSixAC):
			session['valcon6'] = session['th']
		else:		
			session['valcon7'] = session['th']
		
		session['flag'] = 0
		session['counter'] = 0
		mainud = UserData()
		mainud.gambsave((maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,((session['valcon4'])*100)/maingamble.threshold_max,((session['valcon5'])*100)/maingamble.threshold_max,((session['valcon6'])*100)/maingamble.threshold_max,((session['valcon7'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max)
		mainud.gambdbsave(username,(maingamble.threshold_max*100)/maingamble.threshold_max,((session['valcon2'])*100)/maingamble.threshold_max,((session['valcon3'])*100)/maingamble.threshold_max,((session['valcon4'])*100)/maingamble.threshold_max,((session['valcon5'])*100)/maingamble.threshold_max,((session['valcon6'])*100)/maingamble.threshold_max,((session['valcon7'])*100)/maingamble.threshold_max,(maingamble.threshold_min*100)/maingamble.threshold_max)
		if (int(session['mechgamb'][3]) > 0):
			return redirect("gdpr/" + titleid + "/" + username + '/timetrade/1')
		else:
			return redirect("gdpr/" + titleid + "/" + username + '/finish')

#################################################################################
#																				#
#																				#
#																				#
#																				#
#					Post Assessment 											#
#																				#
#																				#
#																				#
#																				#																				
#################################################################################

#################################################################################
#FINISH 
@gdpr.route('/<titleid>/<username>/finish', methods=['GET','POST'])
def gdprfinish_info(titleid, username):
	Greeting_Text = "Thank you for completing the assessemnt {{FirstName}}.  Here are the results:"
	HS_Text = "Health State"
	OR_Text = "Ordinal Scale"
	VAS_Text = "Visual Analog Scale"
	SG_Text = "Standard Gamble"
	TTO_Text = "Time Trade off"
	CSV_Export_Button = "CSV Export"
	Finish_Button = "Finish"
	if session['language'] != "en-US":
		if (db.is_closed()==False):
			db.close()
		db.connect()
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.End_Greeting_Text
		HS_Text = LangLoad.End_HS_Text
		OR_Text = LangLoad.End_OR_Text
		VAS_Text = LangLoad.End_VAS_Text
		SG_Text = LangLoad.End_SG_Text
		TTO_Text = LangLoad.End_TTO_Text
		CSV_Export_Button = LangLoad.End_CSV_Export_Button
		Finish_Button = LangLoad.End_Finish_Button
	if request.method == 'GET':
		maincd = ConditionInfo()
		maincd.load(titleid)
		Title_Program = maincd.getprojecttitle(titleid)
		if (Title_Program is None or Title_Program == ""):
			Title_Program = "Gambler"
		mainud = UserData()
		mainud.retrievefinal(username)
		w=0
		od=int(session['mechgamb'][0])
		vs=int(session['mechgamb'][1])
		gb=int(session['mechgamb'][2])
		tt=int(session['mechgamb'][3])
		if session['mechgamb'] is not None:
			for q in session['mechgamb']:
				if int(q) > 0:
					w = int(q)
					break
		#This is literally madness that I am going to save data in this method but work with me
		#Doesn't matter how you start, it's how you finish
		#It's constantly saving so the final product should come out.		
				
		return render_template('final_gdpr.html',Greeting_Text=Greeting_Text, HS_Text=HS_Text, OR_Text=OR_Text, VAS_Text=VAS_Text, SG_Text = SG_Text, TTO_Text= TTO_Text, CSV_Export_Button = CSV_Export_Button, Finish_Button=Finish_Button, Title_Program = Title_Program, order = session['order'], tt=tt,od=od,gb=gb,vs=vs, FirstName=session['name'], username=session['userid'], First_ConditionAC = maincd.condOneAC,Second_ConditionAC = maincd.condTwoAC,Third_ConditionAC = maincd.condThreeAC,Fourth_ConditionAC = maincd.condFourAC,Fifth_ConditionAC = maincd.condFiveAC,Sixth_ConditionAC = maincd.condSixAC,Seventh_ConditionAC = maincd.condSevenAC,Eighth_ConditionAC = maincd.condEightAC,First_Condition=maincd.condOne, First_Condition_Order=mainud.finalconditionOrderOne, First_Condition_Intensity = mainud.finalconditionIntensityOne, First_Condition_Gamble = mainud.finalconditionGambOne, First_Condition_Time=mainud.finalconditionTimeTOne, Second_Condition=maincd.condTwo, Second_Condition_Order=mainud.finalconditionOrderTwo, Second_Condition_Intensity = mainud.finalconditionIntensityTwo, Second_Condition_Gamble = mainud.finalconditionGambTwo, Second_Condition_Time=mainud.finalconditionTimeTTwo, Third_Condition=maincd.condThree, Third_Condition_Order=mainud.finalconditionOrderThree, Third_Condition_Intensity = mainud.finalconditionIntensityThree, Third_Condition_Gamble = mainud.finalconditionGambThree, Third_Condition_Time=mainud.finalconditionTimeTThree, Fourth_Condition=maincd.condFour, Fourth_Condition_Order=mainud.finalconditionOrderFour, Fourth_Condition_Intensity = mainud.finalconditionIntensityFour, Fourth_Condition_Gamble = mainud.finalconditionGambFour, Fourth_Condition_Time=mainud.finalconditionTimeTFour,Fifth_Condition=maincd.condFive, Fifth_Condition_Order=mainud.finalconditionOrderFive, Fifth_Condition_Intensity = mainud.finalconditionIntensityFive, Fifth_Condition_Gamble = mainud.finalconditionGambFive,  Fifth_Condition_Time=mainud.finalconditionTimeTFive, Sixth_Condition=maincd.condSix, Sixth_Condition_Order=mainud.finalconditionOrderSix, Sixth_Condition_Intensity = mainud.finalconditionIntensitySix, Sixth_Condition_Gamble = mainud.finalconditionGambSix,  Sixth_Condition_Time=mainud.finalconditionTimeTSix, Seventh_Condition=maincd.condSeven, Seventh_Condition_Order=mainud.finalconditionOrderSeven, Seventh_Condition_Intensity = mainud.finalconditionIntensitySeven, Seventh_Condition_Gamble = mainud.finalconditionGambSeven,  Seventh_Condition_Time=mainud.finalconditionTimeTSeven, Eighth_Condition=maincd.condEight, Eighth_Condition_Order=mainud.finalconditionOrderEight, Eighth_Condition_Intensity = mainud.finalconditionIntensityEight, Eighth_Condition_Gamble = mainud.finalconditionGambEight,  Eighth_Condition_Time=mainud.finalconditionTimeTEight, First_Condition_Image=maincd.condOneImage, Second_Condition_Image=maincd.condTwoImage, Third_Condition_Image=maincd.condThreeImage, Fourth_Condition_Image=maincd.condFourImage, Fifth_Condition_Image=maincd.condFiveImage, Sixth_Condition_Image=maincd.condSixImage, Seventh_Condition_Image=maincd.condSevenImage, Eighth_Condition_Image=maincd.condEightImage,slug=titleid,setup=w)


#################################################################################
#Clear information for future use
@gdpr.route('/<titleid>/<username>/end', methods=['GET','POST'])
def gdprend_info(titleid, username):
	if request.method == 'GET':
		if session is not None:
			if 'local' in session:
				GamUI = UserMetaData.delete().where(UserMetaData.titleid == titleid, UserMetaData.userid == username).execute()
				GamUI = UserInfo.delete().where(UserInfo.titleid == titleid, UserInfo.userid == username).execute()
			if session['mechgamb'] is not None:
				for q in session['mechgamb']:
					if int(q) > 0:
						w = int(q)
						break;
			session.clear()
		return redirect("gdpr/" + titleid + "/")

###################################
#Generate CSV Code
@gdpr.route('/<titleid>/<username>/<firstname>/<lastname>/export', methods=['GET','POST'])
@gdpr.route('/<titleid>/<username>/<firstname>/export', methods=['GET','POST'])
@gdpr.route('/<titleid>/<username>/export', methods=['GET','POST'])
def gdprcsv_export(titleid, username,firstname=None,lastname=None):
	maincd = ConditionInfo()
	maincd.load(titleid)
	mainud = UserData()
	mainud.retrievefinal(username)
	v=0
	tqx = maincd.getmech(titleid)
	HS_Text = "Health State"
	OR_Text = "Ordinal Scale"
	VAS_Text = "Visual Analog Scale"
	SG_Text = "Standard Gamble"
	TTO_Text = "Time Trade off"
	if 'language' in session and session['language'] != "en-US":
		UserSystemLangauge = LangUserSystemTranslate()
		LangLoad = UserSystemLangauge.get(LangUserSystemTranslate.language == session['language'])
		Greeting_Text = LangLoad.End_Greeting_Text
		HS_Text = LangLoad.End_HS_Text
		OR_Text = LangLoad.End_OR_Text
		VAS_Text = LangLoad.End_VAS_Text
		SG_Text = LangLoad.End_SG_Text
		TTO_Text = LangLoad.End_TTO_Text	
	for q in tqx:
		if int(q) > 0:
			v = int(q)
			break;
	def generate():
		data = StringIO()
		w = csv.writer(data)
		# write header
		w.writerow((HS_Text,OR_Text,VAS_Text, SG_Text, TTO_Text))
		yield data.getvalue()
		data.seek(0)
		data.truncate(0)

		# write each log item
		for g in range(0,v):
			if (g==0):
				w.writerow((maincd.condOne, mainud.finalconditionOrderOne,  mainud.finalconditionIntensityOne,  mainud.finalconditionGambOne, mainud.finalconditionTimeTOne))
			if (g==1):
				w.writerow((maincd.condTwo, mainud.finalconditionOrderTwo,  mainud.finalconditionIntensityTwo,  mainud.finalconditionGambTwo, mainud.finalconditionTimeTTwo))
			if (g==2):
				w.writerow((maincd.condThree, mainud.finalconditionOrderThree,  mainud.finalconditionIntensityThree,  mainud.finalconditionGambThree, mainud.finalconditionTimeTThree))
			if (g==3):
				w.writerow((maincd.condFour, mainud.finalconditionOrderFour,  mainud.finalconditionIntensityFour,  mainud.finalconditionGambFour, mainud.finalconditionTimeTFour))
			if (g==4):
				w.writerow((maincd.condFive, mainud.finalconditionOrderFive,  mainud.finalconditionIntensityFive,  mainud.finalconditionGambFive, mainud.finalconditionTimeTFive))
			if (g==5):
				w.writerow((maincd.condSix, mainud.finalconditionOrderSix,  mainud.finalconditionIntensitySix,  mainud.finalconditionGambSix, mainud.finalconditionTimeTSix))
			if (g==6):
				w.writerow((maincd.condSeven, mainud.finalconditionOrderSeven,  mainud.finalconditionIntensitySeven,  mainud.finalconditionGambSeven, mainud.finalconditionTimeTSeven))
			if (g==7):
				w.writerow((maincd.condEight, mainud.finalconditionOrderEight,  mainud.finalconditionIntensityEight,  mainud.finalconditionGambEight, mainud.finalconditionTimeTEight))
			yield data.getvalue()
			data.seek(0)
			data.truncate(0)
	# add a filename
	headers = Headers()
	headers.set('Content-Disposition', 'attachment', filename= str(username) + '.csv')
	return Response(
        	stream_with_context(generate()),
        	mimetype='text/csv', headers=headers
    		)
    		
#Generate Metadata CSV Code
@gdpr.route('/<titleid>/<username>/<firstname>/<lastname>/meta/export', methods=['GET','POST'])
@gdpr.route('/<titleid>/<username>/<firstname>/meta/export', methods=['GET','POST'])
@gdpr.route('/<titleid>/<username>/meta/export', methods=['GET','POST'])
def gdprcsv_meta_export(titleid, username,firstname=None,lastname=None):
	UMD = UserMetaData.select().where(UserMetaData.titleid == titleid, UserMetaData.userid == username)
	def generate():
		data = StringIO()
		w = csv.writer(data)
		# write header
		w.writerow(("entryid","userid","titleid","gambleid","currentPage","buttonPress","totalTime","conditionOneTime","conditionTwoTime","conditionThreeTime","conditionFourTime","conditionFiveTime","conditionSixTime","conditionSevenTime","conditionEightTime","conditionOneVideoTime","conditionTwoVideoTime","conditionThreeVideoTime","conditionFourVideoTime","conditionFiveVideoTime","conditionSixVideoTime","conditionSevenVideoTime","conditionEightVideoTime"))
		yield data.getvalue()
		data.seek(0)
		data.truncate(0)

		# write each log item
		for g in UMD.iterator():
			w.writerow((g.entryid,g.userid,g.titleid,g.gambleid,g.currentPage,g.buttonPress,g.totalTime,g.conditionOneTime,g.conditionTwoTime,g.conditionThreeTime,g.conditionFourTime,g.conditionFiveTime,g.conditionSixTime,g.conditionSevenTime,g.conditionEightTime,g.conditionOneVideoTime,g.conditionTwoVideoTime,g.conditionThreeVideoTime,g.conditionFourVideoTime,g.conditionFiveVideoTime,g.conditionSixVideoTime,g.conditionSevenVideoTime,g.conditionEightVideoTime))
			yield data.getvalue()
			data.seek(0)
			data.truncate(0)
	# add a filename
	headers = Headers()
	headers.set('Content-Disposition', 'attachment', filename= str(username) + '_metadata.csv')
	return Response(
        	stream_with_context(generate()),
        	mimetype='text/csv', headers=headers
    		)
    		

