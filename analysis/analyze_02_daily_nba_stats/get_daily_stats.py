# 毎日のランキング
import datetime

from nba_api.stats.endpoints import leaguedashlineups
from typing import List, Dict, Any, Set, NamedTuple
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
from utils.operate_tsv import write_tsv_from_dict_list


def _convert_datetime_to_mmddyyyy(d: str):
    yyyy, mm, dd = d.split('-')
    return f'{mm}/{dd}/{yyyy}'

def daily_info(d):

    # 昨日のdatetime.datetime.date
    yesterday = today + datetime.timedelta(days=-1)

    # スタッツリーダー更新
    # from nba_api.stats.endpoints import leagueleaders

    # d日のGAME_ID, この日の試合番号, 試合時刻取得, HOME_TEAM_ID, VISITOR_TEAM_ID
    from nba_api.stats.endpoints import scoreboardv2
    response = scoreboardv2.ScoreboardV2(game_date=str(yesterday)).get_normalized_dict()
    # ['GameHeader', 'LineScore', 'SeriesStandings', 'LastMeeting', 'EastConfStandingsByDay',
    # 'WestConfStandingsByDay', 'Available', 'TeamLeaders', 'TicketLinks', 'WinProbability']

    # 試合開始時刻
    # for i, _ in enumerate(response['GameHeader']):
    #     print(i, _)
    #
    # 試合結果の各スタッツ
    # print('-' * 20)
    # for i, _ in enumerate(response['LineScore']):
    #     print(i, _)
    #
    # # 勝者
    # print('=' * 20)
    # for i, _ in enumerate(response['SeriesStandings']):
    #     print(i, _)
    #
    # # 東の順位
    # print('-' * 20)
    # for i, _ in enumerate(response['EastConfStandingsByDay']):
    #     print(i, _)
    #
    # # 西の順位
    # print('-' * 20)
    # for i, _ in enumerate(response['WestConfStandingsByDay']):
    #     print(i, _)
    #
    # # この日の各チームのPTSリーダー
    # print('-' * 20)
    # for i, _ in enumerate(response['TeamLeaders']):
    #     print(i, _)

    from nba_api.stats.endpoints import boxscoresummaryv2
    response = boxscoresummaryv2.BoxScoreSummaryV2(game_id='0022100486').get_normalized_dict()
    # dict_keys(['GameSummary', 'OtherStats', 'Officials', 'InactivePlayers', 'GameInfo', 'LineScore', 'LastMeeting',
    #            'SeasonSeries', 'AvailableVideo'])

    # game_idの2チーム各クォータの得点
    for i, _ in enumerate(response['LineScore']):
        print(i, _)

    from nba_api.stats.endpoints import boxscorescoringv2
    response = boxscorescoringv2.BoxScoreScoringV2(game_id='0022100486').get_normalized_dict()

    # game_idの選手ごとの%など
    # sqlTeamsScoringなら、チームごとの%
    for i, _ in enumerate(response['sqlPlayersScoring']):
        print(i, _)

    from nba_api.stats.endpoints import boxscoretraditionalv2
    response = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id='0022100486').get_normalized_dict()

    # 各プレイヤーのスタッツ
    for i, _ in enumerate(response['PlayerStats']):
        print(i, _)

    # 各チームのスタッツ
    for i, _ in enumerate(response['TeamStats']):
        print(i, _)



if __name__ == '__main__':

    today = datetime.datetime.now().date()

    info = daily_info(today)

