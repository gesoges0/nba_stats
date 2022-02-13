import os
import csv
from pathlib import Path
import subprocess

output_dir_path = Path("X:\\Adobe\\PremierePro\\images\\player_images_20220128")


def curl_imgs():
    tsv_path = 'result_2022_01_28.tsv'
    with open(tsv_path, 'r') as f:
        reader = csv.reader(f, delimiter='\t', lineterminator='\n')
        for row in reader:
            player_id, player_name, minutes, net_rtg, img_url = row
            output_file_path = output_dir_path / f'{player_id}.png'
            cmd = ['curl', '-o', str(output_file_path), f'{img_url}']
            subprocess.run(cmd)


def rm_not_imgs():
    for png_path in output_dir_path.glob("*.png"):
        if os.path.getsize(str(png_path)) < 10000:
            print(png_path)
            png_path.unlink()


if __name__ == '__main__':
    print('hello')
    # curl_imgs()

    rm_not_imgs()
