# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True),
                                html.Br(),
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: str(i) for i in range(0, 10001, 1000)},
                                                value=[min_payload, max_payload]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Callback for pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='class', title='Total Success Launches')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Success vs Failed Launches at {selected_site}')
    
    return fig

# Callback for scatter chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(selected_site, selected_payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                (spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title=f'Payload vs Success for {selected_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
