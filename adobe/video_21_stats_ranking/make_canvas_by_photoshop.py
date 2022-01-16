import sys
from photoshop import Session
from pathlib import Path
from typing import Dict, List, Any

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')

from utils.operate_tsv import tsv_to_dict_of_list, tsv_to_dict_by_first_header_column


def replace_and_output_ps(
        template_psd_path: Path,
        output_psd_name: Path,
        replace_text_dict: Dict[str, str],
        replace_img_dict: Dict[str, str],
        output_png_flag: bool = True,
):
    """
    .psdの文字や画像を置換して, psd, pngに出力する
    """
    print('-' * 30)
    print(replace_img_dict)
    with Session(str(template_psd_path), action='open') as ps:
        doc = ps.active_document
        layers = doc.artLayers

        # 各レイヤに対して
        for i, layer in enumerate(layers):

            if layer.name in replace_text_dict:
                tmp = layer.name
                layer.textItem.contents = replace_text_dict[layer.name]
                layer.name = tmp

            if layer.name in replace_img_dict:
                tmp = layer.name
                replace_contents = ps.app.stringIDToTypeID('placedLayerReplaceContents')
                ps.ActionDescriptor.putPath(ps.app.charIDToTypeID('null'), str(replace_img_dict[layer.name]))
                ps.app.executeAction(replace_contents, ps.ActionDescriptor)
                layer.name = tmp

        # ある選手に対して画像を保存
        doc.saveAs(str(output_psd_name) + '.psd', ps.PhotoshopSaveOptions(), asCopy=True)
        if output_png_flag:
            doc.saveAs(str(output_psd_name) + '.png', ps.PNGSaveOptions(), asCopy=True)


if __name__ == '__main__':

    target_date = '2022-01-15'

    target_stats_list = \
        ['AST', 'REB', 'STL', 'BLK', 'DREB', 'OREB', 'TO', 'FGA', 'FGM', 'FG3M', 'FG3A', 'FTM', 'FTA', 'G']
        # ['PTS']

    working_dir = Path('X:\\Adobe\\PremierePro\\21_StatsRanking\\imgs')

    player_info_tsv = Path('C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\players\\active_20220103.tsv')
    player_info_by_player_id: Dict[str, Any] = tsv_to_dict_by_first_header_column(player_info_tsv)

    team_info_tsv = Path('C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\teams\\teams.tsv')
    team_dict_list: Dict[str, str] = tsv_to_dict_of_list(team_info_tsv)

    player_stats_tsv = Path('C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis'
                            f'\\analyze_03_season_stats_ranking\\results_{target_date}\\results_tsv_{target_date}.tsv')
    stats_by_player_id: Dict[str, Any] = tsv_to_dict_by_first_header_column(player_stats_tsv)

    for target_stats in target_stats_list:

        # team-color, team-logo, player-icon の合成画像のディレクトリ
        base_img_dir = working_dir / f'imgs_{target_date}\\sozai_02\\{target_stats}'

        # output
        output_dir = working_dir / f'imgs_{target_date}\\sozai_03\\{target_stats}'
        if not output_dir.exists():
            output_dir.mkdir()

        # teamplate psd
        template_psd_path = working_dir / f'imgs_{target_date}\\sozai_03\\template.psd'

        # 各画像に関して
        for img_path in base_img_dir.glob('*.png'):
            img_name = str(img_path).split('\\')[-1]
            rank, stats, player_id = img_name.replace('.png', '').split('_')
            print(rank, stats, player_id)

            # 選手のfirst_name, last_nameを取得
            first_name = player_info_by_player_id[player_id]['first_name']
            last_name = player_info_by_player_id[player_id]['last_name']

            # playerのスタッツを取得
            stats_dict: Dict[str, str] = stats_by_player_id[player_id]
            num_game: int = int(stats_dict['G'])
            sum_stats: int = int(stats_dict[target_stats])
            per_stats: float = sum_stats / num_game

            # teamの正式名称
            team_full_name: str = ''
            team_abbreviation: str = stats_dict['TEAM_ABBREVIATION']
            for _ in team_dict_list:
                if _['abbreviation'] == team_abbreviation:
                    team_full_name = _['full_name']
                    break

            # output_path(拡張子は含めない)
            output_path = output_dir / f'{rank}_{player_id}'

            # photoshopに書き出す
            replace_text_dict: Dict[str, str] = {
                'stats_unit': f'{target_stats}',
                'per_stats_unit': f'{target_stats}/G',
                'per_stats': f'{per_stats:.1f}',
                'sum_stats': f'{sum_stats}',
                'first_name': first_name,
                'last_name': last_name,
                'rank': rank,
                'sum_game': f'{num_game}',
                'team_name': team_full_name,
            }
            replace_img_dict: Dict[str, str] = {
                'img': img_path,
            }

            # replace & output (psd, png)
            replace_and_output_ps(
                template_psd_path,
                output_path,
                replace_text_dict,
                replace_img_dict
            )




