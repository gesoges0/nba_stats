from nba_api.live.nba.endpoints import boxscore, playbyplay, scoreboard
import json

response = boxscore.BoxScore(game_id="0022100733").get_response()
response = json.loads(response)
print(type(response))

print(response['meta'])
# {'version': 1, 'code': 200, 'request': 'http://nba.cloud/games/0022100733/boxscore?Format=json', 'time': '2022-01-27 20:20:06.674739'}

print(response['game'].keys())
# dict_keys(['gameId', 'gameTimeLocal', 'gameTimeUTC', 'gameTimeHome', 'gameTimeAway', 'gameEt', 'duration',
# 'gameCode', 'gameStatusText', 'gameStatus', 'regulationPeriods', 'period', 'gameClock', 'attendance', 'sellout', 'arena', 'offic
# ials', 'homeTeam', 'awayTeam'])

print(response['game']['gameId'])
# 0022100733

print(response['game']['gameTimeLocal'])
# 2022-01-27T19:30:00-05:00

print(response['game']['gameTimeUTC'])
# 2022-01-28T00:30:00Z

print(response['game']['gameTimeHome'])
# 2022-01-27T19:30:00-05:00

print(response['game']['gameEt'])
# 2022-01-27T19:30:00-05:00

print(response['game']['duration'])
# 50

print(response['game']['gameCode'])
# 20220127/LALPHI

print(response['game']['gameStatusText'])
# Q2 02:08

print(response['game']['gameStatus'])
# 2

print(response['game']['regulationPeriods'])
# 4

print(response['game']['period'])
# 2

print(response['game']['gameClock'])
# PT00M42.80S

print(response['game']['attendance'])
# 0

print(response['game']['sellout'])
# 0

print(response['game']['arena'])
# {'arenaId': 419, 'arenaName': 'Wells Fargo Center', 'arenaCity': 'Philadelphia', 'arenaState': 'PA', 'arenaCountry': 'US', 'arenaTimezone': 'America/New_York'}

print(response['game']['officials'])
# [{'personId': 1148, 'name': 'James Capers', 'nameI': 'J. Capers', 'firstName': 'James', 'familyName': 'Capers', 'jerseyNum': '19', 'assignment': 'OFFICIAL1'}, {'personId': 1201, 'name': 'Leon Wood', 'nameI': 'L. Wood', 'firstName': 'Le
# on', 'familyName': 'Wood', 'jerseyNum': '40', 'assignment': 'OFFICIAL3'}, {'personId': 201246, 'name': 'Kevin Cutler', 'nameI': 'K. Cutler', 'firstName': 'Kevin', 'familyName': 'Cutler', 'jerseyNum': '34', 'assignment': 'OFFICIAL2'}]

for k, v in response['game']['homeTeam'].items():
    if type(v) in [int, str]:
        print(k, v)
    if type(v) == list:
        print(k)
        for i, _ in enumerate(v):
            print(i, _)
    if type(v) == dict:
        print(k)
        for kk, vv in v.items():
            print(kk, vv)
    print('-' * 30)

