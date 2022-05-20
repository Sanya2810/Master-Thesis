import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

from graphs import *
from graphs_ import *
from graphs_2 import *
from dash.dependencies import Input, Output

monthly_value = pd.read_csv('Data/Monthly_Investments.csv')
country_holdings = pd.read_csv('Data/Country_values.csv')
sector_holdings = pd.read_csv('Data/Sector_values.csv')
CI_file = pd.read_csv('Data/Carbon_Intensity_Companies.csv')
bonds_sectorwise = pd.read_csv('Data/Bonds_sectorwise.csv')
bonds_country = pd.read_csv('Data/Bonds_countrywise.csv')
CI_sector = pd.read_csv('Data/Sector_CI.csv')
CI_country = pd.read_csv('Data/Country_CI.csv')
final_data = pd.read_csv('Data/Final_data.csv')
waci_data = pd.read_csv('Data/WACI_data.csv')
data = pd.read_csv('Data/Data.csv')
yearly_sector_waci = pd.read_csv('Data/Yearly_sector_WACI')
#
# emission_intensity = pd.read_excel('Emission_intensity_1.xlsx',engine='openpyxl')
# bonds = pd.read_excel('Bonds_classification_1.xlsx',engine='openpyxl')


# Adding dropdown box
dropdown = dcc.Dropdown(id="year",
                        options=[
                            {"label": '2017', 'value': '2017'},
                            {"label": '2018', 'value': '2018'},
                            {"label": '2019', 'value': '2019'},
                            {"label": '2020', 'value': '2020'},
                            {"label": '2021', 'value': '2021'},
                            {"label": '2022', 'value': '2022'}],
                        value='2017', style={"color": "black"})



dropdown2 = dcc.Dropdown(id="sector_names",
                        options=[
                            {"label": 'Automotive and parts', 'value': 'Automotive and parts'},
                            {"label": 'Beverages', 'value': 'Beverages'},
                            {"label": 'Chemicals', 'value': 'Chemicals'},
                            {"label": 'Construction & Materials', 'value': 'Construction & Materials'},
                            {"label": 'Energy and basic resources', 'value': 'Energy and basic resources'},
                            {"label": 'Food', 'value': 'Food'},
                            {"label": 'Infrastructure and transportation', 'value': 'Infrastructure and transportation'},
                            {"label": 'Insurance', 'value': 'Insurance'},
                            {"label": 'Other sectors', 'value': 'Other sectors'},
                            {"label": 'Real estate', 'value': 'Real estate'},
                            {"label": 'Telecommunication', 'value': 'Telecommunication'},
                            {"label": 'Utilities', 'value': 'Utilities'}
                        ],
                        value='Automotive and parts', style={"color": "black"})

app = dash.Dash(__name__, title="Carbon Footprint", external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    [
        html.Div(children=[html.H1(children='Carbon Footprints of the European Central Bank (ECB)',
                                   style={'textAlign': 'center', 'font-size': 42}),
                           html.Hr()]),
        dbc.Row([
            dbc.Col(dropdown, md=3)],
            justify="left"),
        dbc.Row([
            dbc.Col(dcc.Graph(id="id_graph"),width = 4),
            dbc.Col(dcc.Graph(id="id_graph2"),width = 4),
            dbc.Col(dcc.Graph(id="id_graph7"),width = 4)
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(html.P('Carbon Intensity for individual companies',style={'font-size':24,'textAlign': 'center'}))
        ],
            justify="center"),
        dbc.Row([
            dbc.Col(html.P('Top 10 carbon-intensive companies',style={'font-size':18,'textAlign': 'left'}))
        ],
            justify="left"),
        dbc.Row([
            dbc.Col(dcc.Graph(id = "id_graph8"),width = 4),
            dbc.Col(dcc.Graph(id = "id_graph12"),width = 4),
            dbc.Col(dcc.Graph(id="id_graph9"), width=4)
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(html.P('Top 10 low carbon companies',style={'font-size':18,'textAlign': 'left'}))
        ],
            justify="left"),
        dbc.Row([
            dbc.Col(dcc.Graph(id = "id_graph10"),width = 4),
            dbc.Col(dcc.Graph(id = "id_graph13"),width = 4),
            dbc.Col(dcc.Graph(id = "id_graph11"),width = 4)
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(html.P('Carbon Intensity for Economic Sector',style={'font-size':24,'textAlign': 'center'}))
        ],
            justify="center"),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(dcc.Graph(id = "id_graph5"),width = 6),
            dbc.Col(dcc.Graph(id = "id_graph6"),width = 6)
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(html.P('Carbon Intensity for Country of Risk',style={'font-size':24,'textAlign': 'center'}))
        ],
            justify="center"),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(dcc.Graph(id = "id_graph14"),width = 6),
            dbc.Col(dcc.Graph(id = "id_graph15"),width = 6)
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(html.P('Weighted Average Carbon Intensity (WACI)',style={'font-size':24,'textAlign': 'center'}))
        ],
            justify="center"),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(html.P('Yearly Sector mean WACI',style={'font-size':18,'textAlign': 'left'}))
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
    dbc.Row([
            dbc.Col(dcc.Graph(id="id_graph17"), width=6),
            dbc.Col(dcc.Graph(id="id_graph18"), width=6)
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(html.P('Yearly mean WACI for each sector and country combination',style={'font-size':18,'textAlign': 'left'}))
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="id_graph3"), width=6),
            dbc.Col(dcc.Graph(id="id_graph4"), width=6)
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(html.P('Companies driving carbon-intensity in their respective sector',style={'font-size':18,'textAlign': 'left'}))
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="table1"), width=4),
            dbc.Col(dcc.Graph(id="table2"), width=4),
            dbc.Col(dcc.Graph(id='table3'),width = 4)
        ]),
dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(html.P('Mean WACI changes over the years',style={'font-size':18,'textAlign': 'left'}))
        ]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row([
            dbc.Col(dropdown2, md=4),
            dbc.Col(dcc.Graph(id="graph16"), width=6)
        ], justify='left')
    ],
    style={'text-align': 'center', 'font-size': 18,
           # Update the background color to the entire app
           'background-color': '',
           # Change the text color for the whole app
           'color': 'white'
           },
    fluid=True)

@app.callback(
     [Output('id_graph', 'figure'),
     Output('id_graph2', 'figure'),
     Output('id_graph7', 'figure'),
     Output('id_graph8', 'figure'),
     Output('id_graph12', 'figure'),
     Output('id_graph9', 'figure'),
     Output('id_graph10', 'figure'),
     Output('id_graph13', 'figure'),
     Output('id_graph11', 'figure'),
     Output('id_graph5','figure'),
     Output('id_graph6','figure'),
     Output('id_graph14', 'figure'),
     Output('id_graph15', 'figure'),
     Output('id_graph17', 'figure'),
     Output('id_graph18', 'figure'),
     Output('id_graph3', 'figure'),
     Output('id_graph4', 'figure'),
     Output('table1','figure'),
     Output('table2','figure'),
     Output('table3','figure')
      ],
    [Input('year', 'value')]
)

def update_chart(selected_value):
    month_graph = monthly_graph(monthly_value)
    sector_breakdown = sector_graph(sector_holdings,selected_value)
    country_breakdown = country_graph(country_holdings,selected_value)
    bonds_year_graph = bonds_purchased_co(CI_file,selected_value)
    bonds_year_low = bonds_purchased_co_low(CI_file,selected_value)
    bonds_times_graph_high = time_graph_high(CI_file,selected_value)
    CI_companies_graph = carbon_intensity_co(CI_file,selected_value)
    CI_companies_graph_low = carbon_intensity_co_low(CI_file,selected_value)
    bonds_times_graph_low = time_graph_low(CI_file, selected_value)
    bonds_sector_graph = sector_bonds(bonds_sectorwise,selected_value)
    CI_sector_graph = sector_CI(CI_sector,selected_value)
    bonds_country_graph = country_bonds(bonds_country,selected_value)
    CI_country_graph = country_CI(CI_country,selected_value)
    heatmap_mean = heatmap_mean_waci(final_data,selected_value)
    heatmap_med = heatmap_median_waci(final_data,selected_value)
    table_graph = table_figure(data,selected_value,0)
    table_graph_2 = table_figure(data, selected_value, 1)
    table_graph3 = table_figure(data,selected_value,2)
    sector_contribution = contribution_to_waci(yearly_sector_waci,selected_value)
    sector_mean_waci_graph = yearly_mean_waci_sector(yearly_sector_waci,selected_value)
    return (month_graph,sector_breakdown,country_breakdown,bonds_year_graph,bonds_times_graph_high,CI_companies_graph,bonds_year_low,bonds_times_graph_low,
    CI_companies_graph_low,bonds_sector_graph,CI_sector_graph,bonds_country_graph,CI_country_graph,sector_contribution,sector_mean_waci_graph,heatmap_mean,heatmap_med,table_graph,
            table_graph_2,table_graph3)

@app.callback(
    Output('graph16','figure'),
    [Input('sector_names','value')]
)

def update_chart_2(selected_value):
    overall_time_graph = sector_waci_time_graph(waci_data,selected_value)
    return (overall_time_graph)


if __name__ == '__main__':
    app.run_server(debug=True)
