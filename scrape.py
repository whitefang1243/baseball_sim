from baseball_scraper import baseball_reference
import numpy as np
import time

#this program uses a modified version of the baseball_scraper library

#once again, I do not remember why the teams are ordered like this
#see populate.py for more information
teams = ['STL', 'TOR', 'NYM', 'SFG', 'MIN', 'SEA', 'PHI', 'WSN', 'LAD', 'COL', 'CHC', 'CHW', 'HOU', 'BOS', 'DET', 'PIT', 'TBR', 'KCR', 'MIL', 'BAL', 'TEX', 'CIN', 'ATL', 'SDP', 'ARI', 'LAA', 'OAK', 'NYY', 'CLE', 'MIA']

def old_main(year):
    s = baseball_reference.TeamScraper()
    s.set_season(year)
    data = s.scrape('STL')
    print(data.head())
    arr = data.to_numpy()
    print(arr)
    for i in range(1, len(teams)):
        time.sleep(10)
        data = s.scrape(teams[i])
        print(data.head())
        arr2 = data.to_numpy()
        arr = np.concatenate((arr, arr2))
    for i in range(0, len(arr)):
        arr[i][0] = arr[i][0].strftime('%Y-%m-%d')
        if arr[i][0] is None :
            print(i)
    arr=np.delete(arr, -1, axis = 1)
    print(arr[np.argsort(arr[:, 0])])
    ret_arr = []
    for i in range(0, len(arr)):
        if arr[i][2]=='@':
            ret_arr.append(arr[i])
    print(len(arr))
    print(len(ret_arr))
    return ret_arr

def main(year, flag):
    s = baseball_reference.TeamScraper()
    s.set_season(year)
    data = s.scrape('STL')
    print(data.head())
    arr = data.to_numpy()
    arr=np.delete(arr, -1, axis = 1)
    arr = [arr.tolist()]
    print(arr)
    for i in range(1, len(teams)):
        time.sleep(10)
        data = s.scrape(teams[i])
        print(data.head())
        arr2 = data.to_numpy()
        arr2=np.delete(arr2, -1, axis = 1)
        arr2 = arr2.tolist()
        arr.append(arr2)
    for i in range(0, len(arr)):
        for j in range(0, len(arr[i])):
            arr[i][j][0] = arr[i][j][0].strftime('%Y-%m-%d')
            if arr[i][j][0] is None :
                print(i)
    #ret_arr and any related code is for debugging purposes; will be removed in the future
    ret_arr = []
    for i in range(0, len(arr)):
        ret_arr.append([])
        for j in range(0, len(arr[i])):
            if arr[i][j][2]=='@':
                ret_arr[-1].append(arr[i][j])
    print(len(arr[1]))
    print(len(ret_arr[1]))
    if flag:                #debug purposes
        return arr
    return ret_arr
#main(2024, True)