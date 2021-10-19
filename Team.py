from Constants import *

class Team:
    def __init__(self, teamData):
        # print(teamData)
        self.userID = teamData[USER_ID]
        self.rosterID = teamData[ROSTER_ID]
        teamMetadata = teamData[METADATA]
        self.teamName = teamMetadata[TEAM_NAME]
        self.teamOwnerName = teamData[DISPLAY_NAME]

    def __str__(self):
        return f"Team Owner: {self.teamOwnerName} | Team ID: {self.userID} | Team Name: {self.teamName}"

    def getUserID(self):
        return self.userID

    def getRosterID(self):
        return self.rosterID

    def getTeamName(self):
        return self.teamName

    def getTeamOwnerName(self):
        return self.teamOwnerName
