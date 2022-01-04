import csv
from pathlib import Path
from photoshop import Session

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from utils.static import ROOT
from utils.operate_tsv import read_tsv

if __name__ == '__main__':
    template_psd_path = Path('X:\\Adobe\\PremierePro\\19_lineups')
    tsv_path = ROOT / 'analysis/analyze_00_longest_lineup/MIN_20220103/unique_players_list.tsv'

    # 情報の読み取り
    with open(tsv_path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        for row in reader:
            player_id, *_ = row





    # 描画
    with Session(template_psd_path, action='open') as ps:
        doc = ps.active_document
        layers = doc.artLayers

