import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import numpy as np
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

patients=pd.read_csv('IndividualDetails.csv')
print(patients)
# pbar=patients['State'].value_counts().reset_index()
# print(pbar)
# print(patients["current_status"].value_counts())
total=patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status']=='Deceased'].shape[0]

options=[
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased','value':'Deceased'}
]

app=dash.Dash(__name__,external_stylesheets = external_stylesheets )
server=app.server

app.layout=html.Div([
    html.H1("Covid-19 Pandemic", style={'color': '#fff', 'text-align': 'center', 'fontSize': 40}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases",style={'color': '#000','fontSize': 25}),
                    html.H4(total,style={'color': '#000','fontSize': 22})]
                    ,className='card-body')
            ],className='card bg-danger')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Active",style={'color': '#000','fontSize': 25}),
                        html.H4(active,style={'color': '#000','fontSize': 22})]
                        ,className='card-body')
                ],className='card bg-info')
            ],className='card')],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Recovered",style={'color': '#000','fontSize': 25}),
                        html.H4(recovered,style={'color': '#000','fontSize': 22})]
                        ,className='card-body')
                ],className='card bg-warning')
            ],className='card')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Deaths",style={'color': '#000','fontSize': 25}),
                        html.H4(deaths,style={'color': '#000','fontSize': 22})]
                        ,className='card-body')
                ],className='card bg-success')
            ],className='card')
        ],className='col-md-3')
    ],className='row'),
    html.Div([
        html.Div([],className='col-md-6'),
        html.Div([],className='col-md-6'),
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options,value='All',style={'font-family': 'Arial, sans-serif',
                                                                                'font-size': '16px'}),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12'),
    ],className='row'),
],className='container')

#Based on user we want to display the graph.So do this way:
@app.callback(Output('bar','figure'),[Input('picker','value')])
def update_graph(type):
    if type=='All':
        pbar=patients['State'].value_counts().reset_index()
        return {'data':[go.Bar(x=pbar['State'],y=pbar['count'])],
            'layout':go.Layout(title='State Total Count')}
    else:
        npat = patients[patients['current_status'] == type]
        pbar = npat['State'].value_counts().reset_index()
        return {'data': [go.Bar(x=pbar['State'], y=pbar['count'])],
                'layout': go.Layout(title='State Total Count')}


if __name__=='__main__':
    app.run_server(debug=True)