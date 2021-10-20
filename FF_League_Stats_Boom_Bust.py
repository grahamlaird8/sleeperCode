import json
from sleeper_wrapper import League
from sleeper_wrapper import Stats
from collections import defaultdict

#Defining Variables and Allocating Arrays
id1 = 'Certified Lover Boyd'
id2 = 'Lions fan'
id3 = 'Beats by Ray'
id4 = 'PlayMeInRL'
id5 = 'The Will of D/ST'
id6 = 'Fournettecation'
id7 = 'The Injury Reserve'
id8 = "Call Me If You Get Moss'd"
id9 = 'GB Cheesers'
id10 = 'williams and co.'
numTeams = 10
numWeeks = 6
nameArray = [id1, id2, id3, id4, id5, id6, id7, id8, id9, id10]
league_id = "707439851250753536"
league = League(league_id)
rosters = league.get_rosters()
users = league.get_users()
avgPoints = [0] * numTeams
scores= [0] * numTeams
matchupID = [0] * numTeams
id = [0] * numTeams
scoreDiff = [0] * numTeams
scoreDiffOpp = [0] * numTeams
totalAganistAvg = [0] * numTeams
totalAganistAvg = dict(zip(nameArray,totalAganistAvg))
#Uses the Sleeper API to gets the points every team
#has scored and then average it out
for i in range(0, numTeams ):
    avgPoints[i] = (rosters[i]['settings']['fpts'] +
    rosters[i]['settings']['fpts_decimal']/100 )/numWeeks
teamDataDictAvg = dict(zip(nameArray,avgPoints))
#A loop that runs through every week that has been fully played
for i in range(1, numWeeks + 1):
    #uses the sleeper API to get the matchup ID and score for every players
    matchups = league.get_matchups(i)
    for j in range(0, len(users)):
        scores[j] = ((matchups[j])['points'])
    for j in range(0, len(users)):
        matchupID[j] = ((matchups[j])['matchup_id'])
    #Creats a dictonary where the key is the team name and the
    #values are in order matchupID points scored this week,
    #average point for the season
    teamDataDictScores = dict(zip(nameArray,scores))
    teamDataDictMatchupID = dict(zip(nameArray,matchupID))
    teamDataDict = defaultdict(list)
    for d in (teamDataDictMatchupID, teamDataDictScores, teamDataDictAvg):
        for key, value in d.items():
            teamDataDict[key].append(value)
    #Calculating a teams preformance against the same teams average
    k = 0;
    for key in teamDataDict:
        scoreDiff[k] = float(teamDataDict[key][1]) - float(teamDataDict[key][2])
        k = k + 1
    #Creates a dictonary where the key is the teams name and the value is
    #the same teams difference between the weeks preformance and the same teams
    #average
    teamDataDictDiffAvg = dict(zip(nameArray,scoreDiff))
    teamDataDictAvgID = defaultdict(list)
    #Creates a dictonary where the key is the team name and the values are a
    #list in the order of member id then points against the average
    for d in (teamDataDictMatchupID, teamDataDictDiffAvg):
        for key, value in d.items():
            teamDataDictAvgID[key].append(value)
    #adds the opposing teams difference difference between the weeks preformance
    #and the opposing teams average to the main dictonary after main teams
    #average
    for key in teamDataDictDiffAvg:
        for key1 in teamDataDict:
            if ((key != key1) and (teamDataDictAvgID[key][0] ==
            teamDataDict[key1][0])):
                teamDataDict[key1].append(teamDataDictAvgID[key][1])
    #Adds the opposing teams difference difference between the weeks preformance
    #and the opposing teams average to a running total for each team
    for key in totalAganistAvg:
        totalAganistAvg[key] = totalAganistAvg[key] + teamDataDict[key][3]

#Sorts it running total in terms of lowest points against the average (Luckeist)
#to most points against the average (unluckiest)
totalAganistAvg = dict(sorted(totalAganistAvg.items(), key=lambda item: item[1]))
print(totalAganistAvg)
#test
