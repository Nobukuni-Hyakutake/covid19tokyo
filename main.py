# -*- coding: utf-8 -*-
print('Processing...')
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
url ="https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_positive_cases_by_municipality.csv"
df01 = pd.read_csv(url, encoding="UTF-8")
df01['date']=pd.to_datetime(df01['公表_年月日'],
               format='%Y-%m-%d').dt.date
last_day1=df01['date'].max()

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
#print(out)
#print(out.dtypes)
out.to_csv('docs/covid19tokyo_preprocessed.csv')

out2=df11.loc[:,['group_code','ruby','date','count_1day','count_7days']]
out2.to_csv('docs/covid19tokyo_preprocessed_light.csv')

#やさしいにほんごここから
last_week=last_day1-timedelta(7)
df21=df01.loc[:,['市区町村名','陽性者数','date']]
last_day_mitaka_count=df21.query('(市区町村名=="三鷹市")&(date==@last_day1)').mean()[0]
last_day_musashino_count=df21.query('(市区町村名=="武蔵野市")&(date==@last_day1)').mean()[0]
df_last_week =df21.query('date==@last_week')
df_last_week_mitaka=df_last_week.query('市区町村名=="三鷹市"')
last_week_mitaka_count=df_last_week_mitaka[['陽性者数']].mean()[0]
df_last_week_musashino=df_last_week.query('市区町村名=="武蔵野市"')
last_week_musashino_count=df_last_week_musashino[['陽性者数']].mean()[0]
mitaka_7day_count=int(last_day_mitaka_count-last_week_mitaka_count)
musashino_7day_count=int(last_day_musashino_count-last_week_musashino_count)
mitaka_easy='<html><meta charset="UTF-8"><head><title>東京都 三鷹市 新型コロナウイルス陽性者数 (やさしいにほんご)</title></head><body style="font-size: 24px;" bgcolor="#ffffcc">とうきょうと　<b>みたかし</b><br><b>'+str(last_day1.month)+'がつ'+str(last_day1.day)+'にち</b><br>までのいっしゅうかんに<br>しんがたころなういるすに<br>かんせんしたひとは<br><b>'+str(mitaka_7day_count)+'</b>にんです</body></html>'
fo=open('docs/mitaka_easy.html','wt')
fo.write(mitaka_easy)
fo.close
musashino_easy='<html><meta charset="UTF-8"><head><title>東京都 武蔵野市 新型コロナウイルス陽性者数 (やさしいにほんご)</title></head><body style="font-size: 24px;" bgcolor="#ffffcc">とうきょうと　<b>むさしのし</b><br><b>'+str(last_day1.month)+'がつ'+str(last_day1.day)+'にち</b><br>までのいっしゅうかんに<br>しんがたころなういるすに<br>かんせんしたひとは<br><b>'+str(musashino_7day_count)+'</b>にんです</body></html>'
f2=open('docs/musashino_easy.html','wt')
f2.write(musashino_easy)
f2.close
#やさしいにほんごここまで

import plotly.express as px
import plotly.graph_objects as go

dfmusashino=out.loc[(out['group_code']==132039),['group_code','label','date','count_1day','count_7days','population']].copy()
dfmusashino['sevendays_ave']=round((dfmusashino['count_7days']/7)/dfmusashino['population']*100000,1)
dfmusashino['count_1day_p']=round(dfmusashino['count_1day']/dfmusashino['population']*100000,1)
dfmusashino['stage4']=3.6
dfmusashino['stage3']=2.1

fig02=go.Bar(
    x=dfmusashino["date"], y=dfmusashino["count_1day_p"], name='10万人あたり',
    marker={"color": "#99cc66"},
    hoverinfo = "none",
    )
fig03=go.Scatter(
    x=dfmusashino["date"], y=dfmusashino["sevendays_ave"], name='10万人あたり7日間平均',
    line={"color": "#cc6600"},
)
figstage4=go.Scatter(
    x=dfmusashino["date"], y=dfmusashino["stage4"], name='ステージ4基準', 
    line={"width":1, "color": "red", "dash":"dash"},
    hoverinfo = "none"
)