# teamId 1610612755
# ------------------------------
# teamName 76ers
# ------------------------------
# teamCity Philadelphia
# ------------------------------
# teamTricode PHI
# ------------------------------
# score 54
# ------------------------------
# inBonus 0
# ------------------------------
# timeoutsRemaining 6
# ------------------------------
# periods
# 0 {'period': 1, 'periodType': 'REGULAR', 'score': 32}
# 1 {'period': 2, 'periodType': 'REGULAR', 'score': 22}
# 2 {'period': 3, 'periodType': 'REGULAR', 'score': 0}
# 3 {'period': 4, 'periodType': 'REGULAR', 'score': 0}
# ------------------------------
# players
# 0 {'status': 'ACTIVE', 'order': 1, 'personId': 1629680, 'jerseyNum': '22', 'position': 'SF', 'starter': '1', 'oncourt': '0', 'played': '1', 'statistics': {'assists': 0, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 3, 'field
# GoalsMade': 2, 'fieldGoalsPercentage': 0.666666666666666, 'foulsOffensive': 0, 'foulsDrawn': 1, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 31.0, 'minute
# s': 'PT13M28.93S', 'minutesCalculated': 'PT13M', 'plus': 31.0, 'plusMinusPoints': 0.0, 'points': 4, 'pointsFastBreak': 0, 'pointsInThePaint': 4, 'pointsSecondChance': 0, 'reboundsDefensive': 1, 'reboundsOffensive': 0, 'reboundsTotal':
# 1, 'steals': 3, 'threePointersAttempted': 1, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 1, 'twoPointersAttempted': 2, 'twoPointersMade': 2, 'twoPointersPercentage': 1.0}, 'name': 'Matisse Thybulle', 'nameI': '
# M. Thybulle', 'firstName': 'Matisse', 'familyName': 'Thybulle'}
# 1 {'status': 'ACTIVE', 'order': 2, 'personId': 202699, 'jerseyNum': '12', 'position': 'PF', 'starter': '1', 'oncourt': '1', 'played': '1', 'statistics': {'assists': 3, 'blocks': 0, 'blocksReceived': 2, 'fieldGoalsAttempted': 9, 'fieldG
# oalsMade': 5, 'fieldGoalsPercentage': 0.555555555555556, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 37.0, 'minutes
# ': 'PT17M39.00S', 'minutesCalculated': 'PT18M', 'plus': 35.0, 'plusMinusPoints': -2.0, 'points': 11, 'pointsFastBreak': 0, 'pointsInThePaint': 8, 'pointsSecondChance': 0, 'reboundsDefensive': 3, 'reboundsOffensive': 0, 'reboundsTotal':
#  3, 'steals': 0, 'threePointersAttempted': 3, 'threePointersMade': 1, 'threePointersPercentage': 0.333333333333333, 'turnovers': 1, 'twoPointersAttempted': 6, 'twoPointersMade': 4, 'twoPointersPercentage': 0.666666666666666}, 'name': '
# Tobias Harris', 'nameI': 'T. Harris', 'firstName': 'Tobias', 'familyName': 'Harris'}
# 2 {'status': 'ACTIVE', 'order': 3, 'personId': 203954, 'jerseyNum': '21', 'position': 'C', 'starter': '1', 'oncourt': '1', 'played': '1', 'statistics': {'assists': 4, 'blocks': 1, 'blocksReceived': 1, 'fieldGoalsAttempted': 11, 'fieldG
# oalsMade': 5, 'fieldGoalsPercentage': 0.45454545454545503, 'foulsOffensive': 1, 'foulsDrawn': 4, 'foulsPersonal': 2, 'foulsTechnical': 0, 'freeThrowsAttempted': 6, 'freeThrowsMade': 3, 'freeThrowsPercentage': 0.5, 'minus': 37.0, 'minut
# es': 'PT17M47.00S', 'minutesCalculated': 'PT18M', 'plus': 43.0, 'plusMinusPoints': 6.0, 'points': 13, 'pointsFastBreak': 0, 'pointsInThePaint': 8, 'pointsSecondChance': 1, 'reboundsDefensive': 5, 'reboundsOffensive': 1, 'reboundsTotal'
# : 6, 'steals': 1, 'threePointersAttempted': 2, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 2, 'twoPointersAttempted': 9, 'twoPointersMade': 5, 'twoPointersPercentage': 0.555555555555556}, 'name': 'Joel Embiid',
#  'nameI': 'J. Embiid', 'firstName': 'Joel', 'familyName': 'Embiid'}
# 3 {'status': 'ACTIVE', 'order': 4, 'personId': 1627788, 'jerseyNum': '30', 'position': 'SG', 'starter': '1', 'oncourt': '1', 'played': '1', 'statistics': {'assists': 2, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 4, 'field
# GoalsMade': 3, 'fieldGoalsPercentage': 0.75, 'foulsOffensive': 0, 'foulsDrawn': 3, 'foulsPersonal': 2, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 42.0, 'minutes': 'PT18M29.
# 08S', 'minutesCalculated': 'PT18M', 'plus': 36.0, 'plusMinusPoints': -6.0, 'points': 6, 'pointsFastBreak': 2, 'pointsInThePaint': 6, 'pointsSecondChance': 0, 'reboundsDefensive': 1, 'reboundsOffensive': 0, 'reboundsTotal': 1, 'steals':
#  0, 'threePointersAttempted': 1, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 1, 'twoPointersAttempted': 3, 'twoPointersMade': 3, 'twoPointersPercentage': 1.0}, 'name': 'Furkan Korkmaz', 'nameI': 'F. Korkmaz', '
# firstName': 'Furkan', 'familyName': 'Korkmaz'}
# 4 {'status': 'ACTIVE', 'order': 5, 'personId': 1630178, 'jerseyNum': '0', 'position': 'PG', 'starter': '1', 'oncourt': '0', 'played': '1', 'statistics': {'assists': 5, 'blocks': 1, 'blocksReceived': 1, 'fieldGoalsAttempted': 5, 'fieldG
# oalsMade': 1, 'fieldGoalsPercentage': 0.2, 'foulsOffensive': 0, 'foulsDrawn': 1, 'foulsPersonal': 3, 'foulsTechnical': 0, 'freeThrowsAttempted': 2, 'freeThrowsMade': 1, 'freeThrowsPercentage': 0.5, 'minus': 36.0, 'minutes': 'PT18M15.92
# S', 'minutesCalculated': 'PT18M', 'plus': 45.0, 'plusMinusPoints': 9.0, 'points': 4, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDefensive': 1, 'reboundsOffensive': 0, 'reboundsTotal': 1, 'steals': 0,
#  'threePointersAttempted': 3, 'threePointersMade': 1, 'threePointersPercentage': 0.333333333333333, 'turnovers': 0, 'twoPointersAttempted': 2, 'twoPointersMade': 0, 'twoPointersPercentage': 0.0}, 'name': 'Tyrese Maxey', 'nameI': 'T. Ma
# xey', 'firstName': 'Tyrese', 'familyName': 'Maxey'}
# 5 {'status': 'ACTIVE', 'order': 6, 'personId': 201980, 'jerseyNum': '14', 'starter': '0', 'oncourt': '1', 'played': '1', 'statistics': {'assists': 0, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 4, 'fieldGoalsMade': 2, 'fie
# ldGoalsPercentage': 0.5, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 20.0, 'minutes': 'PT10M30.00S', 'minutesCalcul
# ated': 'PT11M', 'plus': 27.0, 'plusMinusPoints': 7.0, 'points': 6, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDefensive': 2, 'reboundsOffensive': 0, 'reboundsTotal': 2, 'steals': 0, 'threePointersAtt
# empted': 4, 'threePointersMade': 2, 'threePointersPercentage': 0.5, 'turnovers': 1, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointersPercentage': 0.0}, 'name': 'Danny Green', 'nameI': 'D. Green', 'firstName': 'Danny', 'fami
# lyName': 'Green'}
# 6 {'status': 'ACTIVE', 'order': 7, 'personId': 1630198, 'jerseyNum': '7', 'starter': '0', 'oncourt': '1', 'played': '1', 'statistics': {'assists': 0, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 1, 'fieldGoalsMade': 1, 'fie
# ldGoalsPercentage': 1.0, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 13.0, 'minutes': 'PT09M06.07S', 'minutesCalcul
# ated': 'PT09M', 'plus': 21.0, 'plusMinusPoints': 8.0, 'points': 3, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDefensive': 0, 'reboundsOffensive': 0, 'reboundsTotal': 0, 'steals': 0, 'threePointersAtt
# empted': 1, 'threePointersMade': 1, 'threePointersPercentage': 1.0, 'turnovers': 0, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointersPercentage': 0.0}, 'name': 'Isaiah Joe', 'nameI': 'I. Joe', 'firstName': 'Isaiah', 'family
# Name': 'Joe'}
# 7 {'status': 'ACTIVE', 'order': 8, 'personId': 1627777, 'jerseyNum': '20', 'starter': '0', 'oncourt': '0', 'played': '1', 'statistics': {'assists': 1, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 4, 'fieldGoalsMade': 2, 'fi
# eldGoalsPercentage': 0.5, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 13.0, 'minutes': 'PT08M31.00S', 'minutesCalcu
# lated': 'PT09M', 'plus': 21.0, 'plusMinusPoints': 8.0, 'points': 5, 'pointsFastBreak': 3, 'pointsInThePaint': 2, 'pointsSecondChance': 0, 'reboundsDefensive': 0, 'reboundsOffensive': 0, 'reboundsTotal': 0, 'steals': 0, 'threePointersAt
# tempted': 3, 'threePointersMade': 1, 'threePointersPercentage': 0.333333333333333, 'turnovers': 0, 'twoPointersAttempted': 1, 'twoPointersMade': 1, 'twoPointersPercentage': 1.0}, 'name': 'Georges Niang', 'nameI': 'G. Niang', 'firstName
# ': 'Georges', 'familyName': 'Niang'}
# 8 {'status': 'ACTIVE', 'order': 9, 'personId': 203083, 'jerseyNum': '1', 'starter': '0', 'oncourt': '0', 'played': '1', 'statistics': {'assists': 2, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 1, 'fieldGoalsMade': 1, 'fiel
# dGoalsPercentage': 1.0, 'foulsOffensive': 1, 'foulsDrawn': 0, 'foulsPersonal': 1, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 11.0, 'minutes': 'PT06M13.00S', 'minutesCalcula
# ted': 'PT06M', 'plus': 11.0, 'plusMinusPoints': 0.0, 'points': 2, 'pointsFastBreak': 0, 'pointsInThePaint': 2, 'pointsSecondChance': 0, 'reboundsDefensive': 3, 'reboundsOffensive': 0, 'reboundsTotal': 3, 'steals': 1, 'threePointersAtte
# mpted': 0, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 1, 'twoPointersAttempted': 1, 'twoPointersMade': 1, 'twoPointersPercentage': 1.0}, 'name': 'Andre Drummond', 'nameI': 'A. Drummond', 'firstName': 'Andre',
# 'familyName': 'Drummond'}
# 9 {'status': 'ACTIVE', 'order': 10, 'personId': 1629646, 'jerseyNum': '23', 'starter': '0', 'oncourt': '0', 'played': '0', 'statistics': {'assists': 0, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 0, 'fieldGoalsMade': 0, 'f
# ieldGoalsPercentage': 0.0, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 0.0, 'minutes': 'PT00M00.00S', 'minutesCalcu
# lated': 'PT00M', 'plus': 0.0, 'plusMinusPoints': 0.0, 'points': 0, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDefensive': 0, 'reboundsOffensive': 0, 'reboundsTotal': 0, 'steals': 0, 'threePointersAtt
# empted': 0, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 0, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointersPercentage': 0.0}, 'name': 'Charles Bassey', 'nameI': 'C. Bassey', 'firstName': 'Charles',
#  'familyName': 'Bassey'}
# 10 {'status': 'ACTIVE', 'order': 11, 'personId': 1629718, 'jerseyNum': '16', 'starter': '0', 'oncourt': '0', 'played': '0', 'statistics': {'assists': 0, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 0, 'fieldGoalsMade': 0, '
# fieldGoalsPercentage': 0.0, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 0.0, 'minutes': 'PT00M00.00S', 'minutesCalc
# ulated': 'PT00M', 'plus': 0.0, 'plusMinusPoints': 0.0, 'points': 0, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDefensive': 0, 'reboundsOffensive': 0, 'reboundsTotal': 0, 'steals': 0, 'threePointersAt
# tempted': 0, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 0, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointersPercentage': 0.0}, 'name': 'Charlie Brown Jr.', 'nameI': 'C. Brown Jr.', 'firstName': 'Ch
# arlie', 'familyName': 'Brown Jr.'}
# 11 {'status': 'ACTIVE', 'order': 12, 'personId': 1629619, 'jerseyNum': '5', 'starter': '0', 'oncourt': '0', 'played': '0', 'statistics': {'assists': 0, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 0, 'fieldGoalsMade': 0, 'f
# ieldGoalsPercentage': 0.0, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus': 0.0, 'minutes': 'PT00M00.00S', 'minutesCalcu
# lated': 'PT00M', 'plus': 0.0, 'plusMinusPoints': 0.0, 'points': 0, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDefensive': 0, 'reboundsOffensive': 0, 'reboundsTotal': 0, 'steals': 0, 'threePointersAtt
# empted': 0, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 0, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointersPercentage': 0.0}, 'name': 'Myles Powell', 'nameI': 'M. Powell', 'firstName': 'Myles', 'fa
# milyName': 'Powell'}
# 12 {'status': 'INACTIVE', 'notPlayingReason': 'INACTIVE_INJURY', 'notPlayingDescription': 'Left Ankle; Soreness ', 'order': 13, 'personId': 203552, 'jerseyNum': '31', 'starter': '0', 'oncourt': '0', 'played': '0', 'statistics': {'assis
# ts': 0, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 0, 'fieldGoalsMade': 0, 'fieldGoalsPercentage': 0.0, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsM
# ade': 0, 'freeThrowsPercentage': 0.0, 'minus': 0.0, 'minutes': 'PT00M00.00S', 'minutesCalculated': 'PT00M', 'plus': 0.0, 'plusMinusPoints': 0.0, 'points': 0, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboun
# dsDefensive': 0, 'reboundsOffensive': 0, 'reboundsTotal': 0, 'steals': 0, 'threePointersAttempted': 0, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 0, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointer
# sPercentage': 0.0}, 'name': 'Seth Curry', 'nameI': 'S. Curry', 'firstName': 'Seth', 'familyName': 'Curry'}
# 13 {'status': 'INACTIVE', 'notPlayingReason': 'INACTIVE_INJURY', 'notPlayingDescription': 'Back; Contusion ', 'order': 14, 'personId': 1629003, 'jerseyNum': '18', 'starter': '0', 'oncourt': '0', 'played': '0', 'statistics': {'assists':
#  0, 'blocks': 0, 'blocksReceived': 0, 'fieldGoalsAttempted': 0, 'fieldGoalsMade': 0, 'fieldGoalsPercentage': 0.0, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade'
# : 0, 'freeThrowsPercentage': 0.0, 'minus': 0.0, 'minutes': 'PT00M00.00S', 'minutesCalculated': 'PT00M', 'plus': 0.0, 'plusMinusPoints': 0.0, 'points': 0, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDe
# fensive': 0, 'reboundsOffensive': 0, 'reboundsTotal': 0, 'steals': 0, 'threePointersAttempted': 0, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 0, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointersPer
# centage': 0.0}, 'name': 'Shake Milton', 'nameI': 'S. Milton', 'firstName': 'Shake', 'familyName': 'Milton'}
# 14 {'status': 'INACTIVE', 'notPlayingReason': 'INACTIVE_GLEAGUE_ON_ASSIGNMENT', 'order': 15, 'personId': 1630194, 'jerseyNum': '44', 'starter': '0', 'oncourt': '0', 'played': '0', 'statistics': {'assists': 0, 'blocks': 0, 'blocksReceiv
# ed': 0, 'fieldGoalsAttempted': 0, 'fieldGoalsMade': 0, 'fieldGoalsPercentage': 0.0, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0
# .0, 'minus': 0.0, 'minutes': 'PT00M00.00S', 'minutesCalculated': 'PT00M', 'plus': 0.0, 'plusMinusPoints': 0.0, 'points': 0, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDefensive': 0, 'reboundsOffensiv
# e': 0, 'reboundsTotal': 0, 'steals': 0, 'threePointersAttempted': 0, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 0, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointersPercentage': 0.0}, 'name': 'Paul
# Reed', 'nameI': 'P. Reed', 'firstName': 'Paul', 'familyName': 'Reed'}
# 15 {'status': 'INACTIVE', 'notPlayingReason': 'INACTIVE_PERSONAL', 'order': 16, 'personId': 1627732, 'jerseyNum': '25', 'starter': '0', 'oncourt': '0', 'played': '0', 'statistics': {'assists': 0, 'blocks': 0, 'blocksReceived': 0, 'fiel
# dGoalsAttempted': 0, 'fieldGoalsMade': 0, 'fieldGoalsPercentage': 0.0, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0.0, 'minus':
# 0.0, 'minutes': 'PT00M00.00S', 'minutesCalculated': 'PT00M', 'plus': 0.0, 'plusMinusPoints': 0.0, 'points': 0, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDefensive': 0, 'reboundsOffensive': 0, 'rebou
# ndsTotal': 0, 'steals': 0, 'threePointersAttempted': 0, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 0, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointersPercentage': 0.0}, 'name': 'Ben Simmons', 'nam
# eI': 'B. Simmons', 'firstName': 'Ben', 'familyName': 'Simmons'}
# 16 {'status': 'INACTIVE', 'notPlayingReason': 'INACTIVE_GLEAGUE_ON_ASSIGNMENT', 'order': 17, 'personId': 1630531, 'jerseyNum': '11', 'starter': '0', 'oncourt': '0', 'played': '0', 'statistics': {'assists': 0, 'blocks': 0, 'blocksReceiv
# ed': 0, 'fieldGoalsAttempted': 0, 'fieldGoalsMade': 0, 'fieldGoalsPercentage': 0.0, 'foulsOffensive': 0, 'foulsDrawn': 0, 'foulsPersonal': 0, 'foulsTechnical': 0, 'freeThrowsAttempted': 0, 'freeThrowsMade': 0, 'freeThrowsPercentage': 0
# .0, 'minus': 0.0, 'minutes': 'PT00M00.00S', 'minutesCalculated': 'PT00M', 'plus': 0.0, 'plusMinusPoints': 0.0, 'points': 0, 'pointsFastBreak': 0, 'pointsInThePaint': 0, 'pointsSecondChance': 0, 'reboundsDefensive': 0, 'reboundsOffensiv
# e': 0, 'reboundsTotal': 0, 'steals': 0, 'threePointersAttempted': 0, 'threePointersMade': 0, 'threePointersPercentage': 0.0, 'turnovers': 0, 'twoPointersAttempted': 0, 'twoPointersMade': 0, 'twoPointersPercentage': 0.0}, 'name': 'Jaden
#  Springer', 'nameI': 'J. Springer', 'firstName': 'Jaden', 'familyName': 'Springer'}
# ------------------------------
# statistics
# assists 17
# assistsTurnoverRatio 2.125
# benchPoints 16
# biggestLead 12
# biggestLeadScore 29-41
# biggestScoringRun 9
# biggestScoringRunScore 20-30
# blocks 2
# blocksReceived 4
# fastBreakPointsAttempted 2
# fastBreakPointsMade 2
# fastBreakPointsPercentage 1.0
# fieldGoalsAttempted 42
# fieldGoalsEffectiveAdjusted 0.595238095238095
# fieldGoalsMade 22
# fieldGoalsPercentage 0.5238095238095241
# foulsOffensive 2
# foulsDrawn 9
# foulsPersonal 8
# foulsTeam 6
# foulsTechnical 0
# foulsTeamTechnical 0
# freeThrowsAttempted 8
# freeThrowsMade 4
# freeThrowsPercentage 0.5
# leadChanges 5
# minutes PT120M00.00S
# minutesCalculated PT120M
# points 54
# pointsAgainst 48
# pointsFastBreak 5
# pointsFromTurnovers 4
# pointsInThePaint 30
# pointsInThePaintAttempted 21
# pointsInThePaintMade 15
# pointsInThePaintPercentage 0.714285714285714
# pointsSecondChance 1
# reboundsDefensive 16
# reboundsOffensive 1
# reboundsPersonal 17
# reboundsTeam 7
# reboundsTeamDefensive 1
# reboundsTeamOffensive 6
# reboundsTotal 24
# secondChancePointsAttempted 0
# secondChancePointsMade 0
# secondChancePointsPercentage 0.0
# steals 5
# threePointersAttempted 18
# threePointersMade 6
# threePointersPercentage 0.333333333333333
# timeLeading PT20M25.00S
# timesTied 3
# trueShootingAttempts 45.52
# trueShootingPercentage 0.593145869947276
# turnovers 7
# turnoversTeam 1
# turnoversTotal 8
# twoPointersAttempted 24
# twoPointersMade 16
# twoPointersPercentage 0.666666666666666
# ------------------------------


