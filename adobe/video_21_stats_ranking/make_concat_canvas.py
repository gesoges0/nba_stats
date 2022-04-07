import sys

import cv2
import numpy as np
from photoshop import Session
from pathlib import Path
from typing import Dict, List, Any

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')

from utils.operate_tsv import tsv_to_dict_of_list, tsv_to_dict_by_first_header_column
from adobe.tools.other.concatenate_imgs import concatenate_images_with_ndarray
from adobe.tools.other.utils import write_img

if __name__ == '__main__':

    target_date = '2022-02-21'

    target_stats_list = ['FG3M', 'PTS', 'AST', 'REB', 'STL', 'BLK', 'DREB', 'OREB', 'TO', 'FGA', 'FGM', 'FG3M', 'FG3A', 'FTM', 'FTA', 'G']

    working_dir = Path('X:\\Adobe\\PremierePro\\21_StatsRanking\\imgs')

    player_info_tsv = Path('C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\players\\active_20220103.tsv')
    player_info_by_player_id: Dict[str, Any] = tsv_to_dict_by_first_header_column(player_info_tsv)

    team_info_tsv = Path('C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\teams\\teams.tsv')
    team_dict_list: Dict[str, str] = tsv_to_dict_of_list(team_info_tsv)

    player_stats_tsv = Path('C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis'
                            f'\\analyze_03_season_stats_ranking\\results_{target_date}\\results_tsv_{target_date}.tsv')
    stats_by_player_id: Dict[str, Any] = tsv_to_dict_by_first_header_column(player_stats_tsv)

    # strideの画像
    stride_img_path = working_dir / f'stride.png'
    stride_img = np.zeros((720, 13, 3)) + [208, 234, 218][::-1]
    write_img(str(stride_img_path), stride_img)
    stride_img = cv2.imread(str(stride_img_path), cv2.IMREAD_UNCHANGED)

    for target_stats in target_stats_list:

        # output dir
        output_dir = working_dir / f'imgs_{target_date}\\output\\{target_stats}'
        if not output_dir.exists():
            output_dir.mkdir()

        # output file path
        output_file_path = output_dir / f'{target_stats}.png'

        # 結合対象のディレクトリ
        img_dir = working_dir / f'imgs_{target_date}\\sozai_03\\{target_stats}'

        # 画像を取得してPER GAMEのスタッツ順に並べかえ（大きい順に）
        img_paths = [img_path for img_path in img_dir.glob('*.png')]
        img_paths.sort(key=lambda x:
            (
                -int(str(x).replace('.png', '').split('\\')[-1].split('_')[0]),
                int(stats_by_player_id[str(x).replace('.png', '').split('\\')[-1].split('_')[-1]][f'{target_stats}']),
                int(stats_by_player_id[str(x).replace('.png', '').split('\\')[-1].split('_')[-1]][f'{target_stats}'])
                / int(stats_by_player_id[str(x).replace('.png', '').split('\\')[-1].split('_')[-1]]['G'])
             )
        )

        # 各画像を左から結合していく
        for i, img_path in enumerate(img_paths):
            img = cv2.imread(str(img_path), cv2.IMREAD_UNCHANGED)
            tmp_img = concatenate_images_with_ndarray(stride_img, img)
            if i == 0:
                result_img = tmp_img
            else:
                result_img = concatenate_images_with_ndarray(result_img, tmp_img)
        result_img = concatenate_images_with_ndarray(result_img, stride_img)
        write_img(str(output_file_path), result_img)

