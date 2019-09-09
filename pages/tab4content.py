import dash
import dash_draggable
import sd_material_ui
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_daq as daq


from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
html.Div([ 
#     html.Div([
#          dash_table.DataTable(
#         id='tableR',
#         columns=[],
#         data=[],
#         editable=True,
#         filtering=True,
#         sorting=True,
#         sorting_type="multi",
#         row_selectable="multi",
#         row_deletable=True,
#         selected_rows=[],
#          style_cell={'width': '150px'},
#         n_fixed_rows=1,
        
#         pagination_mode="fe",
#             pagination_settings={
#                 "displayed_pages": 1,
#                 "current_page": 0,
#                 "page_size": 5,
#             },
#             navigation="page",
#     ),
   
#  ]),
    html.Div([
    sd_material_ui.FlatButton( id='las-print',
                             label='Export as PDF',
                             backgroundColor='#27cddc',
                             style={'color':'white'},
                             ),], className='no-print'),
  
    
                
    html.Hr(),
    html.Br(),
    html.Div([
     sd_material_ui.IconButton(id='button-text',
                              iconClassName='fas fa-plus-circle',
                              iconStyle={'color':' #fe8a71', 'width': 100, 'height': 100, 'fontSize':40},
                              tooltip='Add textArea', touch=True,
                              tooltipPosition='bottom-right'),
    # html.Button('Add TextArea', id='button-text'),

    
    daq.BooleanSwitch(id='toggle-table', on=True, label="Toggle Table" , color ='#fe8a71'),
    daq.BooleanSwitch(id='toggle-kmeans', on=True, label="Toggle Clustering" , color ='#fe8a71'),
   ],id='wrap', className='no-print'),

    html.Div([],id='textArea'),
   
    html.Div([

    ],id="overview"),
    html.Br(),
    
                    #Dragger for the table in the report
                html.Div([
                html.Div(children=dash_draggable.dash_draggable(id='dragger1',
                        handle='.handle',
                        children=[
                            html.Div([
                                sd_material_ui.Paper(children=[
                                    sd_material_ui.IconButton(
                                        id='button1',
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
                                dash_table.DataTable(
                                id ='tableR',
                                data=[],
                                columns=[],
                                style_cell={'width': '150px'},
                                n_fixed_rows=1,
                            )
                           
                        ])
                ),],id='table-toggle'),
                html.Div([

                ],id="overview-table", className="container"),
                #Dragger for the kmeans graph in the report
    html.Div([                
    html.Div(children=dash_draggable.dash_draggable(id='dragger',
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
                            id='kmeansReport',
                            ),
                           
                        ])
                )], id='toggle-clusters'),



    html.Div([
       

    
    ], id='reportGraphs', className='container'),
        
], className='container-fluid', id='reportDiv'),
], className='jumbotron jumbotron-fluid container-fluid') 
if __name__ == '__main__':
    app.run_server(debug=True)