import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from app import app
import dash_table

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Background ##

            *I'll try to keep all videogame domain knowledge to this two short paragraphs, if you're not familiar with Counter Strike, this first paragraph should provide enough context to demonstrate the insights generated.*

            *Counterstrike:Global Offensive (CS:GO for short) is a competitive First Person Shooter popular on PC. The game consists of two teams: Terrorists, and Counter Terrorists. The Terrorists are given a bomb to plant on the Counter Terrorists side of the map, the Counter Terrorists try to stop this. You can play in a vareity of enviornments (called maps) which each have their own nuanes.*

            *A round in CS:GO starts with a buy period, where each team can use money they acquired to buy better weapons, grenades, and equipment. Money is earned a few ways, killing opponents the previous round, achieving your team's objective the previous rouns, and bonuses if your team loses consecutive rounds in a row.* **If you are not killed the previous round, you get to keep your equipment in the next round** *In competitive CS:GO, teams play a first 16. 15 rounds are played as one team, and then you swap sides to have symetry with your oponent.*

            *Reminders:*
            * Everything else equal, you get more money the better you perform each round
            * Before a round begins, you get to use your money to buy better equipment
            * There are diffent enivornments you can play on (maps)
            * Games are a first to 16 points, after 15 rounds, you swap sides and reset for symetry.


            ** Ok. Lets Talk Data. **

            ## Data Preparation ##

            To start, our dataset is the collection of every CS:GO Major and Qualifer from 2014 to September 2019. 1,200 matches consisting of ~31,000 individual rounds. CS:GO allows for anyone to download any match played during a major. A demo file contains a snapshot every 1/128th second within the game. This results in demo files being ~500MB, far too large for today's analysis, but a highlight of a demo file can be scraped, which captures certain moments within a match.

            The first step is to parse this JSON into a manageable dataframe so we can do general feature engineering and eventually train a model for prediction.

            *Variables:*
            * Round - the current round
            * Equipment_value_team_t - The value of equipment for the Terrorist team at the moment the buy phase ended.
            * Equipment_value_team_ct - The same as above, but for the Counter Terrorist team.
            * ct_score_LR - The score the Counter Terrorist team had at the end of the last round.
            * t_score_LR - The same as above, but for the Counter Terrorist Team
            * map_name - The map the round was played on
            * winner_side - The Target. A 0 or 1, 0 means Terrorists Win. 1 means Counter Terrorists Win.

            *Note: the reason why we use the series score from LAST round is to prevent leakage. If we used the series score variable by default, it would contain information about the target in a feature!*
            

            ## Training and Holdout ##

            With the initial data formatted, it is time into a training and validation set to prevent overfitting of our predictive model. 25% of the round entries will be used to help generate validation scores. Additionally, this model will only be trained on the first 14 out of 15 CS:GO Majors. The most recent Major from September 2019 will be witheld from all analysis, and our eventaul model will be applied to it to evaluate its strength on previously unseen data (our "test" dataset).

            ## Modeling ##

            After some initial modeling exploration, I decided to use an XGBClassifier model to classify the winner of a given round of CS:GO. There were varied paramaters I did a Randomized search across to help boost my model's performance.
            By the end of the hyperparamater tuning, I arrived to a model with an ROC AUC for the Test dataset of 0.70.


            ## Feature Importance
            *explain here*

            ## Permuter Improtance
            *explain here*

            ##Partial Dependence Plot
            *explain here*

            ##SHAP File
            *explain here*














            """
        ),

    ],md=6 
)


df_sample = pd.read_csv('assets/blogtable1.csv',index_col=0)

column2 = dbc.Col(
    [
        html.Img(src='assets/csgo-Kelver-and-Helmet.jpg', className='img-thumbnail',style = {'margin-top': '100px'}),
        dcc.Markdown(
            """

            *Example of the buy menu, each round you spend money on equipment.*


            """
        ,style = {'text-align': 'center'}
        ),
        dcc.Markdown(
            """

            ```
            def json_to_df(json_path):
                with open(json_path, 'r') as json_data:
                    data = json.load(json_data)
                data = pd.DataFrame.from_dict(data, orient='index')
                ...
                ...
                # feature extraction from json
                # done here (many dropped later)
                # view github for full details.

                return df
            ```


            """
        ,style = {'margin-top': '400px'}
        ),
    dcc.Markdown("____",style = {'margin-bottom': '100px'}
        ),
    dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_sample.columns],
            data=df_sample.to_dict('records')),
    dcc.Markdown(
            """

            ```
            #splitting the train set into an 80/20 train/validation set
            X_train, X_val, y_train, y_val = train_test_split(
                X_train, y_train, test_size=0.25,random_state=1337)
            ```


            """
        ,style = {'margin-top': '150px'}
        ),
    ],md=6 
)

layout = dbc.Row([column1, column2])


