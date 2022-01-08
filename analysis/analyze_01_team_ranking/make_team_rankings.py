# 最も出場時間の長いlineupのランキングをtsvにして出力
import datetime
from typing import List, Dict, Any, Set, NamedTuple, Generator
import os
import sys
import argparse
from pathlib import Path

from nba_api.stats.endpoints import leaguedashteamstats

# nba_statsの階層でutils等をimportする
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


def get_response():
    response = leaguedashteamstats.LeagueDashTeamStats()
    return response.get_normalized_dict()


def get_ranking(teams_generator: Generator[List[Dict[str, Any]], None, None]):
    pass


def _convert_yyyymmdd_to_mmddyyyyy(yyyymmdd: datetime.date):
    yyyy, mm, dd = str(yyyymmdd).split('-')
    return mm + '/' + dd + '/' + yyyy


def _date_range(start_date: datetime.date, end_date: datetime.date):
    """
    [start_date, end_date] を返す
    :param start_date:
    :param end_date:
    :return:
    """
    base_date = start_date + datetime.timedelta(days=-1)
    while base_date < end_date:
        base_date += datetime.timedelta(days=1)
        yield base_date


if __name__ == '__main__':

    # nba-apiでleagueleadersを見る
    response = get_response()

    # 今期の開始から本日まで
    start_date = datetime.datetime(year=2021, month=10, day=19).date()
    end_date = datetime.datetime.today().date() + datetime.timedelta(-1) # 現地時間と合わせるため
    print(start_date)
    print(end_date)

    date_list = [_convert_yyyymmdd_to_mmddyyyyy(date) for date in _date_range(start_date, end_date)]
    print(date_list)
    exit()
    tsv_path = ''

    #           d1   d2   d3
    # team_A    r1   r3   r1
    # team_B    r2   r1   r3
    # team_C    r3   r2   r2

    # {team_A: {d1: r1, d2: r3, d3: r1}, team_B: {d1: r2, d2: r1, d3: r3}, team_C: {d1: r3, d2: r2, d3: r2}}

    # get-ranking
    teams_rankinig = get_ranking(response['LeagueDashTeamStats'])

    #