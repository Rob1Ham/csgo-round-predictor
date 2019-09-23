# ds-dash-template

- [How to](#how-to)
  - [Activate the conda environment](#activate-the-conda-environment)
  - [Run the app](#run-the-app)
  - [Change the app name in the browser title bar](#change-the-app-name-in-the-browser-title-bar)
  - [Change the app name in the navigation bar](#change-the-app-name-in-the-navigation-bar)
  - [Change your name and contact info in the footer](#change-your-name-and-contact-info-in-the-footer)
  - [Change Bootswatch theme](#change-bootswatch-theme)
  - [Change navigation bar colors](#change-navigation-bar-colors)
  - [Change home page text & button](#change-home-page-text--button)
  - [Add a page](#add-a-page)
  - [Remove a page](#remove-a-page)
  - [Add an image](#add-an-image)
  - [Add a matplotlib plot](#add-a-matplotlib-plot)
  - [Add a Plotly plot](#add-a-plotly-plot)
  - [Add a scikit-learn pipeline](#add-a-scikit-learn-pipeline)
  - [Exit the Pipenv shell](#exit-the-pipenv-shell)
- [Commit to GitHub](#commit-to-github)
- [Deploy to Heroku](#deploy-to-heroku)

## How to

### Activate the conda environment

✅ When you open a terminal, the prompt should look like this:
```
(unit2) $
```

❌ Not this:
```
(base) $
```

To activate your conda environment, use this command:
```
conda activate unit2
```

### Run the app
```
python3 run.py
```

Then in your browser, go to http://localhost:8050/

Ctrl+C quits the app.

### Change the app name in the browser title bar

Edit `app.py` file, `app.title` string:

```python
app.title = 'YOUR APP NAME' # appears in browser title bar
```

### Change the app name in the navigation bar

Edit `run.py` file, `navbar` object, `brand` string:

```python
navbar = dbc.NavbarSimple(
    brand='YOUR APP NAME',
    ...
)
```

### Change your name and contact info in the footer

Edit `run.py` file, `footer` object:

```python
footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('Your Name', className='mr-2'), 
                    html.A(html.I(className='fas fa-envelope-square mr-1'), href='mailto:<you>@<provider>.com'), 
                    html.A(html.I(className='fab fa-github-square mr-1'), href='https://github.com/<you>/<repo>'), 
                    html.A(html.I(className='fab fa-linkedin mr-1'), href='https://www.linkedin.com/in/<you>/'), 
                    html.A(html.I(className='fab fa-twitter-square mr-1'), href='https://twitter.com/<you>'), 
                ], 
                className='lead'
            )
        )
    )
)
```

Dash components use the `className` parameter for CSS classes. `fa` stands for [Font Awesome](https://fontawesome.com/icons/github-square?style=brands) and is used for social media icons. `mr` stands for "margin right" and these CSS classes are from [Bootstrap](https://getbootstrap.com/docs/4.3/utilities/spacing/). The class `lead` is also from [Bootstrap](https://getbootstrap.com/docs/4.1/content/typography/#lead) to make "lead" paragraphs stand out more. You can add & remove CSS classes if you want. 

### Change Bootswatch theme

Browse themes at https://bootswatch.com/

- `dbc.themes.BOOTSTRAP`
- `dbc.themes.CERULEAN`
- `dbc.themes.COSMO`
- `dbc.themes.CYBORG`
- `dbc.themes.DARKLY`
- `dbc.themes.FLATLY`
- `dbc.themes.JOURNAL`
- `dbc.themes.LITERA`
- `dbc.themes.LUMEN`
- `dbc.themes.LUX`
- `dbc.themes.MATERIA`
- `dbc.themes.MINTY`
- `dbc.themes.PULSE`
- `dbc.themes.SANDSTONE`
- `dbc.themes.SIMPLEX`
- `dbc.themes.SKETCHY`
- `dbc.themes.SLATE`
- `dbc.themes.SOLAR`
- `dbc.themes.SPACELAB`
- `dbc.themes.SUPERHERO`
- `dbc.themes.UNITED`
- `dbc.themes.YETI`

Edit `app.py` file, `external_stylesheets` parameter:

```python
external_stylesheets = [
    dbc.themes.BOOTSTRAP, # Bootswatch theme
    'https://use.fontawesome.com/releases/v5.9.0/css/all.css', # for social media icons
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
```

### Change navigation bar colors

First, choose your [Bootswatch theme](#change-bootswatch-theme).

Then, edit `run.py` file, `navbar` object, `color`, `light` & `dark` parameters:

```python
navbar = dbc.NavbarSimple(
    ...
    color='light', 
    light=True, 
    dark=False
)
```

These parameters are explained in [Dash Bootstrap Components docs](https://dash-bootstrap-components.opensource.faculty.ai/l/components/navbar):

> `color` _(string, optional)_: Sets the color of the NavbarSimple. Main options are primary, light and dark, default light. You can also choose one of the other contextual classes provided by Bootstrap (secondary, success, warning, danger, info, white) or any valid CSS color of your choice (e.g. a hex code, a decimal code or a CSS color name)

> `light` _(boolean, optional)_: Applies the `navbar-light` class to the NavbarSimple, causing text in the children of the Navbar to use dark colors for contrast / visibility.

> `dark` _(boolean, optional)_: Applies the `navbar-dark` class to the NavbarSimple, causing text in the children of the Navbar to use light colors for contrast / visibility.

### Change home page text & button

Edit `pages/index.py` file, `column1` object:

```python
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Value Proposition

            Emphasize how the app will benefit users. Don't emphasize the underlying technology.

            ✅ RUN is a running app that adapts to your fitness levels and designs personalized workouts to help you improve your running.

            ❌ RUN is the only intelligent running app that uses sophisticated deep neural net machine learning to make your run smarter because we believe in ML driven workouts.

            """
        ),
        dcc.Link(dbc.Button('Call To Action', color='primary'), href='/predictions')
    ],
    md=4,
)
```

#### Docs
- [`dbc.Col`](https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout)
- [`dcc.Markdown`](https://dash.plot.ly/dash-core-components/markdown)
- [`dcc.Link`](https://dash.plot.ly/urls)
- [`dbc.Button`](https://dash-bootstrap-components.opensource.faculty.ai/l/components/button)

The RUN app example comes from [Google's People + AI Guidebook](https://pair.withgoogle.com/chapter/mental-models/).

### Add a page

**1.** Make a new file, `pages/pagename.py`

The code should have an object named `layout`, with a Dash component assigned to it. For example:

```python
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
        
            ## PAGE NAME


            """
        ),
    ],
    md=4,
)

column2 = dbc.Col([])

layout = dbc.Row([column1, column2])
```

This layout is explained in [Dash Bootstrap Components docs](https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout):

> The Bootstrap grid has twelve columns. The layout of your app should be built as a series of rows of columns.

> We set `md=4` indicating that on a 'medium' sized or larger screen the column should take up a third of the width. Since we don't specify behaviour on smaller size screens Bootstrap will allow the rows to wrap so as not to squash the content.

**2.** Edit `run.py` file. Import `<pagename>` from the `pages` module.

```python
from pages import index, predictions, insights, process, pagename
```

**3.** Edit `run.py` file, `display_page` function. Return `<pagename>.layout` when `pathname == '/<pagename>'`

```python
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/predictions':
        return predictions.layout
    elif pathname == '/insights':
        return insights.layout
    elif pathname == '/process':
        return process.layout
    elif pathname == '/pagename':
        return pagename.layout
    else:
        return dcc.Markdown('## Page not found')
```

**4.** Edit `run.py` file, `navbar` object. Add `dbc.NavItem` & `dcc.Link` objects for the page.

```python
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link('Predictions', href='/predictions', className='nav-link')), 
        dbc.NavItem(dcc.Link('Insights', href='/insights', className='nav-link')), 
        dbc.NavItem(dcc.Link('Process', href='/process', className='nav-link')), 
        dbc.NavItem(dcc.Link('Page Name', href='/pagename', classname='nav-link')), 
    ],
    ...
)
```

### Remove a page

1. Edit `run.py` file, `navbar` object. Remove the `dbc.NavItem` & `dcc.Link` objects for the page.

2. Edit `run.py` file. Do not import `<pagename>` from the `pages` module.

3. Edit `run.py` file, `display_page` function. Remove the code block that returns `<pagename>.layout` when `pathname == '/<pagename>'`

4. Delete the file, `pages/<pagename>.py`

### Add an image

1. Put the image file `<imagefile.extension>` in the `assets/` directory.

2. Edit the file, `pages/<pagename>.py`. Add a [Dash HTML](https://dash.plot.ly/dash-html-components) Img component in the layout:

```python
html.Img(src='assets/imagefile.extension', className='img-fluid')
```

You can size and position images [with Boostrap](https://getbootstrap.com/docs/4.0/content/images/) (for example, with the `img-fluid` class) or just [with CSS](https://dash.plot.ly/getting-started).

### Add a matplotlib plot

This includes visualization libraries that run on top of Matplotlib:
- Pandas plotting
- PDPBox
- Seaborn
- SHAP `force_plot` with `matplotlib=True` parameter

#### Option 1: Take a screenshot / save the plot as an image

First, you should set matplotlib dots per inch to at least 150, so the text isn't fuzzy.

```python
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 150
```

Then take a screenshot or save the plot as an image, and follow the instructions to [add an image](#add-an-image).

#### Option 2: [Convert matplotlib figures to Plotly figures](https://plot.ly/matplotlib/modifying-a-matplotlib-figure/)

Get it working in your notebook first. For example:

```python
%matplotlib inline
import matplotlib.pyplot as plt

matplotlib_figure = plt.figure()
x = [10,  8, 13,  9, 11, 14,  6,  4, 12,  7,  5]
y = [ 8,  6,  7,  8,  8,  9,  7,  4, 10,  4,  5]
plt.scatter(x, y)
```

Then convert the matplotlib figure to a Plotly figure in your notebook, and test that it works:

```python
from plotly.tools import mpl_to_plotly
plotly_figure = mpl_to_plotly(matplotlib_figure)
plotly_figure.show()
```

After it works in your notebook, put it in your app, with a [Dash Graph component](https://dash.plot.ly/dash-core-components/graph):

```python
import dash_core_components as dcc
import matplotlib.pyplot as plt
from plotly.tools import mpl_to_plotly

matplotlib_figure = plt.figure()
x = [10,  8, 13,  9, 11, 14,  6,  4, 12,  7,  5]
y = [ 8,  6,  7,  8,  8,  9,  7,  4, 10,  4,  5]
plt.scatter(x, y)
plotly_figure = mpl_to_plotly(matplotlib_figure)
layout = dcc.Graph(id='my-graph-name', figure=plotly_figure)
```

### Add a Plotly plot

Follow the instructions in the [official Dash tutorial](https://dash.plot.ly/), or see the example included in `pages/index.py`.

### Add a scikit-learn pipeline

1. [Activate the Pipenv shell](#activate-the-pipenv-shell)
2. [Install packages](#install-packages) (scikit-learn, anything else you want)
3. [Launch Jupyter Notebook](#launch-jupyter-notebook)
4. In your notebook, fit your pipeline. For example:

```python
import category_encoders as ce
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

gapminder = px.data.gapminder()
X = gapminder[['year', 'continent']]
y = gapminder['lifeExp']

pipeline = make_pipeline(
    ce.OneHotEncoder(use_cat_names=True), 
    LinearRegression()
)

pipeline.fit(X, y)
```

5. ["Pickle" the pipeline](https://scikit-learn.org/stable/modules/model_persistence.html):

```python
from joblib import dump
dump(pipeline, 'pipeline.joblib')
```

6. Copy the file `pipeline.joblib` into the `assets/` directory.

7. Edit the file, `pages/<pagename>.py`. Add this code at the top, to load the pipeline.

```python
from joblib import load
pipeline = load('assets/pipeline.joblib')
```

8. Add [Dash components](https://dash.plot.ly/dash-core-components) for inputs. For example:

```python
column1 = dbc.Col(
    [
        dcc.Markdown('## Predictions', className='mb-5'), 
        dcc.Markdown('#### Year'), 
        dcc.Slider(
            id='year', 
            min=1955, 
            max=2055, 
            step=5, 
            value=2020, 
            marks={n: str(n) for n in range(1960,2060,20)}, 
            className='mb-5', 
        ), 
        dcc.Markdown('#### Continent'), 
        dcc.Dropdown(
            id='continent', 
            options = [
                {'label': 'Africa', 'value': 'Africa'}, 
                {'label': 'Americas', 'value': 'Americas'}, 
                {'label': 'Asia', 'value': 'Asia'}, 
                {'label': 'Europe', 'value': 'Europe'}, 
                {'label': 'Oceania', 'value': 'Oceania'}, 
            ], 
            value = 'Africa', 
            className='mb-5', 
        ), 
    ],
    md=4,
)
```

9. Add Dash component for output. For example:

```python
column2 = dbc.Col(
    [
        html.H2('Expected Lifespan', className='mb-5'), 
        html.Div(id='prediction-content', className='lead')
    ]
)
```

10. Add [callback](https://dash.plot.ly/getting-started-part-2) to update output based on inputs. For example:

```python
import pandas as pd

@app.callback(
    Output('prediction-content', 'children'),
    [Input('year', 'value'), Input('continent', 'value')],
)
def predict(year, continent):
    df = pd.DataFrame(
        columns=['year', 'continent'], 
        data=[[year, continent]]
    )
    y_pred = pipeline.predict(df)[0]
    return f'{y_pred:.0f} years'
```

## Commit to GitHub

```
git add .
git status
git commit -m "Commit message"
git push
```

## Deploy to Heroku

1. Watch [DS - Data Engineering - Productization and Cloud - Web Application Deployment](https://www.youtube.com/watch?v=W75JAe7vFF0) (12 minute video from Training Kit).

2. Sign up for Heroku at https://signup.heroku.com/ for a free account.

> If you are registered with the GitHub Student Developer Pack, you are eligible to receive one free Hobby Dyno for up to 2 years (valued at $84/year). (App never sleeps) — https://www.heroku.com/github-students

3. Download and install Heroku CLI (Command Line Interface) https://devcenter.heroku.com/articles/heroku-cli

4. [Activate the conda environment](#activate-the-conda-environment).

5. Test your app locally, with [Gunicorn](https://gunicorn.org/):

```
gunicorn run:server
```

If the gunicorn command is not recognized, install gunicorn:

```
conda install -c phumke gunicorn
```

6. Create a requirements.txt for your environment's dependencies:

```
pip freeze > requirements.txt
```

7. [Commit to GitHub](#commit-to-github).

8. Go to https://dashboard.heroku.com/new-app and give your app a name.

9. Follow the commands that Heroku gives you. For example:

```
heroku login

heroku git:remote -a your-app-name
```

10. [Deploy](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true#deploy-the-app) to Heroku:

```
git push heroku master
```

Then Heroku will set up everything, launch your app, and give you the URL!

How does Heroku know what to do? Because of these files in the repo:

- `requirements.txt` tells Heroku what libraries & versions to install
- `Procfile` tells Heroku what command to run
- `.slugignore` tells Heroku what files to ignore
