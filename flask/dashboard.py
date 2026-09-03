#Libraries 
import json, errno, os
import flask
from flask import *
import csv
try:
	from StringIO import StringIO #Python2->3
except ImportError:
	from io import StringIO
from werkzeug.utils import secure_filename
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
#Packages defined by AJ Adejare
from UserData import *
from GamblerSetup import *
from ConditionInfo import *
import dash
from dash.dependencies import Input, Output
import plotly.express as px
from dash import dcc
from dash import html as dhtml
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from playhouse.shortcuts import model_to_dict, dict_to_model
#from flask_login import *
pd.options.plotting.backend = "plotly"
#Remember, if editing from non CHI-Computer, remove login header redirect (i.e. sso-email)

#Variables for analysis
utility=["finalconditionIntensityOne","finalconditionIntensityTwo","finalconditionIntensityThree","finalconditionIntensityFour","finalconditionIntensityFive","finalconditionIntensitySix","finalconditionIntensitySeven","finalconditionIntensityEight","finalconditionGambOne","finalconditionGambTwo","finalconditionGambThree","finalconditionGambFour","finalconditionGambFive","finalconditionGambSix","finalconditionGambSeven","finalconditionGambEight","finalconditionTimeTOne","finalconditionTimeTTwo","finalconditionTimeTThree","finalconditionTimeTFour","finalconditionTimeTFive","finalconditionTimeTSix","finalconditionTimeTSeven","finalconditionTimeTEight"]
xaxis=["age","finalconditionIntensityOne","finalconditionIntensityTwo","finalconditionIntensityThree","finalconditionIntensityFour","finalconditionIntensityFive","finalconditionIntensitySix","finalconditionIntensitySeven","finalconditionIntensityEight","finalconditionGambOne","finalconditionGambTwo","finalconditionGambThree","finalconditionGambFour","finalconditionGambFive","finalconditionGambSix","finalconditionGambSeven","finalconditionGambEight","finalconditionTimeTOne","finalconditionTimeTTwo","finalconditionTimeTThree","finalconditionTimeTFour","finalconditionTimeTFive","finalconditionTimeTSix","finalconditionTimeTSeven","finalconditionTimeTEight"]
gender={'F':'Female','M':'Male','O':'Non-binary/Other'}
race={'blk':'African/Black American','asn':'Asian','hpi':'Hawaiian/Pacific Islander','nam':'Native/Alsaka American','mna':'Middle Eastern/North African','wht':'White'}
datacl = ["finalconditionIntensityTwo"]
demolist = ['gender','race']
gambler_data = pd.DataFrame()
if (db.is_closed()==False):
		db.close()
db.connect()
GambleLoader = GamblerInfo()
GamblerList = GambleLoader.select(GamblerInfo.titleid, GamblerInfo.otitleid) #Otitle means offical title
GamblerListDisplay = [(c.titleid, c.otitleid) for c in GamblerList]
gamblerprojectslist =[{'label': c.otitleid, 'value': c.titleid} for c in GamblerList]
gamblerprojectslist.append({'label': 'None selected', 'value':'empty'})
db.close()
emptyplot= {
	"layout": {
		"xaxis": {
			"visible": False
		},
		"yaxis": {
			"visible": False
		},
		"annotations": [
			{
				"text": "No data selected.  Please select a datapoint for a graph",
				"xref": "paper",
				"yref": "paper",
				"showarrow": False,
				"font": {
					"size": 28
				}
			}
		]
	}
}

def create_dashboard(server):
		"""Create a Plotly Dash dashboard."""
		dashapp = dash.Dash(__name__, server=server,
				url_base_pathname='/admin/dashboard/',
				external_stylesheets=[dbc.themes.BOOTSTRAP],
#			   static='/gambler/static',
#			   assets_folder= "/admin/dashboard/assets/",
#			   serve_locally = False
		)
