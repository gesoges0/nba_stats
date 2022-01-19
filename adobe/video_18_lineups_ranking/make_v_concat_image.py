import os
import sys
from pathlib import Path

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.time import get_current_datetime_with_yyyymmdd_format
from adobe.tools.other.concatenate_imgs import concatenate_images_with_cv2


if __name__ == '__main__':
    # 作業ディレクトリ
    working_dir_root = Path('X:\\Adobe\\PremierePro\\19_lineups\\images\\lineups_20220117')

    # 入力画像ディレクトリ
    input_images_dir = working_dir_root / 'sozai_04'

    # 出力ディレクトリ
    yyyymmdd = get_current_datetime_with_yyyymmdd_format()
    output_image_path = working_dir_root / f'output_{yyyymmdd}.png'

    # 画像結合
    image_paths = [str(input_image_path) for input_image_path in input_images_dir.iterdir()]
    image_paths.sort(key=lambda x: int(x.split('\\')[-1].replace('.png', '')))
    image_paths = image_paths[:20]
    concatenate_images_with_cv2(image_paths, output_image_path, mode='v')

