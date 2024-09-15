import team
from numpy import random


EXPONENT = 2
TIE_PERCENT = 0.23


def pythRecord(goalsScored, goalsAllowed):
    return 1/(1+(goalsAllowed/goalsScored)**EXPONENT)

def predictWinner(WPa, WPb):
    return (WPa*(1-WPb))/(WPa*(1-WPb)+WPb*(1-WPa))

def checkTie():
    check = random.random()
    if check < TIE_PERCENT:
        return True
    return False

def h2h(teamA: team.Team, teamB: team.Team):        #obsolete function using pythagorean record, here for comparison purposes
    WPa = pythRecord(teamA.GF, teamA.GA)
    WPb = pythRecord(teamB.GF, teamB.GA)
    prediction = predictWinner(WPa, WPb)
    if checkTie():
        return 0
    check = random.random()
    if check <= prediction:
        return 1
    return -1

#assume that the points scored by each team can be represented using a poisson distribution
def h2hV2(teamA: team.Team, teamB: team.Team):  #we average the runs scored per game by one team and the runs allowed by the other to get the former's runs scored
    goalsA = random.poisson(((teamA.GF/teamA.games)+(teamB.GA/teamB.games))/2)
    goalsB = random.poisson(((teamB.GF/teamB.games)+(teamA.GA/teamA.games))/2)
    if goalsA==goalsB:                          #relevant if we use this function for soccer; otherwise, we ignore it
        return 0
    #check = random.random()
    if goalsA>goalsB:
        return 1
    return -1    


#this is similar to above, but we return an actual score instead of just a value representing the result
def h2hRuns(teamA: team.Team, teamB: team.Team):
    goalsA = random.poisson(((teamA.GF/teamA.games)+(teamB.GA/teamB.games))/2)
    goalsB = random.poisson(((teamB.GF/teamB.games)+(teamA.GA/teamA.games))/2)
    return [goalsA, goalsB]  

#debug function
def h2hVerify(teamAGoals, teamBGoals):
    goalsA = random.poisson(teamAGoals)
    goalsB = random.poisson(teamBGoals)
    if goalsA==goalsB:
        return 0
    check = random.random()
    if goalsA>goalsB:
        return 1
    return -1

def test():
    teamA = team.Team("Man City", 26, 4, 4, 89, 31)
    teamB = team.Team("Arsenal", 25, 6, 4, 83, 39)  
    
    print(pythRecord(teamA.GF, teamA.GA))
    print(pythRecord(teamB.GF, teamB.GA))
    
    win = 0
    draw = 0
    loss = 0
    
    for i in range (0,1000):
        result = h2h(teamA, teamB)
        if result==1:
            win+=1
        elif result==-1:
            loss+=1
        else:
            draw+=1
    print (win, draw, loss)
    
    win = 0
    draw = 0
    loss = 0

    for i in range (0,1000):
        result = h2hV2(teamA, teamB)
        if result==1:
            win+=1
        elif result==-1:
            loss+=1
        else:
            draw+=1
    print (win, draw, loss)    
    
#test()
    
    
    