response = playbyplay.PlayByPlay(game_id="0022100733").get_response()
response = json.loads(response)

print(response['meta'])
# {'version': 1, 'code': 200, 'request': 'http://nba.cloud/games/0022100733/playbyplay?Format=json', 'time': '2022-01-27 20:43:54.220988'}

print(response['game']['gameId'])
# 0022100733

for i, _ in enumerate(response['game']['actions']):
    print(i, _)
# 0 {'actionNumber': 2, 'clock': 'PT12M00.00S', 'timeActual': '2022-01-28T00:35:41.7Z', 'period': 1, 'periodType': 'REGULAR', 'actionType': 'period', 'subType': 'start', 'qualifiers': [], 'personId': 0, 'x': None, 'y': None, 'possession'
# : 0, 'scoreHome': '0', 'scoreAway': '0', 'edited': '2022-01-28T00:35:41Z', 'orderNumber': 20000, 'xLegacy': None, 'yLegacy': None, 'isFieldGoal': 0, 'side': None, 'description': 'Period Start', 'personIdsFilter': []}
# 1 {'actionNumber': 4, 'clock': 'PT11M56.00S', 'timeActual': '2022-01-28T00:35:45.3Z', 'period': 1, 'periodType': 'REGULAR', 'teamId': 1610612755, 'teamTricode': 'PHI', 'actionType': 'jumpball', 'subType': 'recovered', 'descriptor': 'st
# artperiod', 'qualifiers': [], 'personId': 1627788, 'x': None, 'y': None, 'possession': 1610612755, 'scoreHome': '0', 'scoreAway': '0', 'edited': '2022-01-28T00:35:45Z', 'orderNumber': 40000, 'xLegacy': None, 'yLegacy': None, 'isFieldGo
# al': 0, 'jumpBallRecoveredName': 'F. Korkmaz', 'jumpBallRecoverdPersonId': 1627788, 'side': None, 'playerName': 'Korkmaz', 'playerNameI': 'F. Korkmaz', 'personIdsFilter': [1627788, 203954, 203076], 'jumpBallWonPlayerName': 'Embiid', 'j
# umpBallWonPersonId': 203954, 'description': 'Jump Ball J. Embiid vs. A. Davis: Tip to F. Korkmaz', 'jumpBallLostPlayerName': 'Davis', 'jumpBallLostPersonId': 203076}
# 2 {'actionNumber': 7, 'clock': 'PT11M43.00S', 'timeActual': '2022-01-28T00:35:58.2Z', 'period': 1, 'periodType': 'REGULAR', 'teamId': 1610612755, 'teamTricode': 'PHI', 'actionType': '2pt', 'subType': 'Layup', 'descriptor': 'driving', '
# qualifiers': ['pointsinthepaint'], 'personId': 203954, 'x': 7.703679369250986, 'y': 57.35294117647059, 'side': 'left', 'shotDistance': 4.18, 'possession': 1610612755, 'scoreHome': '0', 'scoreAway': '0', 'edited': '2022-01-28T00:36:02Z'
# , 'orderNumber': 70000, 'xLegacy': -37, 'yLegacy': 20, 'isFieldGoal': 1, 'shotResult': 'Missed', 'description': 'MISS J. Embiid driving Layup', 'playerName': 'Embiid', 'playerNameI': 'J. Embiid', 'personIdsFilter': [203954]}
# 3 {'actionNumber': 8, 'clock': 'PT11M40.00S', 'timeActual': '2022-01-28T00:36:01.2Z', 'period': 1, 'periodType': 'REGULAR', 'teamId': 1610612747, 'teamTricode': 'LAL', 'actionType': 'rebound', 'subType': 'defensive', 'qualifiers': [],
# 'personId': 203076, 'x': None, 'y': None, 'side': None, 'possession': 1610612747, 'scoreHome': '0', 'scoreAway': '0', 'edited': '2022-01-28T00:36:02Z', 'orderNumber': 80000, 'xLegacy': None, 'yLegacy': None, 'isFieldGoal': 0, 'shotActi
# onNumber': 7, 'reboundTotal': 1, 'reboundDefensiveTotal': 1, 'reboundOffensiveTotal': 0, 'description': 'A. Davis REBOUND (Off:0 Def:1)', 'playerName': 'Davis', 'playerNameI': 'A. Davis', 'personIdsFilter': [203076]}
# 4 {'actionNumber': 9, 'clock': 'PT11M23.00S', 'timeActual': '2022-01-28T00:36:17.7Z', 'period': 1, 'periodType': 'REGULAR', 'teamId': 1610612747, 'teamTricode': 'LAL', 'actionType': '3pt', 'subType': 'Jump Shot', 'descriptor': 'pullup'
# , 'qualifiers': [], 'personId': 1628370, 'x': 69.85873850197109, 'y': 77.94117647058823, 'side': 'right', 'shotDistance': 26.98, 'possession': 1610612747, 'scoreHome': '0', 'scoreAway': '0', 'edited': '2022-01-28T00:36:22Z', 'orderNumb
# er': 90000, 'xLegacy': 140, 'yLegacy': 231, 'isFieldGoal': 1, 'shotResult': 'Missed', 'description': "MISS M. Monk 26' pullup 3PT", 'playerName': 'Monk', 'playerNameI': 'M. Monk', 'personIdsFilter': [1628370]}
# 5 {'actionNumber': 10, 'clock': 'PT11M20.00S', 'timeActual': '2022-01-28T00:36:20.4Z', 'period': 1, 'periodType': 'REGULAR', 'teamId': 1610612747, 'teamTricode': 'LAL', 'actionType': 'rebound', 'subType': 'offensive', 'qualifiers': [],
#  'personId': 1626169, 'x': None, 'y': None, 'side': None, 'possession': 1610612747, 'scoreHome': '0', 'scoreAway': '0', 'edited': '2022-01-28T00:36:20Z', 'orderNumber': 100000, 'xLegacy': None, 'yLegacy': None, 'isFieldGoal': 0, 'shotA
# ctionNumber': 9, 'reboundTotal': 1, 'reboundDefensiveTotal': 0, 'reboundOffensiveTotal': 1, 'description': 'S. Johnson REBOUND (Off:1 Def:0)', 'playerName': 'Johnson', 'playerNameI': 'S. Johnson', 'personIdsFilter': [1626169]}


