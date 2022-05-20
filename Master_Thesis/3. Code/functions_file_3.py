import pandas
import os
import numpy as np
import plotly.express as px

###### 3a. Emissions' Data - CDP ######

def clean_scope1(filename):
    df = filename.copy()
    #select columns
    df = df.iloc[:,[1,5,7]]
    columns = ['ACCOUNT_ID','ACCOUNTING_YEAR','GLOBAL_SCOPE1']
    df.columns = columns
    data = df.sort_values(by = ['ACCOUNT_ID','ACCOUNTING_YEAR']).drop_duplicates(subset=['ACCOUNT_ID'], keep="last")
    data = data.fillna(0)
    return data

def clean_scope2(filename):
    df = filename.copy()
    #select columns
    df = df.iloc[:,[1,5,6,7]]
    columns = ['ACCOUNT_ID','ACCOUNTING_YEAR','GLOBAL_SCOPE2: LOCATION-BASED','GLOBAL_SCOPE2: MARKET-BASED']
    df.columns = columns
    data = df.sort_values(by = ['ACCOUNT_ID','ACCOUNTING_YEAR']).drop_duplicates(subset=['ACCOUNT_ID'], keep="last")
    data = data.fillna(0)
    return data

def finalizedata(file_1,file_2,file_3):
    data = file_1.merge(file_2, on = 'ACCOUNT_ID', how = "left")
    data_2 = data.merge(file_3, on = 'ACCOUNT_ID', how ="left")
    columns = ['ACCOUNT_ID','ACCOUNT_NAME','ISIN','ACCOUNTING_YEAR_x','GLOBAL_SCOPE1','GLOBAL_SCOPE2: LOCATION-BASED','GLOBAL_SCOPE2: MARKET-BASED']
    data_2 = data_2[columns]
    df = data_2.rename(columns = {'ACCOUNTING_YEAR_x':'ACCOUNTING_YEAR'})
    df['GLOBAL_SCOPE2: LOCATION-BASED'] = df['GLOBAL_SCOPE2: LOCATION-BASED'].fillna(0)
    df['GLOBAL_SCOPE2: MARKET-BASED'] = df['GLOBAL_SCOPE2: MARKET-BASED'].fillna(0)
    return df


###### 3b. Emissions - Intensity and Master File ######

def match_data(filename_for_ecb_portfolio, filename_for_cdp_dictionary):
    # check which emissions data matches with the ECB portfolio
    df = filename_for_ecb_portfolio.copy()
    df2 = filename_for_cdp_dictionary.copy()
    # unique companies in the portfolio
    unique = df['ISSUER_NAME'].drop_duplicates().to_frame()
    unique_with_nace = unique.merge(df[['ISSUER_NAME','NACE_CODE']], on = "ISSUER_NAME", how = "left").drop_duplicates(subset =['ISSUER_NAME'])
    # merging unique companies with emissions data
    # companies matched with the emission data
    data = unique_with_nace.merge(df2, left_on = "ISSUER_NAME", right_on ="Issuer Name", how = "left").drop_duplicates(subset = ['ISSUER_NAME'])
    data = data.drop('Issuer Name', axis = 1)
    matched_co = data[~data['Account ID'].isna()]
    unmatched_co = data[data['Account ID'].isna()]
    unmatched_co = unmatched_co[['ISSUER_NAME','NACE_CODE']]
    return matched_co, unmatched_co

# merge emissions data with matched data
def match_emissions(filename_matched_data, filename_emissions_data):
    df = filename_matched_data.copy()
    df2 = filename_emissions_data.copy()
    merge = df.merge(df2,left_on = "Account ID",right_on = "ACCOUNT_ID",how = "left")
    merge['TOTAL_GHG'] = merge['GLOBAL_SCOPE1'] + merge['GLOBAL_SCOPE2: LOCATION-BASED']
    columns_to_keep = ['ISSUER_NAME','ACCOUNT_ID','GLOBAL_SCOPE1','GLOBAL_SCOPE2: LOCATION-BASED','GLOBAL_SCOPE2: MARKET-BASED','TOTAL_GHG']
    merged_data = merge[columns_to_keep]
    return merged_data

