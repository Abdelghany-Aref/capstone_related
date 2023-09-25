# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



# Create the Dash app
app = dash.Dash(__name__)


max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Define the layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Task 1: Dropdown for Launch Site selection
dcc.Dropdown(
    id='site-dropdown',
    options=[
        {'label': 'All Sites', 'value': 'ALL'},  # Default value for all sites
        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},   
        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},   
        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},   
        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},   
    ]),

    # Task 2: Pie chart (empty for now)
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # Task 3: Slider for payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1,
        marks={i: str(i) for i in range(min_payload, max_payload + 1)},
        value=[min_payload, max_payload],
    ),

    # Task 4: Scatter chart 
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Define a callback function for Task 2
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    
    filt= spacex_df['Launch Site'] == selected_site
    values = list(spacex_df[filt].groupby(['class']).count().iloc[:, 0].values)
    
    data = [
        {
            'labels': ['Failure', 'Success'],
            'values':values,  
            'type': 'pie',
        }
    ]
    layout = {'title': f'Successful Launches for {selected_site}'}
    return {'data': data, 'layout': layout}

# Define a callback function for Task 4
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    
    filt = (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1]) & (
        spacex_df['Launch Site'] == selected_site)
    temp_df = spacex_df[filt]
    payload = list(temp_df[['Payload Mass (kg)','class']].values[:, 0])
    classes = list(temp_df[['Payload Mass (kg)','class']].values[:, 1])
    
    data = [
        {
            'x': payload,  
            'y': classes,  
            'mode': 'markers',
            'type': 'scatter',
        }
    ]
    layout = {'title': f'Scatter Chart for {selected_site}'}
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
