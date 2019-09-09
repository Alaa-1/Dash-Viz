import dash
import dash_html_components as html
import dash_core_components as dcc
import sd_material_ui
import dash_bootstrap_components as dbc

import dash_table
import dash_daq as daq


from dash.dependencies import Input, Output, State



app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

#Tab 1 content and logic goes here 
theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#f62e24',
    'secondary': '#f62e24',
}

app.layout =html.Div([
 html.Div([

     html.Br(),

    html.H5("Upload Files"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
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
        multiple=False),
    html.Br(),
    
        daq.PowerButton(
        on=False,
        color=theme['primary'],
        id='powerbutton',
        className='dark-theme-control',
        size=70,
        style={
            'display': 'none',}
    ),
    #  sd_material_ui.FlatButton(id='iut', label='Click me', backgroundColor='#2ab7ca'),

        
        html.Br(),
    
        


# <div class="card border-primary mb-3" style="max-width: 18rem;">
#   <div class="card-header">Header</div>
#   <div class="card-body text-primary">
#     <h5 class="card-title">Primary card title</h5>
#     <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
#   </div>
    







    
    html.Div([
        
     sd_material_ui.IconButton(id='upload',
                              iconClassName='fas fa-cloud-upload-alt',
                              iconStyle={'color':' #899bde', 'width': 100, 'height': 100, 'fontSize':160},
                              ),  
                              html.Div([
                              html.H5("No files were uploaded :(")],className="uploadText"),
          
        # html.H5("No files were uploaded"),

      ], className="centerDiv", id="centerDiv"),
    
    html.Br(),

    # html.H5("Updated Table"),
    html.Div(id="alert"),
    html.Div(id = 'output'),
    html.Div(
        dash_table.DataTable(
    id ='table',
    data=[],
    columns=[],
    style_cell={'width': '150px'},
    n_fixed_rows=1,
    
),
         
    ),
], className='container'),
   
]) #f2f8fe


# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })


# # # # # # # # #
# detail the way that external_css and external_js work and link to alternative method locally hosted
# # # # # # # # #



if __name__ == '__main__':
    app.run_server(debug=True)