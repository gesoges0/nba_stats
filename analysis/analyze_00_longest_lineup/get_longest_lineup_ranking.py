# 最も出場時間の長いlineupのランキングをtsvにして出力
from nba_api.stats.endpoints import leaguedashlineups
from typing import List, Dict, Any
import os
import sys
import argparse
from pathlib import Path

# nba_statsの階層でutils等をimportする
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from utils.operate_tsv import write_tsv
from utils.time import get_current_datetime_with_yyyymmdd_format


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

    # tsvに書き込む
    results = list()
    if not lineups:
        assert False, 'lineups is None'
    header = list(lineups[0].keys())
    results.append(header)
    for lineup in lineups:
        results.append(list(lineup.values()))
    current_date = get_current_datetime_with_yyyymmdd_format()
    tsv_path = Path(os.path.dirname(__file__)) / f'./ranking_lineups_{sorted_key}_{current_date}.tsv'
    if tsv_path.exists():
        assert False, f'{tsv_path} already exists !!!!'
    write_tsv(tsv_path, results)
