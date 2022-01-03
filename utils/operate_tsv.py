import csv
from pathlib import Path
from typing import List, Dict, Any, Iterable


def write_tsv(tsv_path: Path, rows: List[Any]) -> None:
    """
    :param tsv_path: ROOTからのPATH
    :param rows:
    :return:
    """
    with open(tsv_path, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for row in rows:
            writer.writerow(row)


def read_tsv(tsv_path: Path, has_header: bool = True) -> Iterable[List[Any]]:
    """
    :param tsv_path:
    :param has_header:
    :return:
    """
    with open(tsv_path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        if has_header:
            header = next(reader)
            yield header
        for row in reader:
            yield row


def write_tsv_from_dict_list(tsv_path: Path, dict_list: List[Dict[str, Any]]) -> None:
    """
    :param tsv_path:
    :param dict_list:
    :return:
    """
    assert dict_list, 'listが空のため, tsvを作成できません.'
    header = list(dict_list[0].keys())
    rows = list()
    rows.append(header)
    for _dict in dict_list:
        rows.append(list(_dict.values()))
    write_tsv(tsv_path, rows)


def read_all_rows_from_tsv(tsv_path: Path, read_header: bool = False) -> List[List[Any]]:
    with open(tsv_path, 'r') as f:
        rows = []
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        if read_header:
            rows.append(header)
        for row in reader:
            rows.append(row)
        return rows
