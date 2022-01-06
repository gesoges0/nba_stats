# 最長Lineupを決める

### Lineupsを更新
```commandline
cd analysis/analyze_00_longest_lineup
python get_longest_lineup_ranking.py --stat MIN
```

### 選手画像を取得
analysis/analyze_00_longest_lineup/MIN_20200103/unique_players_list.tsvから, player_idとimage_urlを参考にしてcurlで取得する.
保存先は`X:\Adobe\PremierePro\19_lineups\images\canvases_素材2`

※`adobe/video_18_lineups_ranking`以下に作らなかったので, 再現性ないかも. commit-hashは
`74ed55eba87f5666573ce8a10daa4e197737a25e`でcommit-messageは
`add: tsv curl tool`
```commandline
cd adobe/tools/other/
python curl_tsv_row.py
```

### 選手画像から選手の説明画像を作る
`X:\Adobe\PremierePro\19_lineups\images\canvases_素材2`に集めた画像と, 
`X:\Adobe\PremierePro\19_lineups\images\canvases_素材3\template.psd`を用いて, 画像を作成する.
出力先は`X:\Adobe\PremierePro\19_lineups\images\canvases_素材3\output`
```commandline
cd adobe/video_18_lineups_ranking
python make_canvas.py
```

### 結合
`X:\Adobe\PremierePro\19_lineups\images\canvases_素材3`と`X:\Adobe\PremierePro\19_lineups\images\canvases_素材4`の
日本語をローマ字に変換する必要がある(CV2で日本語のパスが処理できないため)
```commandline
cd adobe/video_18_lineups_ranking
python concatenate_canvases.py
```

### 1つのチームの背景テンプレートから各チームの背景テンプレートを複製する
※background-colorの更新はpythonの実行前にPhotoshopで対象のレイヤを選択する必要があった.
```commandline
cd adobe/video_18_lineups_ranking
python make_each_team_canvases.py
```

### 背景画像にチームロゴ画像, 選手画像の順で重ねていく
```commandline
cd adobe/video_18_lineups_ranking
python make_synthetic.py
```

### 縦方向に結合
```commandline
cd adobe/video_18_lineups_ranking
python make_v_concat_image.py
```
