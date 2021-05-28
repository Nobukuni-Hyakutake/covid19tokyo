# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
from datetime import timedelta
print('Processing...')
df01 = pd.read_csv('130001_tokyo_covid19_positive_cases_by_municipality.csv', encoding="UTF-8")
df01['date']=pd.to_datetime(df01['公表_年月日'],
               format='%Y-%m-%d').dt.date
last_day=df01[['date']].max()[0]
print(last_day)
last_week=last_day-timedelta(7)
df02=df01.loc[:,['市区町村名','陽性者数','date']]
df_last_day =df02.query('date==@last_day')
df_last_day_mitaka=df_last_day.query('市区町村名=="三鷹市"')
last_day_mitaka_count=df_last_day_mitaka[['陽性者数']].mean()[0]
df_last_day_musashino=df_last_day.query('市区町村名=="武蔵野市"')
last_day_musashino_count=df_last_day_musashino[['陽性者数']].mean()[0]
df_last_week =df02.query('date==@last_week')
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
print('Done')