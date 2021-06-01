# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
print('Processing...')
url ="https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_positive_cases_by_municipality.csv"
df01 = pd.read_csv(url, encoding="UTF-8")

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

df10=df09.rename(columns={'date_x_x_x':'date','count_sum_x_x_x':'count_sum','count_1day_x_x':'count_1day','count_7days_x':'count_7days'})
df10['last7days_ratio']=(df10['count_7days']/(df10['count_14days']-df10['count_7days'])).replace([np.inf, -np.inf], np.nan)
df10['last_day']=last_day1

#ふりがな・人口を追加する
ruby = pd.read_csv('ruby.csv', encoding="UTF-8")
df11=pd.merge(df10,ruby,on='group_code',how='inner')
df11['population']=df11['population'].astype('float64')

out=df11
print(out)
print(out.dtypes)
out.to_csv('covid19tokyo_preprocessed.csv')

#やさしいにほんごここから

last_week=last_day1-timedelta(7)
df21=df01.loc[:,['市区町村名','陽性者数','date']]
df_last_day =df21.query('date==@last_day')
df_last_day_mitaka=df_last_day.query('市区町村名=="三鷹市"')
last_day_mitaka_count=df_last_day_mitaka[['陽性者数']].mean()[0]
df_last_day_musashino=df_last_day.query('市区町村名=="武蔵野市"')
last_day_musashino_count=df_last_day_musashino[['陽性者数']].mean()[0]
df_last_week =df21.query('date==@last_week')
df_last_week_mitaka=df_last_week.query('市区町村名=="三鷹市"')
last_week_mitaka_count=df_last_week_mitaka[['陽性者数']].mean()[0]
df_last_week_musashino=df_last_week.query('市区町村名=="武蔵野市"')
last_week_musashino_count=df_last_week_musashino[['陽性者数']].mean()[0]
mitaka_7day_count=int(last_day_mitaka_count-last_week_mitaka_count)
musashino_7day_count=int(last_day_musashino_count-last_week_musashino_count)
mitaka_easy='<html><meta charset="UTF-8"><head><title>東京都 三鷹市 新型コロナウイルス陽性者数 (やさしいにほんご)</title></head><body style="font-size: 24px;" bgcolor="#ffffcc">とうきょうと　<b>みたかし</b><br><b>'+str(last_day.month)+'がつ'+str(last_day.day)+'にち</b><br>までのいっしゅうかんに<br>しんがたころなういるすに<br>かんせんしたひとは<br><b>'+str(mitaka_7day_count)+'</b>にんです</body></html>'
fo=open('mitaka_easy.html','wt')
fo.write(mitaka_easy)
fo.close
musashino_easy='<html><meta charset="UTF-8"><head><title>東京都 武蔵野市 新型コロナウイルス陽性者数 (やさしいにほんご)</title></head><body style="font-size: 24px;" bgcolor="#ffffcc">とうきょうと　<b>むさしのし</b><br><b>'+str(last_day.month)+'がつ'+str(last_day.day)+'にち</b><br>までのいっしゅうかんに<br>しんがたころなういるすに<br>かんせんしたひとは<br><b>'+str(musashino_7day_count)+'</b>にんです</body></html>'
f2=open('musashino_easy.html','wt')
f2.write(musashino_easy)
f2.close

#やさしいにほんごここまで

print('Done')