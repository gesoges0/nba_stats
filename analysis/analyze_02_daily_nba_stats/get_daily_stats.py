# 毎日のランキング
import datetime

from nba_api.stats.endpoints import leaguedashlineups
from typing import List, Dict, Any, Set, NamedTuple, Optional
import os
import sys
import argparse
from pathlib import Path


# nba_statsの階層でutils等をimportする
sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')

from utils.operate_tsv import write_tsv
from utils.structures import Player
from utils.time import get_current_datetime_with_yyyymmdd_format
from utils.players import get_players_by_id_dict
from utils.images import get_image_url
from utils.operate_tsv import write_tsv_from_dict_list, tsv_to_dict_by_first_header_column

from dataclasses import dataclass, field
from collections import defaultdict

# ------------------------------------------------------------------------------------------
@dataclass
class TeamRanking:
    team_id: int
    season_id: str
    team: str
    num_g: int
    num_w: int
    num_l: int
    w_pct: float
    home_record: str # '15-4'
    road_record: str
    team_abbreviation: str = field(default='')
    home_w: int = field(default=0)
    home_l: int = field(default=0)
    road_w: int = field(default=0)
    road_l: int = field(default=0)

    def __post_init__(self):
        # team_abbreviationのセット
        team_tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\teams\\teams.tsv'
        team_dict_by_team_id: Dict[str, Any] = tsv_to_dict_by_first_header_column(team_tsv_path)
        self.team_abbreviation = team_dict_by_team_id[str(self.team_id)]['abbreviation']
        # home, roadの勝敗数のセット
        self.home_w, self.home_l = map(int, self.home_record.split('-'))
        self.road_w, self.road_l = map(int, self.road_record.split('-'))


@dataclass
class TeamLeaders:
    game_id: str
    team_id: int
    team_abbreviation: str
    pts_player_id: int
    pts_player_name: str
    pts: int
    reb_player_id: int
    reb_player_name: str
    reb: int
    ast_player_id: int
    ast_player_name: str
    ast: int


@dataclass
class PlayerStats:
    player_id: int
    player_name: str
    nickname: str
    start_position: str
    comment: str
    min: Optional[str]
    fgm: Optional[int]
    fga: Optional[int]
    fg_pct: Optional[float]
    fg3m: Optional[int]
    fg3a: Optional[int]
    fg3_pct: Optional[float]
    ftm: Optional[int]
    fta: Optional[int]
    ft_pct: Optional[float]
    oreb: Optional[int]
    dreb: Optional[int]
    reb: Optional[int]
    ast: Optional[int]
    stl: Optional[int]
    blk: Optional[int]
    to: Optional[int]
    pf: Optional[int]
    pts: Optional[int]
    plus_minus: Optional[float]


@dataclass
class TeamStats:
    min: str
    fgm: int
    fga: int
    fg_pct: float
    fg3m: int
    fg3a: int
    fg3_pct: float
    ftm: int
    fta: int
    ft_pct: float
    oreb: int
    dreb: int
    reb: int
    ast: int
    stl: int
    blk: int
    to: int
    pf: int
    pts: int
    plus_minus: float


@dataclass
class TeamInfo:
    """
    Gameに入れる際の情報
    """
    team_wins_loses: str
    pts: int
    ast: int
    reb: int
    tov: int
    fg_pct: float
    ft_pct: float
    fg3_pct: float
    pts_qtr1: int
    pts_qtr2: int
    pts_qtr3: int
    pts_qtr4: int
    pts_ot1: int = field(default=0)
    pts_ot2: int = field(default=0)
    pts_ot3: int = field(default=0)
    pts_ot4: int = field(default=0)
    _team_leaders: TeamLeaders = None
    _player_stats: List[PlayerStats] = None
    _team_stats: TeamStats = None


    @property
    def team_leaders(self):
        return self._team_leaders

    @team_leaders.setter
    def team_leaders(self, val):
        self._team_leaders = val

    @property
    def player_stats(self):
        return self._player_stats

    @player_stats.setter
    def player_stats(self, val: List[PlayerStats]):
        self._player_stats = val

    @property
    def team_stats(self):
        return self._team_stats

    @team_stats.setter
    def team_stats(self, val):
        self._team_stats = val

