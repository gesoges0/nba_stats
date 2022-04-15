import os
import sys

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.operate_tsv import tsv_to_dict_of_list
from adobe.tools.other.make_synthetic import make_synthetic
from adobe.tools.other.utils import write_img

MAX_N = 50

if __name__ == '__main__':
    # 作業ディレクトリ
    working_dir_root = Path('X:\\Adobe\\PremierePro\\19_lineups\\images')

    # 背景画像ディレクトリ
    bg_images_dir = working_dir_root / 'lineups_20220415\\sozai_03\\output'

    # lineup画像のディレクトリ
    lineup_images_dir = working_dir_root / 'lineups_20220415\\sozai_02\\output'

    # チームロゴ画像のディレクトリ
    team_logo_images_dir = working_dir_root / 'logo_png_resized'

    # output
    output_images_dir = working_dir_root / 'lineups_20220415\\sozai_04'

    # 順位のTSV
    ranking_tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\' \
                       'analyze_00_longest_lineup\\MIN_20220415\\ranking_lineups.tsv'

    # 順位TSVを読み込む
    ranking_lineups: List[Dict[str, str]] = tsv_to_dict_of_list(ranking_tsv_path)

    for i, lineup in enumerate(ranking_lineups[:MAX_N]):
        rank = i + 1
        bg_img_path = bg_images_dir / f'{i}.png'
        team_logo_img_path = team_logo_images_dir / f'{lineup["TEAM_ABBREVIATION"]}.png'
        lineup_img_path = lineup_images_dir / f'{i}.png'

        print(i, lineup['TEAM_ABBREVIATION'])

        # 画像読み込み
        print(bg_img_path)
        bg_img = cv2.cvtColor(cv2.imread(str(bg_img_path), cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2RGBA)
        team_logo_img = cv2.imread(str(team_logo_img_path), cv2.IMREAD_UNCHANGED)
        lineup_img = cv2.imread(str(lineup_img_path), cv2.IMREAD_UNCHANGED)

        # チームロゴを背景に(920, 20)の位置に埋め込む
        result_img: np.ndarray = make_synthetic(bg_img, team_logo_img, (920, 20))

        # lineup画像を背景に(23, 160)の位置に埋め込む
        result_img: np.ndarray = make_synthetic(result_img, lineup_img, (23, 158))

        # 画像書き込み
        result_img_path = output_images_dir / f'{i}.png'
        write_img(str(result_img_path), result_img)
