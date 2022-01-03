from utils.time import get_current_datetime_with_yyyymmdd_format
from src.update_players_tsv import make_players_tsv

if __name__ == '__main__':
    # 本日の曜日を取得
    current_datetime: str = get_current_datetime_with_yyyymmdd_format()

    # playerの辞書を更新する(新規プレイヤーや、Active/Inactiveの更新のため)
    make_players_tsv(current_datetime, 'active')
    make_players_tsv(current_datetime, 'all')

