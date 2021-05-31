# Tableau prep builderでやっている前処理をしてCSV出力までを目指す。
# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
from datetime import timedelta
df01 = pd.read_csv('130001_tokyo_covid19_positive_cases_by_municipality.csv', encoding="UTF-8")
df01['date']=pd.to_datetime(df01['公表_年月日'],
               format='%Y-%m-%d').dt.date
last_day=df01[['date']].max()[0]
print(last_day)
df01['yesterday']=df01['date']-timedelta(1)
###ここで７日前、14日前の列も加える。
##SettingWithCopyWarningを回避のため、先にこれらの値を計算。あとで市区町村絞り込みする。 回避の解説はここ。https://linus-mk.hatenablog.com/entry/2019/02/02/200000
df02=df01.query('集計区分=="市区町村"')
print(df02)
df02.to_csv('covid19tokyo_preprocessed.csv')