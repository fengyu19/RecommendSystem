# -*- coding: utf-8 -*-

# 隐语义模型
import pickle
import pandas as pd
import numpy as np
from math import exp


def loadDataFrom2PKL(pklName1 ,pklName2):
    
    f1 = open(pklName1,'rb')
    UserMovieDict = pickle.load(f1)
    f1.close()
    
    f2 = open(pklName2,'rb')
    MovieUserDict = pickle.load(f2)
    f2.close()
    
    return UserMovieDict, MovieUserDict


def loadDataFrom1PKL(pklName1):
    
    f1 = open(pklName1,'rb')
    Dict = pickle.load(f1)
    f1.close()
    return Dict


def allMovie(MovieUserDict):
    '''
    获取所有电影的列表
    '''
    return [key for key in MovieUserDict.keys()]
    
def getMovieHeat(MovieUserDict):
    '''
    获取电影的热度，电影热度根据评价电影的人数决定
    '''
    MovieHeatDict = dict()
    for key in MovieUserDict.keys():
        MovieHeatDict[key] = len(MovieUserDict[key])
    return MovieHeatDict
    

def getUserPositiveItem(UserMovieDict, UserID):
    '''
    获取一个用户喜爱电影列表
    '''
    positiveItemList = UserMovieDict[UserID]
    return positiveItemList


def getUserNegativeItem(MovieHeatDict, positiveItemList, UserID, positiveItemListLength):
    '''
    获取用户负反馈物品：热门但是用户没有进行过评分与正反馈数量相等
    '''
    allNegativeItemDict = MovieHeatDict.copy()
    for positiveItem in positiveItemList:
        if positiveItem in MovieHeatDict.keys():
#            print(positiveItem)
            del allNegativeItemDict[positiveItem]
    TopmovieList = sorted(allNegativeItemDict.items(),key = lambda x:x[1], reverse=True)[0:positiveItemListLength]
    negativeItemList = [key[0] for key in TopmovieList]
    return negativeItemList


def initTrainingData(positiveItemList ,negativeItemList):
    OnepersonData = dict()
    for each in positiveItemList+negativeItemList:
        if each in positiveItemList:
            OnepersonData[each] = 1.
        else:
            OnepersonData[each] = 0.
    return OnepersonData


def initPara(userID, itemID, classCount):  
    ''''' 
    初始化参数q,p矩阵, 随机 
    :param userCount:用户ID 
    :param itemCount:物品ID 
    :param classCount: 隐类数量 
    :return: 参数p,q 
    '''  
    arrayp = np.random.rand(len(userID), classCount)  
    arrayq = np.random.rand(classCount, len(itemID))  
    p = pd.DataFrame(arrayp, columns=range(0,classCount), index=userID)  
    q = pd.DataFrame(arrayq, columns=itemID, index=range(0,classCount))  
    return p,q  


def lfmPredict(p, q, userID, itemID):  
    ''''' 
    利用参数p,q预测目标用户对目标物品的兴趣度 
    :param p: 用户兴趣和隐类的关系 
    :param q: 隐类和物品的关系 
    :param userID: 目标用户 
    :param itemID: 目标物品 
    :return: 预测兴趣度 
    '''  
    p = np.mat(p.ix[userID].values)  
    q = np.mat(q[itemID].values).T  
    r = (p * q).sum()  
    r = sigmod(r)  
    return r  
  
    
def sigmod(x):  
    ''''' 
    单位阶跃函数,将兴趣度限定在[0,1]范围内 
    :param x: 兴趣度 
    :return: 兴趣度 
    '''  
    y = 1.0/(1+exp(-x))  
    return y


def latenFactorModel(UserMovieDict, MovieUserDict, classCount, iterCount, alpha, lamda):  
    ''''' 
    隐语义模型计算参数p,q 
    :param classCount: 隐类数量 
    :param iterCount: 迭代次数 
    :param alpha: 步长 
    :param lamda: 正则化参数 
    :return: 参数p,q 
    '''
    p, q = initPara(UserMovieDict.keys(), MovieUserDict.keys(), 5)
    for step in range(0, iterCount):  
        for userID in UserMovieDict.keys():
            positiveItemList = getUserPositiveItem(UserMovieDict, userID)
            MovieHeatDict = getMovieHeat(MovieUserDict)
            negativeItemList = getUserNegativeItem(MovieHeatDict, positiveItemList, userID, len(positiveItemList))
            OnepersonData = initTrainingData(positiveItemList, negativeItemList)
            for itemID in OnepersonData.keys():
                    eui = OnepersonData[itemID] - lfmPredict(p, q, userID, itemID)
                    for f in range(0, classCount):  
#                        print('step %d user %d class %d' % (step, int(userID), f))  
                        p[f][userID] += alpha * (eui * q[itemID][f] - lamda * p[f][userID])  
                        q[itemID][f] += alpha * (eui * p[f][userID] - lamda * q[itemID][f])  
        alpha *= 0.9  
    return p, q


def recommand(UserMovieDict, MovieUserDict, userID, p, q, TopN=10):
    userItemlist = getUserPositiveItem(UserMovieDict, userID)
    otherItemList = list(set(allMovie(MovieUserDict)) - set(userItemlist))
    predictDict = dict()
    for itemID in otherItemList:
        predictDict[itemID] = lfmPredict(p, q, userID, itemID)
        rankDict = sorted(predictDict.items(),key = lambda x:x[1],reverse=True)[0:TopN]
    res = []
    for each in rankDict:
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
#            print (movieNum, movieName)
            if item == movieNum:
                movieNameList.append(movieName)
                print(info[2])
    return movieNameList 


UserMovieDict, MovieUserDict = loadDataFrom2PKL('UserMovieDict.pkl','MovieUserDict.pkl')
#positiveItemList = getUserPositiveItem(UserMovieDict, '2')
#MovieHeatDict = getMovieHeat(MovieUserDict)
#negativeItemList = getUserNegativeItem(MovieHeatDict, positiveItemList, '2', len(positiveItemList))
#OnepersonData = initTrainingData(positiveItemList, negativeItemList)

#p, q = initPara(UserMovieDict.keys(), MovieUserDict.keys(), 5)
#r = lfmPredict(p, q, '1', '1193')

p, q = latenFactorModel(UserMovieDict, MovieUserDict, 5, 3, 0.01, 0.01)
ItemList = recommand(UserMovieDict, MovieUserDict, '1', p, q)
movieNameList = getMovieList(ItemList)


