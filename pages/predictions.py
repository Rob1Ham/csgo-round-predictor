import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from app import app

from joblib import load
pipeline = load('assets/pipeline.joblib')
static_image_route = 'assets/'
map_extension = '.png'

column1 = dbc.Col(
    [dcc.Markdown('## Predictions', className='mb-200',style = {'margin-bottom': '3em'}), 
        dcc.Markdown('#### Counter Terrorist Gear Value',style = {'margin-bottom': '3em'}), 
        dcc.Slider(
            id='equipment_value_team_ct', 
            min=1000, 
            max=35000, 
            step=500, 
            value=20100, 
            marks={n: str(n) for n in range(1000,35000,7500)}, 
            className='mb-200', 
        ),
        dcc.Markdown('#### Terrorist Gear Value',style = {'margin-top': '3em'}),
        dcc.Slider(
            id='equipment_value_team_t', 
            min=1000, 
            max=35000, 
            step=5, 
            value=20100, 
            marks={n: str(n) for n in range(1000,35000,7500)}, 
            className='mt-200', 
        ), 

        dcc.Markdown('#### Map', style = {'margin-top': '3em'}),
        dcc.Dropdown(
            id='map_name', 
            options = [
                {'label': 'Dust2', 'value': 'de_dust2'}, 
                {'label': 'Inferno', 'value': 'de_inferno'}, 
                {'label': 'Mirage', 'value': 'de_mirage'}, 
                {'label': 'Train', 'value': 'de_train'}, 
                {'label': 'Overpass', 'value': 'de_overpass'}, 
                {'label': 'Nuke', 'value': 'de_nuke'}, 
            ], 
            value = 'de_dust2', 
            className='mb-105', 
        ),
        dcc.Markdown('#### Terrorist Series Score', style = {'margin-top': '3em'}), 
        dcc.Slider(
            id='t_score_LR', 
            min=0, 
            max=30, 
            step=1, 
            value=5, 
            marks={n: str(n) for n in range(0,31,5)}, 
            className='mb-10', 
        ),
        dcc.Markdown('#### Counter Terrorist Series Score', style = {'margin-top': '3em'}),
        dcc.Slider(
            id='ct_score_LR', 
            min=0, 
            max=30, 
            step=1, 
            value=5, 
            marks={n: str(n) for n in range(0,31,5)}, 
            className='mb-10', 
        ),
        dcc.Markdown('#### Starting Round:', style = {'margin-top': '3em'}),
        html.Div(id='round_count', style={'fontWeight':'bold'}),   
    ],
    md=5,
)

column2 = dbc.Col(
    [
        html.Img(id='image', style={'textAlign': 'center'}),
        html.Div(id='prediction-content', style={'fontWeight':'bold'}),
        html.Img(id='player-pic', style={'textAlign': 'center'}),
    ],
    md=7
)

layout = dbc.Row([column1, column2])


@app.callback(
    Output('map-pic', 'src'),
    [Input('map_name', 'value')])
def update_image_src(value):
    return static_image_route + value + map_extension

@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('map_name', 'value')])
def update_image_src2(value):
    return static_image_route + value + map_extension



@app.callback(
    Output('round_count', 'children'),
    [   Input('t_score_LR', 'value'),
        Input('ct_score_LR', 'value')]
    )
def roundcount(ct_score_LR,t_score_LR):
    total_rounds = (ct_score_LR + t_score_LR + 1)
    return total_rounds

@app.callback(
        Output('prediction-content', 'children'),
        [   Input('round_count', 'children'),
            Input('equipment_value_team_t', 'value'),
            Input('equipment_value_team_ct', 'value'),
            Input('ct_score_LR', 'value'),
            Input('t_score_LR', 'value'),
            Input('map_name', 'value')]
          )

def predict(round, equipment_value_team_t, equipment_value_team_ct,ct_score_LR,t_score_LR,map_name):
    df = pd.DataFrame(
        columns=['round', 'equipment_value_team_t', 'equipment_value_team_ct',
       'ct_score_LR', 't_score_LR', 'map_name'], 
        data=[[round, equipment_value_team_t, equipment_value_team_ct,ct_score_LR,t_score_LR,map_name]]
    )
    pipeline = load('assets/pipeline.joblib')
    y_pred = pipeline.predict(df)[0]
    if y_pred == 1:
        message = "Terrorists win"
        y_pred_proba = pipeline.predict_proba(df)[:,1][0]
        y_pred_proba = y_pred_proba * 100
    else:
        message = "Counter Terrorists win"
        y_pred_proba = pipeline.predict_proba(df)[:,0][0]
        y_pred_proba = y_pred_proba * 100

    return f'{message:}! With a predicted probability of: {y_pred_proba:0.2f}%'

@app.callback(
        Output('player-pic', 'src'),
        [   Input('round_count', 'children'),
            Input('equipment_value_team_t', 'value'),
            Input('equipment_value_team_ct', 'value'),
            Input('ct_score_LR', 'value'),
            Input('t_score_LR', 'value'),
            Input('map_name', 'value')]
          )

def predict1(round, equipment_value_team_t, equipment_value_team_ct,ct_score_LR,t_score_LR,map_name):
    df = pd.DataFrame(
        columns=['round', 'equipment_value_team_t', 'equipment_value_team_ct',
       'ct_score_LR', 't_score_LR', 'map_name'], 
        data=[[round, equipment_value_team_t, equipment_value_team_ct,ct_score_LR,t_score_LR,map_name]]
    )
    pipeline = load('assets/pipeline.joblib')
    y_pred = pipeline.predict(df)[0]
    y_pred = y_pred.astype(int)
    if y_pred == 1:
        imgpath = static_image_route + 't_win.png'
    else:
        imgpath = static_image_route + 'ct_win.png'
    return imgpath