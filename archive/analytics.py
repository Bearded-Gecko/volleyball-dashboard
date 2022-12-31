import dash
from dash import dcc, html, dash_table, Input, Output, State
import plotly.express as px
import csv
import pandas as pd
import os

dash.register_page(__name__) #dash.register_page tells Dash this is a page in your app and adds it to a page registry

df = pd.read_csv('assets/gilbertson_ho_vs_christ_thompson_8_14_2020.csv') #load dataframe

players = list(set(df['Player'].values.tolist())) #get list of unique players

#layout
layout = html.Div(
    [
        html.Div("Stats", style={'fontSize':50, 'textAlign':'center'}),

        html.Br(),

        # dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]), #this will convert pandas df to dash table

        dcc.Dropdown(
            id = "dropdown",
            options = players,
            value = players[0],
            clearable = False
        ),

        html.Br(),

        html.H6(id = "kills", children = [], style={'fontSize':50, 'textAlign':'left'}),

        html.Br(),

        dcc.Graph(
            id = "viz_div",
            style = {'width': '90vh', 'height': '90vh'}
            )

    ]
)


#callback for visualizations
@dash.callback(
    Output(component_id='viz_div', component_property='figure'),
    Output(component_id='kills', component_property='children'),
    Input(component_id='dropdown', component_property='value'))

def get_kill_stats(selected_player):
    
    #get kill stats for selected player
    player_df = df[df['Player'] == selected_player] #filter by player
    non_na_df = player_df[player_df["Offense Type"].notnull()]#filter by non-na kill values
    grouped_df = non_na_df.groupby("Offense Type", as_index = False).agg(kill_counts = ("Offense Type", 'count')) #group by offense type and aggregate sum the counts

    fig = px.bar(grouped_df, x = "Offense Type", y = "kill_counts")

    #get sum of all kills
    total_kills = grouped_df['kill_counts'].sum()

    #create string output of total kills
    number_of_kills = "Total kills was {}".format(total_kills)

    #return barchart Dash object
    return fig, number_of_kills
    

    

    
