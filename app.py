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
myheading='Covid19 Data Visualisation Challenge'

mytitle='Total and New Cases in Top 10 Countries'
tabtitle='Covid19'


linkedin_link='https://www.linkedin.com/groups/10541367/'
notebook_link='https://colab.research.google.com/drive/1MiFntcWHOJcfb3G0_vMzX_tEVUpFRdly#scrollTo=Q4LF2ZvEp0Qk'

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
    y=corona_data.TotalDeaths,
    name='Total Cases',
    marker={'color':color1}
)

covidData2 = [newDeaths]

covidLayout2 = go.Layout(
    barmode='group',
    title = mytitle
)

total_link = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/who_covid_19_situation_reports/who_covid_19_sit_rep_time_series/who_covid_19_sit_rep_time_series.csv'
total_file = pd.read_csv(total_link)
total_case = pd.DataFrame(total_file.iloc[0,:])
total_case = total_case.iloc[3:,:]
total_case = total_case.reset_index()
total_case = total_case.rename(columns={"index": "Date", 0:"Total_Case"})
total_case['Date']= pd.to_datetime(total_case['Date'])

ntdoy_URL = "https://finance.yahoo.com/quote/NTDOY/history?period1=1579564800&period2=1585526400&interval=1d&filter=history&frequency=1d"
ntdoy = pd.read_html(ntdoy_URL)[0]
ntdoy = ntdoy.drop(["Open","High", "Low", "Adj Close**",  "Volume"], axis=1)
ntdoy = ntdoy.iloc[:-1,:]
ntdoy["Date"] = pd.to_datetime(ntdoy['Date'])
ntdoy['Close*']= ntdoy['Close*'].astype("float")
ntdoy = ntdoy.rename(columns={"Close*":"Close"})
ntdoy.sort_values("Date")

limits = [(0,1),(2,10),(11,20),(21,30),(31,48)] # Ranking
colors = ["maroon","red","orange","grey","lightgrey"]
names = ["Top 1", "Top 10", "11~20","21~30","30~48"]
scale = 30

line_plot = total_case.merge(ntdoy, on="Date")
color = 'tab:red'

covid_fig3 = go.Figure()
for i in range(len(limits)):
    lim = limits[i]
    df_sub = bubble_data[lim[0]:lim[1]]
    covid_fig3.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_sub['longitude'],
        lat = df_sub['latitude'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['TotalCases']/scale,
            color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'),
        name = names[i]
        ))

covid_fig3.update_layout(
        width=1000,
        title_text = 'US states Confirmed Cases <br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)'))



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
                'textAlign': 'center',
                'padding': 10
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
        html.Div(
            dcc.Graph(
                id='flyingdog3',
                figure=covid_fig3
            ),
            style={
            'textAlign': 'center',
            'width': '100%',
            'float': 'left',
            'display': 'inline-block'
            }
        ),
        html.Div(
            html.A('Join us on LinkedIn', href=linkedin_link),
            style={
                    'textAlign': 'center'
                }
        ),
        html.Div(
            html.A('Google Colab Notebook', href=notebook_link),
            style={
                    'textAlign': 'center'
                }
        ),
    ]
)

if __name__ == '__main__':
    app.run_server()
