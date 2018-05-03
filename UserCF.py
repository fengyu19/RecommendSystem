# -*- coding: utf-8 -*-

import pickle
from collections import defaultdict
import math

# UserID::MovieID::Rating::Timestamp

def loadData():
    
    UserMovieDict = defaultdict(list)
    MovieUserDict = defaultdict(list)
    i = 0
    with open('ratings.dat', 'r') as data:
        for each_line in data:
            info = each_line.split('::')
            userID = info[0]
            movieID = info[1]
#            score = info[2]
            print (userID,movieID)
            UserMovieDict[userID].append(movieID)
            MovieUserDict[movieID].append(userID)
            i = i+1
            if i > 1000:
                break
    
    with open('UserMovieDict.pkl','wb+') as f1:  # (注:wb+二进制读写)
        pickle.dump(UserMovieDict, f1)
    f1.close()
    
    with open('MovieUserDict.pkl','wb+') as f2:  # (注:wb+二进制读写)
        pickle.dump(MovieUserDict, f2)
    f2.close()
    
    return UserMovieDict, MovieUserDict
    
def loadDataFromPKL(pklName1 ,pklName2):
    
    f1 = open(pklName1,'rb')
    UserMovieDict = pickle.load(f1)
    f1.close()
    
    f2 = open(pklName2,'rb')
    MovieUserDict = pickle.load(f2)
    f2.close()
    
    return UserMovieDict, MovieUserDict


def UserSimilarity(train):
    Weight = defaultdict(dict)
    for u in train.keys():
        for v in train.keys():
            if u == v:
                continue
#            print (train[u])
#            print (train[v])
            Weight[u][v] = len(set(train[u]) & set(train[v]))
            Weight[u][v] /= (1 + math.sqrt(len(train[u]) * len(train[v])))
    return Weight


def recommondation(user_id, UserMovieDict, K):
    rank=defaultdict(float)
    
    W = UserSimilarity(UserMovieDict)
#    print (W[user_id])
    for j, Similarity in sorted(W[user_id].items(),key = lambda x:x[1], reverse=True)[0:K]: #sorted()的返回值为list,list的元素为元组
        for item in UserMovieDict[j]:
            if item in UserMovieDict[user_id]:
                continue
            rank[item] += Similarity
    l = sorted(rank.items(),key = lambda x:x[1],reverse = True)[0:10]
    res = []
    for each in l:
        res.append(each[0])
    return res
        

def getMovieList(item_list):
    f = open('movies.dat', 'r')
    movieNameList = []
    data = f.readlines()
    for item in item_list:
        for each_line in data:
            info = each_line.split('::')
            movieNum = info[0]
            movieName = info[1]
            if item == movieNum:
                movieNameList.append(movieName)
#                print(movieName)
    return movieNameList 


#UserMovieDict, MovieUserDict = loadData()
    
UserMovieDict, MovieUserDict = loadDataFromPKL('UserMovieDict.pkl','MovieUserDict.pkl')
#W = UserSimilarity(UserMovieDict)
rank = recommondation('2', UserMovieDict, 5)
movieNameList = getMovieList(rank)