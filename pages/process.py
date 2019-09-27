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
        
            ## Modeling Process

            *I'll try to keep all videogame domain knowledge to this two short paragraphs, if you're not familiar with Counter Strike, this first paragraph should provide enough context to demonstrate the insights generated.*

            *Counterstrike:Global Offensive (CS:GO for short) is a competitive First Person Shooter popular on PC. The game consists of two teams: Terrorists, and Counter Terrorists. The Terrorists are given a bomb to plant on the Counter Terrorists side of the map, the Counter Terrorists try to stop this. You can play in a vareity of enviornments (called maps) which each have their own nuanes.*

            *A round in CS:GO starts with a buy period, where each team can use money they acquired to buy better weapons, grenades, and equipment. Money is earned a few ways, killing opponents the previous round, achieving your team's objective the previous rouns, and bonuses if your team loses consecutive rounds in a row.* **If you are not killed the previous round, you get to keep your equipment in the next round** *In competitive CS:GO, teams play a first 16. 15 rounds are played as one team, and then you swap sides to have symetry with your oponent.*

            *Reminders:*
            * Everything else equal, you get more money the better you perform each round
            * Before a round begins, you get to use your money to buy better equipment
            * There are diffent enivornments you can play on (maps)
            * Games are a first to 16 points, after 15 rounds, you swap sides and reset for symetry.







            """
        ),

    ],md=6 
)

layout = dbc.Row([column1])