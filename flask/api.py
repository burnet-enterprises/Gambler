#!/usr/local/bin/ python3

#################################################################################
#																				#
#																				#
#																				#
#																				#
#								API Functions									#
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

api = Blueprint('api', 'api', url_prefix='/api')

@api.route('/userdata/retrieve/userdata',methods=['POST'])
#Retrive User Information needs project and user info
def retrieveprojectuserapi():
	"""API Route that retrive a user's data.  POST JSON request must require 'project' and 'user' data. """
	if not request.json:
		abort(400)
	infoj = request.json
	if (db.is_closed()==False):
		db.close()
	db.connect()
	try:
		GamUI = UserInfo.get(UserInfo.titleid == infoj['project'], UserInfo.userid == infoj['user'])
		data = {
		'firstname':GamUI.firstname,
		'lastname':GamUI.lastname,
		'age':GamUI.age,
		'hld':GamUI.hld,
		'gender':GamUI.gender,
		'race':GamUI.race,
		'finalconditionIntensityOne':GamUI.finalconditionIntensityOne,
		'finalconditionIntensityTwo':GamUI.finalconditionIntensityTwo,
		'finalconditionIntensityThree':GamUI.finalconditionIntensityThree,
		'finalconditionIntensityFour':GamUI.finalconditionIntensityFour,
		'finalconditionIntensityFive':GamUI.finalconditionIntensityFive,
		'finalconditionIntensitySix':GamUI.finalconditionIntensitySix,
		'finalconditionIntensitySeven':GamUI.finalconditionIntensitySeven,
		'finalconditionIntensityEight':GamUI.finalconditionIntensityEight,
		'finalconditionTimeTOne':GamUI.finalconditionTimeTOne,
		'finalconditionTimeTTwo':GamUI.finalconditionTimeTTwo,
		'finalconditionTimeTThree':GamUI.finalconditionTimeTThree,
		'finalconditionTimeTFour':GamUI.finalconditionTimeTFour,
		'finalconditionTimeTFive':GamUI.finalconditionTimeTFive,
		'finalconditionTimeTSix':GamUI.finalconditionTimeTSix,
		'finalconditionTimeTSeven':GamUI.finalconditionTimeTSeven,
		'finalconditionTimeTEight':GamUI.finalconditionTimeTEight,
		'finalconditionGambOne':GamUI.finalconditionGambOne,
		'finalconditionGambTwo':GamUI.finalconditionGambTwo,
		'finalconditionGambThree':GamUI.finalconditionGambThree,
		'finalconditionGambFour':GamUI.finalconditionGambFour,
		'finalconditionGambFive':GamUI.finalconditionGambFive,
		'finalconditionGambSix':GamUI.finalconditionGambSix,
		'finalconditionGambSeven':GamUI.finalconditionGambSeven,
		'finalconditionGambEight':GamUI.finalconditionGambEight,
		'finalconditionOrderOne':GamUI.finalconditionOrderOne,
		'finalconditionOrderTwo':GamUI.finalconditionOrderTwo,
		'finalconditionOrderThree':GamUI.finalconditionOrderThree,
		'finalconditionOrderFour':GamUI.finalconditionOrderFour,
		'finalconditionOrderFive':GamUI.finalconditionOrderFive,
		'finalconditionOrderSix':GamUI.finalconditionOrderSix,
		'finalconditionOrderSeven':GamUI.finalconditionOrderSeven,
		'finalconditionOrderEight':GamUI.finalconditionOrderEight
		}
	except UserInfo.DoesNotExist:
		data = {'result':'DoesNotExist'}
	db.close()
	return jsonify(data)
	

