from User import User
from League import League
from Constants import *

#This file gets the overall stats of everyone in a specified league.

league = League("707439851250753536")

users = []
leaguesToExclude = ["738213643656859648", "731348161871876096", "733032950685364224","737622887200120832"]

# declan = User("587035242359988224", leaguesToExclude=leaguesToExclude)
# declan.printAllStats()

# graham = User("499393148506599424", leaguesToExclude=leaguesToExclude)
# graham.printAllStats()



for i in range(1, league.NUM_PLAYERS + 1):
    curUserID = league.getTeamByRosterID(i).getUserID()
    print(f"User ID: {curUserID}\n")
    users.append(User(curUserID, leaguesToExclude=leaguesToExclude))

for user in users:
    user.printAllStats()
