from glob import glob
from pathlib import Path
from typing import List

ROOT = Path('/home/gesogeso/PycharmProjects/nba_stats')


def get_all_players_tsv_file_names() -> List[str]:
    path = ROOT / 'static/players/all_*.tsv'
    return list(glob(str(path)))
