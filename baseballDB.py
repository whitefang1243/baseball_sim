import csv
import predict
import team
import copy
import mysql.connector
import datetime


#connecting to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aa531491",
    database = "test"
)

# TODO  allow for multiple seasons and grabbing odds from an arbitrary date

YEAR = 2014                 #the year we are interested in
mycursor = mydb.cursor()

#grabs games from table
def importGames():
    mycursor.execute("SELECT * FROM t" + str(YEAR))
    myresult = mycursor.fetchall()
    return myresult

#initialize team objects inside the dictionary
#last two parameters are the league and division
def initializeTeams():
    teamDict = dict([])
    teamDict["STL"] = team.Team("STL", 0, 0, 0, 0, 0, 1, 1)
    teamDict["TOR"] = team.Team("TOR", 0, 0, 0, 0, 0, 0, 0)
    teamDict["NYM"] = team.Team("NYM", 0, 0, 0, 0, 0, 1, 0)
    teamDict["SFG"] = team.Team("SFG", 0, 0, 0, 0, 0, 1, 2)
    teamDict["MIN"] = team.Team("MIN", 0, 0, 0, 0, 0, 0, 1)
    teamDict["SEA"] = team.Team("SEA", 0, 0, 0, 0, 0, 0, 2)
    teamDict["PHI"] = team.Team("PHI", 0, 0, 0, 0, 0, 1, 0)
    teamDict["WSN"] = team.Team("WSN", 0, 0, 0, 0, 0, 1, 0)
    teamDict["LAD"] = team.Team("LAD", 0, 0, 0, 0, 0, 1, 2)
    teamDict["COL"] = team.Team("COL", 0, 0, 0, 0, 0, 1, 2)
    teamDict["CHC"] = team.Team("CHC", 0, 0, 0, 0, 0, 1, 1)
    teamDict["CHW"] = team.Team("CHW", 0, 0, 0, 0, 0, 0, 1)
    teamDict["HOU"] = team.Team("HOU", 0, 0, 0, 0, 0, 0, 2)
    teamDict["BOS"] = team.Team("BOS", 0, 0, 0, 0, 0, 0, 0)
    teamDict["DET"] = team.Team("DET", 0, 0, 0, 0, 0, 0, 1)
    teamDict["PIT"] = team.Team("PIT", 0, 0, 0, 0, 0, 1, 1)
    teamDict["TBR"] = team.Team("TBR", 0, 0, 0, 0, 0, 0, 0)
    teamDict["KCR"] = team.Team("KCR", 0, 0, 0, 0, 0, 0, 1)
    teamDict["MIL"] = team.Team("MIL", 0, 0, 0, 0, 0, 1, 1)
    teamDict["BAL"] = team.Team("BAL", 0, 0, 0, 0, 0, 0, 0)
    teamDict["TEX"] = team.Team("TEX", 0, 0, 0, 0, 0, 0, 2)
    teamDict["CIN"] = team.Team("CIN", 0, 0, 0, 0, 0, 1, 1)
    teamDict["ATL"] = team.Team("ATL", 0, 0, 0, 0, 0, 1, 0)
    teamDict["SDP"] = team.Team("SDP", 0, 0, 0, 0, 0, 1, 2)
    teamDict["ARI"] = team.Team("ARI", 0, 0, 0, 0, 0, 1, 2)
    teamDict["LAA"] = team.Team("LAA", 0, 0, 0, 0, 0, 0, 2)
    teamDict["OAK"] = team.Team("OAK", 0, 0, 0, 0, 0, 0, 2)
    teamDict["NYY"] = team.Team("NYY", 0, 0, 0, 0, 0, 0, 0)
    teamDict["CLE"] = team.Team("CLE", 0, 0, 0, 0, 0, 0, 1)
    teamDict["MIA"] = team.Team("MIA", 0, 0, 0, 0, 0, 1, 0)
    #printResults(list(teamDict.values()))
    
    return teamDict

def printResults(teamList):
    teamList.sort(key=lambda x: (x.points, (x.GF-x.GA), x.GF), reverse=True)
    for i in range (0,len(teamList)):
        print(teamList[i])

