# -*- coding: utf-8 -*-
import pickle
import pandas as pd

def loadDataFromPKL(pklName1 ,pklName2):
    
    f1 = open(pklName1,'rb')
    UserMovieDict = pickle.load(f1)
    f1.close()
    
    f2 = open(pklName2,'rb')
    MovieUserDict = pickle.load(f2)
    f2.close()
    
    return UserMovieDict, MovieUserDict


def getUserGraph(UserMovieDict, userID):
    return {'i'+str(item): 1 for item in UserMovieDict[userID]}


def getItemGraph(MovieUserDict, itemID):
    return {'u'+str(user): 1 for user in MovieUserDict[itemID]} 


def initGraph(UserMovieDict, MovieUserDict):
    userList = UserMovieDict.keys()
    itemList = MovieUserDict.keys()
    G = {'u'+str(user): getUserGraph(UserMovieDict, user) for user in userList}
    for item in itemList:
        G['i'+str(item)] = getItemGraph(MovieUserDict, item)
    return G


def personalRank(G, alpha, userID, iterCount=20):
    '''
    随机游走迭代
    :param G: 二分图
    :param alpha: 随机游走的概率
    :param userID: 目标用户
    :param iterCount: 迭代次数
    :return: series
    '''
    rank = {g: 0 for g in G.keys()}
    rank['u'+str(userID)] = 1                                       #根节点为起点选择概率为1,其他顶点为0
    for k in range(iterCount):
        tmp = {g: 0 for g in G.keys()}
        for i, ri in G.items():                                     #遍历每一个顶点
            for j, wij in ri.items():                               #遍历每个顶点连接的顶点
#                print(j, wij)
                tmp[j] += alpha * rank[i] / len(ri)
        tmp['u' + str(userID)] += 1 - alpha                         #根顶点r=1，加上1-alpha
        rank = tmp
    series = pd.Series(list(rank.values()), index=list(rank.keys()))
    series = series.sort_values(ascending=False)
    return series                                                   #返回排序后的series


def recommend(UserMovieDict, series, userID, TopN=10):
    itemList = getUserGraph(UserMovieDict, userID)
    recommendList = [{u: series[u]} for u in list(series.index) if u not in itemList and 'u' not in u]
    return recommendList[:TopN]

    


#G1 = {'A' : {'a' : 1, 'c' : 1},
#         'B' : {'a' : 1, 'b' : 1, 'c':1, 'd':1},  
#             'C' : {'c' : 1, 'd' : 1},  
#             'a' : {'A' : 1, 'B' : 1},  
#             'b' : {'B' : 1},  
#             'c' : {'A' : 1, 'B' : 1, 'C':1},  
#             'd' : {'B' : 1, 'C' : 1}}


UserMovieDict = {'1' : ['11', '33'],
         '2' : ['11', '22', '33', '44'],  
             '3' : ['33', '44']}

MovieUserDict = {'11' : ['1', '2'],  
             '22' : ['2'],  
             '33' : ['1', '2', '3'],  
             '44' : ['2', '3']}


#UserMovieDict = {'1' : {'11' : 1, '33' : 1},
#         '2' : {'11' : 1, '22' : 1, '33':1, '44':1},
#             '3' : {'33' : 1, '44' : 1}}
#
#MovieUserDict = {'11' : {'1' : 1, '2' : 1},  
#             '22' : {'2' : 1},  
#             '33' : {'1' : 1, '2' : 1, '3':1},  
#             '44' : {'2' : 1, '3' : 1}}

#UserMovieDict, MovieUserDict = loadDataFromPKL('UserMovieDict.pkl','MovieUserDict.pkl')
G = initGraph(UserMovieDict, MovieUserDict)
series = personalRank(G, 0.5, '1', iterCount=20)
recommendList = recommend(UserMovieDict, series, '1')
    
