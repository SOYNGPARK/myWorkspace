# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 16:03:59 2019

@author: soug9
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv(r'C:\myWorkspace\data\account_190719.csv')

data.columns

data.dtypes
data.describe()
data.head()

data['수입/지출'].value_counts().sort_index()

out = data[data['수입/지출'] == '지출']

out['분류'].value_counts().sort_index()
out['소분류'].value_counts().sort_index()

out['소분류'][out['분류'] == '고정지출'].value_counts().sort_index()
out['소분류'][out['분류'] == '꾸밈지출'].value_counts().sort_index()
out['소분류'][out['분류'] == '변동지출'].value_counts().sort_index()
out['소분류'][out['분류'] == '특별지출'].value_counts().sort_index()


# 분류 전처리
out['분류'][(out['소분류'] == '장보기') | (out['소분류'] == '외식')] = '변동지출'

out['분류'][out['소분류'] == '옷'] = '꾸밈지출'
out['소분류'][out['소분류'] == '옷'] = '의류(옷/신발)'

out['분류'][out['소분류'] == '미용'] = '꾸밈지출'
out['소분류'][out['소분류'] == '미용'] = '미용(왁싱/네일/속눈썹)'

out['분류'][out['소분류'] == '화장품'] = '꾸밈지출'


out['분류'][out['소분류'] == '선물'] = '특별지출'

# 불필요 칼럼 제거
out = out.drop(['KRW','화폐','자산.1'], axis=1)
out.columns

# 일별 변동지출 데이터 준비
out_unfix_sum = out['금액'][out['분류'] == '변동지출'].groupby(out['날짜']).sum().reset_index()
out_unfix_sum['날짜'] = pd.to_datetime(out_unfix_sum['날짜'])


sr_date_list = pd.date_range('2019-01-01', '2019-06-30', freq='D', name='날짜').to_series()
df_date_list = sr_date_list.to_frame()
df_date_list['요일'] = sr_date_list.dt.dayofweek
df_date_list['주'] = sr_date_list.dt.week

out_unfix_sum1 = pd.merge(df_date_list, out_unfix_sum, how='left', on='날짜').fillna({'금액' : 0})

df = out_unfix_sum1.pivot('주', '요일', '금액')
df = df.sort_index(ascending=False)
df = df.fillna(0).astype('int32')

# 일별 변동지출 시각화

# Heatmap by plt.color
plt.pcolor(df)
plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
plt.yticks(np.arange(0.5, len(df.index), 1), df.index)

plt.title('Heatmap by plt.pcolor()', fontsize=20)
plt.xlabel('day of week', fontsize=14)
plt.ylabel('week', fontsize=14)
plt.colorbar()

plt.figure(figsize=(40,40))
plt.show()


# Heatmap by seaborn

sns.heatmap(df, annot=True, fmt='d', cmap='RdYlGn_r')
plt.title('Heatmap by seaborn', fontsize=20)
plt.figure(figsize=(20, 20))
plt.show() 


# Heatmap by pandas
df.style.background_gradient(cmap='summer')

df.dtypes

























































