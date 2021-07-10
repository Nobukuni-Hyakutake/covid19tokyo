import folium
import json
import pandas as pd

test_map=folium.Map(location=[35.710943,139.462252],zoom_start=11, tiles="cartodbdark_matter")
test_df=pd.read_csv('japan_co.csv')
#base_map=folium.Map(location=[35.655616,139.338853],zoom_start=5.0)#Choropleth追加
folium.Choropleth(
    geo_data=json.load(open("Japan.geojson","r")),
    data=test_df,
    columns=["name","value"],
    key_on="feature.properties.name",
    fill_color="BuGn",
    fill_opacity=0.7,
    line_color="black",
    line_weight=1
    ).add_to(test_map)
test_map.save(outfile="docs/test_map.html")
