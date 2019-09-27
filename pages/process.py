import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from app import app
import dash_table

df_sample = pd.read_csv('assets/blogtable1.csv',index_col=0)
df_shap = pd.read_csv('assets/shapinput.csv',index_col=0)


column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Background ##

            *I'll try to keep all videogame domain knowledge to these two short paragraphs, if you're not familiar with Counter Strike, this first paragraph should provide enough context to demonstrate the insights generated.*

            *Counterstrike:Global Offensive (CS:GO for short) is a competitive First Person Shooter popular on PC. The game consists of two teams: Terrorists, and Counter Terrorists. The Terrorists are given a bomb to plant on the Counter Terrorists side of the map, the Counter Terrorists try to stop this. You can play in a vareity of enviornments (called maps) which each have their own nuances.*

            *A round in CS:GO starts with a buy period, where each team can use money they acquired to buy better weapons, grenades, and equipment. Money is earned a few ways, killing opponents the previous round, achieving your team's objective the previous rouns, and bonuses if your team loses consecutive rounds in a row.* **If you are not killed the previous round, you get to keep your equipment in the next round** *In competitive CS:GO, teams play a first 16. 15 rounds are played as one team, and then you swap sides to have symetry with your oponent.*

            *Reminders:*
            * Everything else equal, you get more money the better you perform each round
            * Before a round begins, you get to use your money to buy better equipment
            * There are diffent enivornments you can play on (maps)
            * Games are a first to 16 points, after 15 rounds, you swap sides and reset for symetry."""),
                        dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),
            html.Img(src='assets/csgo-Kelver-and-Helmet.jpg', className='img-thumbnail',style = {'margin': '10px'}),
        dcc.Markdown(
            """
            *Example of the buy menu, each round you spend money on equipment.*
            """
        ,style = {'text-align': 'center'}
        ),
            dcc.Markdown("____",style = {'margin-top': '20px'}
        ),
        dcc.Markdown(
            """
            # Ok. Lets Talk Data. 
"""),   dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),

dcc.Markdown("""
            ## Data Preparation ##

            To start, our dataset is the collection of every CS:GO Major and Qualifer from 2014 to September 2019. 1,200 matches consisting of ~31,000 individual rounds. CS:GO allows for anyone to download any match played during a major. A demo file contains a snapshot every 1/128th second within the game. This results in demo files being ~500MB, far too large for today's analysis, but a highlight of a demo file can be scraped, which captures certain moments within a match.

            The first step is to parse this JSON into a manageable dataframe so we can do general feature engineering and eventually train a model for prediction.
"""),   dcc.Markdown(
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
        ,style = {'margin': '20px'}
        ),
        dcc.Markdown( """
            *Variables:*
            * Round - the current round
            * Equipment_value_team_t - The value of equipment for the Terrorist team at the moment the buy phase ended.
            * Equipment_value_team_ct - The same as above, but for the Counter Terrorist team.
            * ct_score_LR - The score the Counter Terrorist team had at the end of the last round.
            * t_score_LR - The same as above, but for the Counter Terrorist Team
            * map_name - The map the round was played on
            * winner_side - The Target. A 0 or 1, 0 means Terrorists Win. 1 means Counter Terrorists Win.

            *Note: the reason why we use the series score from the LAST round is to prevent leakage. If we used the series score variable by default, it would contain information about the target in a feature!*

            *Also, there is a class imbalance, across all of the matches, the Terrorist side wins 48% of the time, this will come up again later.*
"""),   dcc.Markdown("____",style = {'margin-bottom': '25px'}
        ),
    dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_sample.columns],
            data=df_sample.to_dict('records')),
            dcc.Markdown("____",style = {'margin-bottom': '25px'}
        ),
        dcc.Markdown(
            """
            *Sample of what our dataframe looks like after parsing the Demo JSONs and some feature engineering. This is what we are building our model on. winner_side is the target. If it is 0, Counter Terrorists won the round. If it is 1, Terrorists won the round.*
            """
        ,style = {'text-align': 'center'}
        ),
        dcc.Markdown("""
            ## Training and Holdout ##

            With the initial data formatted, it is time into a training and validation set to prevent overfitting of our predictive model. 25% of the round entries will be used to help generate validation scores. Additionally, this model will only be trained on the first 14 out of 15 CS:GO Majors. The most recent Major from September 2019 will be witheld from all analysis, and our eventaul model will be applied to it to evaluate its strength on previously unseen data (our "test" dataset).
