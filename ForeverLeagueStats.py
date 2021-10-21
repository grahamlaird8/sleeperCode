from Constants import *
from League import League

league = League("737622887200120832")
# league.printTeams()
league.printMatchupsBetweenWeeks(START_WEEK, MAX_WEEK)

league.printExpectedWinsGraphic()
