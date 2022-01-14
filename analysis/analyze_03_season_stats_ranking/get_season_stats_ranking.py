import datetime
import time
from pathlib import Path
from typing import Dict, List, Any, NamedTuple
from dataclasses import dataclass
from collections import defaultdict, namedtuple
import pickle
import sys


sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.operate_tsv import write_tsv

@dataclass
class Game:
    SEASON_ID: str
    TEAM_ID: int
    TEAM_ABBREVIATION: str
    TEAM_NAME: str
    GAME_ID: str
    GAME_DATE: str # 2021-10-19
    MATCHUP: str
    WL: str
    MIN: int
    PTS: int
    FGM: int
    FGA: int
    FG_PCT: float
    FG3M: int
    FG3A: int
    FG3_PCT: float
    FTM: int
    FTA: int
    FT_PCT: float
    OREB: int
    DREB: int
    REB: int
    AST: int
    STL: int
    BLK: int
    TOV: int
    PF: int
    PLUS_MINUS: float


@dataclass
class PlayerStats:
    GAME_ID: str
    TEAM_ID: int
    TEAM_ABBREVIATION: str
    TEAM_CITY: str
    PLAYER_ID: int
    PLAYER_NAME: str
    NICKNAME: str
    START_POSITION: str
    COMMENT: str
    MIN: str
    FGM: int
    FGA: int
    FG_PCT: float
    FG3M: int
    FG3A: int
    FG3_PCT: float
    FTM: int
    FTA: int
    FT_PCT: float
    OREB: int
    DREB: int
    REB: int
    AST: int
    STL: int
    BLK: int
    TO: int
    PF: int
    PTS: int
    PLUS_MINUS: float


def get_players_info(season, stats_type):
    """
    各選手のすべての試合情報を取得
    """
    from nba_api.stats.endpoints import leaguegamefinder
    from nba_api.stats.endpoints import boxscoretraditionalv2

    # PlayerStats
    results: Dict[int, List[PlayerStats]] = defaultdict(list)

    # TeamStats
    # results: Dict[int, List[TeamStats]] = dict()

    # 今シーズンのゲームをすべて取得
    response = leaguegamefinder.LeagueGameFinder(
        season_nullable=season,
        season_type_nullable='Regular Season'
    ).get_normalized_dict()
    list_len = len(response['LeagueGameFinderResults'])

    for i, _game in enumerate(response['LeagueGameFinderResults']):
        game = Game(**_game)
        print(i, '/', list_len, i/list_len)

        # 各ゲームidから選手ごとのstatsを取得
        res = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game.GAME_ID).get_normalized_dict()

        for j, _player_stats in enumerate(res[stats_type]):
            player_stats = PlayerStats(**_player_stats)

            results[player_stats.PLAYER_ID].append(player_stats)
        time.sleep(2)

    return results


def calc_sum(stats_list_by_plyer_id, target_stats_list: List[str]):
    """
    argmax(satts)
    """
    @dataclass
    class Result:
        player_id: int
        player_name: str
        team_abbreviation: str
        _sum_stats_by_stats: Dict[str, int] = None

        @property
        def sum_stats_by_stats(self):
            return self._sum_stats_by_stats

        @sum_stats_by_stats.setter
        def sum_stats_by_stats(self, val):
            self._sum_stats_by_stats = val


    results: Dict[int, int] = defaultdict(int)
    for _player_id, _stats_list in stats_list_by_plyer_id.items():
        _player_name = _stats_list[0].PLAYER_NAME
        _team_abbreviation = _stats_list[0].TEAM_ABBREVIATION
        result: Result = Result(_player_id, _player_name, _team_abbreviation)

        sum_target_stats_dict = defaultdict(int)

        # 各試合のスタッツ
        for _stats_per_game in _stats_list:
            # 各スタッツタイプ
            for target_stats_type in target_stats_list:
                target_stats = getattr(_stats_per_game, target_stats_type)
                sum_target_stats_dict[target_stats_type] += target_stats if target_stats else 0
        result.sum_stats_by_stats = sum_target_stats_dict
        results[_player_id] = result

    return results


if __name__ == '__main__':

    target_date = datetime.datetime.today().date()
    target_date = target_date + datetime.timedelta(days=-1)

    working_dir = Path('C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\analyze_03_season_stats_ranking')
    output_dir_path = working_dir / f'results_{str(target_date)}'
    path_pickle = output_dir_path / f'results_{str(target_date)}.pickle'
    tsv_path = output_dir_path / f'results_tsv_{str(target_date)}.tsv'

    # playerStats, TeamStats
    stats_type = 'PlayerStats'

    # 出力ディレクトリを出力
    if not output_dir_path.exists():
        output_dir_path.mkdir()
    else:
        print(output_dir_path)

    # スタッツリストを集計
    if not path_pickle.exists():
        player_stats_in_season: Dict[int, Dict[int, str]] = get_players_info(season='2021-22', stats_type=stats_type)
        # with open(path_pickle, 'wb') as p:
        #     pickle.dump(player_stats_in_season)
    else:
        with open(path_pickle, 'rb') as p:
            player_stats_in_season: Dict[int, Dict[int, str]] = pickle.load(p)

    # 1試合につき2つ分が返されるので, 1選手につき1試合のスタッツが2つ分入ってしまう
    # そのため, セットで重複を消す
    for player_id, stats_list in player_stats_in_season.items():
        player_stats_in_season[player_id] = list()
        for stats in stats_list:
            if stats not in player_stats_in_season[player_id]:
                player_stats_in_season[player_id].append(stats)


    # 合計を計算する
    target_stats_list = [
        'PTS',
        'AST',
        'REB',
        'STL',
        'BLK',
        'DREB',
        'OREB',
        'TO',
        'FGA',
        'FGM',
        'FG3M',
        'FG3A',
        'FTM',
        'FTA'
    ]
    sum_stats_by_player_id: Dict[int, int] = calc_sum(
        player_stats_in_season,
        target_stats_list=target_stats_list
    )

    # tsvに埋め込む
    rows: List[List[str]] = [['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION'] + target_stats_list]
    for result in sum_stats_by_player_id.values():
        player_id = result.player_id
        player_name = result.player_name
        team_abbreviation = result.team_abbreviation
        row: List = [player_id, player_name, team_abbreviation]
        for stats_type in target_stats_list:
            row.append(result.sum_stats_by_stats[stats_type])
        rows.append(row)
    write_tsv(tsv_path, rows)
