# 最も出場時間の長いlineupのランキングをtsvにして出力
from nba_api.stats.endpoints import leaguedashlineups
from typing import List, Dict, Any, Set, NamedTuple
import os
import sys
import argparse
from pathlib import Path

# nba_statsの階層でutils等をimportする
sys.path.append('/home/gesogeso/PycharmProjects/nba_stats/')
print(sys.path)
from utils.operate_tsv import write_tsv
from utils.structures import Player
from utils.time import get_current_datetime_with_yyyymmdd_format
from utils.players import get_players_by_id_dict
from utils.images import get_image_url
from utils.operate_tsv import write_tsv_from_dict_list


BEST_N = 300


def get_response():
    response = leaguedashlineups.LeagueDashLineups()
    return response.get_normalized_dict()


if __name__ == '__main__':
    # 引数(sorted_key)
    parser = argparse.ArgumentParser(description='降順にしたいスタッツ(MINがデフォルト)')
    parser.add_argument('--stat', type=str, default='MIN', help='choose [MIN, PTS, FG3M, ...]')
    args = parser.parse_args()

    # 結果を受け取る
    lineups: List[Dict[str, Any]] = get_response()['Lineups']

    # sorted_key順に降順ソート
    sorted_key = args.stat
    lineups.sort(key=lambda x: -x[f'{sorted_key}'])

    # 必要な追加情報を取得(画像はcurlでまとめて取得したいので別途記述)
    players_by_id: Dict[str, Player] = get_players_by_id_dict()

    lineups_ids: List[List[str]] = list()
    lineups_full_names: List[List[str]] = list()
    lineups_image_urls: List[List[str]] = list()
    for lineup in lineups[:BEST_N]:
        team_id = lineup['TEAM_ID']
        season_id = '2021'
        player_ids = lineup['GROUP_ID'][1:-1].split('-')
        # id
        lineup_ids: List[str] = [players_by_id[player_id].id for player_id in player_ids]
        lineups_ids.append(lineup_ids)
        # 選手名
        lineup_full_names: List[str] = [players_by_id[player_id].full_name for player_id in player_ids]
        lineups_full_names.append(lineup_full_names)
        # 各選手の画像URL
        lineup_image_urls = [get_image_url(player_id, team_id, season_id) for player_id in player_ids]
        lineups_image_urls.append(lineup_image_urls)

    # 結果を出力する
    current_date = get_current_datetime_with_yyyymmdd_format()
    dir_path = Path(os.path.dirname(__file__)) / f'{sorted_key}_{current_date}'
    tsv_path = dir_path / f'ranking_lineups.tsv'
    assert lineups, 'lineups is None !!!!'
    assert not dir_path.exists(), f'既に{dir_path}が存在しています !!!!'
    assert not tsv_path.exists(), f'{tsv_path} already exists !!!!'

    dir_path.mkdir()
    write_tsv_from_dict_list(tsv_path, lineups)

    result_ids = list()
    header_player = [f'player{i}' for i in range(1, 5 + 1)]
    result_ids.append(header_player)
    for lineup_ids in lineups_ids:
        result_ids.append(lineup_ids)
    tsv_path = dir_path / f'ranking_lineups_ids.tsv'
    write_tsv(tsv_path, result_ids)

    result_players = list()
    header_player = [f'player{i}' for i in range(1, 5 + 1)]
    result_players.append(header_player)
    for lineup_full_names in lineups_full_names:
        result_players.append(lineup_full_names)
    tsv_path = dir_path / f'ranking_lineups_full_names.tsv'
    write_tsv(tsv_path, result_players)

    result_image_urls = list()
    header_image_url = [f'player{i}' for i in range(1, 5 + 1)]
    result_image_urls.append(header_image_url)
    for lineup_image_urls in lineups_image_urls:
        result_image_urls.append(lineup_image_urls)
    tsv_path = dir_path / f'ranking_lineups_image_urls.tsv'
    write_tsv(tsv_path, result_image_urls)

    # 重複を排除した情報
    class PlayerTeamSeasonUrl(NamedTuple):
        player_id: str
        player_name: str
        team_id: str
        seaon_id: str
        url: str

    players_set: Set = set()
    for lineup in lineups[:BEST_N]:
        team_id = lineup['TEAM_ID']
        season_id = '2021'
        player_ids = lineup['GROUP_ID'][1:-1].split('-')
        for player_id in player_ids:
            player_team_season_url = \
                PlayerTeamSeasonUrl(player_id,
                                    players_by_id[player_id].full_name,
                                    team_id,
                                    season_id,
                                    get_image_url(player_id, team_id, season_id)
                                    )
            players_set.add(player_team_season_url)
    result_players = [[_.player_id, _.player_name, _.team_id, _.seaon_id, _.url] for _ in players_set]
    header = ['player_id', 'player_full_name', 'team_id', 'season_id', 'image_url']
    result_players.insert(0, header)
    tsv_path = dir_path / 'unique_players_list.tsv'
    write_tsv(tsv_path, result_players)


