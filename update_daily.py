from utils.time import get_current_datetime_with_yyyymmdd_format
from src.operate_players_tsv import make_players_tsv
# from src.operate_teams_tsv import make_teams_tsv


def update_daily():
    # 本日の曜日を取得
    current_datetime: str = get_current_datetime_with_yyyymmdd_format()

    # playerの辞書を更新する(新規プレイヤーや、Active/Inactiveの更新のため)
    make_players_tsv(current_datetime, 'active')
    make_players_tsv(current_datetime, 'all')

    # チームの更新（起こらないのでコメントアウト)
    # make_teams_tsv()

