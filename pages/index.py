import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from app import app

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

Layout in Bootstrap is controlled using the grid system. The Bootstrap grid has 
twelve columns.

There are three main layout components in dash-bootstrap-components: Container, 
Row, and Col.

The layout of your app should be built as a series of rows of columns.

We set md=4 indicating that on a 'medium' sized or larger screen each column 
should take up a third of the width. Since we don't specify behaviour on 
smaller size screens Bootstrap will allow the rows to wrap so as not to squash 
the content.
"""

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Who wins the next round of CS:GO?

            I've built a machine learning model that better predicts the probability a team will win the next round of CS:GO.
            I've written a blog post detailing on how my model works, and have deployed an interactive version of the predictor for you to try yourself!

            """
        ),
            dcc.Markdown("_______"
        ),
        html.Div(
    [
        dcc.Link(dbc.Button('Read the blog', color='primary'), href='/predictions',className='mr-3'),
        dcc.Link(dbc.Button('Use the Predictor!', color='danger'), href='/predictions'),
    ]
),
        
            dcc.Markdown("_______"
        ),
                dcc.Markdown(
        ),
        
        
        dcc.Markdown(
            """
        
            I personally scraped this data across 1,200 demo files from all of the CS:GO Majors and their qualifiers. I've aggregated the highlights of each match into a JSON and have published the dataset to Kaggle if you'd like to build your own model or explore the data further!

            Thank you to HLTV.org for hosting the raw demo files, and CS:GO Demo Manager for streamlining the data export process.    

            """
        ),        
                    dcc.Markdown("_______"
        ),
        dcc.Link(dbc.Button('Raw Data', color='primary'), href='/predictions'),
        
    ],
    md=4,
)

column2 = dbc.Col(
    [
        html.Img(src='assets/csgo-boxart', className='img-thumbnail')
    ]
)

layout = dbc.Row([column1, column2])