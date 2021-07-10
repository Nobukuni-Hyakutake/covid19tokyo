# 東京都 区市町村別 新型コロナウイルス陽性者数のビジュアライゼーション
## 機能の解説
[main.py](https://github.com/Nobukuni-Hyakutake/covid19tokyo/blob/main/main.py)を実行すると最新データを読み込んで、下記が出力されます。
|ファイル|内容|公開先|
|:---|:---|:---|
|[docs/mitaka_easy.html](https://github.com/Nobukuni-Hyakutake/covid19tokyo/blob/main/docs/mitaka_easy.html)|三鷹市 やさしいにほんご表記|[リンク](https://nobukuni-hyakutake.github.io/covid19tokyo/mitaka_easy.html)|
|[docs/musashino_easy.html](https://github.com/Nobukuni-Hyakutake/covid19tokyo/blob/main/docs/musashino_easy.html)|武蔵野市 やさしいにほんご表記|[リンク](https://nobukuni-hyakutake.github.io/covid19tokyo/musashino_easy.html)|
|[docs/mitaka_graph.html](https://github.com/Nobukuni-Hyakutake/covid19tokyo/blob/main/docs/mitaka_graph.html)|三鷹市 時系列グラフ|[リンク](https://nobukuni-hyakutake.github.io/covid19tokyo/mitaka_graph.html)|
|[docs/musashino_graph.html](https://github.com/Nobukuni-Hyakutake/covid19tokyo/blob/main/docs/musashino_graph.html)|武蔵野市 時系列グラフ|[リンク](https://nobukuni-hyakutake.github.io/covid19tokyo/musashino_graph.html)|
|[docs/covid19tokyo_preprocessed.csv](https://github.com/Nobukuni-Hyakutake/covid19tokyo/blob/main/docs/covid19tokyo_preprocessed.csv)|Tableau用 前処理データ|[ダッシュボードリンク](https://public.tableau.com/app/profile/hyakutake/viz/32100/DB)|
|[docs/tokyo_map.html](https://github.com/Nobukuni-Hyakutake/covid19tokyo/blob/main/docs/tokyo_map.html)|東京都全体 区市町村別マップ|[リンク](https://nobukuni-hyakutake.github.io/covid19tokyo/tokyo_map.html)|
## Source
|項目|Source|
|:---|:---|
|陽性者数|[東京都_新型コロナウイルス感染症陽性者数（区市町村別）](https://catalog.data.metro.tokyo.lg.jp/dataset/t000010d0000000085/resource/d7b09ad5-077e-403b-b9ba-3f56bcaa55f2)|
|人口|[e-Stat](https://www.e-stat.go.jp)|
|位置|[国土交通省 国土数値情報 東京](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P34.html#prefecture13)|
|都道府県境界線|[日本の区画情報](https://github.com/kokubonatsumi/Japanmap)|
