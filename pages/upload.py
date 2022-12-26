import base64
import datetime
import io

import dash
from dash import dcc, html, dash_table, Input, Output, State, no_update
import plotly.express as px
import csv
import pandas as pd
import os

dash.register_page(__name__) #dash.register_page tells Dash this is a page in your app and adds it to a page registry

#layout
layout = html.Div(
    [
        dcc.Upload( #this is the upload layout object to upload csv file
            id = "upload_data",
            children = html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            
            style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },

        #allow multiple files to be uploaded
        multiple = True

        ),
        html.Div(id = "headlines"),
        html.Div(id = 'kill_graph', style = {'width': '49%', 'display': 'inline-block'}), #this layout will host our data visualizations, e.g., graphs
        html.Div(id = 'kill_heatmap', style = {'width': '49%', 'display': 'inline-block'}), #this layout will host our data visualizations, e.g., graphs
        html.Div(id='output-data-upload'), #this is where we will put a table of csv if needed

    ])

def parse_contents(contents, filename, date): #this function will parse through the csv when callback is triggered for uploading csv-it accesses inherent properties of content, filename, and date. 
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    players = list(set(df['Player'].values.tolist())) #get list of unique players
    kill_types = list(set(df['Offense Type'].values.tolist())) #get list of unique players

    return html.Div([ #when a csv is uploaded, this parse function will also return a drop down and data visualization
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        html.Hr(),  # horizontal line


        dcc.Dropdown(
            id = "dropdown",
            options = players,
            value = players[0],
            clearable = False
            ),
        
        html.Button(id = "submit-button", children = "Create Graph"), #this button is 
        
        dcc.Store(id = 'stored-data', data = df.to_dict('records')), #store contents of csv for use in different callback

        dash_table.DataTable( #return table
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),

        # # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })

    ])

#CALLBACK TO UPLOAD DATA FOR USE WITH SECOND CALLBACK
@dash.callback(Output('output-data-upload', 'children'), 
              Input('upload_data', 'contents'), #callback is triggered by uploaded data
              State('upload_data', 'filename'),
              State('upload_data', 'last_modified'))

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

#SECOND CALLBACK TO GENERATE VISUALIZATIONS FROM FIRST CALLBACK 
@dash.callback(Output('kill_graph', 'children'),
              Output('kill_heatmap', 'children'),
              Output('headlines', 'children'),
              Input("submit-button", "n_clicks"), #callback is triggered by clicking button
              State('stored-data', 'data'),
              State('dropdown', 'value'))

def get_kill_stats(n, data, player):
    if n is None:
        return no_update
    else:

        #BAR CHART (TYPE OF KILLS)
        df = pd.DataFrame.from_dict(data)
        player_df = df[df['Player'] == player] #filter by player
        non_na_df = player_df[player_df["Offense Type"].notnull()]#filter by non-na kill values
        grouped_df = non_na_df.groupby("Offense Type", as_index = False).agg(kill_counts = ("Offense Type", 'count')) #group by offense type and aggregate sum the counts

        #convert errors to negative counts
        for index, row in grouped_df.iterrows():
            if "error" in row['Offense Type']:
                grouped_df.at[index, 'kill_counts'] = -row['kill_counts'] #make any errors have negative count

        #sort dataframe
        grouped_df = grouped_df.sort_values(by = 'kill_counts', ascending =  False)

        fig = px.bar(grouped_df, x = "Offense Type", y = "kill_counts") #bar chart
    
        #HEADLINES

        #net points
        net_points = grouped_df['kill_counts'].sum()

        #scored points
        scored_points = grouped_df[grouped_df['kill_counts'] > 0]['kill_counts'].sum()

        #errors
        errors = abs(grouped_df[grouped_df['kill_counts'] < 0]['kill_counts'].sum()) #take positive of negative number

        #headline outputs
        scored_message = "{} points scored".format(scored_points)
        error_message = "{} errors".format(errors)
        net_message = "Net score: {}".format(net_points)

        #HEATMAP (LOCATION OF KILLS)
        #heat map of kill locations
        location_df = non_na_df.groupby("Location", as_index = False).agg(location_counts = ("Location", 'count')) #group by offense type and aggregate sum the counts

        #convert locations to int
        location_df['Location'] = location_df['Location'].astype(int)

        #iterate through locations and their values to arrange in format for heatmap
        location_counts = []
        for i in range(1, 7, 1):
            if i in location_df['Location'].tolist():
                location_counts.append(location_df.loc[location_df['Location'] == i]['location_counts'].values[0])
            else:
                location_counts.append(0)

        #now rearrange court index and counts to match heatmap orientation, i.e. convert [[1, 2, 3], [4, 5, 6]], which represents the heat map, to [[4, 3, 2], [5, 6, 1]], which represents the court
        court_indexes = [4, 3, 2, 5, 6, 1]

        court_counts = []

        for court_indexes in court_indexes:
            court_counts.append(location_counts[court_indexes-1])

        rearranged_locations = [court_counts[0:3], court_counts[3:6]] #correct court indexes for heat map


        rearranged_locations = [location_counts[0:3], location_counts[3:6]]

        hm = px.imshow(rearranged_locations, color_continuous_scale = 'Greens', text_auto = True, title = "Location of Kills on Court (non-shank points)") #heat map

        #return visualizations and other elements
        return html.Div([
            dcc.Graph(figure = fig),
        ]), html.Div([ 
            dcc.Graph(figure = hm, style = {'width': '49%', 'display': 'inline-block'}), 
            ]), html.Div([
                html.H2(children = scored_message, style={'fontSize':24, 'textAlign':'left'}),
                html.H2(children = error_message, style={'fontSize':24, 'textAlign':'left'}),
                html.H2(children = net_message, style={'fontSize':24, 'textAlign':'left'}),
            ])

    