figstage3=go.Scatter(
    x=dfmusashino["date"], y=dfmusashino["stage3"], name='ステージ3基準',
    line={"width":1, "color": "#ffcc00", "dash":"dash"},
    hoverinfo = "none"
)
layout=go.Layout(
#    font=dict(size=20),
    title={"text":'武蔵野市 新型コロナウイルス陽性者数',
    },
    xaxis={
        "linecolor": "black"   
        },    
yaxis={
        "title":{
        "text": '10万人あたり',
        },
        "linecolor": "black",   
        },
    hovermode='x',
    plot_bgcolor="#ffffff"
    )

fig04=go.Figure(data=[fig02, fig03, figstage4, figstage3], layout=layout)
fig04.update_yaxes(
    rangemode="nonnegative"
)
fig04.update_layout(legend_orientation="h")
fig04.update_layout(legend={"x":0,"y":-0.2})

fig04.update_xaxes(type='date', tickformat="%y/%-m/%-d", tick0='2020-05-01', dtick="M2") 
#fig04.show()
fig04.write_html("docs/musashino_graph.html")

dfmitaka=out.loc[(out['group_code']==132047),['group_code','label','date','count_1day','count_7days','population']].copy()
dfmitaka['sevendays_ave']=round((dfmitaka['count_7days']/7)/dfmitaka['population']*100000,1)
dfmitaka['count_1day_p']=round(dfmitaka['count_1day']/dfmitaka['population']*100000,1)
dfmitaka['stage4']=3.6
dfmitaka['stage3']=2.1

fig12=go.Bar(
    x=dfmitaka["date"], y=dfmitaka["count_1day_p"], name='10万人あたり',
    marker={"color": "#99cc66"},
    hoverinfo = "none",
    )
fig13=go.Scatter(
    x=dfmitaka["date"], y=dfmitaka["sevendays_ave"], name='10万人あたり7日間平均',
    line={"color": "#cc6600"},
)

layout=go.Layout(
#    font=dict(size=20),
    title={"text":'三鷹市 新型コロナウイルス陽性者数',
    },
    xaxis={
        "linecolor": "black"   
        },    
yaxis={
        "title":{
        "text": '10万人あたり',
        },
        "linecolor": "black",   
        },
    hovermode='x',
    plot_bgcolor="#ffffff"
    )

fig14=go.Figure(data=[fig12, fig13, figstage4, figstage3], layout=layout)
fig14.update_yaxes(
    rangemode="nonnegative"
)
fig14.update_layout(legend_orientation="h")
fig14.update_layout(legend={"x":0,"y":-0.2})

fig14.update_xaxes(type='date', tickformat="%y/%-m/%-d", tick0='2020-05-01', dtick="M2") 
#fig04.show()
fig14.write_html("docs/mitaka_graph.html")

print('last day is:')
print(last_day1)
print('Done')

#map表示(工事中 groupcode, lat, lonのテーブルまで作成済み)
dfmap01=pd.read_csv('office_address.csv')
dfmap02=dfmap01.loc[(dfmap01['public_office_classification']==1),['group_code','office_no','public_office_name']]
dfmap02['office_no']=dfmap02['office_no'].str.replace(pat='#p',repl='').astype('int64')
dfmap11=pd.read_csv('office_position.csv')
dfmap11['id']=dfmap11['id'].str.replace(pat='p',repl='').astype('int64')
dfmap12=pd.concat([dfmap11, dfmap11['position'].str.split(' ', expand=True).astype('float64')], axis=1).drop('position', axis=1)
dfmap12.columns=['office_no','lat','lon']
dfmap13=pd.merge(dfmap02,dfmap12,on='office_no',how='inner').loc[:,['group_code','lat','lon']]
mapstep00100=dfmap13
#/map表示