@dataclass
class Game:
    game_id: str
    home_team_id: int
    visitor_team_id: int
    home_team_abbreviation: str = field(default='')
    visitor_team_abbreviation: str = field(default='')
    _home_team_info: TeamInfo = None
    _visitor_team_info: TeamInfo = None

    def __post_init__(self):
        # team_abbreviationのセット
        team_tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\teams\\teams.tsv'
        team_dict_by_team_id: Dict[str, Any] = tsv_to_dict_by_first_header_column(team_tsv_path)
        self.home_team_abbreviation = team_dict_by_team_id[str(self.home_team_id)]['abbreviation']
        self.visitor_team_abbreviation = team_dict_by_team_id[str(self.visitor_team_id)]['abbreviation']

    @property
    def home_team_info(self):
        return self._home_team_info

    @home_team_info.setter
    def home_team_info(self, val: TeamInfo):
        self._home_team_info = val

    @property
    def visitor_team_info(self):
        return self._visitor_team_info

    @visitor_team_info.setter
    def visitor_team_info(self, val: TeamInfo):
        self._visitor_team_info = val
# ------------------------------------------------------------------------------------------


def _convert_datetime_to_mmddyyyy(d: str):
    yyyy, mm, dd = d.split('-')
    return f'{mm}/{dd}/{yyyy}'

