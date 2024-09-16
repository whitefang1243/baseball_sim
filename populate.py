import mysql.connector
import scrape
import numpy as np


#I have no idea why this is in the order this is in, it just is
#in the future, may need a way to unhardcode this to account for changing abbrevations/team numbers
#eg. OAK may be changing to LVA or SAC in the next few seasons (FJF, FRM)
teams = ['STL', 'TOR', 'NYM', 'SFG', 'MIN', 'SEA', 'PHI', 'WSN', 'LAD', 'COL', 'CHC', 'CHW', 'HOU', 'BOS', 'DET', 'PIT', 'TBR', 'KCR', 'MIL', 'BAL', 'TEX', 'CIN', 'ATL', 'SDP', 'ARI', 'LAA', 'OAK', 'NYY', 'CLE', 'MIA']

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Aa531491",
  database = "test"
)
YEAR = 2020                 #year we are loading/updating
CURRENT = 2024              #current year
mycursor = mydb.cursor()

#we need to check if the table for this season exists already
sql = "SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = 'test') AND (TABLE_NAME = 't" + str(YEAR) + "')"
mycursor.execute(sql)
for x in mycursor:
    print(x[0])
    if x[0]>0:
        if YEAR!=CURRENT:                                   #if a table for this season exists, and the season is not the active season, check if it is populated
            sql = "SELECT COUNT(*) FROM t" + str(YEAR)      #jank, but idk how to fix this
            mycursor.execute(sql)
            count = mycursor.fetchone()[0]
            if count>0:                                     #if populated, kill the program 
                print("Season has already been loaded, terminating program")    #TODO:  add a way to override this whole check
                exit()
        sql = "DELETE FROM `t" + str(YEAR) + "`"
        mycursor.execute(sql)
        mydb.commit()
    else:                                                   #if table does not exist, create table based on t2024 (current season)
        sql = "CREATE TABLE t" + str(YEAR) + " LIKE t2024"
        mycursor.execute(sql)
        mydb.commit()

#blank the table before loading new stuff
#TODO: add a way to backup this table before deleting it
arr = scrape.main(YEAR, True)                   #we do the scrape before the delete just in case
sql = "DELETE FROM `t" + str(YEAR) + "`"
mycursor.execute(sql)
mydb.commit()

#load table from scraped data
for i in range(0, len(arr)):
    streak = 0                          #aka: how to quantify how terrible the white sox are
    for j in range(0, len(arr[i])):
        #print(arr[i][j])
        sql = "INSERT INTO `t" + str(YEAR) + "` (date, team, opponent, result, runs, runsAllowed, gameNo, HA, Streak) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        if np.isnan(arr[i][j][5]):
            val = (arr[i][j][0], arr[i][j][1], arr[i][j][3], arr[i][j][4], 0, 0, j, arr[i][j][2], 0)     
        else:
            if j==0:
                streak = 1 
            else:                               #streak is done by comparing current result to the previous one
                if arr[i][j][5]>arr[i][j][6]:   #once again, we need to check score manually bc results column is weird
                    if arr[i][j-1][5]>arr[i][j-1][6]:
                        streak += 1
                    else:
                        streak = 1
                if arr[i][j][5]<arr[i][j][6]:
                    if arr[i][j-1][5]<arr[i][j-1][6]:
                        streak += 1
                    else:
                        streak = 1
            val = (arr[i][j][0], arr[i][j][1], arr[i][j][3], arr[i][j][4], int(arr[i][j][5]), int(arr[i][j][6]), j, arr[i][j][2], streak)
        mycursor.execute(sql, val)
        mydb.commit()


#this is just here to verify if everything is correct
for i in range(0, len(teams)):
    sql = "SELECT COUNT(*) FROM `t" + str(YEAR) + "` WHERE (team=%s or opponent=%s) and HA='@'"
    val = (teams[i], teams[i])
    mycursor.execute(sql, val)
    for x in mycursor:
        print(teams[i], x)