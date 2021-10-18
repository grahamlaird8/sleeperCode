import ast

import requests
import json

def apiCall():
    pointsGameWeek = 0
    avgOppScore = 0
    totalScoreOpp = 0
    totalOppScores = 0
    totalPointsVsMe = 0
    # Use a breakpoint in the code line below to debug your script.
    curWeek = 6
    for i in range(1, curWeek + 1):
        result = requests.get("https://api.sleeper.app/v1/league/707439851250753536/matchups/" + str(i)).json()
        # print(json.dumps(result, indent=4, sort_keys=True))
        for obj in result:
            # print(obj)
            #my team is roster id 1 according to api
             if obj.get("roster_id") == 1:
                matchupID = obj.get("matchup_id")
                # print(matchupID)

        for obj2 in result:
            if obj2.get("matchup_id") == matchupID and obj2.get("roster_id") != 1:
                rosterID = obj2.get("roster_id")
                # print(rosterID)
                pointsGameWeek = obj2.get("points")
                # print(pointsGameWeek)
                for j in range(1, curWeek+1):
                    result2 = requests.get("https://api.sleeper.app/v1/league/707439851250753536/matchups/" + str(j)).json()
                    for obj3 in result2:
                        if obj3.get("roster_id") == rosterID and j != i:
                            # print(float(obj3.get("points")))
                            totalScoreOpp += float(obj3.get("points"))
                    # print(totalScoreOpp)
                    # print(curWeek-1)
                    avgOppScore = totalScoreOpp / (curWeek-1)
                    # print(avgOppScore)
                totalScoreOpp = 0
                # print("Average opp score: " + str(avgOppScore))
        print("The average score the player I faced in week " + str(i) + " is " + str(avgOppScore) + " (not including vs me) and their score vs me was " + str(pointsGameWeek))
        totalOppScores += avgOppScore
        # print(totalOppScores)
        totalPointsVsMe += pointsGameWeek
        i += 1
        avgOppScore = 0

        pointsGameWeek = 0




    result = requests.get("https://api.sleeper.app/v1/league/707439851250753536/matchups/" + str(curWeek))
    # parsed = json.loads(result.json())
    # print(json.dumps(result.json(), indent=4, sort_keys=True))
    # print(parsed)
    avgOppScores = totalOppScores / curWeek
    # print(avgOppScores)
    totalAvgVsMe = totalPointsVsMe / curWeek
    # print(totalAvgVsMe)

    print("\nOn average, my opponents outscored their average points by " + str(totalAvgVsMe - avgOppScores) + " points")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    apiCall()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
