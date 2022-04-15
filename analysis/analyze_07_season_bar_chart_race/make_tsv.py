from nba_api.stats.endpoints import leaguegamefinder
from dataclasses import dataclass
import sys
import csv


@dataclass
class PlayerByGame:
    SEASON_ID: str
    PLAYER_ID: int
    PLAYER_NAME: str
    TEAM_ID: int
    TEAM_ABBREVIATION: str
    TEAM_NAME: str
    GAME_ID: str
    GAME_DATE: str
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
    PLUS_MINUS: int

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    @property
    def img_url(self):
        return f'https://cdn.nba.com/headshots/nba/latest/1040x760/{self.PLAYER_ID}.png'


if __name__ == '__main__':
    # 対象スタッツ
    target_stats = sys.argv[1]
    if not target_stats:
        print('no target_stats!')
        exit()

    # 今期の試合を全て抽出
    player_stats_per_game = leaguegamefinder.LeagueGameFinder(
        'P',
        season_nullable='2021-22',
        season_type_nullable='Regular Season',
        league_id_nullable='00',
    ).get_normalized_dict()['LeagueGameFinderResults']

    # 各試合について各選手のスタッツを記録する
    player_stats_per_game_by_date_and_player = dict()
    player_by_id = dict()
    for player_stats in player_stats_per_game:
        # print('\n'.join([f'{k}: {type(v).__name__}' for k,v in player_stats.items()]))
        pbg = PlayerByGame.from_dict(player_stats)
        player_stats_per_game_by_date_and_player[(pbg.GAME_DATE, pbg.PLAYER_ID)] = pbg
        player_by_id[pbg.PLAYER_ID] = pbg

    # 全ての日付を取得する
    dates = set()
    for player_stats in player_stats_per_game:
        dates.add(player_stats['GAME_DATE'])
    dates = sorted(list(dates))

    # 全ての選手
    players = set()
    for player_stats in player_stats_per_game:
        players.add(player_stats['PLAYER_ID'])
    players = sorted(list(players))

    # 各日について各選手の対象スタッツを取得する
    player_stats_each_date_by_player_id = \
        {
            player_id:
                [
                    getattr(player_stats_per_game_by_date_and_player[(date, player_id)], target_stats)
                    if player_stats_per_game_by_date_and_player.get((date, player_id)) else 0
                    for date in dates
                ]
            for player_id in players
        }

    # 各選手の累計スタッツ
    player_sum_stats_each_date_by_player_id = dict()
    for player_id in players:
        player_sum_stats_each_date_by_player_id[player_id] = player_stats_each_date_by_player_id[player_id]
        for i, date in enumerate(dates[1:], 1):
            player_sum_stats_each_date_by_player_id[player_id][i] = \
                player_sum_stats_each_date_by_player_id[player_id][i-1] + \
                player_sum_stats_each_date_by_player_id[player_id][i]

    # グラフの動きが忙しくなるので選定
    # 残す選手ID
    # 1日の最大枠 10
    remaining_player_ids = set()
    ranking_by_date = dict()
    for player_id, sum_stats in player_sum_stats_each_date_by_player_id.items():
        for i, stats in enumerate(sum_stats):
            if not ranking_by_date.get(i):
                ranking_by_date[i] = [(stats, player_id)]
            elif len(ranking_by_date[i]) >= 10:
                if min(ranking_by_date[i]) <= (stats, player_id):
                    ranking_by_date[i].remove(min(ranking_by_date[i]))
                    ranking_by_date[i].append((stats, player_id))
            else:
                ranking_by_date[i].append((stats, player_id))
    for i, ranking in ranking_by_date.items():
        for (stats, player_id) in ranking:
            remaining_player_ids.add(player_id)
    for player_id in players:
        if player_id not in remaining_player_ids:
            del player_sum_stats_each_date_by_player_id[player_id]

    tsv_path = f'output_{target_stats}.tsv'
    with open(tsv_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(['PLAYER_NAME', 'PLAYER_IMG', 'TEAM'] + [date[5:].replace('-', '/') for date in dates])
        for player_id in players:
            if player_id not in remaining_player_ids:
                continue
            # 基礎情報
            base_pbg = player_by_id[player_id]
            output = [base_pbg.PLAYER_NAME, base_pbg.img_url, base_pbg.TEAM_ABBREVIATION]
            writer.writerow(output + player_sum_stats_each_date_by_player_id[player_id])
    exit()

    # 各試合について（HOME_ABB, AWAY_ABB, HOME_SCORE, AWAY_SCORE）を抽出する
    games = leaguegamefinder.LeagueGameFinder(
        'T',
        season_nullable='2021-22',
        season_type_nullable='Regular Season'
    ).get_normalized_dict()['LeagueGameFinderResults']

    print(games[0])
    print(games[1])

    # 1試合につきHOME, AWAY側を主軸とした2データ得られる
