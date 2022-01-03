from utils.operate_tsv import write_tsv
from typing import List, Dict, Any
from utils.static import ROOT
from nba_api.stats.static import teams


def get_active_teams() -> List[Dict[str, Any]]:
    """
    :return: 現在あるチームを返す
    """
    return teams.get_teams()


def make_teams_tsv() -> None:
    """
    チームの変更はそうそう起こり得るものではないため、ファイル名は固定しても大丈夫
    チームの変更などがあった場合にのみ対処する
    :param update_date: YYYYMMDD
    :return:
    """
    teams_list: List[Dict[str, Any]] = get_active_teams()
    header = list(teams_list[0].keys())
    rows = list()
    rows.append(header)
    for team in teams_list:
        rows.append(list(team.values()))

    tsv_path = ROOT / 'static/teams/teams.tsv'
    write_tsv(tsv_path, rows)