@api.route('/userdata/retrieve/lastuser',methods=['POST'])
#Retrieve User Information needs Proejct info
def retrieveprojectlastuserapi():
	"""API Route that retrive the last user's data based on the project.  POST JSON request must require 'project' and  """
	if not request.json:
		abort(400)
	infoj = request.json
	if (db.is_closed()==False):
		db.close()
	db.connect()
	try:
		GamUI = UserInfo.select().where(UserInfo.titleid == infoj['project']).order_by(UserInfo.uid.desc()).get()
		data = {
		'uid': GamUI.uid,
		'firstname':GamUI.firstname,
		'lastname':GamUI.lastname,
		'age':GamUI.age,
		'hld':GamUI.hld,
		'gender':GamUI.gender,
		'race':GamUI.race,
		'userid':GamUI.userid,
		'finalconditionIntensityOne':GamUI.finalconditionIntensityOne,
		'finalconditionIntensityTwo':GamUI.finalconditionIntensityTwo,
		'finalconditionIntensityThree':GamUI.finalconditionIntensityThree,
		'finalconditionIntensityFour':GamUI.finalconditionIntensityFour,
		'finalconditionIntensityFive':GamUI.finalconditionIntensityFive,
		'finalconditionIntensitySix':GamUI.finalconditionIntensitySix,
		'finalconditionIntensitySeven':GamUI.finalconditionIntensitySeven,
		'finalconditionIntensityEight':GamUI.finalconditionIntensityEight,
		'finalconditionTimeTOne':GamUI.finalconditionTimeTOne,
		'finalconditionTimeTTwo':GamUI.finalconditionTimeTTwo,
		'finalconditionTimeTThree':GamUI.finalconditionTimeTThree,
		'finalconditionTimeTFour':GamUI.finalconditionTimeTFour,
		'finalconditionTimeTFive':GamUI.finalconditionTimeTFive,
		'finalconditionTimeTSix':GamUI.finalconditionTimeTSix,
		'finalconditionTimeTSeven':GamUI.finalconditionTimeTSeven,
		'finalconditionTimeTEight':GamUI.finalconditionTimeTEight,
		'finalconditionGambOne':GamUI.finalconditionGambOne,
		'finalconditionGambTwo':GamUI.finalconditionGambTwo,
		'finalconditionGambThree':GamUI.finalconditionGambThree,
		'finalconditionGambFour':GamUI.finalconditionGambFour,
		'finalconditionGambFive':GamUI.finalconditionGambFive,
		'finalconditionGambSix':GamUI.finalconditionGambSix,
		'finalconditionGambSeven':GamUI.finalconditionGambSeven,
		'finalconditionGambEight':GamUI.finalconditionGambEight,
		'finalconditionOrderOne':GamUI.finalconditionOrderOne,
		'finalconditionOrderTwo':GamUI.finalconditionOrderTwo,
		'finalconditionOrderThree':GamUI.finalconditionOrderThree,
		'finalconditionOrderFour':GamUI.finalconditionOrderFour,
		'finalconditionOrderFive':GamUI.finalconditionOrderFive,
		'finalconditionOrderSix':GamUI.finalconditionOrderSix,
		'finalconditionOrderSeven':GamUI.finalconditionOrderSeven,
		'finalconditionOrderEight':GamUI.finalconditionOrderEight
		}
	except UserInfo.DoesNotExist:
		data = {'result':'DoesNotExist'}
	db.close()

	return jsonify(data)

@api.route('/userdata/retrieve/project',methods=['POST'])
#Retrieve Project Information needs Project info
def retrieveprojectinfoapi():
	"""API Route that retrive a project's data.  POST JSON must require 'project' and 'user' """
	if not request.json:
		abort(400)
	infoj = request.json
	if (db.is_closed()==False):
		db.close()
	db.connect()
	try:
		GamScen = GamblerInfo.get(GamblerInfo.titleid==infoj['project'])
		data = {
		"mechgamb": GamScen.mechgamb,
		"condOne": GamScen.conditionOne,
		"condTwo": GamScen.conditionTwo,
		"condThree": GamScen.conditionThree,
		"condFour": GamScen.conditionFour,
		"condFive": GamScen.conditionFive,
		"condSix": GamScen.conditionSix,
		"condSeven": GamScen.conditionSeven,
		"condEight": GamScen.conditionEight,
		"condOneImage": GamScen.imageOnename,
		"condTwoImage": GamScen.imageTwoname,
		"condThreeImage": GamScen.imageThreename,
		"condFourImage": GamScen.imageFourname,
		"condFiveImage": GamScen.imageFivename,
		"condSixImage": GamScen.imageSixname,
		"condSevenImage": GamScen.imageSevenname,
		"condEightImage": GamScen.imageEightname		
		}
	except GamblerInfo.DoesNotExist:
		data = {"error":"No project exists"}
	db.close()
	return jsonify(data)

@api.route('/userdata/delete/userdata',methods=['POST'])
#Retrive User Information needs project and user info
def deleteprojectuserapi():
	"""API Route that deletes a user's data.  POST JSON must require 'project' and 'user' """
	if not request.json:
		abort(400)
	infoj = request.json
	if (db.is_closed()==False):
		db.close()
	db.connect()
	GamUI = UserMetaData.delete().where(UserMetaData.titleid == infoj['project'], UserMetaData.userid == infoj['user']).execute()
	GamUI = UserInfo.delete().where(UserInfo.titleid == infoj['project'], UserInfo.userid == infoj['user']).execute()
	db.close()
	return jsonify({'result':'success'})

@api.route('/live/projectposition/', methods=['POST'])
@api.route('/live/projectposition', methods=['POST'])
def liveuser():
	"""API Route that deletes a user's data.  POST JSON must require 'project' and 'user' """
	if not request.json:
		abort(400)
	infoj = request.json
	if (db.is_closed()==False):
		db.close()
	db.connect()
	if 'project' not in infoj:
		return jsonify({"error":"No project data is in the request"})
	try:
		GamScen = GamblerInfo.select().where(GamblerInfo.titleid==infoj['project'])
	except GamblerInfo.DoesNotExist:
		return jsonify({"error":"No project exists"})
	if 'user' not in infoj:
		GamUI = UserMetaData.select().where(UserMetaData.titleid == infoj['project']).order_by(UserMetaData.entryid.desc()).get()
	else:
		GamUI = UserMetaData.get(UserMetaData.titleid == infoj['project'], UserMetaData.userid == infoj['user'])
	data = { ##Note you can't assume that utility is done because of going back but it's an okay estimation.
	'userid':GamUI.userid,
	'titleid':GamUI.titleid,
	'currentPage': GamUI.currentPage,
	}
	return jsonify(data)
