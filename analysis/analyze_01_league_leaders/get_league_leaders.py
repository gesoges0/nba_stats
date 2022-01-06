# 最も出場時間の長いlineupのランキングをtsvにして出力
from typing import List, Dict, Any, Set, NamedTuple
import os
import sys
import argparse
from pathlib import Path

from nba_api.stats.endpoints import shotchartlineupdetail

# nba_statsの階層でutils等をimportする
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))




def get_shotchart_detail():
    response = shotchartlineupdetail.ShotChartLineupDetail()
    return response.get_normalized_dict()


if __name__ == '__main__':
    # nba-apiでleagueleadersを見る
    response = get_shotchart_detail()
    print(response)