# merge emissions data with companies in CDP data
def match_emissions_cdp(filename_companies, filename_emissions_data):
    df = filename_companies.copy()
    df2 = filename_emissions_data.copy()
    data = df.merge(df2, left_on= "Account_Id", right_on = "ACCOUNT_ID",how = "left")
    columns_to_keep =['Account_Id','Account_Name','NACE_Code','Revenue','GLOBAL_SCOPE1','GLOBAL_SCOPE2: LOCATION-BASED','GLOBAL_SCOPE2: MARKET-BASED']
    data = data[columns_to_keep]
    data = data.fillna(0)
    data['TOTAL_GHG'] = data['GLOBAL_SCOPE1'] + data['GLOBAL_SCOPE2: LOCATION-BASED']
    data['Revenue'] = data['Revenue'].apply(lambda x: x/1000)
    data['GHG/REVENUE'] = data['TOTAL_GHG']/data['Revenue']
    return data

# calculate emissions intensity based on NACE code of sectors
def intensity(filename):
    df = filename.copy()
    table = df.groupby(by = "NACE_Code").agg({'GHG/REVENUE':['mean','median']})
    table = table.reset_index()
    columns = ['NACE_CODE','MEAN_INTENSITY','MEDIAN_INTENSITY']
    table.columns = columns
    table = table.round(2)
    return table

def emissions_portfolio(file1,file2,file3):
    df = file1.merge(file2,on="ISSUER_NAME",how = "left")
    df2 = df.merge(file3, on = "ISSUER_NAME", how = "left")
    columns_to_keep = ['NCB', 'ISIN_CODE', 'ISSUER_NAME', 'MATURITY_DATE', 'COUPON_RATE','PUBLISHED_DATE', 'YEAR', 'MONTH', 'TOTAL__REVENUE', 'SIC_CODE','NACE_CODE_x', 'ECONOMIC_SECTOR', 'QUARTER','GLOBAL_SCOPE1','GLOBAL_SCOPE2: LOCATION-BASED','TOTAL_GHG','MEAN_INTENSITY','MEDIAN_INTENSITY','COUNTRY_OF_RISK']
    data = df2[columns_to_keep]
    data.loc[:,'GLOBAL_SCOPE1':'MEDIAN_INTENSITY'] = data.loc[:,'GLOBAL_SCOPE1':'MEDIAN_INTENSITY'].fillna(0)
    data['GHG: MEAN_INTENSITY'] = data['TOTAL__REVENUE']*data['MEAN_INTENSITY']
    data['GHG: MEDIAN_INTENSITY'] = data['TOTAL__REVENUE']*data['MEDIAN_INTENSITY']
    data['TOTAL_GHG: MEAN_INTENSITY'] = data['GHG: MEAN_INTENSITY'] + data['TOTAL_GHG']
    data['TOTAL_GHG: MEDIAN_INTENSITY'] = data['GHG: MEDIAN_INTENSITY'] + data['TOTAL_GHG']
    columns = ['NCB', 'ISIN_CODE', 'ISSUER_NAME', 'MATURITY_DATE', 'COUPON_RATE','PUBLISHED_DATE', 'YEAR', 'MONTH', 'TOTAL__REVENUE', 'SIC_CODE','NACE_CODE_x', 'ECONOMIC_SECTOR', 'QUARTER','COUNTRY_OF_RISK','TOTAL_GHG: MEAN_INTENSITY','TOTAL_GHG: MEDIAN_INTENSITY']
    data_2 = data[columns]
    data_2 = data_2.rename(columns = {'NACE_CODE_x':'NACE_CODE'})
    return data_2






###### 5b. Carbon Intensity for sector and country of risk ######
def carbon_intensity(file,groupby_name):
    columns = ['YEAR']
    columns.append(groupby_name)
    df = file.groupby(columns)[['TOTAL_GHG: MEAN_INTENSITY','TOTAL__REVENUE']].sum()
    df = df.reset_index()
    df['CARBON_INTENSITY']= (df['TOTAL_GHG: MEAN_INTENSITY']/df['TOTAL__REVENUE']).round(2)
    columns_to_select = ['YEAR','CARBON_INTENSITY']
    columns_to_select.append(groupby_name)
    carbon_intensity = df[columns_to_select]
    return carbon_intensity

