from nba_api.stats.endpoints import leaguedashplayerbiostats, leaguedashplayerstats
from nba_api.stats.library.parameters import PerModeDetailed
from collections import defaultdict
from dataclasses import dataclass
import csv

@dataclass
class Stats:
    player_id: int
    player_name: str
    net_rtg: float
    _minutes: float = None

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, val):
        self._minutes = val


response = leaguedashplayerbiostats.LeagueDashPlayerBioStats().get_normalized_dict()

players = dict()
for i, _ in enumerate(response['LeagueDashPlayerBioStats']):
    players[_['PLAYER_ID']] = Stats(player_id=_['PLAYER_ID'], player_name=_['PLAYER_NAME'], net_rtg=_['NET_RATING'])

response = leaguedashplayerstats.LeagueDashPlayerStats().get_normalized_dict()

for i, _ in enumerate(response['LeagueDashPlayerStats']):
    players[_['PLAYER_ID']].minutes = _['MIN']



with open('result_2022_01_28.tsv', 'w') as f:
    writer = csv.writer(f, delimiter='\t', lineterminator='\n')
    for player_id, stats in players.items():
        img_url = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
        writer.writerow([player_id, stats.player_name, stats.minutes, stats.net_rtg, img_url])
