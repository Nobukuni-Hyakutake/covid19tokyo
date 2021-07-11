# -*- coding: utf-8 -*-
print('Processing...')
import pandas as pd
import numpy as np
import json
from folium.features import DivIcon
import folium
from datetime import datetime
from datetime import timedelta
url ="https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_positive_cases_by_municipality.csv"
df01 = pd.read_csv(url, encoding="UTF-8")
#df01 = pd.read_csv('130001_tokyo_covid19_positive_cases_by_municipality.csv', encoding="UTF-8")
df01['date']=pd.to_datetime(df01['公表_年月日'],
               format='%Y-%m-%d').dt.date
last_day1=df01['date'].max()

#東京都全体の1日ごとの集計
dfw01=df01 \
    .groupby(['date']) \
        .agg({'陽性者数':['sum']}).reset_index()
dfw01.columns=['date','count_w_sum']
dfw02=dfw01
dfw01['yesterday']=dfw01['date']-timedelta(1)
dfw02=dfw02.rename(columns={'count_w_sum':'count_w_sum_yesterday'})
dfw03=pd.merge(dfw01,dfw02,left_on='yesterday',right_on='date',how='inner')
dfw03['count_w_1day']=dfw03['count_w_sum']-dfw03['count_w_sum_yesterday']
dfw=dfw03.loc[:,['date_x','count_w_1day']]
dfw=dfw.rename(columns={'date_x':'date'})
dfw.to_csv('docs/dfw.csv')
#/東京都全体の1日ごとの集計

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
ruby2 = pd.read_csv('ruby2.csv', encoding="UTF-8")
df11=pd.merge(df10,ruby2,on='group_code',how='inner')
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

