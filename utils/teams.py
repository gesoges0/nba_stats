import csv
from typing import Union, Dict, List


def get_teams_info() -> List[Dict[str, Union[str, int]]]:
    """apiでteam_idはintなので変換注意"""
    res = []
    tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\teams\\teams.tsv'
    with open(tsv_path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        for row in reader:
            res.append({k: v for k, v in zip(header, row)})
    return res


def get_team_info_by_team_id() -> Dict[str, Dict[str, Union[str, int]]]:
    """apiでteam_idはintなので変換注意"""
    res = dict()
    tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\teams\\teams.tsv'
    with open(tsv_path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        for row in reader:
            res[row[0]] = {k: v for k, v in zip(header, row)}
    return res