def handleSchedule(games,tDict, unfinished):
    print(datetime.datetime.now().strftime('\nStandings estimations as of %m/%d/%Y \n'))
    for i in range(0, len(games)):      #go through all games
        if games[i][-2]!='@':           #to avoid double counting, we only look at away games ("@" is shorter than "Home")
            continue
        if games[i][4]==games[i][5]:    #append uncompleted games to the list of games to be sim
            unfinished.append(games[i])
            continue

        #otherwise, we record the result of each game and the runs for each team
        teamA = games[i][1]
        teamB = games[i][2]
        AScore = int(games[i][4])
        BScore = int(games[i][5])

        #we gotta check score directly instead of the "results" column, bc W/L symbols are weird and I don't want to clean it
        if AScore>BScore:
            tDict[teamA].wins+=1
            tDict[teamB].losses+=1
        elif AScore<BScore:
            tDict[teamB].wins+=1
            tDict[teamA].losses+=1
        #update runs scored/surrendered
        tDict[teamA].GF+=AScore
        tDict[teamB].GF+=BScore
        tDict[teamA].GA+=BScore
        tDict[teamB].GA+=AScore
        
        #update function lets us consolidate the update of certain counting stats (eg. total games played, points scored)
        tDict[teamA].update()
        tDict[teamB].update()

def handleScheduleWithDate(games,tDict, unfinished, date):
    print(date.strftime('\nStandings estimations after %m/%d/%Y \n'))
    for i in range(0, len(games)):      #go through all games
        if games[i][-2]!='@':           #to avoid double counting, we only look at away games ("@" is shorter than "Home")
            continue
        if games[i][4]==games[i][5] or games[i][0]>date:    #also check for games after specified date
            unfinished.append(games[i])
            continue

        #otherwise, we record the result of each game and the runs for each team
        teamA = games[i][1]
        teamB = games[i][2]
        AScore = int(games[i][4])
        BScore = int(games[i][5])

        #we gotta check score directly instead of the "results" column, bc W/L symbols are weird and I don't want to clean it
        if AScore>BScore:
            tDict[teamA].wins+=1
            tDict[teamB].losses+=1
        elif AScore<BScore:
            tDict[teamB].wins+=1
            tDict[teamA].losses+=1
        #update runs scored/surrendered
        tDict[teamA].GF+=AScore
        tDict[teamB].GF+=BScore
        tDict[teamA].GA+=BScore
        tDict[teamB].GA+=AScore
        
        #update function lets us consolidate the update of certain counting stats (eg. total games played, points scored)
        tDict[teamA].update()
        tDict[teamB].update()   


def runSim(games, tDict):   #simulation function using poisson distribution
    teamDict = copy.deepcopy(tDict)
    for i in range(len(games)):                     #for all of the remaining games, simulate
        nameA = games[i][1]
        nameB = games[i][2]
        teamA = teamDict[nameA]                     #this is inefficient, but prevents me from having to retype teamDict
        teamB = teamDict[nameB]
        while True:                                 #need to handle ties, bc the function was originally made for soccer
            result = predict.h2hV2(teamA, teamB)
            if result==1:
                teamA.wins+=1
                teamB.losses+=1
                break
            elif result==-1:
                teamB.wins+=1
                teamA.losses+=1
                break
        teamA.update()
        teamB.update()
        teamDict[nameA] = teamA
        teamDict[nameB] = teamB
    return teamDict