# plots
def graph_CI(file,groupby_name,year):
    df = file[file['YEAR']==year].sort_values(by = 'CARBON_INTENSITY')
    fig = px.bar(df, y=groupby_name, x="CARBON_INTENSITY",orientation='h')
    return fig



###### 4c. Weighted Average Carbon Intensity (WACI) ######
def clean_master_file(filename):
    # create new_columns
    filename['TOTAL_GHG/REVENUE: AVG_INTENSITY'] = filename['TOTAL_GHG: MEAN_INTENSITY']/filename['TOTAL__REVENUE']
    filename['TOTAL_GHG/REVENUE: MED_INTENSITY'] = filename['TOTAL_GHG: MEDIAN_INTENSITY']/filename['TOTAL__REVENUE']
    filename['QTR'] = [x[-2:] for x in filename['QUARTER']]

    conditions = [(filename['QTR'] == 'Q1') | (filename['QTR']=='Q2'),
             (filename['QTR'] == 'Q3') | (filename['QTR']=='Q4')]
    values = ['A1','A2']
    filename['NEW_QTR'] = np.select(conditions, values, default = np.nan)
    #filename['new_QUARTER'] = np.where(filename['QTR'] == 'Q4', filename['YEAR'] + 1, filename['YEAR'])
    #filename['QUARTER_NEW'] = filename['new_QUARTER'].astype(str) + filename['NEW_QTR']
    filename['NEW_QUARTER'] = filename['YEAR'].astype(str) + filename['NEW_QTR']
    columns_to_drop = ['QTR','NEW_QTR']
    data = filename.drop(columns = columns_to_drop,axis = 1)
    return data

def risk_country(filename):
    data = filename.copy()
    euro_area = ['Portugal', 'Luxembourg','Slovakia','Slovenia','Austria','Finland','Estonia','Ireland','Lithuania']
    other_area = ['United Kingdom','Sweden']
    data['RISK_COUNTRY'] = np.where(data['COUNTRY_OF_RISK'].isin(euro_area),'Other (euro area)',data['COUNTRY_OF_RISK'])
    data['RISK_COUNTRY'] = np.where(data['COUNTRY_OF_RISK'].isin(other_area),'Other (non-euro area)',data['RISK_COUNTRY'])
    return data

def mean_weighted_carbon_intensity(qtr, file):
    data = file[file['NEW_QUARTER'] == qtr]
    total_portfolio_value = data['TOTAL_HOLDINGS'].iloc[0]
    data['PROP_VALUE'] = data['SECTOR_CSPP_HOLDINGS']*data['COUNTRY_CSPP_HOLDINGS']*total_portfolio_value
    data['WEIGHTS'] = data['PROP_VALUE']/total_portfolio_value
    data['MEAN_WACI'] = (data['WEIGHTS']*data['MEAN_WEIGHTED_INTENSITY'])/data['WEIGHTS'].sum()
    columns = ['ECONOMIC_SECTOR','RISK_COUNTRY','MEAN_WACI']
    mean_data = data[columns]
    mean_data = mean_data.pivot(index = 'RISK_COUNTRY',columns = 'ECONOMIC_SECTOR')
    mean_data = mean_data.fillna(0)
    return mean_data
 
def median_weighted_carbon_intensity(qtr, file):
    data = file[file['NEW_QUARTER'] == qtr]
    total_portfolio_value = data['TOTAL_HOLDINGS'].iloc[0]
    data['PROP_VALUE'] = data['SECTOR_CSPP_HOLDINGS']*data['COUNTRY_CSPP_HOLDINGS']*total_portfolio_value  
    data['MEDIAN_WACI'] = (data['PROP_VALUE']*data['MED_WEIGHTED_INTENSITY'])/total_portfolio_value
    columns_2 = ['ECONOMIC_SECTOR','RISK_COUNTRY','MEDIAN_WACI']
    med_data = data[columns_2]
    med_data = med_data.pivot(index = 'RISK_COUNTRY',columns = 'ECONOMIC_SECTOR')
    med_data = med_data.fillna(0)
    return med_data

