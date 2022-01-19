## video_21

### 順位tsvを更新
```commandline
cd nba_stats/analysis/analyze_03_season_stats_ranking
python get_season_stats_ranking.py
```

### curl
```commandline
cd nba_stats/adobe/video_21_stats_ranking
python curl_imgs.py
```

### ベースの画像をつくる（チームカラーの画像）
```commandline
python make_base_canvas.py
```

### 選手とチームロゴの合成画像をつくる
```commandline
python make_synthetic_images_player_and_logo.py
```

### Photoshopでランキング画像の1枚を作成
```commandline
python make_canvas_by_photoshop.py
```

### 画像を横並びに結合する
```commandline
python make_concat_canvas.py
```