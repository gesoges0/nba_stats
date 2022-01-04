import subprocess
from pathlib import Path


if __name__ == '__main__':
    # windowsではconvertはNTFSに変更するものなので注意
    dir_path = Path('X:\\Adobe\\PremierePro\\19_lineups\\images\\logo')
    from_extension = 'svg'
    to_extension = 'png'

    for file_path in dir_path.glob(f'*.{from_extension}'):
        from_file = str(file_path)
        to_file = str(from_file.replace(f'.{from_extension}', f'.{to_extension}'))
        cmd = ['convert', f'{from_file}', f'{to_file}']
        subprocess.run(cmd)