def waci_calculation_file(filename,portfolio_value_file,sector_breakdown_file,country_breakdown_file):
    # add country of risk column
    df = risk_country(filename)
    # using average intensity calculated from CDP data for weighted intensity calculation
    grouped_data = df.groupby(['NEW_QUARTER','ECONOMIC_SECTOR','RISK_COUNTRY'])['TOTAL_GHG/REVENUE: AVG_INTENSITY'].agg(
    MEAN_WEIGHTED_INTENSITY= "mean", MED_WEIGHTED_INTENSITY = "median")
    grouped_data = grouped_data.reset_index()
    df2 = grouped_data.merge(portfolio_value_file,left_on = 'NEW_QUARTER',right_on ="KEY", how = "left")
    df3 = df2.merge(sector_breakdown_file,on =['KEY','ECONOMIC_SECTOR'], how = "left")
    data = df3.merge(country_breakdown_file, on = ['KEY','RISK_COUNTRY'],how = "left" )
    return data

def df_to_plotly(df):
    y = [x[1] for x in df.columns]
    return {'z': df.values.tolist(),
            'x': y,
            'y': df.index.tolist()}

###### 4c. Yearly Weighted Average Carbon Intensity (WACI) ######
def yearly_waci_calculation_file(filename,portfolio_value_file,sector_breakdown_file,country_breakdown_file):
    # add country of risk column
    df = risk_country(filename)
    # using average intensity calculated from CDP data for weighted intensity calculation
    grouped_data = df.groupby(['YEAR','ECONOMIC_SECTOR','RISK_COUNTRY'])['TOTAL_GHG/REVENUE: AVG_INTENSITY'].agg(
    MEAN_WEIGHTED_INTENSITY= "mean", MED_WEIGHTED_INTENSITY = "median")
    grouped_data = grouped_data.reset_index()
    df2 = grouped_data.merge(portfolio_value_file,left_on = 'YEAR',right_on ="YEAR", how = "left")
    df3 = df2.merge(sector_breakdown_file,on =['YEAR','ECONOMIC_SECTOR'], how = "left")
    data = df3.merge(country_breakdown_file, on = ['YEAR','RISK_COUNTRY'],how = "left" )
    return data

def clean_master_file_yearly(filename):
    # create new_columns
    filename['TOTAL_GHG/REVENUE: AVG_INTENSITY'] = filename['TOTAL_GHG: MEAN_INTENSITY']/filename['TOTAL__REVENUE']
    filename['TOTAL_GHG/REVENUE: MED_INTENSITY'] = filename['TOTAL_GHG: MEDIAN_INTENSITY']/filename['TOTAL__REVENUE']
    return filename

def yearly_mean_weighted_carbon_intensity(year, file):
    data = file[file['YEAR'] == year]
    total_portfolio_value = data['TOTAL_HOLDINGS(USD)'].iloc[0]
    data['PROP_VALUE'] = data['SECTOR_CSPP_HOLDINGS']*data['COUNTRY_CSPP_HOLDINGS']*total_portfolio_value
    data['WEIGHTS'] = data['PROP_VALUE']/total_portfolio_value
    data['MEAN_WACI'] = ((data['WEIGHTS']*data['MEAN_WEIGHTED_INTENSITY'])/data['WEIGHTS'].sum()).round(2)
    columns = ['ECONOMIC_SECTOR','RISK_COUNTRY','MEAN_WACI']
    mean_data = data[columns]
    mean_data = mean_data.pivot(index = 'RISK_COUNTRY',columns = 'ECONOMIC_SECTOR')
    mean_data = mean_data.fillna(0)
    return mean_data

