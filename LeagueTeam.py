from Constants import *

class LeagueTeam:
    def __init__(self, league, team):
        self.league = league
        self.team = team
        self.scores = {}
        self.populateScores()
        self.wins = 0
        self.setWins()
        self.totalPointsScored = 0
        self.setTotalPointsScored()
        self.totalPointsAgainst = 0
        self.setTotalPointsAgainst()

    def populateScores(self):
        self.totalPoints = 0
        matchupsWeeks = self.league.getMatchupsBetweenWeeks(START_WEEK, MAX_WEEK)
        for week in matchupsWeeks.keys():
            for matchup in matchupsWeeks[week]:
                if matchup.team1 == self.team:
                    self.scores[week] = {POINTS_FOR: matchup.team1Score, POINTS_AGAINST: matchup.team2Score}
                elif matchup.team2 == self.team:
                    self.scores[week] = {POINTS_FOR: matchup.team2Score, POINTS_AGAINST: matchup.team1Score}

    def setWins(self):
        for item in self.scores.values():
            if item[POINTS_FOR] > item[POINTS_AGAINST]:
                self.wins += 1

    def setTotalPointsScored(self):
        self.totalPointsScored = 0
        for score in self.scores.values():
            self.totalPointsScored += score[POINTS_FOR]
        self.totalPointsScored = round(self.totalPointsScored, 2)

    def setTotalPointsAgainst(self):
        self.totalPointsAgainst = 0
        for score in self.scores.values():
            self.totalPointsAgainst += score[POINTS_AGAINST]
        self.totalPointsAgainst = round(self.totalPointsAgainst, 2)