"""),       dcc.Markdown(
            """

            ```
            #splitting the train set into an 75/25 train/validation set
            X_train, X_val, y_train, y_val = train_test_split(
                X_train, y_train, test_size=0.25,random_state=1337)
            ```


            """
        ,style = {'margin-top': '25px'}
        ),

dcc.Markdown("""
            ## Modeling ##

            After some initial modeling exploration, I decided to use an XGBClassifier model to classify the winner of a given round of CS:GO. There were varied paramaters I did a Randomized search across to help boost my model's performance.
            By the end of the hyperparamater tuning, I arrived to a model with an ROC AUC for the Test dataset of 0.70. A perfect model has a ROC of 1, and if you were to guess the Counter Terrorists won each time, the model has a ROC of 0.5.
"""),   
html.Img(src='assets/roc_curve.png', className='img-thumbnail', style={'display': 'block','margin': '0 auto'}),
            dcc.Markdown(
            """
            *The ROC Curve for our Model. The red line is if we were to assume that the Counter Terrorists won each time (Occurs 52% of the time) The blue line visualizes the effective improvement our model has in its ability to classify the winner of a round of CS:GO.*
            """
        ,style = {'text-align': 'center'}),
dcc.Markdown("""
            ## Feature Analysis
            With an initial model built, we can deconstruct elements of it to understand which features have the greatest impact in determining the forecasted value for a given round of CS:GO. 


            ### Feature Importance          
            Feature Importance is the first method I'll use to explore the model. XGBoost relies on a Random Forest structure consisting of many decision trees to come to a prediction. Each tree is built iteravely where each new tree will adjust to correct errors made by the previous tree. This decision structure allows for a quantitiatve measure for the improtance of a given variable, leveraging how early and how often in the process a feature is used for a decision tree split. This is visualized in the Feature Improtance graph to the right.
"""),   
                        dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),
html.Img(src='assets/feature_importance.png', className='img-thumbnail', style={'display': 'block','margin': '0 auto'}),

            dcc.Markdown(
            """
            *A Feature Importance chart, showing from most to least important features in the developed model.*
            """
        ,style = {'text-align': 'center'}
        ),
                                dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),




dcc.Markdown("""
            ### Permuter Improtance
            Permuter importance is another metric used for evaluating the strength of a variable in a model. If a given variable has predictive strength, shuffling all of the values in the feature column should decrease the overall predictive power of a model. In short, the variances in the feature should be related to variances the target, and because we are shuffling values within a feature column, we are pulling form the same distribution that the feature has, so should be fair game to mix around for the sake of evaluation! The counterexample would be a variable that has no predictive ability, say a completly random distribution of numbers. Shuffling among a random distribution of numbers should have no predictive power in a model.
"""),   
         html.Img(src='assets/permutation_importance.png', style={'display': 'block','margin': '0 auto'}, className='img-thumbnail',),
            dcc.Markdown(
            """
            *A Permutation Importance Chart, removing the bias of high cardinal variables (Maps) to highlight core features being equipment value for each team and the round score.*
            """
        ,style = {'text-align': 'center'}
        ),

dcc.Markdown("""            
            Comparing the Feature Importance and Permuter Importance, there is an observable dropoff in the predictive power of the map features. This is because **Feature Importance and Permuter importance is that scikit-learn's Random Forest feature importance tend to inflate the importance of high cardinality categorical objects. **
