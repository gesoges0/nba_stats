import os
import sys
import subprocess
from pathlib import Path

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats\\utils')
# print(sys.path)
# from utils.static import ROOT
from operate_tsv import read_tsv

if __name__ == '__main__':
    tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\' \
               'analyze_00_longest_lineup\\MIN_20220127\\unique_players_list.tsv'
    working_dir_path = Path(f'X:\\Adobe\\PremierePro\\19_lineups')
    output_dir_path = working_dir_path / 'images\\lineups_20220127\\sozai_00'
    if not output_dir_path.exists():
        output_dir_path.mkdir()

    # ヘッダーの名前を直接指定する
    header_name = 'player_id'
    file_name_header_column = 'image_url'

    # ヘッダーの列番号を指定する
    column_no = None
    file_name_column_no = None

    # ヘッダーの列名からヘッダーの番号へ変換
    if not column_no and not file_name_column_no:
        header = next(read_tsv(tsv_path))
        assert header_name in header, f'header_name: {header_name}がheaderに存在しません !!!!'
        assert file_name_header_column in header, \
            f'file_name_header_column: {file_name_header_column}がheaderに存在しません !!!!'
        column_no = header.index(header_name)
        file_name_column_no = header.index(header_name)

    # 画像をcurlで取得していく
    for row in read_tsv(tsv_path, skip_header=True):
        player_id, *_, image_url = row
        # image_url = '/'.join(image_url.split('/')[:7]) + '/' + 'latest' + '/' + '/'.join(image_url.split('/')[-2:])
        file_path = output_dir_path / f'{player_id}.png'
        cmd = ['curl', '-o', f'{file_path}', f'{image_url}']
        print(cmd)
        subprocess.run(cmd)
