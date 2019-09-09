import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc
import sd_material_ui


from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout =html.Div([
html.Div([
    
 html.Div([
         dash_table.DataTable(
        id='tablef',
        columns=[],
        data=[],
        editable=True,
        filtering=True,
        sorting=True,
        sorting_type="multi",
        row_selectable="multi",
        row_deletable=True,
        selected_rows=[],
         style_cell={'width': '150px'},
        n_fixed_rows=1,
        
        pagination_mode="fe",
            pagination_settings={
                "displayed_pages": 1,
                "current_page": 0,
                "page_size": 5,
            },
            navigation="page",
    ),
   
 ]),
 
html.Div([
        
    daq.ColorPicker(
        id='my-color-picker',
        label='Color Picker',
        value={"hex": "#0B6AAD"},
    ),
   
 ]),
 
html.Br(),
html.Hr(),

html.Div([
    html.Div([
    html.H5("Visualize"),
    # sd_material_ui.IconButton(id='barChartIcon',
    #                           iconClassName='far fa-chart-bar',
    #                           iconStyle={ 'width': 100, 'height': 100, 'fontSize':40},
    #                           ),
    dcc.Dropdown(id='dropdown_viz',
        multi = True,
        placeholder='Choose visualization',
        options=[
        {'label': 'Bar', 'value': 'B'},
        {'label': 'Scatterplot', 'value': 'S'},
        {'label': 'Pie', 'value': 'P'},
        {'label': 'Line', 'value': 'L'},
        {'label': 'Bubble', 'value': 'Bb'},
        {'label': 'Box plot', 'value': 'Bp'}

    ],
        ),
        
        
        html.Br(),
]),
html.Div([
            html.H5("Filter Column"),
    dcc.Dropdown(id='dropdown_table_filterColumn',
        multi = True,
        placeholder='Filter Column',
        ),
]),], className="drp3"),

    
#  html.Div([
# # html.Div([
# #     dcc.Graph(id='datatable-upload-graph', style={'display':'none'}),],className='col-sm-6'),
#     # html.Div([
#     # dcc.Graph(id = 'scatter',style={'display': 'none'}),],className='col-sm-6'),
#     ],className='row'),
#     html.Div([
#         html.Div([
#     dcc.Graph(id = 'pie', style={'display':'none'}),], className='col-sm-6 '),
    
#     #line chart
#     html.Div([
#     dcc.Graph(id= 'line', style={'display':'none'}),],className='col-sm-6'),
# ],className='row'),
# html.Div([daq.ColorPicker(
#   id='my-daq-colorpicker',
#   label="colorPicker"
# )]),
html.Div(
    [
],id='graphs', className='container'),
], className='container'),
], className='jumbotron jumbotron-fluid')

# app.css.append_css({
#     "external_url": 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'
# })
if __name__ == '__main__':
    app.run_server(debug=True)