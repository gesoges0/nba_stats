# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players

# LeagueGameFinderだと10/28/1983からしかゲーム情報が取得できない

def get_player_common_info(player_id):
    response = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    return response.get_normalized_dict()

    # response = leaguegamelog.LeagueGameLog()
    # return response.get_normalized_dict()

def get_active_players():
    response = players.get_active_players()
    return response

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    players = get_active_players()
    for player in players:
        player_info = get_player_common_info(player['id'])
        player_id = player['id']
        team_id = player_info['CommonPlayerInfo'][0]['TEAM_ID']
        img_url = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/{team_id}/2021/260x190/{player_id}.png'
        print(player, player_info['CommonPlayerInfo'][0]['TEAM_ABBREVIATION'])
        print(img_url)
        # print(f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/1610612749/2021/260x190/203507.png')
        # print(f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/1610612741/2021/260x190/203897.png')




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
