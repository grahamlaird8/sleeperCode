from Constants import *
from Team import Team
import League

class Matchup:
    def __init__(self, matchupData, league):
        team1Data = matchupData[0]
        team2Data = matchupData[1]
        self.team1Score = team1Data[POINTS]
        self.team2Score = team2Data[POINTS]
        # print(team1Data)
        # print(team1Data[ROSTER_ID])
        self.team1 = league.getTeamByRosterID(team1Data[ROSTER_ID])
        self.team2 = league.getTeamByRosterID(team2Data[ROSTER_ID])
        # print(team2Data[ROSTER_ID])
        # print(self.team1)
        # print(self.team2)

    def __str__(self):
        return f"{self.team1.getTeamOwnerName()} {self.team1Score} - {self.team2Score} {self.team2.getTeamOwnerName()}"
