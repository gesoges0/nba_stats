from glob import glob
from pathlib import Path
from typing import List, Dict

ROOT = Path('/home/gesogeso/PycharmProjects/nba_stats')

HEX_COLOR_CODE_BY_TEAM_ABBREVIATION: Dict[str, str] = {
        'ATL': 'E03A3E',
        'BOS': '007A33',
        "BKN": '000000',
        'CHA': '00788C',
        'CHI': 'CE1141',
        'CLE': '860038',
        'DAL': '00538C',
        'DEN': '0E2240',
        'DET': '1D42BA',
        'GSW': 'FFC72C',
        'HOU': 'CE1141',
        'IND': 'FDBB30',
        'LAC': '1D428A',
        'LAL': '552583',
        'MEM': '5D76A9',
        'MIA': '98002E',
        'MIL': '00471B',
        'MIN': '0C2340',
        'NOP': '0C2340',
        'NYK': 'F58426',
        'OKC': '007AC1',
        'ORL': '0077C0',
        'PHI': '006BB6',
        'PHX': 'E56020',
        'POR': 'E03A3E',
        'SAC': '5A2D81',
        'SAS': '8A8D8F',
        'TOR': 'CE1141',
        'UTA': '002B5C',
        'WAS': '002B5C',
    }


def get_all_players_tsv_file_names() -> List[str]:
    path = ROOT / 'static/players/all_*.tsv'
    return list(glob(str(path)))


def get_team_hex_color_code(team_abbreviation: str) -> str:
    assert team_abbreviation in HEX_COLOR_CODE_BY_TEAM_ABBREVIATION, f'{team_abbreviation} not exists !!!!'
    return HEX_COLOR_CODE_BY_TEAM_ABBREVIATION[team_abbreviation]
