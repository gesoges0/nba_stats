from utils.time import get_current_datetime_with_yyyymmdd_format
from src.operate_players_tsv import make_players_tsv
from utils.operate_tsv import read_all_rows_from_tsv
from utils.static import get_all_players_tsv_file_names
from utils.images import get_players_images, make_player_images_tsv
from utils.structures import Player
from typing import Set, List, Any
# from src.operate_teams_tsv import make_teams_tsv


def _get_new_players_id_list() -> List[Player]:
    """
    最新のtsvと一つ前のtsvを比較して, 新規参入したプレイヤーを取得
    ※ 移籍すると画像（ユニフォーム）が変わるがそれには対応できていない
    :return:
    """
    # static/players/all_*.tsvのpathのリスト
    all_players_tsv_files = get_all_players_tsv_file_names()

    if len(all_players_tsv_files) == 0:
        assert False, 'len(static/players/all_*.tsv) must be more than 2 files.'

    elif len(all_players_tsv_files) == 1:
        after_tsv_path = all_players_tsv_files[-1]
        before_players_list: List[Player] = []
        after_players_list: List[Player] = [Player(*p) for p in read_all_rows_from_tsv(after_tsv_path)]

    elif len(all_players_tsv_files) >= 2:
        before_tsv_path = all_players_tsv_files[-2]
        after_tsv_path = all_players_tsv_files[-1]
        before_players_list: List[Player] = [Player(*p) for p in read_all_rows_from_tsv(before_tsv_path)]
        after_players_list: List[Player] = [Player(*p) for p in read_all_rows_from_tsv(after_tsv_path)]

    # 最新のtsvにあって, 前回のtsvに無いプレイヤーのidリストを返す
    new_players_id_list: List[Player] = list(set(after_players_list) - set(before_players_list))
    return new_players_id_list


def update_daily():
    # 本日の曜日を取得(YYYYMMDD)
    current_datetime: str = get_current_datetime_with_yyyymmdd_format()

    # playerの辞書を更新する(新規プレイヤーや、Active/Inactiveの更新のため)
    make_players_tsv(current_datetime, 'active')
    make_players_tsv(current_datetime, 'all')

    # チームの更新（起こらないのでコメントアウト)
    # make_teams_tsv()

    # 新規プレイヤー（前回のtsvには無くて, 今回のtsvにはある選手）の画像を取得
    # チーム移籍は考慮されていないため, 専用の処理を別途書く
    new_players_list: List[Player] = _get_new_players_id_list()
    if new_players_list:
        # 新規差分の選手の画像URL付きtsvを更新
        pass

        # imageをローカルに落とす

        # 新規差分の選手の画像URL付きtsvを前回のも含めたtsvにまとめる

