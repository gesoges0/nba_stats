import os
import sys
from pathlib import Path

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.static import ROOT
from utils.operate_tsv import read_tsv, tsv_to_dict_by_first_header_column
from adobe.tools.other.concatenate_imgs import concatenate_images_with_cv2


if __name__ == '__main__':
    tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\' \
               'analyze_00_longest_lineup\\MIN_20220415\\ranking_lineups.tsv'
    working_dir_path = Path('X:\\Adobe\\PremierePro\\19_lineups')
    input_img_path_format = str(working_dir_path / 'images\\lineups_20220415\\sozai_01\\output\\{}.png')

    output_dir = working_dir_path / 'images\\lineups_20220415\\sozai_02\\output'
    if not output_dir.exists():
        output_dir.mkdir()

    BEST_N = 50

    tsv_generator = read_tsv(tsv_path, skip_header=False)
    header = next(tsv_generator)
    for i, row in enumerate(tsv_generator):
        print(i, row)
        if i == BEST_N:
            break
        print(i)
        _, group_id, *_ = row
        # 各選手のid
        ids = group_id[1:-1].split('-')
        canvas_image_paths = []
        for player_id in ids:
            input_img_path = input_img_path_format.format(player_id)
            if not os.path.exists(input_img_path):
                assert False, f'{input_img_path} not exists !'
            canvas_image_paths.append(input_img_path)
        output_file_path = output_dir / f'{i}.png'
        print(output_file_path)
        concatenate_images_with_cv2(canvas_image_paths, output_file_path)

    print('end!')