response = scoreboard.ScoreBoard().get_response()
response = json.loads(response)

print(response['meta'])
# {'version': 1, 'request': 'https://nba-prod-us-east-1-mediaops-stats.s3.amazonaws.com/NBA/liveData/scoreboard/todaysScoreboard_00.json', 'time': '2022-01-27 08:49:37.4937', 'code': 200}

print(response['scoreboard'].keys())
# dict_keys(['gameDate', 'leagueId', 'leagueName', 'games'])

for k, v in response['scoreboard'].items():
    if type(v) == str:
        print(k, v)
    elif type(v) == list:
        print(k)
        for i, _ in enumerate(v):
            print(i, _)

# gameDate 2022-01-27
# leagueId 00
# leagueName National Basketball Association
# games

# 0 {'gameId': '0022100733', 'gameCode': '20220127/LALPHI', 'gameStatus': 2, 'gameStatusText': 'Q3 06:49', 'period': 3, 'gameClock': 'PT06M49.00S', 'gameTimeUTC': '2022-01-28T00:30:00Z', 'gameEt': '2022-01-27T19:30:00-05:00', 'regulation
# Periods': 4, 'ifNecessary': False, 'seriesGameNumber': '', 'seriesText': '', 'homeTeam': {'teamId': 1610612755, 'teamName': '76ers', 'teamCity': 'Philadelphia', 'teamTricode': 'PHI', 'wins': 28, 'losses': 19, 'score': 67, 'seed': None,
#  'inBonus': '0', 'timeoutsRemaining': 6, 'periods': [{'period': 1, 'periodType': 'REGULAR', 'score': 32}, {'period': 2, 'periodType': 'REGULAR', 'score': 22}, {'period': 3, 'periodType': 'REGULAR', 'score': 13}, {'period': 4, 'periodTy
# pe': 'REGULAR', 'score': 0}]}, 'awayTeam': {'teamId': 1610612747, 'teamName': 'Lakers', 'teamCity': 'Los Angeles', 'teamTricode': 'LAL', 'wins': 24, 'losses': 24, 'score': 58, 'seed': None, 'inBonus': '0', 'timeoutsRemaining': 3, 'peri
# ods': [{'period': 1, 'periodType': 'REGULAR', 'score': 22}, {'period': 2, 'periodType': 'REGULAR', 'score': 26}, {'period': 3, 'periodType': 'REGULAR', 'score': 10}, {'period': 4, 'periodType': 'REGULAR', 'score': 0}]}, 'gameLeaders':
# {'homeLeaders': {'personId': 202699, 'name': 'Tobias Harris', 'jerseyNum': '12', 'position': 'F', 'teamTricode': 'PHI', 'playerSlug': 'tobias-harris', 'points': 14, 'rebounds': 4, 'assists': 3}, 'awayLeaders': {'personId': 203076, 'nam
# e': 'Anthony Davis', 'jerseyNum': '3', 'position': 'FC', 'teamTricode': 'LAL', 'playerSlug': 'anthony-davis', 'points': 27, 'rebounds': 7, 'assists': 0}}, 'pbOdds': {'team': None, 'odds': 0.0, 'suspended': 1}}

