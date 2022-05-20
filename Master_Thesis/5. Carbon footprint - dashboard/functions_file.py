import pandas as pd


def mean_weighted_carbon_intensity(year, file):
    data = file[file['YEAR'] == int(year)]
    total_portfolio_value = data['TOTAL_HOLDINGS(USD)'].iloc[0]
    data['PROP_VALUE'] = data['SECTOR_CSPP_HOLDINGS']*data['COUNTRY_CSPP_HOLDINGS']*total_portfolio_value
    data['WEIGHTS'] = data['PROP_VALUE']/total_portfolio_value
    data['MEAN_WACI'] = ((data['WEIGHTS']*data['MEAN_WEIGHTED_INTENSITY'])/data['WEIGHTS'].sum()).round(2)
    columns = ['ECONOMIC_SECTOR','RISK_COUNTRY','MEAN_WACI']
    mean_data = data[columns]
    mean_data = mean_data.pivot(index = 'RISK_COUNTRY',columns = 'ECONOMIC_SECTOR')
    mean_data = mean_data.fillna(0)
    return mean_data

def median_weighted_carbon_intensity(year, file):
    data = file[file['YEAR'] == int(year)]
    total_portfolio_value = data['TOTAL_HOLDINGS(USD)'].iloc[0]
    data['PROP_VALUE'] = data['SECTOR_CSPP_HOLDINGS']*data['COUNTRY_CSPP_HOLDINGS']*total_portfolio_value
    data['WEIGHTS'] = data['PROP_VALUE']/total_portfolio_value
    data['MEDIAN_WACI'] = ((data['WEIGHTS']*data['MED_WEIGHTED_INTENSITY'])/data['WEIGHTS'].sum()).round(2)
    columns = ['ECONOMIC_SECTOR','RISK_COUNTRY','MEDIAN_WACI']
    mean_data = data[columns]
    mean_data = mean_data.pivot(index = 'RISK_COUNTRY',columns = 'ECONOMIC_SECTOR')
    mean_data = mean_data.fillna(0)
    return mean_data

def df_to_plotly(df):
    y = [x[1] for x in df.columns]
    return {'z': df.values.tolist(),
            'x': y,
            'y': df.index.tolist()}