def daily_info(target_date: str):

    games_dict: List[Game] = dict()
    ranking_dict: Dict[str, List[TeamRanking]] = {'East': [], 'West': []}

    # d日のGAME_ID, この日の試合番号, 試合時刻取得, HOME_TEAM_ID, VISITOR_TEAM_ID
    from nba_api.stats.endpoints import scoreboardv2
    response = scoreboardv2.ScoreboardV2(game_date=target_date).get_normalized_dict()
    # ['GameHeader', 'LineScore', 'SeriesStandings', 'LastMeeting', 'EastConfStandingsByDay',
    # 'WestConfStandingsByDay', 'Available', 'TeamLeaders', 'TicketLinks', 'WinProbability']

    # 両チーム合わせた試合情報、試合時刻など
    for i, _ in enumerate(response['GameHeader']):
        game = Game(game_id=_['GAME_ID'], home_team_id=_['HOME_TEAM_ID'], visitor_team_id=_['VISITOR_TEAM_ID'])
        games_dict[game.game_id] = game

    # 試合結果の各スタッツ
    for i, _ in enumerate(response['LineScore']):
        print(i, _)
        team_info = TeamInfo(
            team_wins_loses=_['TEAM_WINS_LOSSES'],
            pts=_['PTS'],
            ast=_['AST'],
            reb=_['REB'],
            tov=_['TOV'],
            fg_pct=_['FG_PCT'],
            ft_pct=_['FT_PCT'],
            fg3_pct=_['FG3_PCT'],
            pts_qtr1=_['PTS_QTR1'],
            pts_qtr2=_['PTS_QTR2'],
            pts_qtr3=_['PTS_QTR3'],
            pts_qtr4=_['PTS_QTR4'],
        )
        game = games_dict[_['GAME_ID']]
        if _['TEAM_ID'] == game.home_team_id:
            game.home_team_info = team_info
            games_dict[_['GAME_ID']] = game
        if _['TEAM_ID'] == game.visitor_team_id:
            game.visitor_team_info = team_info
            games_dict[_['GAME_ID']] = game

    # 連勝記録
    # print('=' * 20)
    # for i, _ in enumerate(response['SeriesStandings']):
    #     print(i, _)

    # # 東の順位
    print('-' * 20)
    for i, _ in enumerate(response['EastConfStandingsByDay']):
        team_ranking = TeamRanking(
            team_id=_['TEAM_ID'],
            season_id=_['SEASON_ID'],
            team=_['TEAM'],
            num_g=_['G'],
            num_w=_['W'],
            num_l=['L'],
            w_pct=['W_PCT'],
            home_record=_['HOME_RECORD'],  # '15-4'
            road_record=_['ROAD_RECORD'],
        )
        ranking_dict['East'].append(team_ranking)

    # 西の順位
    print('-' * 20)
    for i, _ in enumerate(response['WestConfStandingsByDay']):
        team_ranking = TeamRanking(
            team_id=_['TEAM_ID'],
            season_id=_['SEASON_ID'],
            team=_['TEAM'],
            num_g=_['G'],
            num_w=_['W'],
            num_l=['L'],
            w_pct=['W_PCT'],
            home_record=_['HOME_RECORD'],  # '15-4'
            road_record=_['ROAD_RECORD'],
        )
        ranking_dict['West'].append(team_ranking)

    # # この日の各チームのPTSリーダー
    print('-' * 20)
    for i, _ in enumerate(response['TeamLeaders']):
        team_leaders = TeamLeaders(
            game_id=_['GAME_ID'],
            team_id=_['TEAM_ID'],
            team_abbreviation=_['TEAM_ABBREVIATION'],
            pts_player_id=_['PTS_PLAYER_ID'],
            pts_player_name=_['PTS_PLAYER_NAME'],
            pts=_['PTS'],
            reb_player_id=_['REB_PLAYER_ID'],
            reb_player_name=_['REB_PLAYER_NAME'],
            reb=_['REB'],
            ast_player_id=_['AST_PLAYER_ID'],
            ast_player_name=_['AST_PLAYER_NAME'],
            ast=_['AST'],
        )
        game = games_dict[_['GAME_ID']]
        if _['TEAM_ID'] == game.home_team_id:
            game.home_team_info.team_leaders = team_leaders
            games_dict[_['GAME_ID']] = game
        if _['TEAM_ID'] == game.visitor_team_id:
            game.visitor_team_info.team_leaders = team_leaders
            games_dict[_['GAME_ID']] = game



    # from nba_api.stats.endpoints import boxscoresummaryv2
    # response = boxscoresummaryv2.BoxScoreSummaryV2(game_id='0022100486').get_normalized_dict()
    # # dict_keys(['GameSummary', 'OtherStats', 'Officials', 'InactivePlayers', 'GameInfo', 'LineScore', 'LastMeeting',
    # #            'SeasonSeries', 'AvailableVideo'])
    #
    # # game_idの2チーム各クォータの得点
    # for i, _ in enumerate(response['LineScore']):
    #     print(i, _)
    #

    from nba_api.stats.endpoints import boxscorescoringv2
    from nba_api.stats.endpoints import boxscoretraditionalv2

    for game_id, game in games_dict.items():

        # 各ゲームの情報

        # game_idの選手ごとの%など
        # sqlTeamsScoringなら、チームごとの%
        # response = boxscorescoringv2.BoxScoreScoringV2(game_id=game_id).get_normalized_dict()
        # for i, _ in enumerate(response['sqlPlayersScoring']):
        #     print(i, _)

        response = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).get_normalized_dict()
        # # 各プレイヤーのスタッツ
        home_team_players_stats_list = []
        road_team_players_stats_list = []
        for i, _ in enumerate(response['PlayerStats']):
            player_stats = PlayerStats(
                player_id=_['PLAYER_ID'],
                player_name=_['PLAYER_NAME'],
                nickname=_['NICKNAME'],
                start_position=_['START_POSITION'],
                comment=_['COMMENT'],
                min=_['MIN'],
                fgm=_['FGM'],
                fga=_['FGA'],
                fg_pct=_['FG_PCT'],
                fg3m=_['FG3M'],
                fg3a=_['FG3A'],
                fg3_pct=_['FG3_PCT'],
                ftm=_['FTM'],
                fta=_['FTA'],
                ft_pct=_['FT_PCT'],
                oreb=_['OREB'],
                dreb=_['DREB'],
                reb=_['REB'],
                ast=_['AST'],
                stl=_['STL'],
                blk=_['BLK'],
                to=_['TO'],
                pf=_['PF'],
                pts=_['PTS'],
                plus_minus=_['PLUS_MINUS'],
            )
            if game.home_team_id == _['TEAM_ID']:
                home_team_players_stats_list.append(player_stats)
            else:
                road_team_players_stats_list.append(player_stats)
        games_dict[game_id].home_team_info.player_stats = home_team_players_stats_list
        games_dict[game_id].visitor_team_info.player_stats = road_team_players_stats_list

        # # 各チームのスタッツ
        for i, _ in enumerate(response['TeamStats']):
            team_stats = TeamStats(
                min=_['MIN'],
                fgm=_['FGM'],
                fga=_['FGA'],
                fg_pct=_['FG_PCT'],
                fg3m=_['FG3M'],
                fg3a=_['FG3A'],
                fg3_pct=_['FG3_PCT'],
                ftm=_['FTM'],
                fta=_['FTA'],
                ft_pct=_['FT_PCT'],
                oreb=_['OREB'],
                dreb=_['DREB'],
                reb=_['REB'],
                ast=_['AST'],
                stl=_['STL'],
                blk=_['BLK'],
                to=_['TO'],
                pf=_['PF'],
                pts=_['PTS'],
                plus_minus=_['PLUS_MINUS'],
            )
            if game.home_team_id == _['TEAM_ID']:
                games_dict[game_id].home_team_info.team_stats = team_stats
            else:
                games_dict[game_id].visitor_team_info.team_stats = team_stats

    return games_dict


def make_initial_enviroment(target_date):
    """
    ディレクトリを作成する
    """
    dir_path = Path(
        f'C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\analyze_02_daily_nba_stats\\output\\output_{target_date}'
    )
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