#DAsh does not know how to serve files based upon how Flask is mounted, so you got to do the full URL
#This is how I got the inspiration for the modificaitons
# 
# 		dashapp.config.update({
# 				"routes_pathname_prefix": '/gambler/admin/dashboard/',
# 				'requests_pathname_prefix': '/gambler/admin/dashboard/'
# 				})
#	   dashapp.config.supress_callback_exceptions = True
		# Create Dash Layout
		dashapp.layout = dhtml.Div(children=[
		dhtml.Nav(className = "nav nav-pills", children=[
        dhtml.A('Home', className="nav-item nav-link btn", href='/'),
        dhtml.A('About', className="nav-item nav-link active btn", href='/about'),
        dhtml.A('Documentation', className="nav-item nav-link active btn", href='/docs/'),
        dhtml.A('Contact', className="nav-item nav-link active btn", href='/contact/'),
        dhtml.A('Language', className="nav-item nav-link active btn", href='/language'),
        dhtml.A('Disclaimer', className="nav-item nav-link active btn", href='/disclaimer'),
        dhtml.A('Admin', className="nav-item nav-link active btn", href='/admin') 
        
			]),
				dhtml.H1('Gambler Utility Dashboard'),
				dhtml.H2(id='projectname', children=""),
				dhtml.Br(),
				dhtml.Br(),
				dcc.Store(id='dataframe'),
				dcc.Dropdown(
										id='project',
										options=gamblerprojectslist,
										value="empty"
								),
				dcc.Tabs(id='dashtabs', value='tab-1', children=[
						dcc.Tab(label='Age Utility analysis', value='tab-1', children=[
								dbc.Row([ dbc.Col(dhtml.Div([dhtml.P('X-axis value'),
										dcc.Dropdown(
																id='xlabel',
																options=[{'label': i, 'value': i} for i in xaxis],
																value="age"
														)]),width={"size": 3, "offset": 1}),
										dbc.Col(dhtml.Div([dhtml.P('Y-axis values'),
										dcc.Dropdown(
																id='columnlabels',
																options=[{'label': i, 'value': i} for i in utility],
																multi=True,
														)]))
										]),
								dhtml.Div(dcc.Dropdown(
														id='trendline',
														options=[{'label': 'None', 'value': "Empty"},{'label': 'Ordinary least squares', 'value': "ols"},
														{'label': 'Locally Weighted Scatterplot Smoothing', 'value': "lowess"},],
														value='Empty'
												)),
										dcc.Graph(id='example',figure=emptyplot, animate=False)
								]),
						dcc.Tab(label='Demographics', value='tab-2', children=[
								dcc.Checklist(id='subgroup',options=[{'label': 'Subgroup analysis count', 'value': 'yes'}]),
								dhtml.P("Note: Values less than 5 have been filter out."),
								dcc.Graph(id='example2',figure=emptyplot, animate=True)
								]
						),
				]),

				dcc.Interval( #How to trigger event
						id='graph-update',
						interval=1000, #in miliseconds 
						n_intervals = 0
						)

		])
		init_callbacks(dashapp)
#	   dashapp.wsgi_app = ReverseProxied(app=dashapp,script_name='/admin/dashboard/', server=dashapp.server)

		return dashapp.server
		
def init_callbacks(dashapp):
	@dashapp.callback(
		[Output('projectname', 'children'),Output('dataframe', 'data')],
		[Input(component_id='project', component_property='value')]
	)	
	def projectload(project):
		if (db.is_closed()==False):
				db.close()
		db.connect()
		if project == 'empty':
			return (" ",None)
		gamblertitle = GambleLoader.get(GamblerInfo.titleid==project)
#		query = UserInfo.get(UserInfo.titleid == project)
		query = UserInfo.select().where(UserInfo.titleid == project)
		gambler_data = pd.DataFrame(query.dicts())
		holddata = gambler_data.to_json()
		db.close()
		return (gamblertitle.otitleid,holddata)
	@dashapp.callback(
		Output('example', 'figure'),
		[Input(component_id='xlabel', component_property='value'),Input(component_id='columnlabels', component_property='value'),Input(component_id='trendline', component_property='value'), Input('graph-update', 'n_intervals'),Input('dataframe', 'data')]
	)	
	def label_data_y(input_x,input_labels,input_trend,n,dataframe):
		if dataframe == None:
			return (emptyplot)
		gambler_data = pd.read_json(dataframe)
		trendline = None
		if input_trend != "Empty":
			trendline=input_trend
		if input_labels:
			plot = gambler_data.plot.scatter(x=input_x,y=input_labels,trendline=trendline, labels=dict(index="Age", value="Utility"),title="Health Utility Graph")
			plot.update_xaxes(range=[-5,105])
			plot.update_yaxes(range=[-5,105])
			return plot
		else:
			return (emptyplot)

	@dashapp.callback(
		Output('example2', 'figure'),
		[Input(component_id='subgroup', component_property='value'),Input('dataframe', 'data')]
	)	
	def label_data_groups(subgroup,dataframe):
		print(subgroup)
		if dataframe == None:
			return (emptyplot)
		gambler_data = pd.read_json(dataframe)
		gambler_data['race'] = gambler_data['race'].map(race)
		gambler_data['gender'] = gambler_data['gender'].map(gender)
	##Filter identifiable data 
		if subgroup:
			newdf = pd.DataFrame(columns=["Race-Gender","Count"])
			newdf["Race-Gender"] = gambler_data['race'] + "-" + gambler_data['gender']
			newdf['Count'] = gambler_data.groupby(demolist)['race'].transform('count')
			df = newdf[newdf['Count'] > 5]
			return px.histogram(df, x="Race-Gender",title="Counts")
		else:
			df = gambler_data.groupby('race').filter(lambda x: len(x) >= 5)
			df  = df.groupby('gender').filter(lambda x: len(x) >= 5)
			return px.histogram(df, x=demolist,title="Counts")
 
