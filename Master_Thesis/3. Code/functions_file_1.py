
########## 1a. CSPP holdings - download portfolio data ##########
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# function for downloading the data
def download_data(self,x):
    if self.find_element(By.XPATH,"/html/body/div[2]/main/div[7]/div[2]/div/div/div/table/tbody/tr["+ str(x) +"]/td[5]/a").is_displayed():
        dates = self.find_element(By.XPATH,"/html/body/div[2]/main/div[7]/div[2]/div/div/div/table/tbody/tr["+ str(x) +"]/td[5]/a")
        action = ActionChains(self)
        action.move_to_element(dates).click().perform()
        time.sleep(2)
        button = self.find_element(By.CLASS_NAME,"ecb-buttonHighlight.active")
        action = ActionChains(self)
        action.move_to_element(button).perform()
        time.sleep(2)
        button.click()
    return self


########## 1b. CSPP holdings - Combined portfolio data (2017-2022) ##########

import glob
import pandas as pd
import os
import datetime

def read_file_ecb(filename,url):
    data = pd.read_csv(url + filename,header = None,skiprows=1,encoding="ISO-8859-1")
    #data.columns = columns
    year = filename[-12:-8]
    month = filename[-8:-6]
    day = filename[-6:-4]
    data['PUBLISHED_DATE'] = datetime.datetime(int(year),int(month),int(day))
    data['YEAR'] = year
    data['MONTH'] = month
    return data

def names_of_file(url):
    filelist = []
    os.chdir(url)
    for files in enumerate(glob.glob("*.csv")):
        filelist.append(files)
    return filelist


########## 1c. CSPP holdings - sector and country breakdown ##########

import datetime as dt
import xlrd
import numpy as np

def clean_portfolio_value(filename):
    # selecting rows for which we have downloaded ECB bonds data
    df = filename.iloc[12:,:]
    # calculating portfolio value for every quarter starting from June 2017 to Feb 2022
    df['DATE'] = df['End of Month'].map(lambda x: dt.datetime.strptime(x, '%b-%y'))
    df['DATE'] = df['End of Month'].map(lambda x: dt.datetime.strptime(x, '%b-%y'))
    df['QTR'] = df['DATE'].dt.to_period('Q').dt.strftime('Q%q')
    df['YEAR'] = pd.DatetimeIndex(df['DATE']).year

    conditions = [(df['QTR'] == 'Q1') | (df['QTR']=='Q2'),
             (df['QTR'] == 'Q3') | (df['QTR']=='Q4')]
    values = ['A1','A2']
    df['NEW_QTR'] = np.select(conditions, values, default = np.nan)
    df['KEY'] = df['YEAR'].astype(str) + df['NEW_QTR']
    df['Total holdings'] = df['Total holdings'].str.replace(",","")
    df['Total holdings'] = df['Total holdings'].apply(pd.to_numeric)
    data = df.groupby('KEY')['Total holdings'].agg(TOTAL_HOLDINGS = "mean")
    data = data.reset_index()
    data['TOTAL_HOLDINGS(USD)'] = (data['TOTAL_HOLDINGS'] * 1.05).round(0)
    return data

def clean_portfolio_yearly(filename):
    # selecting rows for which we have downloaded ECB bonds data
    df = filename.iloc[12:,:]
    # calculating portfolio value for every quarter starting from June 2017 to Feb 2022
    df['DATE'] = df['End of Month'].map(lambda x: dt.datetime.strptime(x, '%b-%y'))
    df['DATE'] = df['End of Month'].map(lambda x: dt.datetime.strptime(x, '%b-%y'))
    df['QTR'] = df['DATE'].dt.to_period('Q').dt.strftime('Q%q')
    df['YEAR'] = pd.DatetimeIndex(df['DATE']).year
    df['Total holdings'] = df['Total holdings'].str.replace(",","")
    df['Total holdings'] = df['Total holdings'].apply(pd.to_numeric)
    data = df.groupby('YEAR')['Total holdings'].agg(TOTAL_HOLDINGS = "mean")
    data = data.reset_index()
    data['TOTAL_HOLDINGS(USD)'] = (data['TOTAL_HOLDINGS'] * 1.05).round(0)
    return data


def country_breakdown(path_for_file,sheet_names_array):
    data = pd.DataFrame()
    for i in range(len(sheet_names_array)):
        df = pd.read_excel(path_for_file, sheet_name = sheet_names_array[i],skiprows = 10, 
                       skipfooter=22, usecols = "A:C",header= None)
        df['Year'] = sheet_names_array[i][-4:]
        df['QTR'] =  sheet_names_array[i][-7:-5]
        data = pd.concat([data,df])
    condition = [(data['QTR']=='Q1') |(data['QTR']=='Q2'),
                (data['QTR']=='Q3') |(data['QTR']=='Q4')]
    values = ['A1','A2']
    data['NEW_QTR'] = np.select(condition,values, default=np.nan)
    data['KEY'] = data['Year'].astype(str) + data['NEW_QTR']
    cols_to_drop = ['Year','NEW_QTR','QTR']
    data = data.drop(cols_to_drop,axis = 1)
    columns = ['RISK_COUNTRY','COUNTRY_CSPP_HOLDINGS','COUNTRY_ELIGIBLE_CSPP_UNIVERSE','KEY']
    data.columns = columns
    return data

def sector_breakdown(path_for_file, sheet_names_array):
    data = pd.DataFrame()
    for i in range(len(sheet_names_array)):
        df = pd.read_excel(path_for_file, sheet_name = sheet_names_array[i],skiprows = 24,
                       skipfooter=3,usecols = "A:C",header= None)
        df['Year'] = sheet_names_array[i][-4:]
        df['QTR'] =  sheet_names_array[i][-7:-5]
        data = pd.concat([data,df])
    condition = [(data['QTR']=='Q1') |(data['QTR']=='Q2'),
                (data['QTR']=='Q3') |(data['QTR']=='Q4')]
    values = ['A1','A2']
    data['NEW_QTR'] = np.select(condition,values, default=np.nan)
    data['KEY'] = data['Year'].astype(str) + data['NEW_QTR']
    cols_to_drop = ['Year','NEW_QTR','QTR']
    data = data.drop(cols_to_drop,axis = 1)
    columns = ['ECONOMIC_SECTOR','SECTOR_CSPP_HOLDINGS','SECTOR_ELIGIBLE_CSPP_UNIVERSE','KEY']
    data.columns = columns
    return data
    