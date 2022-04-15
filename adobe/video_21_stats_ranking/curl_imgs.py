import datetime
import os
import sys
import subprocess
from pathlib import Path

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats\\utils')
# print(sys.path)
# from utils.static import ROOT
from operate_tsv import read_tsv

if __name__ == '__main__':
    target_date = '2022-04-11'  # tsvの日付と合わせる

    tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\' \
               f'analyze_03_season_stats_ranking\\results_{target_date}\\results_tsv_{target_date}.tsv'
    working_dir_path = Path(f'X:\\Adobe\\PremierePro\\21_StatsRanking')

    output_dir_path = working_dir_path / f'imgs\\imgs_{target_date}\\sozai_00'
    if not output_dir_path.exists():
        output_dir_path.mkdir()

    # ヘッダーの名前を直接指定する
    header_name = 'PLAYER_ID'

    # ヘッダーの列番号を指定する
    column_no = None

    # ヘッダーの列名からヘッダーの番号へ変換
    if not column_no:
        header = next(read_tsv(tsv_path))
        assert header_name in header, f'header_name: {header_name}がheaderに存在しません !!!!'
        column_no = header.index(header_name)

    # 画像をcurlで取得していく
    for row in read_tsv(tsv_path, skip_header=True):
        player_id = row[column_no]
        url = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
        # image_url = '/'.join(image_url.split('/')[:7]) + '/' + 'latest' + '/' + '/'.join(image_url.split('/')[-2:])
        file_path = output_dir_path / f'{player_id}.png'
        cmd = ['curl', '-o', f'{file_path}', f'{url}']
        print(cmd)
        subprocess.run(cmd)
