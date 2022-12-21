import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__, path='/') #dash.register_page tells Dash this is a page in your app and adds it to a page registry; '/' represents home page

#display readme info

# df = px.data.gapminder()

layout = html.Div(
    [
        html.Div("Read Me", style={'fontSize':50, 'textAlign':'center'}),
        html.Img(src = r'assets/vball_court.jpg', alt = 'image'),
        html.Div("you must record player and offensive and defensive type of each point in a set", style={'fontSize':24, 'textAlign':'left'})



    ]
)