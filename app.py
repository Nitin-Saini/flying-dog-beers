import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import seaborn as sns
import numpy as np
import requests
import geopandas as gpd
import plotly.graph_objects as go

########### Define your variables
myheading='Covid19Dashboard'

mytitle='Total and New Cases in Top 10 Countries'
tabtitle='Covid19'


githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

url = 'https://www.worldometers.info/coronavirus/#countries'
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
r = requests.get(url, headers=header)
corona = pd.read_html(r.text)[1]
corona.fillna(0, inplace=True)
corona['CountryCode'] = corona['Country,Other'].str[:3].str.upper() 
# Taking top 10 affected countries due to coronavirus
corona_data = corona.sort_values(by=['TotalCases'], ascending=False).iloc[1:11, :]

if corona_data.NewCases.dtype != 'int64':
    # corona_data.NewCases = corona_data.NewCases.map(lambda x: x.lstrip('+'))
    corona_data.NewCases = corona_data.NewCases.replace(',','', regex=True).astype('int')

if corona_data.TotalCases.dtype != 'int64':
    corona_data.TotalCases = corona_data.TotalCases.replace(',','', regex=True).astype('int')

if corona_data.TotalDeaths.dtype != 'int64':
    corona_data.TotalDeaths = corona_data.TotalDeaths.replace(',','', regex=True).astype('int')

if corona_data.NewDeaths.dtype != 'int64':
    # corona_data.NewDeaths = corona_data.NewDeaths.map(lambda x: x.lstrip('+'))
    corona_data.NewDeaths = corona_data.NewDeaths.replace(',','', regex=True).astype('int')

if corona_data.TotalRecovered.dtype != 'int64':
    corona_data.TotalRecovered = corona_data.TotalRecovered.replace(',','', regex=True).astype('int')

########## Set up the chart

color1='orange'
totalCases = go.Bar(
    x=corona_data['Country,Other'],
    y=corona_data.TotalCases,
    name='Total Cases',
    marker={'color':color1}
)
color2='red'
newCases = go.Bar(
    x=corona_data['Country,Other'],
    y=corona_data.NewCases,
    name='New Cases',
    marker={'color':color2}
)

covidData1 = [totalCases, newCases]

covidLayout1 = go.Layout(
    barmode='group',
    title = mytitle
)

color1='orange'
newDeaths = go.Bar(
    x=corona_data['Country,Other'],
    y=corona_data.TotalCases,
    name='Total Cases',
    marker={'color':color1}
)

covidData2 = [newDeaths]

covidLayout2 = go.Layout(
    barmode='group',
    title = mytitle
)

covid_fig1 = go.Figure(data=covidData1, layout=covidLayout1)
covid_fig2 = go.Figure(data=covidData2, layout=covidLayout2)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(
    children=
    [
        html.H1(myheading,
                style={
                'textAlign': 'center'
                }
            ),
        html.Div(
            dcc.Graph(
                id='flyingdog',
                figure=covid_fig1
            ),
            style={
            'textAlign': 'center',
            'width': '50%',
            'float': 'left',
            'display': 'inline-block'
            }
        ),
        html.Div(
            dcc.Graph(
                id='flyingdog1',
                figure=covid_fig2
            ),
            style={
            'textAlign': 'center',
            'width': '50%',
            'float': 'left',
            'display': 'inline-block'
            }
        ),
        html.A('Code on Github', href=githublink),
        html.Br(),
        html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()
