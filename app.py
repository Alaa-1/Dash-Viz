import dash
import dash_draggable
import dash_daq as daq

import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_table
import sd_material_ui
import dash_bootstrap_components as dbc


import sqlite3 

from dash.dependencies import Input, Output, State 
import pandas as pd
import numpy as np

import json
import datetime
import operator
import os

import base64
import io

#import the tabs layouts
from pages import tab1content, tab2content, tab3Content, tab4content, tab5content
#Kmeans 
import random as rd
from collections import defaultdict
import matplotlib.cm as cm
from sklearn.cluster import KMeans




app = dash.Dash(__name__)

#pysql = lambda q: pdsql.sqldf(q, globals())


app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#39CCCC',
    'color': 'white',
    'padding': '6px'
}
##################
#Tabs layout
###################
app.layout = html.Div([
   

    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[

        dcc.Tab(label='Data', value='tab-1', style=tab_style, selected_style=tab_selected_style, children=
            tab1content.app.layout
        ),
        dcc.Tab(label='Overview', value='tab-2', style=tab_style, selected_style=tab_selected_style , children=
            tab5content.app.layout),
        dcc.Tab(label='visualize', value='tab-3', style=tab_style, selected_style=tab_selected_style , children=
            tab2content.app.layout),
        dcc.Tab(label='Clustering', value='tab-4', style=tab_style, selected_style=tab_selected_style, children=
            tab3Content.app.layout),
        dcc.Tab(label='Reports', value='tab-5', style=tab_style, selected_style=tab_selected_style, children=tab4content.app.layout),
        
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline'),
    
      

    
])

 
#################################################################################################""""
# File upload section
# (parsing data/passing the values to the table/updating the dropdown filter/displayign the table)
################################################################################################## """"

def parse_contents(contents, filename):
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
        return None

    return df
########################################
#Passing the data to the table in tab-1
#########################################

@app.callback([Output('table', 'columns'),
            Output('table', 'data'),
            Output('table', 'style_data_conditional'),
            Output('alert','children'),
            Output('centerDiv','style'),],
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
              
 
# @cache.cached(timeout=TIMEOUT,  key_prefix='all_comments')
def update_table(contents, filename):
   
    if contents is not None:
        df = parse_contents(contents, filename)
        if df is not None:
            aa = [{"name": i, "id": i} for i in sorted(df.columns)]
            sty = {'display':'none'}
            
             # print(row_indices)
            miss = df.columns[df.isna().any()].tolist()
            missing = df.loc[:, df.isnull().any()].to_dict()
            row = np.where(df.isnull())
            if df.isnull().values.any():
                sum = df.isnull().sum().sum()
                print("you have missing values")
                alert =  dbc.Alert(f"Your data has {sum} missing values !", color="danger",dismissable=True)
            else:
                alert =  dbc.Alert("Your data has been uploaded successfully.", color="success", dismissable=True)

            inds = pd.isnull(df).any(1).to_numpy().nonzero()[0]
            # print(inds)
        

            styles = [{}]
            for i in inds:
                style={
                    "if": {"row_index": i},
                    "backgroundColor": "#FA8072",
                    'color': 'white'}
                styles.append(style)
            return [{"name": i, "id": i} for i in (df.columns)],  df.to_dict('records'), styles, alert, sty
        else:
            return [{}]
    else:
        return [{}]





###############################
# The filtered table in tab-2
##############################
@app.callback([Output('tablef', 'columns'),
            Output('tablef', 'data')],
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_tablef(contents, filename):
    if contents is not None:
        df = parse_contents(contents, filename)
        if df is not None:
            aa = [{"name": i, "id": i} for i in sorted(df.columns)]
            # print(aa)

            return [{"name": i, "id": i} for i in (df.columns)],  df.to_dict('records')
        else:
            return [{}]
    else:
        return [{}]

###############################################################################""""

#########################################
#Yet another table for the report tab
#######################################
@app.callback([Output('tableR', 'columns'),
            Output('tableR', 'data')],
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_tableR(contents, filename):
    if contents is not None:
        df = parse_contents(contents, filename)
        if df is not None:
            aa = [{"name": i, "id": i} for i in sorted(df.columns)]
            # print(aa)

            return [{"name": i, "id": i} for i in (df.columns)],  df.to_dict('records')
        else:
            return [{}]
    else:
        return [{}]
#########################################
# callback update options of filter dropdown
###########################################
@app.callback(Output('dropdown_table_filterColumn', 'options'),
              [Input('powerbutton', 'False'),
               Input('tablef', 'data')])
def update_filter_column_options(value, tablerows):
    if value == False:
        print ("df empty")
        return []

    else:
        dff = pd.DataFrame(tablerows) # <- problem! dff stays empty even though table was uploaded

        print ("updating... dff empty?:"), dff.empty #result is True, labels stay empty

        return [{'label': i, 'value': i} for i in (list(dff))]




# ##############################################
# # passing the data, graph type and creating charts
# ##############################################
@app.callback([Output('graphs', 'children'),
               Output('reportGraphs','children'),
               ],
            [Input('tablef', 'data'),
            Input('dropdown_viz','value'),
             Input('dropdown_table_filterColumn','value'),
             Input("my-color-picker", 'value')])
#rows from tabelf/
##selected: is the selected values from the first dropd/
###value: is the selected value from the viz dropd
def display_graphs(rows, value, selected, selected_color):
    df = pd.DataFrame(rows)
    ##settign up the colors
    color = selected_color["hex"]
    
    sel= []
    for s in selected:
        sel.append(s)

    data= []
    
    def get_index(name):
        '''
        return the index of a column name
        '''
        for column in df.columns:
            if column == name:
                index = df.columns.get_loc(column)
                return index
       
    chosen= []
    labels = []
    for i in sel:
        chosen.append(get_index(i))
        labels.append(i)

    
    
    
#creating a text area and passing it into text variable
    text =dcc.Textarea(
        id='text',
        draggable = True,
        value='',
        style={'width': '100%'}
        )
                            
                                          
#condition for the color picked
#if the user select 2 columns he can change the color else it's by default
    mrks = {}
    if len(sel)<=2 : 
        mrks.update({"color": color})
    else:
        mrks.update({})
###################################

    graphs= []

    baar = []
    scaat= []
    liine = []
    buuble = []
    boox = []
    for c,l in zip (range(1,len(chosen)), range(1, len(labels))):
        baar.append(go.Bar(x = df[df.columns[chosen[0]]],
                y = df[df.columns[chosen[c]]],
                marker= mrks,
                name = labels[l]))

        scaat.append(go.Scatter(
                        x = df[df.columns[chosen[0]]],
                        y = df[df.columns[chosen[c]]],
                        name = labels[l],
                        mode = 'markers',
                        marker= mrks,

                        
                    ))
        liine.append(go.Scatter(
                        x = df[df.columns[chosen[0]]],
                        y = df[df.columns[chosen[c]]],
                        name = labels[l],
                        mode = 'lines',
                        marker = mrks,
                        
                    ))
        buuble.append(go.Scatter(
                x = df[df.columns[chosen[0]]],
                y = df[df.columns[chosen[c]]],
                name = labels[l],
                mode='markers',
                marker = {
                            'size': df[df.columns[chosen[c]]]*3,
                           
                        },
                
               
        
                   
                    ))


        boox.append(go.Box(x = df[df.columns[chosen[0]]],
                y = df[df.columns[chosen[c]]],
                name = labels[l],
                marker= mrks))


    
    if df.empty:
        raise dash.exceptions.PreventUpdate()
    else:
        for values in value:
            if values == 'B' :
                graphs.append(html.Div(
            children=dash_draggable.dash_draggable(id='dragger',
                        handle='.handle',
                        
                        children=[
                            html.Div([
                                sd_material_ui.Paper(children=[
                                    sd_material_ui.IconButton(
                                        id='button',
                                        iconClassName='fas fa-grip-lines',
                                        iconStyle={'color': 'grey',
                                                   'width': 50,
                                                   'height': 50,
                                                   'position': 'relative',
                                                   'top': '2px',
                                                   'left': '-12px'},
                                        tooltip='Drag Me', touch=True,
                                        tooltipPosition='bottom-right')],
                                    zDepth=3,
                                    circle=True,
                                    style=dict(height=50,
                                               width=50,
                                               textAlign='center',
                                               position='relative',
                                               display='inline-block',
                                               top='25px',
                                               left='-25px')
                                )], className='handle no-print'),
                                dcc.Graph(
                            id='Bar',
                            figure={
                    'data':baar,
                    
                    'layout':go.Layout(title= f"Bar chart: {sel[0]} By {sel[1]}",  barmode='stack' ),
                     }
                    ),
                    text,
                           
                        ])
                ))
                


            elif values == 'S' :
                graphs.append(html.Div(
            children=dash_draggable.dash_draggable(id='dragger',
                        handle='.handle',
                        
                        children=[
                            html.Div([
                                sd_material_ui.Paper(children=[
                                    sd_material_ui.IconButton(
                                        id='button',
                                        iconClassName='fas fa-grip-lines',
                                        iconStyle={'color': 'grey',
                                                   'width': 50,
                                                   'height': 50,
                                                   'position': 'relative',
                                                   'top': '2px',
                                                   'left': '-12px'},
                                        tooltip='Drag Me', touch=True,
                                        tooltipPosition='bottom-right')],
                                    zDepth=3,
                                    circle=True,
                                    style=dict(height=50,
                                               width=50,
                                               textAlign='center',
                                               position='relative',
                                               display='inline-block',
                                               top='25px',
                                               left='-25px')
                                )], className='handle no-print'),
                                dcc.Graph(
                        id='Scatter',
                        figure={
                'data':scaat,
                    'layout':go.Layout(title= "Scatter plot"),
            }
                    ),
                    text,
                           
                        ])

                        
                ))
            

            elif values == 'P' :
                graphs.append(html.Div(
            children=dash_draggable.dash_draggable(id='dragger',
                        handle='.handle',
                        
                        children=[
                            html.Div([
                                sd_material_ui.Paper(children=[
                                    sd_material_ui.IconButton(
                                        id='button',
                                        iconClassName='fas fa-grip-lines',
                                        iconStyle={'color': 'grey',
                                                   'width': 50,
                                                   'height': 50,
                                                   'position': 'relative',
                                                   'top': '2px',
                                                   'left': '-12px'},
                                        tooltip='Drag Me', touch=True,
                                        tooltipPosition='bottom-right')],
                                    zDepth=3,
                                    circle=True,
                                    style=dict(height=50,
                                               width=50,
                                               textAlign='center',
                                               position='relative',
                                               display='inline-block',
                                               top='25px',
                                               left='-25px')
                                )], className='handle no-print'),
                                dcc.Graph(
                        id='Pie',
                        figure={
                            'data':[go.Pie(
                labels = df[df.columns[chosen[0]]],
                values = df[df.columns[chosen[1]]]
                    
            )],
            'layout':go.Layout(title= "Pie chart")
            }
                
            
                    ),
                    text,
                           
                        ])

                        
                ))
            
            elif values == 'L' :
                    graphs.append(html.Div(
            children=dash_draggable.dash_draggable(id='dragger',
                        handle='.handle',
                        
                        children=[
                            html.Div([
                                sd_material_ui.Paper(children=[
                                    sd_material_ui.IconButton(
                                        id='button',
                                        iconClassName='fas fa-grip-lines',
                                        iconStyle={'color': 'grey',
                                                   'width': 50,
                                                   'height': 50,
                                                   'position': 'relative',
                                                   'top': '2px',
                                                   'left': '-12px'},
                                        tooltip='Drag Me', touch=True,
                                        tooltipPosition='bottom-right')],
                                    zDepth=3,
                                    circle=True,
                                    style=dict(height=50,
                                               width=50,
                                               textAlign='center',
                                               position='relative',
                                               display='inline-block',
                                               top='25px',
                                               left='-25px')
                                )], className='handle no-print'),
                               dcc.Graph(
                            id='Line',
                            figure={
                    'data':liine,
            'layout':go.Layout(title= "Line chart")
                }
                        ),
                        text,
                           
                        ])

                        
                ))
            
            
            elif values == 'Bb' :
                graphs.append(html.Div(
            children=dash_draggable.dash_draggable(id='dragger',
                        handle='.handle',
                        
                        children=[
                            html.Div([
                                sd_material_ui.Paper(children=[
                                    sd_material_ui.IconButton(
                                        id='button',
                                        iconClassName='fas fa-grip-lines',
                                        iconStyle={'color': 'grey',
                                                   'width': 50,
                                                   'height': 50,
                                                   'position': 'relative',
                                                   'top': '2px',
                                                   'left': '-12px'},
                                        tooltip='Drag Me', touch=True,
                                        tooltipPosition='bottom-right')],
                                    zDepth=3,
                                    circle=True,
                                    style=dict(height=50,
                                               width=50,
                                               textAlign='center',
                                               position='relative',
                                               display='inline-block',
                                               top='25px',
                                               left='-25px')
                                )], className='handle no-print'),
                               dcc.Graph(
                            id='Bubble',
                            figure={
                    'data':buuble, 
                    'layout':go.Layout(title= "Bubble chart"),
                     }
                    ),
                    text,
                           
                        ])

                        
                ))
            
            if values == 'Bp' :
                graphs.append(html.Div(
            children=dash_draggable.dash_draggable(id='dragger',
                        handle='.handle',
                        
                        children=[
                            html.Div([
                                sd_material_ui.Paper(children=[
                                    sd_material_ui.IconButton(
                                        id='button',
                                        iconClassName='fas fa-grip-lines',
                                        iconStyle={'color': 'grey',
                                                   'width': 50,
                                                   'height': 50,
                                                   'position': 'relative',
                                                   'top': '2px',
                                                   'left': '-12px'},
                                        tooltip='Drag Me', touch=True,
                                        tooltipPosition='bottom-right')],
                                    zDepth=3,
                                    circle=True,
                                    style=dict(height=50,
                                               width=50,
                                               textAlign='center',
                                               position='relative',
                                               display='inline-block',
                                               top='25px',
                                               left='-25px')
                                )], className='handle no-print'),
                                dcc.Graph(
                            id='Box',
                            figure={
                    'data':boox,
                    
                    'layout':go.Layout(title= "Box Plot",  boxmode='group' ),
                     }
                    ),
                    text,
                           
                        ])
                ))
            
            
            
            
         
    return graphs, graphs
        


@app.callback([Output('scatter1', 'figure'),
                Output('kmeansReport','figure')],
              [Input('tablef', 'data'),
              Input('input','value'),
              Input('dropdown_table_filterColumn','value')])
def k_means(rows,input_value, selected):
    df = pd.DataFrame(rows)
    first_selection = selected[0]
    second_selection = selected[1]

    def get_index(name):
        '''
        return the index of a column name
        '''
        for column in df.columns:
            if column == name:
                index = df.columns.get_loc(column)
                return index
            
    xi = get_index(first_selection)
    yi = get_index(second_selection)

    X = df.iloc[:,[xi,yi]].values
    # print(X)
    if input_value is None:
        raise dash.exceptions.PreventUpdate()
    else:
        
        wcss = []
        for i in range(1,11):
            kmeans = KMeans(n_clusters = i, init= 'k-means++', max_iter = 300, n_init= 10 )
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
        kmeans = KMeans(n_clusters = int(input_value), init = 'k-means++', max_iter= 300, n_init= 10)
        y_kmeans = kmeans.fit_predict(X)
        # print(y_kmeans)
       
        data = []
        
        trace1 = {
        "x": X[y_kmeans == 0, 0], 
        "y": X[y_kmeans == 0, 1], 
        "marker": {
            "color": "blue", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 0", 
        "type": "scatter"
        }
        trace2 = {
        "x": X[y_kmeans == 1, 0], 
        "y": X[y_kmeans == 1, 1], 
        "marker": {
            "color": "green", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 1", 
        "type": "scatter"
        }
        trace3 = {
        "x": X[y_kmeans == 2, 0], 
        "y": X[y_kmeans == 2, 1], 
        "marker": {
            "color": "red", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 2", 
        "type": "scatter"
        }
        trace4 = {
        "x": X[y_kmeans == 3, 0], 
        "y": X[y_kmeans == 3, 1], 
        "marker": {
            "color": "yellow", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 3", 
        "type": "scatter"
        }
        trace5 = {
        "x": X[y_kmeans == 4, 0], 
        "y": X[y_kmeans == 4, 1], 
        "marker": {
            "color": "black", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 4", 
        "type": "scatter"
        }
        trace6 = {
        "x": X[y_kmeans == 5, 0], 
        "y": X[y_kmeans == 5, 1], 
        "marker": {
            "color": "purple", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 5", 
        "type": "scatter"
        }
        trace7 = {
        "x": X[y_kmeans == 6, 0], 
        "y": X[y_kmeans == 6, 1], 
        "marker": {
            "color": "#38EAD9", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 6", 
        "type": "scatter"
        }
        trace8 = {
        "x": X[y_kmeans == 7, 0], 
        "y": X[y_kmeans == 7, 1], 
        "marker": {
            "color": "#F96A06", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 7", 
        "type": "scatter"
        }
        trace9 = {
        "x": X[y_kmeans == 8, 0], 
        "y": X[y_kmeans == 8, 1], 
        "marker": {
            "color": "#06F909", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 8", 
        "type": "scatter"
        }
        trace10 = {
        "x": X[y_kmeans == 9, 0], 
        "y": X[y_kmeans == 9, 1], 
        "marker": {
            "color": "#F708DD", 
            "line": {
            "color": "white", 
            "width": 0.5
            }, 
            "size": 12
        }, 
        "mode": "markers", 
        "name": "K-Means Cluster 9", 
        "type": "scatter"
        }
        
        data.append(trace1)
        data.append(trace2)
        data.append(trace3)
        data.append(trace4)
        data.append(trace5)
        data.append(trace6)
        data.append(trace7)
        data.append(trace8)
        data.append(trace9)
        data.append(trace10)

        layout = {
        "legend": {"font": {"size": 16}}, 
        "title": f"K-Means Clustering K = {input_value}", 
        "titlefont": {"size": 24}, 
        "xaxis": {
            
            "showgrid": True, 
            "showticklabels": True, 
            "ticks": "", 
            "zeroline": False
        }, 
        "yaxis": {
            
            "showgrid": True, 
            "showticklabels":True, 
            "ticks": "", 
            "zeroline": False
        }
        }
        return {'data': data, 'layout': layout}, {'data': data, 'layout': layout}

    
        
@app.callback(Output('elbow', 'figure'),
              [Input('tablef', 'data'),
              Input('dropdown_table_filterColumn','value')])
def elbow_method(rows, selected):
    df = pd.DataFrame(rows)
    first_selection = selected[0]
    second_selection = selected[1]

    def get_index(name):
        '''
        return the index of a column name
        '''
        for column in df.columns:
            if column == name:
                index = df.columns.get_loc(column)
                return index
            
    xi = get_index(first_selection)
    yi = get_index(second_selection)


    X = df.iloc[:,[xi,yi]].values
    
    
    wcss = []
    for i in range(1,11):
        kmeans = KMeans(n_clusters = i, init= 'k-means++', max_iter = 300, n_init= 10 )
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    kmeans = KMeans(n_clusters = 3, init = 'k-means++', max_iter= 300, n_init= 10)
    y_kmeans = kmeans.fit_predict(X)
    # print(y_kmeans)
    
    return {

            'data':[go.Scatter(
                x = list(range(1,11)),
                y = list(wcss),
                mode = 'lines+markers',
                marker = {
                    'color': 'rgb(255,0,0)'
                }
            )],
            'layout':go.Layout(title= 'The Elbow Method')
        }


#Toggle the table in the repot tab
@app.callback(
   Output('table-toggle','style'),
   [Input('toggle-table','on')])

def show_hide_table(visibility_state):
    # print(f"The status is {visibility_state}")
    
    if visibility_state == True:
        return {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}
#Toggle the clustering in the repot tab
@app.callback(
   Output('toggle-clusters','style'),
   [Input('toggle-kmeans','on')])

def show_hide_kmeans(visibility_state):
    
    
    if visibility_state == True:
        return {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}

#Add text Area in the report
@app.callback(Output('textArea', 'children'),
              [Input('button-text', 'n_clicks'),])
def add_textArea(click):
    textArea = []
    if click < 1:
        print ("no click")
    else:
        for c in range (click):   
            # print(f"click click click{click}")
            textArea.append(html.Div(
                children=dash_draggable.dash_draggable(id='dragger',
                            handle='.handle',
                            defaultPosition={'x': 50, 'y': 50},
                            children=[
                                html.Div([
                                    sd_material_ui.Paper(children=[
                                        sd_material_ui.IconButton(
                                            id='button',
                                            iconClassName='fas fa-grip-lines',
                                            iconStyle={'color': 'grey',
                                                    'width': 50,
                                                    'height': 50,
                                                    'position': 'relative',
                                                    'top': '2px',
                                                    'left': '-12px'},
                                            tooltip='Drag Me', touch=True,
                                            tooltipPosition='bottom-right')],
                                        zDepth=3,
                                        circle=True,
                                        style=dict(height=50,
                                                width=50,
                                                textAlign='center',
                                                position='relative',
                                                display='inline',
                                                top='25px',
                                                left='-25px')
                                    )], className='handle no-print'),
                                dcc.Textarea(
                                            id='text',
                                            # placeholder='Enter a value...',
                                            draggable = True,
                                            value='',
                                            style={'width': '100%'}
                                                ),
                            
                            ])

                            
                    ))
    return textArea

##########################
# tab5content stuff
#######################
@app.callback([Output('data', 'options'),
            Output('group', 'options')],
              [Input('powerbutton', 'False'),
               Input('tablef', 'data')])
def update_data_dropdown(value, tablerows):
    if value == False:
        print ("df empty")
        return [], []

    else:
        dff = pd.DataFrame(tablerows) # <- problem! dff stays empty even though table was uploaded

        print ("updating... dff empty?:"), dff.empty #result is True, labels stay empty

        return [{'label': i, 'value': i} for i in (list(dff))], [{'label': i, 'value': i} for i in (list(dff))]

#FIXME:
@app.callback([Output('card', 'children'),
                Output('overview','children')],
               
            [Input('tablef', 'data'),
            Input('view','value'),
            Input('data','value'),
            Input('group','value')])

def return_metrics(rows,metric,selected,group):
    df = pd.DataFrame(rows)

    sel= []
    for s in selected:
        sel.append(s)

    selDescribe = (df[sel[0]].describe()).tolist()
    mmetrics = []
    selSum = []
    selAvg = []
    selMax = []
    selMin = []
    for i in sel:
        selSum.append((df[i].sum()))
        selAvg.append((df[i].mean()))
        selMax.append((df[i].max()))
        selMin.append((df[i].min()))
     
    cards =[]

    if df.empty or metric is None:
        raise dash.exceptions.PreventUpdate()
    else:
        for i,j in zip (range(len(sel)), sel):
            for values in metric:
                if values == 'count' :
                    cards.append(html.Div(
                children=dash_draggable.dash_draggable(id='dragger',
                            handle='.handle',
                            defaultPosition={'x': 50, 'y': 50},
                            children=[
                                html.Div([
                                    sd_material_ui.Paper(children=[
                                        sd_material_ui.IconButton(
                                            id='button',
                                            iconClassName='fas fa-grip-lines',
                                            iconStyle={'color': 'grey',
                                                    'width': 50,
                                                    'height': 50,
                                                    'position': 'relative',
                                                    'top': '2px',
                                                    'left': '-12px'},
                                            tooltip='Drag Me', touch=True,
                                            tooltipPosition='bottom-right')],
                                        zDepth=3,
                                        circle=True,
                                        style=dict(height=50,
                                                width=50,
                                                textAlign='center',
                                                position='relative',
                                                display='inline',
                                                top='25px',
                                                left='-25px')
                                    )], className='handle'),
                                html.Div([
                                        html.Div([
                                            html.Div([
                                                html.Div([
                                                    html.H5(f"Count of {j}" ,className='text-center', id='title'),
                                                ],className='card-header'),
                                                html.H5(selDescribe[0], className='card-title text-center', id='metrics'),
                                            ],className='card-body text-primary'),
                                        ],className='card border-primary mb-3'),
                                        ],className='col-sm-3', style={'max-width':'18rem'}),
                            
                            ]),        
                    ))
                    
                elif values == 'sum':
                    cards.append(html.Div(
                children=dash_draggable.dash_draggable(id='dragger',
                            handle='.handle',
                            defaultPosition={'x': 50, 'y': 50},
                            children=[
                                html.Div([
                                    sd_material_ui.Paper(children=[
                                        sd_material_ui.IconButton(
                                            id='button',
                                            iconClassName='fas fa-grip-lines',
                                            iconStyle={'color': 'grey',
                                                    'width': 50,
                                                    'height': 50,
                                                    'position': 'relative',
                                                    'top': '2px',
                                                    'left': '-12px'},
                                            tooltip='Drag Me', touch=True,
                                            tooltipPosition='bottom-right')],
                                        zDepth=3,
                                        circle=True,
                                        style=dict(height=50,
                                                width=50,
                                                textAlign='center',
                                                position='relative',
                                                display='inline',
                                                top='25px',
                                                left='-25px')
                                    )], className='handle'),
                                html.Div([
                                        html.Div([
                                            html.Div([
                                                html.Div([
                                                    html.H5(f"Sum of All {j}" ,className='text-center', id='title'),
                                                ],className='card-header'),
                                                html.H5(selSum[i], className='card-title text-center', id='metrics'),
                                            ],className='card-body text-primary'),
                                        ],className='card border-primary mb-3'),
                                        ],className='col-sm-3', style={'max-width':'18rem'})
                            
                            ]),        
                    ))
                    

        
                elif values == 'avg':
                    cards.append(html.Div(
                children=dash_draggable.dash_draggable(id='dragger',
                            handle='.handle',
                            defaultPosition={'x': 50, 'y': 50},
                            children=[
                                html.Div([
                                    sd_material_ui.Paper(children=[
                                        sd_material_ui.IconButton(
                                            id='button',
                                            iconClassName='fas fa-grip-lines',
                                            iconStyle={'color': 'grey',
                                                    'width': 50,
                                                    'height': 50,
                                                    'position': 'relative',
                                                    'top': '2px',
                                                    'left': '-12px'},
                                            tooltip='Drag Me', touch=True,
                                            tooltipPosition='bottom-right')],
                                        zDepth=3,
                                        circle=True,
                                        style=dict(height=50,
                                                width=50,
                                                textAlign='center',
                                                position='relative',
                                                display='inline',
                                                top='25px',
                                                left='-25px')
                                    )], className='handle'),
                                html.Div([
                                        html.Div([
                                            html.Div([
                                                html.Div([
                                                    html.H5(f"Average of {j}" ,className='text-center', id='title'),
                                                ],className='card-header'),
                                                html.H5(selAvg[i], className='card-title text-center', id='metrics'),
                                            ],className='card-body text-primary'),
                                        ],className='card border-primary mb-3'),
                                        ],className='col-sm-3', style={'max-width':'18rem'})
                            
                            ]),        
                    ))
                    

                    
            
                elif values == 'max':
                    cards.append(html.Div(
                children=dash_draggable.dash_draggable(id='dragger',
                            handle='.handle',
                            defaultPosition={'x': 50, 'y': 50},
                            children=[
                                html.Div([
                                    sd_material_ui.Paper(children=[
                                        sd_material_ui.IconButton(
                                            id='button',
                                            iconClassName='fas fa-grip-lines',
                                            iconStyle={'color': 'grey',
                                                    'width': 50,
                                                    'height': 50,
                                                    'position': 'relative',
                                                    'top': '2px',
                                                    'left': '-12px'},
                                            tooltip='Drag Me', touch=True,
                                            tooltipPosition='bottom-right')],
                                        zDepth=3,
                                        circle=True,
                                        style=dict(height=50,
                                                width=50,
                                                textAlign='center',
                                                position='relative',
                                                display='inline',
                                                top='25px',
                                                left='-25px')
                                    )], className='handle'),
                                html.Div([
                                        html.Div([
                                            html.Div([
                                                html.Div([
                                                    html.H5(f"Max of {j}" ,className='text-center', id='title'),
                                                ],className='card-header'),
                                                html.H5(selMax[i], className='card-title text-center', id='metrics'),
                                            ],className='card-body text-danger'),
                                        ],className='card border-danger mb-3'),
                                        ],className='col-sm-3', style={'max-width':'18rem'})
                            
                            ]),        
                    ))
                   
                elif values =='min':
                    cards.append(html.Div(
                children=dash_draggable.dash_draggable(id='dragger',
                            handle='.handle',
                            defaultPosition={'x': 50, 'y': 50},
                            children=[
                                html.Div([
                                    sd_material_ui.Paper(children=[
                                        sd_material_ui.IconButton(
                                            id='button',
                                            iconClassName='fas fa-grip-lines',
                                            iconStyle={'color': 'grey',
                                                    'width': 50,
                                                    'height': 50,
                                                    'position': 'relative',
                                                    'top': '2px',
                                                    'left': '-12px'},
                                            tooltip='Drag Me', touch=True,
                                            tooltipPosition='bottom-right')],
                                        zDepth=3,
                                        circle=True,
                                        style=dict(height=50,
                                                width=50,
                                                textAlign='center',
                                                position='relative',
                                                display='inline',
                                                top='25px',
                                                left='-25px')
                                    )], className='handle'),
                                html.Div([
                                        html.Div([
                                            html.Div([
                                                html.Div([
                                                    html.H5(f"Min of {j}" ,className='text-center', id='title'),
                                                ],className='card-header'),
                                                html.H5(selMin[i], className='card-title text-center', id='metrics'),
                                            ],className='card-body text-success'),
                                        ],className='card border-success mb-3'),
                                        ],className='col-sm-3', style={'max-width':'18rem'})
                            
                            ]),        
                    ))
                   
           
    
    return cards, cards
###################
# Grouped by 
###################
@app.callback([Output('outTable', 'children'),
                Output('overview-table','children')],
                
            [Input('tablef', 'data'),
            Input('view','value'),
            Input('data','value'),
            Input('group','value'),])

def return_gb(rows,metric,selected,group):
    df = pd.DataFrame(rows)

    sel= []
    for s in selected:
        sel.append(s)
    gp= []
    for g in group:
        gp.append(g)

    gb = df[[sel[0],sel[1]]].groupby(df[gp[0]])
    gbtable = []
    if df.empty or gp is None or metric is None:
        raise dash.exceptions.PreventUpdate()
    else:
        for values in metric:
            if values == 'count':
                gb = df[[sel[0],sel[1]]].groupby(df[gp[0]]).count().reset_index()
            elif values == 'sum':
                gb = df[[sel[0],sel[1]]].groupby(df[gp[0]]).sum().reset_index()
            elif values == 'avg':
                gb = df[[sel[0],sel[1]]].groupby(df[gp[0]]).mean().reset_index()
            elif values == 'max':
                gb = df[[sel[0],sel[1]]].groupby(df[gp[0]]).max().reset_index()
            elif values == 'min':
                gb = df[[sel[0],sel[1]]].groupby(df[gp[0]]).min().reset_index()
           
                

            
    return html.Div(
                children=dash_draggable.dash_draggable(id='dragger',
                            handle='.handle',
                            defaultPosition={'x': 50, 'y': 50},
                            children=[
                                html.Div([
                                    sd_material_ui.Paper(children=[
                                        sd_material_ui.IconButton(
                                            id='button',
                                            iconClassName='fas fa-grip-lines',
                                            iconStyle={'color': 'grey',
                                                    'width': 50,
                                                    'height': 50,
                                                    'position': 'relative',
                                                    'top': '2px',
                                                    'left': '-12px'},
                                            tooltip='Drag Me', touch=True,
                                            tooltipPosition='bottom-right')],
                                        zDepth=3,
                                        circle=True,
                                        style=dict(height=50,
                                                width=50,
                                                textAlign='center',
                                                position='relative',
                                                display='inline',
                                                top='25px',
                                                left='-25px')
                                    )], className='handle'),
                                 dash_table.DataTable(
                                                    id ='groupby',
                                                    data= gb.to_dict('records'),
                                                    columns=[{"name": i, "id": i} for i in (gb.columns)],
                                                    style_cell={'width': '150px'},
                                                    n_fixed_rows=1,
                                                    
                                                ),
                            
                            ])

                            
                    ),html.Div(
                children=dash_draggable.dash_draggable(id='dragger',
                            handle='.handle',
                            defaultPosition={'x': 50, 'y': 50},
                            children=[
                                html.Div([
                                    sd_material_ui.Paper(children=[
                                        sd_material_ui.IconButton(
                                            id='button',
                                            iconClassName='fas fa-grip-lines',
                                            iconStyle={'color': 'grey',
                                                    'width': 50,
                                                    'height': 50,
                                                    'position': 'relative',
                                                    'top': '2px',
                                                    'left': '-12px'},
                                            tooltip='Drag Me', touch=True,
                                            tooltipPosition='bottom-right')],
                                        zDepth=3,
                                        circle=True,
                                        style=dict(height=50,
                                                width=50,
                                                textAlign='center',
                                                position='relative',
                                                display='inline',
                                                top='25px',
                                                left='-25px')
                                    )], className='handle'),
                                 dash_table.DataTable(
                                                    id ='groupby',
                                                    data= gb.to_dict('records'),
                                                    columns=[{"name": i, "id": i} for i in (gb.columns)],
                                                    style_cell={'width': '150px'},
                                                    n_fixed_rows=1,
                                                    
                                                ),
                            
                            ])

                            
                    )
    
#Write sql queries (not finished: works only in terminal)
@app.callback(Output('out', 'children'),
            [Input('tablef', 'data'),
            Input('sql','value')])

def return_gb(rows, value):

    df = pd.DataFrame(rows)
    
    q1 = """SELECT df.Team FROM df """
 
    # print (f"your qurey is :{ps.sqldf(q1, locals())}")
    # create aliases for your dataframes
#     query_string = """
#     select * from df
# """

#     new_dataframe = pandasql.sqldf(query_string, globals()).head()
#     print(f"alaa :{new_dataframe}")
    



    
    
# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })
external_css = [
               

                "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                "https://use.fontawesome.com/releases/v5.8.2/css/all.css",
                "https://cdnjs.cloudflare.com/ajax/libs/gridstack.js/0.4.0/gridstack.css"
               
               ]
               #"https://codepen.io/AllenGT/pen/VOaRdP.css",

for css in external_css:
    app.css.append_css({"external_url": css})


app.scripts.config.serve_locally = True


external_js = ["https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.0/jquery-ui.js",

    ]

# for js in external_js:
#     app.scripts.append_script({"external_url": js}) 
if __name__ == '__main__':
    app.run_server(debug=False)