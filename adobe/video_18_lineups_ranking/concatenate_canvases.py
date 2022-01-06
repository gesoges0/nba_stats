import os
import sys
from pathlib import Path

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.static import ROOT
from utils.operate_tsv import read_tsv, tsv_to_dict_by_first_header_column
from adobe.tools.other.concatenate_imgs import concatenate_images_with_cv2


if __name__ == '__main__':
    tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\' \
               'analyze_00_longest_lineup\\MIN_20220103\\ranking_lineups.tsv'
    working_dir_path = Path('X:\\Adobe\\PremierePro\\19_lineups')
    output_dir = working_dir_path / 'images\\canvases_sozai4'

    BEST_N = 300

    tsv_generator = read_tsv(tsv_path, skip_header=False)
    header = next(tsv_generator)
    for i, row in enumerate(tsv_generator):
        if i == BEST_N:
            break
        print(i)
        _, group_id, *_ = row
        # 各選手のid
        ids = group_id[1:-1].split('-')
        canvas_image_paths = [working_dir_path / f'images\\canvases_sozai3\\output\\{player_id}.png' for player_id in ids]
        output_file_path = output_dir / f'{i}.png'
        concatenate_images_with_cv2(canvas_image_paths, output_file_path, stride=2)

    print('end!')





