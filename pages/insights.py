import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Gathering

            I wanted to take a brief aside again to Thank CS:GO Demos Manager and HLTV.org for their contributions to gathering this data.

            Each Match has a JSON between 2-5MB of data, and while most of it was not applicable to my model (because it would result in model leakage), there is a lot more potential for this dataset.

            As a means of paying it forward, I have posted all of the raw data I have gathered to Kaggle.
            
            The highlight JSONs are broken out by Event and Round of the Event the match took place in. There are just over 1,200 matches available to use for analysis. If you use the data for any analysis let me know, I'd love to see it! 
            """
        ),
        dcc.Link(dbc.Button('CS:GO Demso Manager', color='primary'), href='https://csgo-demos-manager.com/',className='mr-3'),
        dcc.Link(dbc.Button('HLTV.org', color='primary'), href='https://hltv.org',className='mr-3'),
        dcc.Link(dbc.Button('Kaggle Dataset', color='primary'), href='https://kaggle.com',className='mr-3'),
    ],
    md=12,
)


column2 = dbc.Col(
    [
        
    ]
)

layout = dbc.Row([column1, column2])