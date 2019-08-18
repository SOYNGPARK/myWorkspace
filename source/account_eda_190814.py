# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 13:31:50 2019

@author: soug9
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import datetime



#
def create_calendar(out, year, month) :
    
    n_of_days = calendar.monthrange(year, month)[1]
    s_date = datetime.datetime(year, month, 1)
    e_date = datetime.datetime(year, month, n_of_days)
    
    sr_date_list = pd.date_range(s_date, e_date, freq='D', name='날짜').to_series()
    df_date_list = sr_date_list.to_frame()
    df_date_list['요일'] = sr_date_list.dt.dayofweek
    df_date_list['주'] = sr_date_list.dt.week
    
    out_unfix_sum = out['금액'][out['분류'] == '변동지출'].groupby(out['날짜']).sum().reset_index()
    out_unfix_sum['날짜'] = pd.to_datetime(out_unfix_sum['날짜'])
    
    out_unfix_sum1 = pd.merge(df_date_list, out_unfix_sum, how='left', on='날짜').fillna({'금액' : 0})
    
    df = out_unfix_sum1.pivot('주', '요일', '금액')
    
    #df = df.fillna(-10000).astype('int32')
    df.columns  = ['M', 'T', 'W', 'Th', 'F', 'S', 'S']

    return df

def seaborn(df, season_num) :
 
    cmap = eval(season_cmap(season_num)) 

    undercol = 'grey'
    overcol = 'red'
    cmap.set_under(color=undercol, alpha=0.3)
    cmap.set_over(color=overcol, alpha=0.8)
    sns.heatmap(df, mask=df.isnull(), annot=True, fmt='g', cmap=cmap, linewidths=1, vmin=0.1, vmax=100000)
    #plt.title('Heatmap by seaborn', fontsize=20)
    plt.xlabel('day of week', fontsize=14)
    plt.ylabel('week', fontsize=14)
    plt.figure(figsize=(20, 20))
    plt.show() 

def season_cmap(num) :
    season_cmap_dic = {0 : 'sns.cubehelix_palette(as_cmap=True, light=.9)', #winter
            1 : 'sns.light_palette("hotpink", as_cmap=True)', #spring
            2 : 'sns.light_palette((210, 90, 60), as_cmap=True, input="husl")' #summer
            } 

    return season_cmap_dic.get(num, 'sns.cubehelix_palette(as_cmap=True, light=.9)')

def season(month) :
    season_dic = {12 : 0, 1 : 0, 2 : 0, 
                  3 : 1, 4 : 1, 5 : 1,
                  6 : 2, 7 : 2, 8 : 2, 
                  9 : 3, 10 : 3, 11: 3}
    return season_dic.get(month, 0)


#
data = pd.read_csv(r'C:\myWorkspace\data\account_190814.csv')

out = data[data['수입/지출'] == '지출']
    
df_ex = create_calendar(out, 2019, 1)
seaborn(df_ex, 0)

months = list(range(1,9))
for month in months :
    df = create_calendar(out, 2019, month)
    seaborn(df, season(month))










