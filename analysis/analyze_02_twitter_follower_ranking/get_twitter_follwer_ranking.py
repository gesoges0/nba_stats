import os
import sys
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

sys.path.append('C:\\Users\\elasticnet\\Desktop\\nba_stats')
from utils.static import ROOT
from utils.operate_tsv import tsv_to_dict_of_list

if __name__ == '__main__':

    # 選手の辞書
    tsv_path = 'C:\\Users\\elasticnet\\Desktop\\nba_stats\\static\\players\\all_20220103.tsv'
    player_by_full_name: Dict[str, Dict[str, Any]] = {c['full_name']: c for c in tsv_to_dict_of_list(tsv_path)}

    num_follwer_by_full_name: Dict[str, int] = {c['full_name']: 0 for c in tsv_to_dict_of_list(tsv_path)}

    url = 'https://www.basketball-reference.com/friv/twitter.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    cnt = 0
    for i, tr_soup in enumerate(soup.find('tbody').find_all('tr')):
        # print(i, tr_soup.text, tr_soup.find_all('a')[-1].get('href'), tr_soup.find('a').text)
        full_name = tr_soup.find('a').text
        twitter_url = tr_soup.find_all('a')[-1].get('href')

        if full_name in player_by_full_name:
            num_follwer_by_full_name[full_name] = 1
        else:
            print(full_name)
            cnt += 1

    print(cnt)