for i in range (62):
    dfgraph00201=out.loc[(out['number']==i),['group_code','label','ruby','date','count_1day','count_7days','population','en','number']].copy().reset_index()
    label00201=dfgraph00201['label'][0]
    en00201=dfgraph00201['en'][0]
    title00201=dfgraph00201['label'][0]+' 新型コロナウイルス陽性者数'
    dfgraph00201['sevendays_ave']=round((dfgraph00201['count_7days']/7)/dfgraph00201['population']*100000,1)
    dfgraph00201['count_1day_p']=round(dfgraph00201['count_1day']/dfgraph00201['population']*100000,1)
    dfgraph00201['stage4']=3.6
    dfgraph00201['stage3']=2.1

    fig00202=go.Bar(
        x=dfgraph00201["date"], y=dfgraph00201["count_1day_p"], name='10万人あたり',
        marker={"color": "#99cc66"},
        hoverinfo = "none",
        )
    fig00203=go.Scatter(
        x=dfgraph00201["date"], y=dfgraph00201["sevendays_ave"], name='10万人あたり7日間平均',
        line={"color": "#cc6600"},
    )
    figstage4=go.Scatter(
        x=dfgraph00201["date"], y=dfgraph00201["stage4"], name='ステージ4基準', 
        line={"width":1, "color": "red", "dash":"dash"},
        hoverinfo = "none"
)

    figstage3=go.Scatter(
        x=dfgraph00201["date"], y=dfgraph00201["stage3"], name='ステージ3基準',
        line={"width":1, "color": "#ffcc00", "dash":"dash"},
        hoverinfo = "none"
    )
    layout=go.Layout(
#    font=dict(size=20),
        title={"text":title00201,
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

    fig04=go.Figure(data=[fig00202, fig00203, figstage4, figstage3], layout=layout)
    fig04.update_yaxes(
        rangemode="nonnegative"
        )
    fig04.update_layout(legend_orientation="h")
    fig04.update_layout(legend={"x":0,"y":-0.1})

    fig04.update_xaxes(type='date', tickformat="%y/%-m/%-d", tick0='2020-05-01', dtick="M2") 

    fig04.write_html("docs/"+en00201+"_g.html")

df00101=out
df00101['g_url']='https://nobukuni-hyakutake.github.io/covid19tokyo/'+out['en']+'_g.html'
#map表示(工事中)
pd.set_option('display.max_rows', 100)
dfmap01=pd.read_csv('office_address.csv')
dfmap02=dfmap01.loc[(dfmap01['public_office_classification']==1),['group_code','office_no','public_office_name']]
dfmap02['office_no']=dfmap02['office_no'].str.replace(pat='#p',repl='').astype('int64')
dfmap11=pd.read_csv('office_position.csv')
dfmap11['id']=dfmap11['id'].str.replace(pat='p',repl='').astype('int64')
dfmap12=pd.concat([dfmap11, dfmap11['position'].str.split(' ', expand=True).astype('float64')], axis=1).drop('position', axis=1)
dfmap12.columns=['office_no','lat','lon']
dfmap13=pd.merge(dfmap02,dfmap12,on='office_no',how='inner').loc[:,['group_code','lat','lon']]
mapstep00100=dfmap13

dfmap20=df00101.query('date==last_day')
dfmap21=dfmap20.loc[:,['date','group_code','count_7days','last7days_ratio','pref','label','population','en','g_url','number']]
dfmap21['group_code']=dfmap21['group_code'].astype('str')
dfmap21['group_code']=dfmap21['group_code'].str[0:5]
mapstep00100['group_code']=mapstep00100['group_code'].astype('str')
dfmap30=pd.merge(dfmap21,mapstep00100,on='group_code',how='inner')
dfmap30['date']=dfmap30['date'].astype('datetime64')

dfmap30['last7days_ratio']=round(dfmap30['last7days_ratio'],2)
dfmap30['sevendays_ave_p']=round(dfmap30['count_7days']/dfmap30['population']*100000,2)
dfmap30['color']="#559e83"
dfmap30.loc[(dfmap30['last7days_ratio']<0.9),['color']]="#c3cb71"
dfmap30.loc[(dfmap30['last7days_ratio']>1.1),['color']]="#1b85b8"

dfmap30.to_csv('step00200.csv')

    
dfmap30['popup']='<a href="'+dfmap30['g_url']+'">Daily graph</a>'

test='Kokubunji'
test2='国分寺市'
base_amount=1.0
scale=40
tokyo_map=folium.Map(location=[35.710943,139.462252],zoom_start=11, tiles="openstreetmap")

tokyo_map=folium.Map(location=[35.710943,139.462252],zoom_start=11, tiles="cartodbdark_matter")
test_df=pd.read_csv('japan_co.csv')
#base_map=folium.Map(location=[35.655616,139.338853],zoom_start=5.0)#Choropleth追加
cho=folium.Choropleth(
    geo_data=json.load(open("Tokyo.geojson","r")),
    data=test_df,
    columns=["name","value"],
    key_on="feature.properties.name",
    fill_color="BuGn",
    fill_opacity=0.8,
    line_color="black",
    line_weight=1
    )
#凡例を隠す
for key in cho._children:
    if key.startswith('color_map'):
        del(cho._children[key])
#/凡例を隠す
cho.add_to(tokyo_map)

for index, row in dfmap30.iterrows():
    location=(row['lat'],row['lon'])
    radius=scale*(row['sevendays_ave_p']/base_amount)*0.7
    color=row['color']
    popup=row['popup']
    folium.Circle(
        location=location,
        radius=radius,
        color=color,
        fill_color=color,
        popup=popup
        ).add_to(tokyo_map)

for i in range(62):
    dfgraph00202=dfmap30.loc[(dfmap30['number']==i),['label','count_7days','population','en','number','lat','lon']]
    dfgraph00202=dfgraph00202.reset_index()
    label00202=dfgraph00202['label'][0]
    en00202=dfgraph00202['en'][0]
    dfgraph00202['sevendays_ave_p']=round((dfgraph00202['count_7days']/7)/dfgraph00202['population']*100000,1)
    sevendays_ave_p00201=dfgraph00202['sevendays_ave_p'][0]
    text00202='''<div style="font-size: 10pt" style="text-align:center;">'''+en00202+'<br>'+str(sevendays_ave_p00201)+'</div>'
    lat00202=dfgraph00202['lat'][0]
    lon00202=dfgraph00202['lon'][0]
    folium.map.Marker(
        [lat00202,lon00202],
        icon=DivIcon(
            icon_size=(0,0),
            icon_anchor=(20,20),
            html=text00202
            )
        ).add_to(tokyo_map)
tokyo_map.save(outfile="docs/tokyo_map.html")
#/map表示

print('last day is:')
print(last_day1)
print('Done')

