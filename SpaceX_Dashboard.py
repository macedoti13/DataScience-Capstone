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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All sites', 'value': 'All'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
                                             ],
                                             value='All',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                                min=0, max=10000, step=1000, 
                                                marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'},
                                                value=[min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'All':
        df = filtered_df.groupby(['Launch Site'])['class'].sum().to_frame()
        df = df.reset_index()
        fig = px.pie(df, values='class', names='Launch Site', title='Total success launches by site')
    else:
        df = filtered_df[filtered_df['Launch Site'] == entered_site]['class'].value_counts().to_frame()
        df['name'] = ['failure', 'success']
        fig = px.pie(df, values='class', names='name', title=f'Total Success Launches for {entered_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))

def get_scatter_plot(entered_site, slider_interval):
    df = spacex_df
    if entered_site == 'All':
        df2 = df[df["Payload Mass (kg)"] >= slider_interval[0]]
        df3 = df2[df["Payload Mass (kg)"] <= slider_interval[1]]
        fig2 = px.scatter(df3, y='class', x='Payload Mass (kg)', color='Booster Version Category')
    else:
        df = df[df['Launch Site'] == entered_site]
        df2 = df[df["Payload Mass (kg)"] >= slider_interval[0]]
        df3 = df2[df["Payload Mass (kg)"] <= slider_interval[1]]
        fig2 = px.scatter(df3, y='class', x='Payload Mass (kg)', color='Booster Version Category')
    return fig2
        

# Run the app
if __name__ == '__main__':
    app.run_server()