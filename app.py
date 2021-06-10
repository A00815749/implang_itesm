import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import pandas as pd
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import numpy as np
import math
import plotly.graph_objects as go
from matplotlib import cm
from math import log10
from pywaffle import Waffle
from itertools import cycle

app = dash.Dash(__name__, title='Instituto Municipal de Planeación y Gestión Urbana - IMPLANG', external_stylesheets=[dbc.themes.BOOTSTRAP],
				meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])



server = app.server


# Connect to app pages

from apps import home, itesm


#Reading data
#Areas Verdes
av = pd.read_csv('bases/areas_verdes.csv')
#Denue
dn = pd.read_csv('bases/DENUE_2020.csv')
dnk1 = pd.read_csv('bases/DENUEK1.csv')

#Inegi 
ine = pd.read_csv('bases/INEGI_2020.csv')
inek1 = pd.read_csv('bases/INEGIK1.csv')

#Denue y Areas Verdes
denAV = pd.read_csv('bases/DenAV.csv')

#Inegi y Areas Verdes
ineAV = pd.read_csv('bases/inegiAV.csv')

#Color palettes
#Paleta de colores y sus variantes
colors = ['#4478A6', '#519872', '#F2D544', '#F28907', '#F26B6B']
palette = cycle(['#4478A6', '#519872', '#F2D544', '#F28907', '#F26B6B'])
palet = cycle([ '#4478A6', '#519872', '#A69B8F', '#D4A0A7', '#815E5B', '#F2D544', '#F28907', '#F26B6B', '#B57BA6','#54DEFD'])
palettec = cycle(['#4478A6', '#519872', '#F2D544', '#F28907', '#F26B6B', '#54DEFD', '#B57BA6', '#D4A0A7', '#A69B8F', '#815E5B'])

# App Layout

app.layout = dbc.Container([

	dbc.NavbarSimple(
		[

        	dbc.Button('PROYECTOS', href='/apps/proyectos', color='light'),

		],
		brand='IMPLANG',
		brand_href='/apps/home'
	),

	html.Div(id='page-content', children=[]),
	dcc.Location(id='url', refresh=False)

])


@app.callback(Output(component_id='page-content', component_property=
					'children'),
			[Input(component_id='url', component_property='pathname')])

def display_page(pathname):
	if pathname == '/apps/proyectos':
		return itesm.layout
	else:
		return home.layout


if __name__ == '__main__':
	app.run_server(debug=True)


