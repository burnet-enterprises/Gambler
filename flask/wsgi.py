#!/usr/local/bin python3.7
import sys
import logging
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Flask")
"""Implements the application for deployment"""
try:
	from flask.mainapp import mainapp as application
except:
	from mainapp import mainapp as application
application.secret_key = os.getenv('SECRET_KEY', 'dev')
