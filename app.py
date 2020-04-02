import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import seaborn as sns
import numpy as np
import requests
import geopandas as gpd
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

########### Define your variables
myheading='Covid19 Data Visualisation Challenge'
apptitle='Covid19-Dashboard'
linkedin_link='https://www.linkedin.com/groups/10541367/'
notebook_link='https://colab.research.google.com/drive/1MiFntcWHOJcfb3G0_vMzX_tEVUpFRdly#scrollTo=Q4LF2ZvEp0Qk'

#data for first 2 charts
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

# Set up the chart first 2 charts
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

chartData1 = [totalCases, newCases]
chartLayout1 = go.Layout(
    barmode='group',
    title = 'Total and New Cases in Top 10 Countries'
)

color3='black'
newDeaths = go.Bar(
    x=corona_data['Country,Other'],
    y=corona_data.TotalDeaths,
    name='Total Cases',
    marker={'color':color3}
)

chartData2 = [newDeaths]
chartLayout2 = go.Layout(
    barmode='group',
    title = 'Total Deaths in Top 10 Countries'
)

covid_fig1 = go.Figure(data=chartData1, layout=chartLayout1)
covid_fig2 = go.Figure(data=chartData2, layout=chartLayout2)


# setting up 3rd chart by Luca Chuang
url = 'https://www.worldometers.info/coronavirus/country/us/'
r = requests.get(url, headers=header)
corona_data = pd.read_html(r.text)[1]
corona_data = corona_data.fillna(0)
corona_data = corona_data.sort_values(by=['TotalCases'], ascending=False).iloc[1:, :]
x = ["Diamond Princess Cruise","Wuhan Repatriated","Puerto Rico",
     "Alaska","Guam", "Northern Mariana Islands","United States Virgin Islands",
     "Hawaii", "District Of Columbia"]
us_data = corona_data[~corona_data['USAState'].isin(x)]
us_data = us_data.rename(columns={'USAState': 'State'})

df = pd.read_csv('https://raw.githubusercontent.com/jasperdebie/VisInfo/master/us-state-capitals.csv')
df = df.drop("description", axis=1)
x = ['Alaska', 'Hawaii']
df = df[~df['name'].isin(x)]
df = df.rename(columns= {"name":"State"})

bubble_data = df.merge(us_data, on="State")
bubble_data['text'] = bubble_data['State'] + '<br>TotalCases:' + (bubble_data['TotalCases']).astype(str)
bubble_data = bubble_data.sort_values(by = ["TotalCases"], ascending=False)

total_link = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/who_covid_19_situation_reports/who_covid_19_sit_rep_time_series/who_covid_19_sit_rep_time_series.csv'
total_file = pd.read_csv(total_link)
total_case = pd.DataFrame(total_file.iloc[0,:])
total_case = total_case.iloc[3:,:]
total_case = total_case.reset_index()
total_case = total_case.rename(columns={"index": "Date", 0:"Total_Case"})
total_case['Date']= pd.to_datetime(total_case['Date'])

limits = [(0,1),(2,10),(11,20),(21,30),(31,48)] # Ranking
colors = ["maroon","red","orange","grey","lightgrey"]
names = ["Top 1", "Top 10", "11~20","21~30","30~48"]
scale = 30

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
        title_text = 'Confirmed Cases in the US',
        showlegend = True,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)'))

# Setting up chart 4 by Smridhi Mangla
#download confirmed cases data from JHU dashboard
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
df_confirmed = pd.read_csv(url)

#top ten impacted countries 
df_tmp_subset = df_confirmed.drop(['Province/State','Lat','Long'],axis=1)
df_tmp_subset = pd.DataFrame(df_tmp_subset.groupby(['Country/Region'],as_index=False).sum())
df_tmp_subset = df_tmp_subset.sort_values(by=df_confirmed.columns[len(df_confirmed.columns)-1], ascending=False)
df_topten_countries = df_tmp_subset[0:10]

x_axis = df_topten_countries.columns
covid_fig4 = go.Figure()
annotations = []

for i in range(0,10,1):
  y = df_topten_countries.iloc[i,1:].values.flatten().tolist()
  covid_fig4.add_trace(go.Scatter(x=x_axis[1:], y=y,
                    mode='lines+markers',
                    name=df_topten_countries.iloc[i,0]))

# Title
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='',
                              font=dict(family='Arial',
                                        size=18,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
covid_fig4.update_layout(annotations=annotations,
    title_text='Confirmed Case Trend of Top Ten Impacted Countries')

#Adding heatmap 
covid19data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
covid19states = pd.DataFrame(covid19data['Country/Region'])
covid19data.drop(covid19data.iloc[:, :-22], axis=1, inplace=True)
covid19data = covid19data.diff(axis=1)
covid19data['total_cases'] = covid19data.sum(axis=1)
covid19data.drop(covid19data.iloc[:, :-22], axis=1, inplace=True)
covid19data = covid19states.merge(covid19data, left_index = True, right_index = True)
covid19data = covid19data.sort_values(by='total_cases', ascending=False)
covid19data.columns = ["Country","D21-7", "D21-6", "D21-5", "D21-4", "D21-3", "D21-2", "D21-1",
                   "D14-7", "D14-6", "D14-5", "D14-4", "D14-3", "D14-2", "D14-1",
                   "D7-7", "D7-6", "D7-5", "D7-4", "D7-3", "D7-2", "D7-1",
                   "total_deaths"]
covid19data['total_deaths'] = covid19data['total_deaths'].astype('object')

for column in covid19data.columns:
  if covid19data[column].dtype == 'float':
    covid19data[column] = covid19data[column].astype('int')

colsLast7 = [('Last7Days', col) for col in covid19data.columns if 'D7-' in col]
colsLast14 = [('Last14Days', col) for col in covid19data.columns if 'D14-' in col]
colsLast21 = [('Last21Days', col) for col in covid19data.columns if 'D21-' in col]
totalStats = [('TotalStats', col) for col in covid19data.columns if 'total' in col]
totalState = [('Countries', col) for col in covid19data.columns if 'Country' in col]
th_props = [
  ('font-size', '12px'),
  ('text-align', 'left'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#f7f7f9')
  ]

# Set CSS properties for td elements in dataframe
td_props = [
  ('font-size', '11px')
  ]
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]

#covid19data.columns = pd.MultiIndex.from_tuples(totalState + colsLast21 + colsLast14 + colsLast7 + totalStats)
#covid19data = covid19data.style.background_gradient(cmap='Reds', axis=1).set_table_styles([{'selector': 'th', 'props': [('font-size', '10pt')]}]).set_table_styles(styles)
#covid_fig5 = ff.create_annotated_heatmap(covid19data.to_dict("rows"))

# Initiating the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=apptitle

# Setting up the layout
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
                id='chart1',
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
                id='chart2',
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
                id='chart3',
                figure=covid_fig3
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
                id='chart4',
                figure=covid_fig4
            ),
            style={
            'textAlign': 'center',
            'width': '50%',
            'float': 'left',
            'display': 'inline-block'
            }
        ),
        # html.Div(
        #     dcc.Graph(
        #         id='chart5',
        #         figure=covid_fig5
        #     ),
        #     style={
        #     'textAlign': 'center',
        #     'width': '50%',
        #     'float': 'left',
        #     'display': 'inline-block'
        #     }
        # ),
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
