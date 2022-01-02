import csv
from pathlib import Path
from typing import List, Any, Iterable


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
