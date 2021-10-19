import json

from Constants import *
import requests
from Team import Team
from Matchup import Matchup
from LeagueTeam import LeagueTeam

class League:

    def __init__(self, leagueID):
        self.BASE_URL = f"https://api.sleeper.app/v1/league/{leagueID}/"
        self.teams = None
        self.leagueTeams = None
        self.populateTeams()
        self.NUM_PLAYERS = round(len(self.teams))
        self.populateLeagueTeams()
        self.teamStats = None
        self.populateTeamStats()

    def populateTeams(self):
        teamsData = self.getFullTeamData()
        self.teams = []
        for i in range(len(teamsData)):
            curTeamData = teamsData[i]
            self.teams.append(Team(curTeamData))

    def populateLeagueTeams(self):
        self.leagueTeams = []
        for team in self.teams:
            self.leagueTeams.append(LeagueTeam(self, team))

    def getFullTeamData(self):
        print("Getting full team data...\n")
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
            item[WEEK] = week
            matchupID = item[MATCHUP_ID]
            matchupIDDict[matchupID].append(item)

        return [Matchup(matchupData, self) for matchupData in matchupIDDict.values()]

    def getMatchupsBetweenWeeks(self, start, end):
        weekMatchupDict = {}
        for i in range(start, end + 1):
            weekMatchupDict[i] = self.getMatchupsByWeek(i)
        return weekMatchupDict

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

    def populateTeamStats(self):
        print("Populating team stats...\n")
        self.teamStats = {}
        for leagueTeam in self.leagueTeams:
            curTeamStats = {}
            curTeamStats[WINS] = leagueTeam.wins
            curTeamStats[POINTS_FOR] = leagueTeam.totalPointsScored
            curTeamStats[POINTS_AGAINST] = leagueTeam.totalPointsAgainst
            self.teamStats[leagueTeam.team.teamOwnerName] = curTeamStats

        for curLeagueTeam in self.leagueTeams:
            expectedWins = 0
            curScores = curLeagueTeam.scores
            for otherLeagueTeam in self.leagueTeams:
                if curLeagueTeam.team == otherLeagueTeam.team:
                    continue
                otherScores = otherLeagueTeam.scores
                for week in curScores.keys():
                    if curScores[week][POINTS_FOR] > otherScores[week][POINTS_FOR]:
                        expectedWins += 1

            self.teamStats[curLeagueTeam.team.teamOwnerName][EXPECTED_WINS] = round(expectedWins/(self.NUM_PLAYERS - 1), 2)

    def printExpectedWins(self):
        for teamOwner in self.teamStats.keys():
            # print(f"{teamOwner}: {self.teamStats[teamOwner][POINTS_FOR]} - {self.teamStats[teamOwner][POINTS_AGAINST]}")
            expWins = self.teamStats[teamOwner][EXPECTED_WINS]
            teamWins = self.teamStats[teamOwner][WINS]
            winDiff = round(teamWins - expWins, 2)
            print(f"{teamOwner}: Wins: {teamWins} Exp Wins: {expWins} ({winDiff})")