"""),   dcc.Markdown("""  
            ## Partial Dependence Plot
            Feature Importance and Permuter importance are valuable metrics, but are not able to explain if there is a positive or negative relationships with a given variable. A dependence plot can allow us to evaluate how our target (winner of a CS:GO match) is impacted by the shifts in multiple variables. In this case, I will be evaluating the two more important features demonstrated above, Equipment Values for the Terrorist and Counter Terrorist teams. As can be shown on the Partial Depenence Plot to the right, along the minor diagnal (lower left to upper right), the percentages stay very close to .5. Intuitively this makes sense, if you have roughly equally skilled players with the same resources, everything else equal it is a coinflip as to who will win the round. As you stray from the diagnol though, you are able to view that the larger a surplus a team has in resources when compared to the other team, the further you stray from a value of .5. In our dataset the Terrorists winning was encoded as a 1, with Counter Terrorists winning encoded as a 0. So as a grid value approaches 0, the higher likelyhood the Counter Terrorists will win and vice versa.
"""),   html.Img(src='assets/pdp.png', className='img-thumbnail', style={'display': 'block','margin': '0 auto'}),
                     dcc.Markdown(
            """
            *A Partial Dependence Plot looking at the impact Equipment Values for the Terrorist and Counter Terrorist team have on round results. The closer to 1, the more likely The Terrorists Team wins the round.*
            """
        ,style = {'text-align': 'center'}
        ),


dcc.Markdown("""  
            ## SHAP File
            Fianlly, to provide the breadown of how an individual prediction if generated, we can use SHAP files to deconstruct the black box of XGBoost. First, I am taking an example round from the Test Set (Starladder Berlin).
"""),

             dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_shap.columns],
            data=df_shap.to_dict('records')),
                                 dcc.Markdown(
            """
            *Example round from the test set to use for SHAP values.*
            """
        ,style = {'text-align': 'center'}),
        html.Img(src='assets/match_snapshot.png', className='img-thumbnail', style={'display': 'block','margin': '0 auto'}),
                                 dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),
                                         dcc.Markdown(
            """
            *Screenshot from the event broadcast at this moment in time. This verifies our dataframe is correct, as well as visually shows how differences in money impacts gameplay. See how the team on the left (CR4ZY, playing Counter Terrorist) has much less money, and is left with pistols while the team on the right have much more powerful guns?*
            """
        ,style = {'text-align': 'center'}
        ),

                                dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),
         html.Img(src='assets/shap_file3.png', className='img-thumbnail', style={'display': 'block','margin': '0 auto'}),
                                 dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),
                                         dcc.Markdown(
            """
            *Visualizing how the model weighs the factors from the example round above. The red arrows push to the left, showing strength for the case that Terrorists win. Blue pushes left, making the case Counter Terorists should win.*
            """
        ,style = {'text-align': 'center'}
        ),
                                         dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),
                                         dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),

dcc.Markdown("""  
            As seen in the print statement, there is an expected value of -0.15, this is because of the class imbalance noted previously, where the condition for winner to equal 1 (Terrorist win) occurs 48% of the time.

            The numberline of the SHAP File represents the spectrum of likelyhood that each side will win the round. The further to the left the output value lands, the more likely Counter Terrorists will win. The further to the right, the more likely Terrorists win.

            We can see from the Shap values, the model is extremly confident that the Terrorists will win. They are up 4-0, have a signifigant gear advantage, it is their game to lose.
"""),
                                 dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),
                                         dcc.Markdown("____",style = {'margin-bottom': '20px'}
        ),
dcc.Markdown("""  
            # So. What Happens?
                Let us take a look."""),
    html.Div([        
    html.Iframe(
        src='https://www.youtube.com/embed/yzjUTe-Zxgc?start=672',style={'width': '560px', 'height': '315px', 'display': 'block','margin': '0 auto'}),
        dcc.Markdown(
            """
            *This video starts in the middle of the predicted roun, with 4 players left alive on each side.*
            *The model is predicting the Terrorist Team (orange color in game) will win with high confidence , and the Counter Terrorist (light blue color in game) will lose.*
            """
        ,style = {'text-align': 'center'}
        ),
dcc.Markdown("""  
           A major upset! Espiranto pulls off a "4K" (when you kill 4 out of the 5 opponents on your own). While the model is wrong, it does not make it an inherently bad model. Afterall, upsets are what keep games interesting!"""),
    ])
    
    ],md=12 
)









column2 = dbc.Col(
    [
           
            
    ],md=6 
)

layout = dbc.Row([column1, column2])


