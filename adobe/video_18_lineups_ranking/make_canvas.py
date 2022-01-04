import os
import sys
import subprocess
from pathlib import Path
from photoshop import Session
from typing import Dict, Any, NamedTuple

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.static import ROOT
from utils.operate_tsv import read_tsv, tsv_to_dict_by_first_header_column


class TmpPlayer(NamedTuple):
    player_id: str
    first_name: str
    last_name: str
    image_path: str


if __name__ == '__main__':
    tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\analysis\\' \
               'analyze_00_longest_lineup\\MIN_20220103\\unique_players_list.tsv'
    working_dir_path = Path(f'X:\\Adobe\\PremierePro\\19_lineups')
    output_dir_path = working_dir_path / 'images\\canvases_素材3\\output'
    template_psd_path = working_dir_path / 'images\\canvases_素材3\\template.psd'

    # first_name, last_nameを引くために, player情報を持つ字書を宣言
    all_players_tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\players\\all_20220103.tsv'
    player_by_id: Dict[str, Dict[str, Any]] = tsv_to_dict_by_first_header_column(all_players_tsv_path)

    # player情報読み取り（欲しい情報はplayer_id, first_name, last_name）
    target_player_list = list()
    for row in read_tsv(tsv_path, skip_header=True):
        player_id, *_ = row
        player_info = player_by_id[player_id]
        first_name, last_name = player_info['first_name'], player_info['last_name']
        image_path = working_dir_path / f'images\\canvases_素材2\\{player_id}.png'
        player = TmpPlayer(player_id, first_name, last_name, image_path)
        target_player_list.append(player)

    # for target_player in sorted(target_player_list, key=lambda x: -len(x.last_name))[:20]:
    #     print(target_player.player_id, target_player.first_name, target_player.last_name)
    # print('---------------------')
    # for target_player in sorted(target_player_list, key=lambda x: -len(x.first_name))[:10]:
    #     print(target_player.player_id, target_player.first_name, target_player.last_name)
    # print('---------------------')

    target_player_list.sort(key=lambda x: -len(x.last_name))

    # template.psdを書き換えていく
    with Session(str(template_psd_path), action='open') as ps:
        doc = ps.active_document
        layers = doc.artLayers

        # 各選手に対して
        for target_player in target_player_list:

            # 各レイヤに対して
            for i, layer in enumerate(layers):

                if layer.name == 'first_name':
                    tmp = layer.name
                    layer.textItem.contents = target_player.first_name
                    layer.name = tmp

                if layer.name == 'last_name':
                    tmp = layer.name
                    layer.textItem.contents = target_player.last_name
                    layer.name = tmp

                if layer.name == 'image':
                    tmp = layer.name
                    replace_contents = ps.app.stringIDToTypeID('placedLayerReplaceContents')
                    ps.ActionDescriptor.putPath(ps.app.charIDToTypeID('null'), str(target_player.image_path))
                    ps.app.executeAction(replace_contents, ps.ActionDescriptor)
                    layer.name = tmp

            # ある選手に対して画像を保存
            output_file_path = output_dir_path / f'{target_player.player_id}'
            doc.saveAs(str(output_file_path) + '.psd', ps.PhotoshopSaveOptions(), asCopy=True)
            doc.saveAs(str(output_file_path) + '.png', ps.PNGSaveOptions(), asCopy=True)
