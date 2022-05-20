#### Yearly graphs and Carbon Intensity for individual companies
import plotly.express as px

def monthly_graph(data):
    data = data.sort_values(['Year', 'Month_Number'])
    data[['Month', 'Year']] = data[['Month', 'Year']].astype(str)
    data['Time'] = data.Month.str.cat(data.Year, sep="-")
    fig = px.line(data, x='Time', y='Total holdings')
    fig.update_layout(template="plotly_dark", title_text='CSPP holdings',
    yaxis = dict(
        tickfont=dict(size=8)), xaxis = dict(
        tickfont=dict(size=8)), legend = dict(
        y=1,
        x=1, font=dict(size=8)
    ), font = dict(size=10),
                      margin=dict(l=30, r=30, t=60, b=30))

    fig.update_yaxes(
        title_text="Total holdings ($m)",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Time",
        title_font={"size": 10},
        title_standoff=10)
    return fig

def sector_graph(file, year):
    data = file[file['YEAR'] == int(year)].sort_values(by='SECTOR_HOLDINGS', ascending=False)
    fig = px.bar(data, x="ECONOMIC_SECTOR", y="SECTOR_HOLDINGS",
                 color_discrete_sequence=['#b0b8f2'])
    fig.update_layout(template="plotly_dark", title_text='Sector breakdown for ' + str(year),
    yaxis = dict(
        tickfont=dict(size=8)), xaxis = dict(
        tickfont=dict(size=8)),font = dict(size = 10),
                      margin=dict(l=30, r=30, t=60, b=30))
    fig.update_yaxes(
        title_text="Sector holdings ($m)",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Economic Sectors",
        title_font={"size": 10},
        title_standoff=10)
    # newnames = {str(year) + 'A1': 'First Half Year', str(year) + 'A2': 'Second Half Year'}
    # fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))
    return fig

def country_graph(file,year):
    data = file[file['YEAR'] == int(year)].sort_values(by='COUNTRY_HOLDINGS', ascending=False)
    fig = px.bar(data, x="RISK_COUNTRY", y="COUNTRY_HOLDINGS",
                 color_discrete_sequence=['#7177ed'])
    fig.update_layout(template="plotly_dark", title_text='Country of risk breakdown for ' + str(year),
                      legend_title_text="", yaxis = dict(
tickfont = dict(size=8)),xaxis = dict(
tickfont = dict(size=8)),font = dict(size = 10),
                      margin=dict(l=30, r=30, t=60, b=30))
    fig.update_yaxes(
        title_text="Country of risk holdings ($m)",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Country of Risk",
        title_font={"size": 10},
        title_standoff=10)
    # newnames = {str(year) + 'A1': 'First Half Year', str(year) + 'A2': 'Second Half Year'}
    # fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))
    return fig

def bonds_purchased_co(file, year):
    df = file[file['YEAR'] == int(year)].iloc[:10, :].sort_values(
        'CARBON_INTENSITY')
    fig = px.bar(df, x="NUMBER_OF_BONDS", y="ISSUER_NAME", orientation='h', color_discrete_sequence=['#b0b8f2'],text_auto=True)
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
        title_text="Company Names",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Number of Bonds",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_traces(width=0.6)
    return fig

def carbon_intensity_co(file, year):
    df = file[file['YEAR'] == int(year)].iloc[:10, :].sort_values(
        'CARBON_INTENSITY')
    fig = px.bar(df, x="CARBON_INTENSITY", y="ISSUER_NAME", orientation='h', color_discrete_sequence=['#b68ee5'],
                 hover_data={'CARBON_INTENSITY':True,'ECONOMIC_SECTOR':True,'ISSUER_NAME':False})
    fig.update_layout(template="plotly_dark", title_text='Carbon Intensity' + "<br><sup>(tCO\u2082/$ million revenue)</sup>"
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
        title_text="Company Names",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Carbon Intensity (tCO\u2082/$ million revenue)",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_traces(width=0.6)
    return fig

# time graph for high emitting companies
def time_graph_high(file,year):
    df = file[file['YEAR'] == int(year)].iloc[:10, :].sort_values(
        'CARBON_INTENSITY')
    df2 = df[['ISSUER_NAME']].merge(file[['ISSUER_NAME', 'YEAR', 'NUMBER_OF_BONDS']],
                                    on='ISSUER_NAME', how="left").drop_duplicates()
    df2 = df2[df2['YEAR'] != 2022]
    df3 = df2.sort_values(by='YEAR')
    fig = px.line(df3, x="YEAR", y="NUMBER_OF_BONDS", color='ISSUER_NAME',markers=True)
    fig.update_layout(template="plotly_dark",legend_title_text="", title_text='Yearly bonds distribution ',
                      yaxis=dict(
                          tickfont=dict(size=8)), xaxis=dict(
            tickfont=dict(size=8)), legend = dict(
        y=1,
        x=1, font=dict(size=6)
    ), font=dict(size=10),
                      margin=dict(l=30, r=10, t=60, b=30))

    fig.update_yaxes(
        title_text="Number of Bonds",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Year",
        title_font={"size": 10},
        title_standoff=10)
    return fig


# lowest CI for companies
def bonds_purchased_co_low(file, year):
    df = file[file['YEAR'] == int(year)].iloc[-10:, :].sort_values(
        'CARBON_INTENSITY')
    fig = px.bar(df, x="NUMBER_OF_BONDS", y="ISSUER_NAME", orientation='h', color_discrete_sequence=['#b0b8f2'],text_auto=True)
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
        title_text="Company Names",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Number of Bonds",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_traces(width=0.6)
    return fig

def carbon_intensity_co_low(file, year):
    df = file[file['YEAR'] == int(year)].iloc[-10:, :].sort_values(
        'CARBON_INTENSITY')
    fig = px.bar(df, x="CARBON_INTENSITY", y="ISSUER_NAME", orientation='h', color_discrete_sequence=['#b68ee5'],
                 hover_data={'CARBON_INTENSITY':True,'ECONOMIC_SECTOR':True,'ISSUER_NAME':False})
    fig.update_layout(template="plotly_dark", title_text='Carbon Intensity' + "<br><sup>(tCO\u2082/$ million revenue)</sup>"
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
        title_text="Company Names",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Carbon Intensity (tCO\u2082/$ million revenue)",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_traces(width=0.6)
    return fig

# time graph for high emitting companies
def time_graph_low(file,year):
    df = file[file['YEAR'] == int(year)].iloc[-10:, :].sort_values(
        'CARBON_INTENSITY')
    df2 = df[['ISSUER_NAME']].merge(file[['ISSUER_NAME', 'YEAR', 'NUMBER_OF_BONDS']],
                                    on='ISSUER_NAME', how="left").drop_duplicates()
    df2 = df2[df2['YEAR'] != 2022]
    df3 = df2.sort_values(by='YEAR')
    fig = px.line(df3, x="YEAR", y="NUMBER_OF_BONDS", color='ISSUER_NAME',markers=True)
    fig.update_layout(template="plotly_dark",legend_title_text="", title_text='Yearly bonds distribution ',
                      yaxis=dict(
                          tickfont=dict(size=8)), xaxis=dict(
            tickfont=dict(size=8)), legend = dict(
        y=1,
        x=1, font=dict(size=6)
    ), font=dict(size=10),
                      margin=dict(l=30, r=10, t=60, b=30))

    fig.update_yaxes(
        title_text="Number of Bonds",
        title_font={"size": 10},
        title_standoff=10)
    fig.update_xaxes(
        title_text="Year",
        title_font={"size": 10},
        title_standoff=10)
    return fig