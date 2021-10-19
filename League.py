import json

from Constants import *
import requests
from Team import Team
from Matchup import Matchup

class League:

    def __init__(self, leagueID):
        self.BASE_URL = f"https://api.sleeper.app/v1/league/{leagueID}/"

        self.teams = None
        self.populateTeams()

        self.NUM_PLAYERS = round(len(self.teams))

    def populateTeams(self):
        teamsData = self.getFullTeamData()
        self.teams = []
        for i in range(len(teamsData)):
            curTeamData = teamsData[i]
            self.teams.append(Team(curTeamData))

    def getFullTeamData(self):
        teamsData = requests.get(f"{self.BASE_URL}users").json()
        rostersData = requests.get(f"{self.BASE_URL}rosters").json()
        for curRosterData in rostersData:
            for curTeamData in teamsData:
                if curRosterData[OWNER_ID] == curTeamData[USER_ID]:
                    for rosterKey in curRosterData.keys():
                        if rosterKey not in curTeamData.keys():
                            curTeamData[rosterKey] = curRosterData[rosterKey]
                        else:
                            curTeamData[f"{ROSTER_REPEAT_PREFIX}{rosterKey}"] = curRosterData[rosterKey]
        # print(teamsData)
        return teamsData

    def printTeams(self):
        for team in self.teams:
            print(team)
        print()

    def getMatchupsByWeek(self, week):
        weekMatchupData = requests.get(f"{self.BASE_URL}{MATCHUPS}/{week}").json()
        matchupIDDict = {}

        for i in range(1, self.NUM_PLAYERS // 2 + 1):
            matchupIDDict[i] = []

        for item in weekMatchupData:
            matchupID = item[MATCHUP_ID]
            matchupIDDict[matchupID].append(item)

        return [Matchup(matchupData, self) for matchupData in matchupIDDict.values()]

    def getMatchupsByWeeks(self, weeks):
        weekMatchupDict = {}
        for week in weeks:
            weekMatchupDict[week] = self.getMatchupsByWeek(week)
        return weekMatchupDict

    def printMatchupsByWeek(self, week):
        matchups = self.getMatchupsByWeek(week)
        print(f"Week {week} Scores:")
        for matchup in matchups:
            print(matchup)

    def printMatchupsBetweenWeeks(self, startWeek, endWeek):
        for i in range(startWeek, endWeek + 1):
            self.printMatchupsByWeek(i)
            print()

    def printMatchupsByWeeks(self, weeks):
        for week in weeks:
            self.printMatchupsByWeek(week)
            print()

    def getTeamByRosterID(self, rosterID):
        curTeam = None
        for team in self.teams:
            if rosterID == team.getRosterID():
                curTeam = team
        # print(f"{rosterID}: {curTeam}\n")
        return curTeam