def main(games, tDict, n, date):
    unfinished = []     #games to be simulated
    #print(games[0])
    if date is None:
        handleSchedule(games,tDict,unfinished)
    else:
        handleScheduleWithDate(games,tDict,unfinished,date)

    #following portion is just for simulating games and recording who makes the playoffs in each sim
    for i in range (0, n):
        teamDict = runSim(unfinished, tDict)
        sortedList = list(teamDict.values())            #sort list of teams after sim (needed for playoffs)
        sortedList.sort(key=lambda x: (x.points, (x.GF-x.GA), x.GF), reverse=True)      #sort by wins, run difference, then runs
        for j in range(0, len(sortedList)):                     #for each team, record their result, update best/worst, wins, losses, etc
            name = sortedList[j].name                           #get the name, use it to get result from dict
            tDict[name].position+=j+1
            tDict[name].worst = max(tDict[name].worst, j+1)
            tDict[name].best = min(tDict[name].best, j+1)
            tDict[name].tWins += teamDict[name].wins
            tDict[name].tLoss += teamDict[name].losses

        for j in range(0, 2):           #this section is for playoffs, run this loop once per league
            count = [0,0,0,0]           # we need to keep track of division winners and wildcards for each league
            #note this section technically does not follow the proper tiebreaker rules, 
            #but even I don't understand them, so I'll pretend they don't exist
            for k in range(0, len(sortedList)):
                name = sortedList[k].name                
                if sum(count)>5:                #if we already have all 5 playoff teams, break
                    break
                if teamDict[name].league!=j:            #if wrong league, continue
                    continue
                if count[teamDict[name].division]==0:   #if no division winner so far, set as winner
                    count[teamDict[name].division]+=1
                    tDict[name].winDiv+=1
                elif count[3]<3:                        #else if not all wildcards have been filled, set as wildcard
                    count[3]+=1
                    tDict[name].WC+=1

    #printing the results in a (somewhat) neat and legible table
    sortedList = list(tDict.values())
    sortedList.sort(key=lambda x: (x.position/n))
    print("name".ljust(8) + " " + 
          str("avgWins").ljust(8) + " " + 
          str("avgLoss").ljust(8) + " " + 
          str("best").ljust(8) + " " + 
          str("worst").ljust(8) + " " + 
          str("winDiv%").ljust(8) + " " + 
          str("Playoff%").ljust(8) + " "
          )
    for j in range(0, len(sortedList)):
        print(sortedList[j].name.ljust(8) + " " + 
              str(round(sortedList[j].tWins/n,2)).ljust(8) + " " + 
              str(round(sortedList[j].tLoss/n,2)).ljust(8) + " " + 
              str(sortedList[j].best).ljust(8) + " " + 
              str(sortedList[j].worst).ljust(8) + " " + 
              str(round(sortedList[j].winDiv/n*100,2)).ljust(8) + " " + 
              str(round((sortedList[j].winDiv/n*100 + sortedList[j].WC/n*100),2)).ljust(8) + " "
              )


def oneGame(games, tDict, n, a, b):
    handleSchedule(games,tDict, [])     #we don't need the unfinished games thing, so just leave it like this

    winLoss = [0,0]
    avgRuns = [0,0]
    allGames = [[],[]]

    #this section is largely the same as the runSim function, but we actually care about the runs scored by each side
    for i in range(0, n):
        nameA = a
        nameB = b
        teamA = tDict[nameA]
        teamB = tDict[nameB]
        while True:
            result = predict.h2hRuns(teamA, teamB)
            if result[0]!=result[1]:
                break
        allGames[0].append(result[0])
        allGames[1].append(result[1])
        if result[0]>result[1]:
            winLoss[0]+=1
        else:
            winLoss[-1]+=1
        avgRuns[0]+=result[0]
        avgRuns[1]+=result[1]

    #average runs per game
    avgRuns[0] = avgRuns[0]/n
    avgRuns[1] = avgRuns[1]/n
    allGames[0].sort()
    allGames[1].sort()
    print(allGames[0][len(allGames[0])//2], allGames[1][len(allGames[1])//2])
    print(winLoss)
    print(avgRuns)
    
    print("Verification")       #make sure the result makes sense by testing it against itself essentially
    
    res = [0,0]
    for i in range(0, n):
        nameA = a
        nameB = b
        teamA = tDict[nameA]
        teamB = tDict[nameB]
        while True:
            result = predict.h2hV2(teamA, teamB)
            if result==1:
                res[0]+=1
                break
            elif result==-1:
                res[1]+=1
                break
    print(res)
    


#oneGame(importGames(), initializeTeams(), 1000, "CHW", "BAL")

#main(importGames(), initializeTeams(), 1000, None)
datetime.date(2024, 3, 28)
main(importGames(), initializeTeams(), 1000, datetime.date(YEAR, 5, 28))
