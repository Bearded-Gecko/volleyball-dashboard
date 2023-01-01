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
        html.Br(),
        html.Div("File must be of type, .CSV", style={'fontSize':18, 'textAlign':'left'}),
        html.Br(),
        html.Div("CSV formatting should at least contain the following 4 features, attributes, or headings: 'Player', 'Set', 'Event', and 'Location' in any order", style={'fontSize':18, 'textAlign':'left'}),
        html.Div("*see example csv data/file below", style={'fontSize':18, 'textAlign':'left', 'font-weight': 'bold'}),
        html.Hr(),

        html.Div(children = [
        html.Div("Data Feature Definitions", style={'fontSize':50, 'textAlign':'left'}),
        html.Br(),

        #Player
        html.B("Player", style={'fontSize':24, 'textAlign':'left'}),
        html.Div("Name of player, e.g., Donald, John, Taylor Crabb", style={'fontSize':18, 'textAlign':'left'}),
        html.Br(),

        #Set
        html.B("Set", style={'fontSize':24, 'textAlign':'left'}),
        html.Div("Set number, e.g., 1, 4, 10, 999", style={'fontSize':18, 'textAlign':'left'}),
        html.Div("*set numbers were designed to be continuous, e.g., sets 1-3 could be from a tournament, and sets 4-8 could be from practice games", style={'fontSize':18, 'textAlign':'left', 'font-weight': 'bold'}),
        html.Br(),

        #Event
        html.B("Event", style={'fontSize':24, 'textAlign':'left'}),
        html.Div("Offensive or defensive play for a given player and set number, e.g., dig, hard driven, tool", style={'fontSize':24, 'textAlign':'left'}),
        html.Br(),
        
        #Location
        html.B("Location", style={'fontSize':24, 'textAlign':'left'}),
        html.Div("Location: integer court location of offensive or defense play where applicable, e.g., 1, 2, 3, 4, 5, or 6; see below image:", style={'fontSize':24, 'textAlign':'left'}),
        html.Br(),
        html.Img(src = r'assets/vball_court.jpg', alt = 'image'),

        ]),
        html.Hr(),
        
        html.Div("How to record data", style={'fontSize':50, 'textAlign':'left'}),
        html.Div("Record events for each set and player that you want to track, e.g., 'block' for Ben on set number 42", style={'fontSize':18, 'textAlign':'left'}),
        html.Br(),

        html.B("Offense", style={'fontSize':24, 'textAlign':'left'}),
        html.Div("Offensive events can consist of any of the following: 'hard driven', 'hit shank', 'roll shot', 'tip', 'block kill', 'cut shot', 'touch', 'block shank', 'tool'", style={'fontSize':18, 'textAlign':'left'}),
        html.Div("Any unsuccessful kills can be labled as attempts, e.g., 'hitting attempt', for use in hitting percentage calculations", style={'fontSize':18, 'textAlign':'left'}),
        html.Br(),

        html.B("Defense", style={'fontSize':24, 'textAlign':'left'}),
        html.Div("Record digs for a particular player, set, and location", style={'fontSize':18, 'textAlign':'left'}),
        html.Br(),

        html.B("When and how to record court location", style={'fontSize':24, 'textAlign':'left'}),
        html.Div("Court locations for offense should be based on the court opposite from the player attacking, while court locations for defensive events should be based on the court side of the playing defending", style={'fontSize':18, 'textAlign':'left'}),
        html.Div("Original intent of locations was designed to capture offensive/defensive events that land on the court, e.g., hard driven spike to court location 5 or dig at court location 2. Some offensive hits like 'hit shank' or 'block shank' may not be recorded depending on the user recording the data", style={'fontSize':18, 'textAlign':'left'}),
        html.Hr(),

        html.Div("Example CSV Data", style={'fontSize':50, 'textAlign':'left'}),
        html.Div("*Data was recorded from sets 1, 2, and 3 for players consisting of Michael, Mark, Ben, Kyle from the following YouTube video: https://www.youtube.com/watch?v=CyXlrFxfWn8", style={'fontSize':18, 'textAlign':'left'}),
        html.Div("*Data can be downloaded at: https://u.pcloud.link/publink/show?code=XZ3umeVZN4ADcVw9sykuTepWrkHe1QPcfdv7", style={'fontSize':18, 'textAlign':'left'}),
        html.Div("*Data visualizations, in the Example tab at the top, were derived from the below data", style={'fontSize':18, 'textAlign':'left'}),
        html.Br(),
        html.Div(children = [dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])]),
        html.Hr(),

    ]
)