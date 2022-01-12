import csv
from glob import glob
from typing import List, Dict, Any
from utils.static import ROOT
from utils.operate_tsv import read_all_rows_from_tsv
from utils.structures import Player
from nba_api.stats.endpoints import commonplayerinfo


def get_players_by_id_dict() -> Dict[str, Player]:
    """
    player_idから選手情報を取得
    :return: Player
    """
    tsv_path = glob(str(ROOT / 'static/players/all_*'))[-1]
    players_by_id: Dict[str, Player] = {p[0]: Player(*p) for p in read_all_rows_from_tsv(tsv_path)}
    return players_by_id