#### Carbon Intensity for sector and country of risk

import plotly.express as px

def sector_CI(file,year):
    df = file[file['YEAR'] == int(year)].sort_values('CARBON_INTENSITY')
    fig = px.bar(df, x="CARBON_INTENSITY", y="ECONOMIC_SECTOR", orientation='h', color_discrete_sequence=['#b68ee5'])
    fig.update_layout(template="plotly_dark",
                      title_text='Carbon Intensity' + "<br><sup>(tCO\u2082/$ million revenue)</sup>",
                      legend_title_text="",
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
        title_text="Economic Sector",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Carbon Intensity (tCO\u2082/$ million revenue)",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_traces(width=0.6)
    return fig


# country carbon intensity
def country_CI(file,year):
    df = file[file['YEAR'] == int(year)].sort_values('CARBON_INTENSITY')
    fig = px.bar(df, x="CARBON_INTENSITY", y="RISK_COUNTRY", orientation='h', color_discrete_sequence=['#b68ee5'])
    fig.update_layout(template="plotly_dark",
                      title_text='Carbon Intensity' + "<br><sup>(tCO\u2082/$ million revenue)</sup>",
                      legend_title_text="",
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
        title_text="Country of Risk",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Carbon Intensity (tCO\u2082/$ million revenue)",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_traces(width=0.6)
    return fig

# bonds purchased sector wise
def sector_bonds(file,year):
    data = file[file['YEAR'] == int(year)].sort_values('NUMBER_OF_BONDS')
    fig = px.bar(data, x="NUMBER_OF_BONDS", y="ECONOMIC_SECTOR", orientation='h', color_discrete_sequence=['#b0b8f2'])
    fig.update_layout(template="plotly_dark", title_text='Bonds distribution for ' + str(year), legend_title_text="",
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
        title_text="Economic Sector",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Number of Bonds",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_traces(width=0.6)
    return fig

def country_bonds(file,year):
    data = file[file['YEAR'] == int(year)].sort_values('NUMBER_OF_BONDS')
    fig = px.bar(data, x="NUMBER_OF_BONDS", y="RISK_COUNTRY", orientation='h', color_discrete_sequence=['#b0b8f2'])
    fig.update_layout(template="plotly_dark", title_text='Bonds distribution for ' + str(year), legend_title_text="",
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
        title_text="Country of Risk",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Number of Bonds",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_traces(width=0.6)
    return fig
