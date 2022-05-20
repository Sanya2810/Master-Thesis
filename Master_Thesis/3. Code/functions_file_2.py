import glob
import pandas as pd
import os
import numpy as np


########## 2a. Company Information - Data collection ##########
def bonds_file(url):
    filelist = []
    os.chdir(url)
    for files in enumerate(glob.glob("*.xlsx")):
        filelist.append(files)
    return filelist

def read_file_bonds(filename,url):
    data = pd.read_excel(url + filename,header = None,skiprows = 6)
    return data


########## 2b. Company Information - with CSPP holdings ##########

def clean_file(filename):
    data = filename.copy()
    columns_to_keep = ['ISIN','TOTAL_REVENUE']
    data = data[columns_to_keep]
    data = data.dropna()
    data = data.drop_duplicates()
    return data

def merge_revenue(portfolio_file,snp_file,mapped_file):
    subset = ['NCB', 'ISIN_CODE', 'ISSUER_NAME', 'MATURITY_DATE', 'COUPON_RATE','PUBLISHED_DATE', 'YEAR', 'MONTH']
    merge_data = portfolio_file.merge(snp_file, left_on = ['ISIN_CODE'],right_on = ['ISIN'],how="left").drop_duplicates(subset = subset)
    # Filter only rows that have total revenue as na
    data = merge_data[merge_data['TOTAL_REVENUE'].isna()][['ISSUER_NAME','ISIN_CODE']].drop_duplicates(subset = 'ISIN_CODE')
    # map ISSUER_NAME with revenue_mapping data
    revenue = data.merge(mapped_file,left_on = ["ISSUER_NAME"], right_on = ["Unique Company's Name (ECB Portfolio)"],how = "left").drop_duplicates()
    rev_data = revenue[['ISIN_CODE','Total Revenue']]
    # ecb_portfolio with revenue data
    df = merge_data.merge(rev_data, on = "ISIN_CODE",how = "left")
    return df
    

def clean_file_rev(filename):
    df = filename.copy()
    df['TOTAL_REVENUE'] = df['TOTAL_REVENUE'].fillna(0)
    df['Total Revenue'] = df['Total Revenue'].fillna(0)
    df['TOTAL__REVENUE'] = df['TOTAL_REVENUE'] + df['Total Revenue']
    columns_to_drop = ['TOTAL_REVENUE','Total Revenue','ISIN']
    df1 = df.drop(columns_to_drop,axis = 1)
    return df1

def clean_file_industry(filename):
    data = filename.copy()
    columns_to_drop = ['Unique_ISIN_Code']
    data_2 = data.drop(columns_to_drop,axis = 1)
    data_2['SIC_CODE'] = data_2['SIC_CODE'].fillna(0)
    data_2['SIC_CODE']= data_2['SIC_CODE'].astype(int)
    return data_2

def merge_country(file_1, file_2,mapped_file):
    data = file_1.merge(file_2,left_on = "ISIN_CODE",right_on = "ISIN",how = "left")
    columns_to_drop = ['Issuer Name','Instrument Item ID','ISIN','Maturity Date\n(dd/mm/yyyy)','Country of Incorporation Name [|(Ultimate Parent)]']
    df = data.drop(columns = columns_to_drop,axis = 1)
    df = df.rename(columns ={'Country of Incorporation Name [|(Issuer)]':'COUNTRY_OF_RISK'})
    df2 = df.merge(mapped_file, left_on = "ISSUER_NAME",right_on = "ISSUER_NAME/ISIN",how ="left")
    return df2

def clean_country(filename):
    df = filename.copy()
    df['COUNTRY_OF_RISK'] = np.where(df['COUNTRY_OF_RISK_x'].isna(),df['COUNTRY_OF_RISK_y'],df['COUNTRY_OF_RISK_x'])
    df['COUNTRY_OF_RISK'] = np.where(df['ISIN_CODE'] == 'FI4000312095','Finland',df['COUNTRY_OF_RISK'])
    columns_to_drop = ['COUNTRY_OF_RISK_x','ISSUER_NAME/ISIN','COUNTRY_OF_RISK_y']
    df = df.drop(columns_to_drop,axis = 1)
    return df



########## 2c. Cleaned Company Information with portfolio data ##########

def clean_issuer_info(filename):
    conditions = [(filename['ISIN_CODE']=='DE000A2YB699'),(filename['ISIN_CODE']=='DE000A2YB7A7'),(filename['ISIN_CODE']=='FI4000312095'),(filename['ISIN_CODE']=='FR0013321536')]
    values = ['Schaeffler AG','Schaeffler AG','DNA Oyj','CARMILA']
    filename['ISSUER_NAME_2'] = np.select(conditions,values,default = 'NAN')
    filename['ISSUER_NAME'] = np.where(filename['ISSUER_NAME_2']=='NAN',filename['ISSUER_NAME'],filename['ISSUER_NAME_2'])
    df = filename.drop(['ISSUER_NAME_2'],axis = 1)
    return df




