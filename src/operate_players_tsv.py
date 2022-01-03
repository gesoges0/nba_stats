from utils.operate_tsv import write_tsv
from typing import List, Dict, Any
from utils.static import ROOT
from nba_api.stats.static import players


def get_all_players() -> List[Dict[str, Any]]:
    """
    歴代全てのplayerを取得する
    :return:
    """
    response = players.get_players()
    return response


def get_active_players() -> List[Dict[str, Any]]:
    """
    active_playerを取得する
    :return:
    """
    response = players.get_active_players()
    return response


def make_players_tsv(update_date: str, active_or_all: str = "active") -> None:
    """
    update_date: YYYYMMDD
    active_or_all: 'active' or 'all'
    """
    assert active_or_all in ["active", "all"], 'active_or_all must be "active" or "all"'
    tsv_path = ROOT / "static/players" / f"{active_or_all}_{update_date}.tsv"
    if tsv_path.exists():
        print(f"{tsv_path} already exists !!!!!")
        return
    _players = None
    if active_or_all == "active":
        _players = get_active_players()
    else:
        _players = get_all_players()
    header = list(_players[0].keys())
    rows = list()
    rows.append(header)
    for _player in _players:
        rows.append(list(_player.values()))
    write_tsv(tsv_path, rows)


if __name__ == "__main__":
    make_players_tsv("20220102", "active")
