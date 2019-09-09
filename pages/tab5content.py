import dash
import dash_html_components as html
import dash_core_components as dcc

import dash_table
import dash_daq as daq


from dash.dependencies import Input, Output, State



app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout =html.Div([
    
    html.Br(),
    html.Div([
        html.Div([
             dcc.Dropdown(
        id='data',
        placeholder='Select Column',
        multi = True,
       
    ),
    
            
     
     dcc.Dropdown(
        id='view',
        multi = True,
        options=[
            {'label': 'Count', 'value': 'count'},
            {'label': 'Sum', 'value': 'sum'},
            {'label': 'Average', 'value': 'avg'},
            {'label': 'Max', 'value': 'max'},
            {'label': 'Min', 'value': 'min'},
            

        ],
        placeholder='View',
       
    ),
     dcc.Dropdown(
        id='group',
        placeholder='Grouped By',
        multi = True,
        
    ),
    ], className="dropdowns"),
    html.Div([
         html.Div(id='outputt')

    ]),

# html.Div([
#          dash_table.DataTable(
#         id='tableColumn',
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

], id='card'),


]),
html.Div([
    html.Div([

    ],id="outTable")   
    ]),
    
])





if __name__ == '__main__':
    app.run_server(debug=True)