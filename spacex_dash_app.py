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
site_names = list(spacex_df["Launch Site"].unique())
options_dropdown=[{'label': 'All Sites', 'value': 'ALL'}]+[{'label': name, 'value': name} for name in site_names]
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options = options_dropdown,
                                            value='ALL',
                                            placeholder='Select a Launch Site',
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000:'5000', 7500: '7500', 10000: '10000'},
                                                value=[2500, 7500])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='All Sites Success Rate')
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"]==entered_site]
        test = filtered_df.groupby("class").count().reset_index()
        fig = px.pie(test, values='Launch Site', 
        names='class', 
        title=f'{entered_site} site Success Rate')
        return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, payload_interval):
    minmass, maxmass = payload_interval
    cond1 = spacex_df["Payload Mass (kg)"]>=minmass
    cond2 = spacex_df["Payload Mass (kg)"]<=maxmass
    mass_filter_df = spacex_df[cond1 & cond2]

    if entered_site == 'ALL':
        fig = px.scatter(mass_filter_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    
    else:
        filtered_df = mass_filter_df[mass_filter_df["Launch Site"]==entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
