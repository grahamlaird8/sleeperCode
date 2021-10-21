import requests
from League import League
from Constants import *

class User:
    def __init__(self, userID, season=2021, leaguesToExclude=[]):
        self.userID = userID
        self.season = season
        self.leagueIDs = self.getLeaguesForUser(userID)
        self.leagues = []
        self.populateLeagues(leaguesToExclude)
        self.NUM_LEAGUES = len(self.leagues)
        self.ownerName = self.leagues[0].getTeamByOwnerID(self.userID).getTeamOwnerName()
        self.userStats = {}
        self.STATS_LIST = [WINS, EXPECTED_WINS, POINTS_FOR, POINTS_AGAINST]
        self.populateUserStats()

    def getLeaguesForUser(self, userID):
        leagueDictsList = requests.get(f"https://api.sleeper.app/v1/user/{userID}/leagues/nfl/{self.season}").json()
        leagueIDs = []
        for leagueDict in leagueDictsList:
            leagueIDs.append(leagueDict[LEAGUE_ID])
        return leagueIDs

    def populateLeagues(self, leaguesToExlude):
        for leagueID in self.leagueIDs:
            if leagueID not in leaguesToExlude:
                print(f"Parsing league {leagueID}\n")
                try:
                    self.leagues.append(League(leagueID))
                except:
                    print(f"Failed to parse league with id: {leagueID}\n")

    def populateUserStats(self):
        newUserStats = {}
        newUserStats[LEAGUE_COUNT] = len(self.leagues)
        for stat in self.STATS_LIST:
            newUserStats[stat] = 0

        for league in self.leagues:
            leagueTeamStats = league.getStatsForTeam(self.userID)
            # print(leagueTeamStats)
            for stat in self.STATS_LIST:
                newUserStats[stat] += leagueTeamStats[stat]

        # print(newUserStats)
        for stat in self.STATS_LIST:
            newUserStats[stat] = round(newUserStats[stat], 2)
        # print(newUserStats)

        newUserStats[AVG_WINS] = round(newUserStats[WINS]/self.NUM_LEAGUES, 2)
        newUserStats[AVG_WIN_PERCENTAGE] = round(newUserStats[WINS]/self.NUM_LEAGUES/(MAX_WEEK-START_WEEK+1), 3)
        newUserStats[AVG_EWINS] = round(newUserStats[EXPECTED_WINS]/self.NUM_LEAGUES, 2)
        newUserStats[AVG_EWIN_PERCENTAGE] = round(newUserStats[EXPECTED_WINS]/self.NUM_LEAGUES/(MAX_WEEK-START_WEEK+1), 3)

        # print(newUserStats)
        self.userStats = newUserStats

    def printAllStats(self):
        print(f"User Stats for {self.ownerName}:")
        for stat in self.userStats.keys():
            print(f"{stat}: {self.userStats[stat]}")
        print()
