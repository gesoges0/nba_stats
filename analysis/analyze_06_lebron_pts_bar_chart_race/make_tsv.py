import csv
import time
from dataclasses import dataclass, field
from nba_api.stats.endpoints import playerprofilev2
from nba_api.stats.static.players import get_players
from typing import List, Dict, Any, Set
from pathlib import Path
import pickle


@dataclass
class Analyzer:
    stats: str
    _all_players: List[Dict[str, Any]] = None
    _full_name_by_player_id: Dict[int, str] = field(default_factory=dict)
    _season_totals_regular_season_by_season_by_player_id: Dict[int, Dict[int, Dict[str, Any]]] = field(default_factory=dict)
    _output_path: Path = Path('output.tsv')
    _pickle_path: Path = Path('season_totals_regular_season_by_season_by_player_id.pickle')
    _output_path_for_flourish: Path = Path('output_for_flourish.tsv')
    _output_path_for_flourish_with_flag: Path = Path('output_path_for_flourish_with_flag.tsv')

    @property
    def pickle_path(self):
        return self._pickle_path

    def get_all_players(self):
        """全選手のIDを取得する """
        self._all_players = get_players()
        self.get_full_name_by_player_id()
        print(len(self._all_players))

    def get_season_totals(self):
        """各選手のSeasonTotalsRegularSeasonを取得"""
        for i, player in enumerate(self._all_players):
            print(i, i / len(self._all_players))
            print(player)
            self._season_totals_regular_season_by_season_by_player_id[player['id']] = dict()

            player_profile: List[Dict[str, Any]] = playerprofilev2.PlayerProfileV2(player_id=player['id']).get_normalized_dict()['SeasonTotalsRegularSeason']
            for _ in player_profile:
                self._season_totals_regular_season_by_season_by_player_id[player['id']][_['SEASON_ID']] = _[self.stats]
                # {'PLAYER_ID': 76001, 'SEASON_ID': '1990-91', 'LEAGUE_ID': '00', 'TEAM_ID': 1610612757, 'TEAM_ABBREVIATION': 'POR', 'PLAYER_AGE': 23.0, 'GP': 43, 'GS': 0, 'MIN': 290, 'FGM': 55, 'FGA': 116, 'FG_PCT': 0.474, 'FG3M': 0, 'FG3A': 0, 'FG3_PCT': 0.0, 'FTM': 25, 'FTA': 44, 'FT_PCT': 0.568, 'OREB': 27, 'DREB': 62, 'REB': 89, 'AST': 12, 'STL': 4, 'BLK': 12, 'TOV': 22, 'PF': 39, 'PTS': 135}

            time.sleep(5)

    def save_pickle(self):
        with open(self._pickle_path, 'wb') as f:
            pickle.dump(self._season_totals_regular_season_by_season_by_player_id, f)
        print('saved')

    def load_pickle(self):
        self.get_all_players()
        with open(self._pickle_path, 'rb') as f:
            self._season_totals_regular_season_by_season_by_player_id = pickle.load(f)
        print(self._season_totals_regular_season_by_season_by_player_id)

    def get_full_name_by_player_id(self):
        for player in self._all_players:
            self._full_name_by_player_id[player['id']] = player['full_name']

    def output_to_tsv(self):

        # seasonのリストを取得
        seasons: Set[str] = set()
        for player_id, season_totals_dict in self._season_totals_regular_season_by_season_by_player_id.items():
            for season in season_totals_dict.keys():
                seasons.add(season)
        seasons = sorted(list(seasons))

        # output用のリストを取得
        header = ['player_id', 'full_name', 'image_url'] + seasons
        rows = [header]
        for player_id, season_totals_dict in self._season_totals_regular_season_by_season_by_player_id.items():
            full_name = self._full_name_by_player_id[player_id]
            image_url = 'hoge'
            row = [player_id, full_name, image_url]
            for season in seasons:
                if season in season_totals_dict:
                    row.append(season_totals_dict[season])
                else:
                    row.append(0)
            rows.append(row)

        # output tsv
        with open(self._output_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            for row in rows:
                writer.writerow(row)

    def output_for_flourish(self):
        # 選手情報取得
        self.get_full_name_by_player_id()

        # seasonのリストを取得
        seasons: Set[str] = set()
        for player_id, season_totals_dict in self._season_totals_regular_season_by_season_by_player_id.items():
            for season in season_totals_dict.keys():
                seasons.add(season)
        seasons = sorted(list(seasons))

        # tsv読み取り
        rows_expect_header = []
        header = []
        with open(self._output_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            header = next(reader)
            for row in reader:
                rows_expect_header.append(row)

        # res[0] = a[0] and res[i] = totals[i-1] + a[i]
        new_row_by_player_id = dict()
        info_area = 3
        for row in rows_expect_header:
            player_id, *_ = row[:info_area]
            stats_each_year = row[info_area:]
            stats_totals = [0 for _ in range(len(stats_each_year))]
            for i, s in enumerate(stats_each_year):
                if i == 0:
                    continue
                stats_totals[i] = stats_totals[i-1] + int(stats_each_year[i])
            new_row_by_player_id[int(player_id)] = row[:info_area] + stats_totals

        # output tsv
        with open(self._output_path_for_flourish, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            writer.writerow(header)
            for player_id in self._season_totals_regular_season_by_season_by_player_id:
                writer.writerow(new_row_by_player_id[player_id])

        # 総合得点のcolumns単位で見て, 上位10にあがる選手にflagを立てる
        # tsvを読み込んで, playerごとの各年代の累計得点辞書を取得
        no = 20
        player_id_flags_set = set()
        total_stats_by_player_id = dict()
        with open(self._output_path_for_flourish, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            header = next(reader)
            for row in reader:
                player_id, *_ = row[:info_area]
                total_stats_by_player_id[int(player_id)] = {s: int(ts) for s, ts in zip(header[info_area:], row[info_area:])}
        # playerごとの各年代累計得点辞書から, その年代のランキングを取得, 上位20位のplayerにflagをつける
        for season in header[info_area:]:
            ranking = []
            for player_id, total_stats_dict in total_stats_by_player_id.items():
                total_stats = total_stats_dict[season]
                ranking.append((player_id, total_stats))
            ranking.sort(key=lambda x: -x[1])
            for tpl in ranking[:no]:
                player_id_flags_set.add(tpl[0])
        # flagのあるplayerのみをtsvに書き込む
        # この人たちレベルだと写真あるのでimage部分書き換える
        with open(self._output_path_for_flourish_with_flag, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            writer.writerow(header)
            for player_id in self._season_totals_regular_season_by_season_by_player_id:
                if player_id in player_id_flags_set:
                    new_row = new_row_by_player_id[player_id]
                    new_row[2] = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
                    writer.writerow(new_row)


if __name__ == '__main__':
    analyzer = Analyzer(stats='PTS')
    # AST, BEB, BLK, FG3PM, STL

    if not analyzer.pickle_path.exists():
        analyzer.get_all_players()
        analyzer.get_season_totals()
        analyzer.save_pickle()
    else:
        analyzer.load_pickle()

    # analyzer.output_to_tsv()

    analyzer.output_for_flourish()
