import cv2
import sys
from pathlib import Path
import numpy as np

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.static import HEX_COLOR_CODE_BY_TEAM_ABBREVIATION

if __name__ == '__main__':

    # 作業場
    target_date = '2022-01-19'
    working_dir = Path(f'X:\\Adobe\\PremierePro\\21_StatsRanking\\imgs\\imgs_{target_date}\\sozai_01')
    if not working_dir.exists():
        working_dir.mkdir()

    # 縦, 横
    height, width = 385, 307

    # サイズ
    for team_abbreviation, team_color in HEX_COLOR_CODE_BY_TEAM_ABBREVIATION.items():
        img_path = working_dir / f'{team_abbreviation}.png'
        R, G, B = int(team_color[:2], 16), int(team_color[2:4], 16), int(team_color[4:6], 16)
        team_color_img = np.zeros((height, width, 3))
        team_color_img += [R, G, B][::-1]  # RGBで青指定
        cv2.imwrite(str(img_path), team_color_img)