# 1 {'gameId': '0022100734', 'gameCode': '20220127/MINGSW', 'gameStatus': 1, 'gameStatusText': '10:00 pm ET', 'period': 0, 'gameClock': '', 'gameTimeUTC': '2022-01-28T03:00:00Z', 'gameEt': '2022-01-27T22:00:00Z', 'regulationPeriods': 4,
# 'ifNecessary': False, 'seriesGameNumber': '', 'seriesText': '', 'homeTeam': {'teamId': 1610612744, 'teamName': 'Warriors', 'teamCity': 'Golden State', 'teamTricode': 'GSW', 'wins': 35, 'losses': 13, 'score': 0, 'seed': None, 'inBonus':
#  None, 'timeoutsRemaining': 0, 'periods': [{'period': 1, 'periodType': 'REGULAR', 'score': 0}, {'period': 2, 'periodType': 'REGULAR', 'score': 0}, {'period': 3, 'periodType': 'REGULAR', 'score': 0}, {'period': 4, 'periodType': 'REGULAR
# ', 'score': 0}]}, 'awayTeam': {'teamId': 1610612750, 'teamName': 'Timberwolves', 'teamCity': 'Minnesota', 'teamTricode': 'MIN', 'wins': 24, 'losses': 23, 'score': 0, 'seed': None, 'inBonus': None, 'timeoutsRemaining': 0, 'periods': [{'
# period': 1, 'periodType': 'REGULAR', 'score': 0}, {'period': 2, 'periodType': 'REGULAR', 'score': 0}, {'period': 3, 'periodType': 'REGULAR', 'score': 0}, {'period': 4, 'periodType': 'REGULAR', 'score': 0}]}, 'gameLeaders': {'homeLeader
# s': {'personId': 0, 'name': '', 'jerseyNum': '', 'position': '', 'teamTricode': 'GSW', 'playerSlug': None, 'points': 0, 'rebounds': 0, 'assists': 0}, 'awayLeaders': {'personId': 0, 'name': '', 'jerseyNum': '', 'position': '', 'teamTric
# ode': 'MIN', 'playerSlug': None, 'points': 0, 'rebounds': 0, 'assists': 0}}, 'pbOdds': {'team': None, 'odds': 0.0, 'suspended': 1}}
