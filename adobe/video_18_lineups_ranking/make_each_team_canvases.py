import os
import sys
from pathlib import Path
from typing import List, Dict
from photoshop import Session

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.static import HEX_COLOR_CODE_BY_TEAM_ABBREVIATION
from utils.operate_tsv import tsv_to_dict_of_list

RANK_N = 50

if __name__ == '__main__':
    # 背景色と文字を変えるためのtemplate psd
    template_psd_path = 'X:\\Adobe\\PremierePro\\19_lineups\\images\\lineups_20220127\\sozai_03\\template.psd'

    # lineupのランキングのtsv
    tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\' \
               'analyze_00_longest_lineup\\MIN_20220127\\ranking_lineups.tsv'

    # 出力先
    output_dir_path = Path('X:\\Adobe\\PremierePro\\19_lineups\\images\\lineups_20220127\\sozai_03\\output')

    # 目的のスタッツ
    target_stat = 'MIN'
    target_stat_1 = 'PLUS_MINUS'

    # 目的スタッツのstrからの変換関数
    def _convert(_target_stat: str) -> str:
        return str(int(float(_target_stat)))

    # unitのコンバーター
    def _convert_unit(_unit: str) -> str:
        if _unit == 'PLUS_MINUS':
            return '+/-'
        return _unit


    # 辞書リスト
    rank_list: List[Dict[str, str]] = tsv_to_dict_of_list(tsv_path)

    # 変換
    with Session(template_psd_path, action='open') as ps:
        doc = ps.active_document
        layers = doc.artLayers

        # 順位を見ていく
        for i, info_dict in enumerate(rank_list[:RANK_N]):
            team_abbreviation = info_dict['TEAM_ABBREVIATION']
            bg_color_hex = HEX_COLOR_CODE_BY_TEAM_ABBREVIATION[team_abbreviation]

            rank = str(i + 1)
            if len(rank) == 1:
                rank = '  ' + rank
            elif len(rank) == 2:
                rank = ' ' + rank

            # statが小数の場合の処理
            stat = _convert(info_dict[target_stat])
            # statが小数の場合の処理
            stat_1 = _convert(info_dict[target_stat_1])

            print(i, team_abbreviation, stat, bg_color_hex)

            # レイヤー変更
            for layer in layers:

                if layer.name == 'team':
                    tmp = layer.name
                    layer.textItem.contents = team_abbreviation
                    layer.name = tmp

                if layer.name == 'stat':
                    tmp = layer.name
                    layer.textItem.contents = stat
                    layer.name = tmp

                if layer.name == 'rank':
                    tmp = layer.name
                    layer.textItem.contents = rank
                    layer.name = tmp

                if layer.name == 'unit':
                    tmp = layer.name
                    layer.textItem.contents = _convert_unit(target_stat)
                    layer.name = tmp

                if layer.name == 'stat_1':
                    tmp = layer.name
                    layer.textItem.contents = stat_1
                    layer.name = tmp

                if layer.name == 'unit_1':
                    tmp = layer.name
                    layer.textItem.contents = _convert_unit(target_stat_1)
                    layer.name = tmp

                if layer.name == 'background':
                    backgroundColor = ps.SolidColor()
                    backgroundColor.rgb.hexValue = bg_color_hex
                    ps.active_document.selection.fill(backgroundColor)

            # save
            output_file_path = output_dir_path / f'{i}'
            doc.saveAs(str(output_file_path) + '.psd', ps.PhotoshopSaveOptions(), asCopy=True)
            doc.saveAs(str(output_file_path) + '.png', ps.PNGSaveOptions(), asCopy=True)
