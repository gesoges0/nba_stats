from pathlib import Path
import sys
import cv2
from typing import List, Dict, Any
from dataclasses import dataclass

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.operate_tsv import tsv_to_dict_of_list
from adobe.tools.other.make_synthetic import make_synthetic

@dataclass
class Rank:
    rank: int
    info: Dict[str, Any]

def get_ranking(rows: List[Dict[str, str]], target_key) -> List[Rank]:

    def _val(s, g):
        return s / g

    results: List[Rank] = list()
    # 得点の低い順にソート
    unique_vals = list(
        set(
            [_val(int(_[target_key]), int(_['G'])) if int(_['G']) else -1 for _ in rows]
        )
    )
    unique_vals.sort(reverse=True)
    # 全体の順位
    rank_all = 1
    for val in unique_vals:
        # この値のカウント
        count = 0
        # 得点 val の選手に rankを付ける
        for row in rows:
            if int(row['G']) < 51:
                continue
            if _val(int(row[target_key]), int(row['G'])) == val:
                rank = Rank(rank_all, row)
                results.append(rank)
                count += 1
        rank_all += count
    return results


if __name__ == '__main__':

    target_date = '2022-02-21'
    target_stats_list = \
        ['PTS', 'AST', 'REB', 'STL', 'BLK', 'DREB', 'OREB', 'TO', 'FGA', 'FGM', 'FG3M', 'FG3A', 'FTM', 'FTA', 'G']
    RANK_LIMITATION = 100
    working_dir = Path('X:\\Adobe\\PremierePro\\21_StatsRanking\\imgs')

    # base(team_color)画像のpath
    base_img_dir = working_dir / f'imgs_{target_date}\\sozai_01'

    # team_logo
    team_logo_dir = working_dir / 'team_logo_resized_width_307'

    # player img
    player_img_dir = working_dir / f'imgs_{target_date}\\sozai_00_resized'

    for target_stats in target_stats_list:

        # output dir
        output_dir = working_dir / f'imgs_{target_date}\\sozai_02\\{target_stats}'
        if not output_dir.exists():
            output_dir.mkdir()

        # ランキングTSVを読み込む
        tsv_path = f'C:\\Users\\elasticnet\\Desktop\\nba_stats\\' \
                   f'analysis\\analyze_03_season_stats_ranking\\results_{target_date}\\results_tsv_{target_date}.tsv'
        rows: List[Dict[str, Any]] = tsv_to_dict_of_list(tsv_path)

        rankings: List[Rank] = get_ranking(rows, target_key=target_stats)

        # 対象のランキング（28位が5人いたときは28となる）
        limit_rank = sorted([rank for rank in rankings], key=lambda x: x.rank)[RANK_LIMITATION-1].rank

        # limit_rank 以内の選手に絞る
        rankings_limit = [rank for rank in rankings if rank.rank <= limit_rank]

        for rank in rankings_limit:
            print(target_stats, rank)
            base_img_path = base_img_dir / f'{rank.info["TEAM_ABBREVIATION"]}.png'
            team_logo_path = team_logo_dir / f'{rank.info["TEAM_ABBREVIATION"]}.png'
            player_img_path = player_img_dir / f'{rank.info["PLAYER_ID"]}.png'
            assert base_img_path.exists(), f'{base_img_path} does not exists!'
            assert team_logo_path.exists(), f'{team_logo_path} does not exists!'
            # assert player_img_path.exists(), f'{player_img_path} does not exists!'
            if not player_img_path.exists():
                continue

            base_img = cv2.imread(str(base_img_path), cv2.IMREAD_UNCHANGED)
            team_logo_img = cv2.imread(str(team_logo_path), cv2.IMREAD_UNCHANGED)
            player_img_img = cv2.imread(str(player_img_path), cv2.IMREAD_UNCHANGED)

            output_path = output_dir / f'{rank.rank}_{rank.info["PTS"]}_{rank.info["PLAYER_ID"]}.png'

            tmp = make_synthetic(bg_img=base_img, fg_img=team_logo_img, coordinate=(0, 0))
            tmp = make_synthetic(bg_img=tmp, fg_img=player_img_img, coordinate=(6, 165))

            cv2.imwrite(str(output_path), tmp)


