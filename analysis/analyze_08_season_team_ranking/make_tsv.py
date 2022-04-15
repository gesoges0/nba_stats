from nba_api.stats.endpoints import scoreboardv2, leaguegamefinder
import csv
import sys
import pickle
import time

sys.path.append('../../utils')
# from teams import get_team_info_by_team_id


# 全ての日程を取得
def _convert(date_string):
    yyyy, mm, dd = date_string.split('-')
    return f'{mm}/{dd}/{yyyy}'

# teamとabbreviationの対応
team_abbreviation_by_team_id = {
    1610612756: 'PHX',
    1610612763: 'MEM',
    1610612748: 'MIA',
    1610612744: 'GSW',
    1610612742: 'DAL',
    1610612749: 'MIL',
    1610612738: 'BOS',
    1610612755: 'PHI',
    1610612743: 'DEN',
    1610612761: 'TOR',
    1610612762: 'UTA',
    1610612750: 'MIN',
    1610612741: 'CHI',
    1610612751: 'BKN',
    1610612739: 'CLE',
    1610612737: 'ATL',
    1610612766: 'CHA',
    1610612746: 'LAC',
    1610612740: 'NOP',
    1610612752: 'NYK',
    1610612764: 'WAS',
    1610612759: 'SAS',
    1610612747: 'LAL',
    1610612758: 'SAC',
    1610612757: 'POR',
    1610612754: 'IND',
    1610612760: 'OKC',
    1610612765: 'DET',
    1610612753: 'ORL',
    1610612745: 'HOU',
}

if __name__ == '__main__':
    # 全ての日程を取得
    res = leaguegamefinder.LeagueGameFinder('T', season_nullable='2021-22', league_id_nullable='00', season_type_nullable='Regular Season').get_normalized_dict()
    # for i, _ in enumerate(res['LeagueGameFinderResults']):
    #     if _['GAME_DATE'] != '2022-04-10':
    #         break
    #     print(i, _['MATCHUP'])
    # exit()
    dates = sorted(list(set(_convert(_['GAME_DATE']) for _ in res['LeagueGameFinderResults'])), key=lambda d: (d.split('/')[2], d.split('/')[0], d.split('/')[1]))

    # 全日程のランキング
    ranking = {'east': dict(), 'west': dict()}

    # 各日程における順位を取得
    res = scoreboardv2.ScoreboardV2(game_date='01/01/2022').get_normalized_dict()
    for i, date in enumerate(dates):
        print(i, len(dates), date)
        res = scoreboardv2.ScoreboardV2(game_date=date).get_normalized_dict()
        ranking['east'][date] = res['EastConfStandingsByDay']
        ranking['west'][date] = res['WestConfStandingsByDay']
        time.sleep(5)

    # apiの取得結果を保存
    pickle_path = 'result.bin'
    with open(pickle_path, 'wb') as p:
        pickle.dump(ranking, p)

    # picke読み込み
    # ranking = None
    # with open(pickle_path, 'rb') as p:
    #     ranking = pickle.load(p)

    # team一覧
    # team_info_by_team_id = get_team_info_by_team_id()
    teams = {'east': [], 'west': []}
    for conference in ['east', 'west']:
        # 各カンファレンスのチームID一覧を取得
        team_ids = [_['TEAM_ID'] for _ in ranking[conference]['01/01/2022']]
        # チームIDからABBREVIATIONに変換
        team_abbreviation = sorted([team_id for team_id in team_ids])
        teams[conference] = team_abbreviation

    # チームをキーとしてランキングを取得できるようにする
    ranking_by_team_id = dict()
    for conference in ['east', 'west']:
        ranking_by_team_id[conference] = dict()
        for date in ranking[conference]:
            ranking_by_team_id[conference][date] = dict()
            for rank, info in enumerate(ranking[conference][date], 1):
                ranking_by_team_id[conference][date][info['TEAM_ID']] = rank

    # TSVに出力 (横軸: 日程, 縦軸: チーム)
    for conference in ['east', 'west']:
        tsv_path = f'./output_{conference}.tsv'
        with open(tsv_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            header = ['TEAM_ABBREVIATION', 'TEAM_CREST'] + [date for date in dates]
            writer.writerow(header)
            for team_id in teams[conference]:
                writer.writerow(
                    [
                        team_abbreviation_by_team_id[team_id],
                        f'https://cdn.nba.com/logos/nba/{team_id}/global/D/logo.svg'
                    ] +
                    [ranking_by_team_id[conference][date][team_id] for date in dates]
                )
