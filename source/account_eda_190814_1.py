# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 14:12:55 2019

@author: soug9
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import datetime


def create_calendar(year, month) :
    
    n_of_days = calendar.monthrange(year, month)[1]
    s_date = datetime.datetime(year, month, 1)
    e_date = datetime.datetime(year, month, n_of_days)
    
    sr_date_list = pd.date_range(s_date, e_date, freq='D', name='날짜').to_series()
    df_date_list = sr_date_list.to_frame()
    df_date_list['요일'] = sr_date_list.dt.dayofweek
    df_date_list['주'] = sr_date_list.dt.week
    
    out_unfix_sum1 = pd.merge(df_date_list, out_unfix_sum, how='left', on='날짜').fillna({'금액' : 0})
    
    df = out_unfix_sum1.pivot('주', '요일', '금액')
    
    #df = df.fillna(0).astype('int32')
    df.columns  = ['M', 'T', 'W', 'Th', 'F', 'S', 'S']

    return df

def seaborn(df) :
    
    sns.heatmap(df, annot=True, fmt='d', cmap='RdYlGn_r')
    plt.title('Heatmap by seaborn', fontsize=20)
    plt.xlabel('day of week', fontsize=14)
    plt.ylabel('week', fontsize=14)
    plt.figure(figsize=(20, 20))
    plt.show() 

df_ex = create_calendar(2019,1)
seaborn(df_ex)
