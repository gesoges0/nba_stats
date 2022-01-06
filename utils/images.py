from typing import List, Set, NamedTuple
from utils.structures import Player
from utils.operate_tsv import write_tsv
from utils.time import get_current_datetime_with_yyyymmdd_format
from utils.static import ROOT
from tqdm import tqdm
from nba_api.stats.endpoints import playerprofilev2


def get_players_images(players_id: List[str]) -> None:
    print(players_id)
    # id からチームを検索
    # URLを作成
    # utisls/staticのパラメタを使って 特定のディレクトリに配置する
    pass


def _get_player_profile_v2(id: int):
    response = playerprofilev2.PlayerProfileV2(player_id=id)
    return response.get_normalized_dict()


def get_image_url(player_id: str, team_id: str, season_id: str) -> None:
    """
    画像を取得する, arxivが既にあったらそれをcurlを使わずにarxivを使う
    :param player_id:
    :param team_id:
    :param season_id:
    :return:
    """
    url = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/{team_id}/{season_id}/260x190/{player_id}.png'
    return url




def exists_image(player_id: str, team_id: str, season_id: str) -> bool:
    """
    画像があるかを判定する
    :param player_id:
    :param team_id:
    :param season_id:
    :return:
    """
    pass


def get_image_and_arxiv(player_id: str, team_id: str, season_id: str) -> None:
    """
    一旦保存した画像の(player_id, team_id, season_id, url)をtsvにarxivしておく
    :param player_id:
    :param team_id:
    :param season_id:
    :return:
    """
    pass

def make_player_images_tsv(players_list: List[Player]) -> None:
    """
    新規に発行する画像URLをTSVに追加する
    :param players_list:
    :return:
    """

    # 現在のロスター一覧を取得する

    # ロスターにPlayerが含まれていたら画像URLをつくる





