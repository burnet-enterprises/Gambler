from flask import Flask, flash, render_template, redirect, url_for, session, request, send_from_directory, abort
from flask import Response, Blueprint
from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import WSGIRequestHandler
import datetime



class ScriptNameHandler(WSGIRequestHandler):
	"""Script handler for allowing The Gambler to be deployable anywhere."""

	def make_environ(self):
		environ = super().make_environ()
		script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
		path_info = environ['PATH_INFO']
		if script_name:
			environ['SCRIPT_NAME'] = script_name
			path_info = environ['PATH_INFO']
		if path_info.startswith(script_name):
			environ['PATH_INFO'] = path_info[len(script_name):]
		scheme = environ.get('HTTP_X_SCHEME', '')
		if scheme:
			environ['wsgi.url_scheme'] = scheme
		return environ

class PrefixMiddleware(object):
	"""Middleware prefix for allowing The Gambler to be deployable anywhere."""

	def __init__(self, app, prefix=''):
		self.app = app
		self.prefix = prefix

	def __call__(self, environ, start_response):

		if environ['PATH_INFO'].startswith(self.prefix):
			environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
			environ['SCRIPT_NAME'] = self.prefix
			return self.app(environ, start_response)
		else:
			start_response('404', [('Content-Type', 'text/plain')])
			return ["This url does not belong to the app.".encode()]

class ReverseProxied(object):
	"""Reverse proxy for allowing The Gambler to be deployable anywhere."""

	def __init__(self, app, script_name=None, scheme=None, server=None):
		self.app = app
		self.script_name = script_name
		self.scheme = scheme
		self.server = server

	def __call__(self, environ, start_response):
		script_name = environ.get('HTTP_X_SCRIPT_NAME', '') or self.script_name
		if script_name:
			environ['SCRIPT_NAME'] = script_name
			path_info = environ['PATH_INFO']
			if path_info.startswith(script_name):
				environ['PATH_INFO'] = path_info[len(script_name):]
		scheme = environ.get('HTTP_X_SCHEME', '') or self.scheme
		if scheme:
			environ['wsgi.url_scheme'] = scheme
		server = environ.get('HTTP_X_FORWARDED_SERVER', '') or self.server
		if server:
			environ['HTTP_HOST'] = server
		return self.app(environ, start_response)
