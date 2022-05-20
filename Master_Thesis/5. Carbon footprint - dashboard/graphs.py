import plotly.graph_objects as go
from functions_file import *
import plotly.express as px
# heatmap for WACI
def heatmap_mean_waci(file,key):

    # mean_waci
    mean_waci = mean_weighted_carbon_intensity(key,file)
    fig = go.Figure(data=go.Heatmap(df_to_plotly(mean_waci), colorscale='blugrn',xgap=2,ygap=2))
    fig.update_layout(template="plotly_dark",title_text = 'Mean Weighted Carbon Intensity (WACI)'+
                                                          "<br><sup>(tCO\u2082/$ million revenue)</sup>")
    return fig

def heatmap_median_waci(file,key):
    # median_waci
    median_waci = median_weighted_carbon_intensity(key,file)
    fig = go.Figure(data=go.Heatmap(df_to_plotly(median_waci), colorscale='blugrn',xgap = 2,ygap=2))
    fig.update_layout(template="plotly_dark",title_text = 'Median Weighted Carbon Intensity (WACI)'+
                                                          "<br><sup>(tCO\u2082/$ million revenue)</sup>")
    return fig


def table_figure(file,year,index):
    df = file[file['Year'] == int(year)]
    sector = df['Economic Sector'].unique()
    table = df[df['Economic Sector']==sector[index]]
    data = table.drop(['Economic Sector','Year'],axis = 1)
    data = data.sort_values(by = 'Avg. Emission Intensity',ascending=False)
    data['Avg. Emission Intensity'] = data['Avg. Emission Intensity'].round(1)
    data = data.drop_duplicates()
    data = data.iloc[:10, :]
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(data.columns.tolist()),
                #fill_color = 'rgb(18, 116, 117)',
                align='left'),
    cells=dict(values=[data['Issuer Name'].tolist(), data['Risk Country'].tolist(), data['Number of bonds'].tolist(),data['Avg. Emission Intensity'].tolist()],
               align='left',height=30,
               #fill_color='rgb(189, 206, 181)'
               ),
    columnwidth=[500,400,300,300])
])
    fig.update_layout(template="plotly_dark",title_text =  sector[index] ,
                      margin=dict(l=30, r=30, t=60, b=30)
                      )
    return fig

def graph(file):
    if file['RISK_COUNTRY'].nunique() == 1:
        fig = px.line(file,x='YEAR', y='MEAN_WACI')
    else:
        fig = px.line(file, x='YEAR', y='MEAN_WACI', color='RISK_COUNTRY')
    return fig

def sector_waci_time_graph(file,sector):
    data = file[file['ECONOMIC_SECTOR']==sector]
    fig = graph(data)
    fig.update_layout(template="plotly_dark", title_text='Mean WACI for ' + str(sector),
        yaxis = dict(
            tickfont=dict(size=8)), xaxis = dict(
            tickfont=dict(size=8)), legend = dict(
            y=1,
            x=1, font=dict(size=8)
        ), font = dict(size=10),
                          margin=dict(l=30, r=30, t=60, b=30))

    fig.update_yaxes(
            title_text="Mean WACI",
            title_font={"size": 10},
            title_standoff=10)
    fig.update_xaxes(
            title_text="Year",
            title_font={"size": 10},
            title_standoff=10)
    return fig

def contribution_to_waci(file,year):
    df = file[file['YEAR'] == int(year)].sort_values('Contribution', ascending=True)
    fig = go.Figure()

    fig.add_trace(go.Bar(y=df['ECONOMIC_SECTOR'].tolist(),
                         x=df['WEIGHTS'].tolist(),
                         name="Weights", orientation='h', marker = {'color':'#b68ee5'}
                         ))

    fig.add_trace(go.Bar(y=df['ECONOMIC_SECTOR'].tolist(),
                         x=df['Contribution'].tolist(),
                         name="Contribution to WACI", orientation='h', marker = {'color':'#b0b8f2'}
                         ))

    fig.update_layout(title_text="Sectoral contributions to WACI for " + str(year), template="plotly_dark",
                      font=dict(size=10))

    fig.update_yaxes(
        title_text="Economic Sector",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Contribution to WACI (%)",
        title_font={"size": 10},
        title_standoff=10)
    return fig

def yearly_mean_waci_sector(file,year):
    df = file[file['YEAR'] == int(year)].sort_values(
        'MEAN_WACI')
    fig = px.bar(df, x="MEAN_WACI", y="ECONOMIC_SECTOR", orientation='h', color_discrete_sequence=['#b68ee5'],
                 hover_data={'MEAN_WACI': True, 'ECONOMIC_SECTOR': True})
    fig.update_layout(template="plotly_dark",
                      title_text='Weighted Average Carbon Intensity' + "<br><sup>(tCO\u2082/$ million revenue)</sup>"
                      , legend_title_text="",
                      yaxis=dict(
                          tickfont=dict(size=8)), xaxis=dict(
            tickfont=dict(size=8)), legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.25,
            xanchor="right",
            x=1, font=dict(size=8)
        ), font=dict(size=10),
                      margin=dict(l=30, r=30, t=60, b=30))
    fig.update_yaxes(
        title_text="Economic Sectoes",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Weighted Average Carbon Intensity (tCO\u2082/$ million revenue)",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_traces(width=0.6)
    return fig