def yearly_median_weighted_carbon_intensity(year, file):
    data = file[file['YEAR'] == year]
    total_portfolio_value = data['TOTAL_HOLDINGS(USD)'].iloc[0]
    data['PROP_VALUE'] = data['SECTOR_CSPP_HOLDINGS']*data['COUNTRY_CSPP_HOLDINGS']*total_portfolio_value
    data['WEIGHTS'] = data['PROP_VALUE']/total_portfolio_value
    data['MEDIAN_WACI'] = ((data['WEIGHTS']*data['MED_WEIGHTED_INTENSITY'])/data['WEIGHTS'].sum()).round(2)
    columns = ['ECONOMIC_SECTOR','RISK_COUNTRY','MEDIAN_WACI']
    mean_data = data[columns]
    mean_data = mean_data.pivot(index = 'RISK_COUNTRY',columns = 'ECONOMIC_SECTOR')
    mean_data = mean_data.fillna(0)
    return mean_data

# to determine the companies driving sectors to be carbon intensive
def create_data(file,condition):
    df = risk_country(file)
    mask = df[['ECONOMIC_SECTOR', 'RISK_COUNTRY','YEAR']].agg(tuple, 1).isin(condition)
    x = df[mask]
    y = x.groupby(by=['ISSUER_NAME','RISK_COUNTRY',"ECONOMIC_SECTOR","YEAR"])['ISIN_CODE'].count()
    y = y.reset_index()
    df2 = x[['ISSUER_NAME','RISK_COUNTRY',"ECONOMIC_SECTOR",'TOTAL_GHG/REVENUE: AVG_INTENSITY']]
    df3 = y.merge(df2 , on = ['ISSUER_NAME','RISK_COUNTRY',"ECONOMIC_SECTOR"],how ="left").drop_duplicates()
    return df3

def check_difference_waci(file,key):
    df = file[file['YEAR']==key]
    df['DIFF'] = df['MEAN_WACI'].round(2) - df['MEDIAN_WACI'].round(2)
    df2 = df.sort_values(by = 'DIFF',ascending = False)
    # Top 10 rows with maximum difference
    df3 = df2.iloc[:10,:]
    df3['new'] = df3[['ECONOMIC_SECTOR', 'RISK_COUNTRY','YEAR']].apply(tuple, axis=1)
    sector_name = df3['ECONOMIC_SECTOR'].unique()
    condition = df3['new'].tolist()
    return sector_name, condition

def yearly_waci_sector_calculation(filename,portfolio_value_file,sector_breakdown_file):
    # add country of risk column
    df = risk_country(filename)
    # using average intensity calculated from CDP data for weighted intensity calculation
    grouped_data = df.groupby(['YEAR','ECONOMIC_SECTOR'])['TOTAL_GHG/REVENUE: AVG_INTENSITY'].agg(
    MEAN_WEIGHTED_INTENSITY= "mean", MED_WEIGHTED_INTENSITY = "median")
    grouped_data = grouped_data.reset_index()
    df2 = grouped_data.merge(portfolio_value_file,left_on = 'YEAR',right_on ="YEAR", how = "left")
    df3 = df2.merge(sector_breakdown_file,on =['YEAR','ECONOMIC_SECTOR'], how = "left")
    return df3

def contribution_calculate(file):
    new_df2 = file.copy()
    new_df2['WEIGHTS'] = (new_df2['SECTOR_CSPP_HOLDINGS']*new_df2['TOTAL_HOLDINGS(USD)'])/new_df2['TOTAL_HOLDINGS(USD)']
    new_df2['SUM_WEIGHTS'] = new_df2.groupby('YEAR')['WEIGHTS'].transform('sum')
    new_df2['MEAN_WACI'] = new_df2['WEIGHTS']*new_df2['MEAN_WEIGHTED_INTENSITY']/new_df2['SUM_WEIGHTS']
    new_df2['MEDIAN_WACI'] = new_df2['WEIGHTS']*new_df2['MED_WEIGHTED_INTENSITY']/new_df2['SUM_WEIGHTS']
    new_df2['Contribution'] = (new_df2['MEAN_WACI'] / new_df2.groupby('YEAR')['MEAN_WACI'].transform('sum')).round(4)
    return new_df2

