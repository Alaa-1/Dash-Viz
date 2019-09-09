import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table


from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    # html.H5("Enter the number of k"),
    # dcc.Input(id='input', type='text'),
    dcc.Graph(id = 'elbow'),
    html.Br(),
    html.H5("Enter the number of k"),
    dcc.Input(id='input', type='text'),
    dcc.Graph(id = 'scatter1')
    
    ],className="container")
    


# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })
if __name__ == '__main__':
    app.run_server(debug=True)