def make_tsv_daily_each_game_pts_leader(games_dict, stat):
    """
    各試合のPTSランキングをTSVに吐き出す
    GAME_ID, PLAYER_ID, PLAYER_NAME, PLAYER_TEAM, TEAMS(VISITOR@HOME), PTS
    """
    results: List[str] = list()
    header = [
        'GAME_ID',
        'HOME_TEAM_ABBREVIATION',
        'VISITOR_TEAM_ABBREVIATION',
        'HOME_TEAM_PTS',
        'VISITOR_TEAM_PTS',
        'HOME_TEAM_LEADER_PLAYER_ID',
        'HOME_TEAM_LEADER_PLAYER_NAME',
        f'HOME_TEAM_LEADER_{stat.upper()}',
        'VISITOR_TEAM_LEADER_PLAYER_ID',
        'VISITOR_TEAM_LEADER_PLAYER_NAME',
        f'VISITOR_TEAM_LEADER_{stat.upper()}',
        'GAME_LEADER_PLAYER_ID',
        'GAME_LEADER_PLAYER_NAME',
        'GAME_LEADER_PLAYER_TEAM',
        f'GAME_LEADER_{stat.upper()}'
    ]
    results.append(header)
    for game_id, game in games_dict.items():
        if getattr(game.home_team_info.team_leaders, stat) >= getattr(game.visitor_team_info.team_leaders, stat):
            game_leader = game.home_team_info.team_leaders
        else:
            game_leader = game.visitor_team_info.team_leaders

        results_per_game =[
            game_id,
            game.home_team_abbreviation,
            game.visitor_team_abbreviation,
            getattr(game.home_team_info, stat),
            getattr(game.visitor_team_info, stat),
            getattr(game.home_team_info.team_leaders, f'{stat}_player_id'),
            getattr(game.home_team_info.team_leaders, f'{stat}_player_name'),
            getattr(game.home_team_info.team_leaders, stat),
            getattr(game.visitor_team_info.team_leaders, f'{stat}_player_id'),
            getattr(game.visitor_team_info.team_leaders, f'{stat}_player_name'),
            getattr(game.visitor_team_info.team_leaders, stat),
            getattr(game_leader, f'{stat}_player_id'),
            getattr(game_leader, f'{stat}_player_name'),
            game_leader.team_abbreviation,
            getattr(game_leader, stat),
        ]
        results.append(results_per_game)
    for result in results:
        print(result)
    return results


def make_tsv_daily_each_game_pts_ranking(game_dict: str, stat: str) -> List[str]:
    """
    statの得点ランキングのTSVを出力
    """
    results: List[str] = list()
    header = [
        'GAME_ID',
        'HOME_TEAM_ABBREVIATION',
        'VISITOR_TEAM_ABBREVIATION',
    ]
    # ランキング
    for i in range(1, 10 + 1):
        header.append(f'PLAYER_ID_{i}')
        header.append(f'PLAYER_NAME_{i}')
        header.append(f'PLAYER_TEAM_ABBREVIATION_{i}')
        header.append(f'PLAYER_stats_{i}')
        header.append(f'PLAYER_rank_{i}')  # ランクに重複を許すため, このカラムで制御する
    results.append(header)
    for game_id, game in games_dict.items():
        players = []
        print(game_id, game)
        print(game.home_team_info.player_stats)
        for player in game.home_team_info.player_stats:
            players.append((player, game.home_team_abbreviation))
        for player in game.visitor_team_info.player_stats:
            players.append((player, game.visitor_team_abbreviation))
        # statsが高い順に並び替え
        players.sort(key=lambda x: -getattr(x[0], stat) if getattr(x[0], stat) else 0)
        result = list()
        result.append(game_id)
        result.append(game.home_team_abbreviation)
        result.append(game.visitor_team_abbreviation)
        for i, (p, abbreviation) in enumerate(players[:10]):
            result.append(p.player_id)
            result.append(p.player_name)
            result.append(abbreviation)
            result.append(getattr(p, stat))
            result.append(i + 1)
        results.append(result)
    return results


if __name__ == '__main__':
    today = datetime.datetime.now().date()  # 2022-01-12
    yesterday = today + datetime.timedelta(days=-2)  # 2022-01-11
    target_date = yesterday
    games_dict: Dict[str, Game] = daily_info(str(yesterday))

    # WORKING_ROOT \
    #     = Path(f'C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\analyze_02_daily_nba_stats\\{target_date}')

    # 作業ディレクトリの作成
    output_dir = make_initial_enviroment(str(target_date))

    # 毎日の得点の各チームのリーダー（主にサムネ用になると思う）
    target_stat = 'pts'
    tsv_path = output_dir / f'daily_pts_leaders_{target_date}_{target_stat}.tsv'
    results: List[str] = make_tsv_daily_each_game_pts_leader(games_dict, stat=target_stat)
    write_tsv(tsv_path, results)

    # 毎日の得点ランキング
    target_stat = 'pts'
    tsv_path = output_dir / f'daily_pts_ranking_{target_date}_{target_stat}.tsv'
    results: List[str] = make_tsv_daily_each_game_pts_ranking(games_dict, stat=target_stat)
    write_tsv(tsv_path, results)




