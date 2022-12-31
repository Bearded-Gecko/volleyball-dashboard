import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/') #dash.register_page tells Dash this is a page in your app and adds it to a page registry; '/' represents home page

#display readme info

df = pd.read_csv("assets/gilbertson_ho_vs_christ_thompson_8_14_2020_modified_sets_1_to_3.csv")

layout = html.Div(
    [
        html.Div("Requirements", style={'fontSize':50, 'textAlign':'left'}),
        html.H2("File must be of type, .CSV", style={'textAlign':'left'}),
        html.H2("File must contain the following 4 headers: 'Player', 'Set', 'Event', and 'Location' in any order", style={'textAlign':'left'}),
        html.Hr(),

        html.Div("Heading Definitions", style={'fontSize':50, 'textAlign':'left'}),
        html.H2("Player: name of player, e.g., Michael, John, Taylor Crabb", style={'textAlign':'left'}),
        html.H2("Set: set number, e.g., 1, 4, 10, 999", style={'textAlign':'left'}),
        html.H2("Event: offensive or defense play for a given player and set number, e.g., dig, hard driven, tool", style={'textAlign':'left'}),
        html.H2("Location: integer court location of offensive or defense play where applicable, e.g., 1, 2, 3, 4, 5, or 6; see below image:", style={'textAlign':'left'}),
        html.Img(src = r'assets/vball_court.jpg', alt = 'image'),
        html.Hr(),
        
        html.Div("How to record data", style={'fontSize':50, 'textAlign':'left'}),
        html.Div("Record events for each set and each player that you want to track", style={'fontSize':24, 'textAlign':'left'}),

        html.H1("Offense"),
        html.Div("Offensive events can consist of any of the following: 'hard driven', 'hit shank', 'roll shot', 'tip', 'block kill', 'cut shot', 'touch', 'block shank', 'tool'", style={'fontSize':24, 'textAlign':'left'}),
        html.Div("Any unsuccessful kills can be labled as attempts, e.g., 'hitting attempt', for use in hitting percentage calculations", style={'fontSize':24, 'textAlign':'left'}),

        html.H1("Defense"),
        html.Div("Record digs for a particular player, set, and location", style={'fontSize':24, 'textAlign':'left'}),

        html.H1("When to record location"),
        html.Div("Court locations for offense should be based on the court opposite from the player attacking, while court locations for defensive events should be based on the court side of the playing defending", style={'fontSize':24, 'textAlign':'left'}),
        html.Div("Original intent of locations was designed to capture offensive/defensive events that land on the court, e.g., hard driven spike to court location 5 or dig at court location 2. Some offensive hits like 'hit shank' or 'block shank' may not be recorded depending on the user recording the data", style={'fontSize':24, 'textAlign':'left'}),
        html.Hr(),

        html.Div("Example CSV Data", style={'fontSize':50, 'textAlign':'left'}),
        html.H2("Example used 3 sets and player names consisted of Michael, Mark, Ben, Kyle"),
        html.H2("Example data can be downloaded at: https://u.pcloud.link/publink/show?code=XZ3umeVZN4ADcVw9sykuTepWrkHe1QPcfdv7"),
        html.Br(),
        html.Div(children = [dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])]),

        

        html.Hr(),

    ]
)