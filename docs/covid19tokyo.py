# Tableau prep builderでやっている前処理をしてCSV出力までを目指す。
# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
from datetime import timedelta
df01 = pd.read_csv('130001_tokyo_covid19_positive_cases_by_municipality.csv', encoding="UTF-8")
df01['date']=pd.to_datetime(df01['公表_年月日'],
               format='%Y-%m-%d').dt.date
last_day1=df01[['date']].max()[0]
print(last_day1)
##SettingWithCopyWarningを回避のため、copyとする。解説はここ。https://linus-mk.hatenablog.com/entry/2019/02/02/200000
df02=df01.loc[(df01['集計区分']=='市区町村'),:].copy()
df03=df02.rename(columns={'全国地方公共団体コード':'group_code','陽性者数':'count_sum'})
df04=df03.loc[:,['group_code','count_sum','date']]
df04['group_code']=df04['group_code'].astype('int64')
df04['count_sum']=df04['count_sum'].astype('float64')
#1日分の陽性者数の算出ここから
df04['yesterday']=df04['date']-timedelta(1)
df05=pd.merge(df04,df04,left_on=['group_code','yesterday'],right_on=['group_code','date'],how='inner')
df05['count_1day']=df05['count_sum_x']-df05['count_sum_y']
df06=df05.loc[:,['group_code','count_sum_x','date_x','count_1day']]
#1日分の陽性者数の算出ここまで

#7日分の陽性者数の算出ここから
df06['sevendays_before']=df06['date_x']-timedelta(7)
df07=pd.merge(df06,df06,left_on=['group_code','sevendays_before'],right_on=['group_code','date_x'],how='inner')
df07['count_7days']=df07['count_sum_x_x']-df07['count_sum_x_y']
df08=df07.loc[:,['group_code','count_sum_x_x','date_x_x','count_1day_x','count_7days']]
#7日分の陽性者数の算出ここまで

#14日分の陽性者数の算出ここから
df08['fourteendays_before']=df08['date_x_x']-timedelta(14)
df09=pd.merge(df08,df08,left_on=['group_code','fourteendays_before'],right_on=['group_code','date_x_x'],how='inner')
df09['count_14days']=df09['count_sum_x_x_x']-df09['count_sum_x_x_y']
df09=df09.loc[:,['group_code','date_x_x_x','count_sum_x_x_x','count_1day_x_x','count_7days_x','count_14days']]
#14日分の陽性者数の算出ここまで


#df04['last_day']=last_day1

out=df09
print(out)
print(out.dtypes)
out.to_csv('covid19tokyo_preprocessed.csv')
