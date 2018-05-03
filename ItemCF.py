# -*- coding: utf-8 -*-

from collections import defaultdict
import math

def readFile(fileData):
    
    data=[]
    rates=[]
    f=open(fileData,"r")
    data=f.readlines()
    f.close()
    i = 0
    for line in data:
        dataLine=line.split("::")
        rates.append([int(dataLine[0]),int(dataLine[1]),int(dataLine[2])])
        if i >= 1000:
            break
        i += 1
    return rates


def createDict(rates):
    user_dict={}
    movie_dict={}
    for i in rates:
        if i[0] in user_dict:
            user_dict[i[0]].append((i[1],i[2]))
        else:
            user_dict[i[0]]=[(i[1],i[2])]
        if i[1] in movie_dict:
            movie_dict[i[1]].append(i[0])
        else:
            movie_dict[i[1]]=[i[0]]
    return user_dict,movie_dict


def itemCF(user_dict):
    N=dict()
    C=defaultdict(defaultdict)
    W=defaultdict(defaultdict)
    for key in user_dict:
        for i in user_dict[key]:
            if i[0] not in N.keys(): #i[0]表示movie_id
                N[i[0]] = 0
            N[i[0]] += 1               #N[i[0]]表示评论过某电影的用户数
            
            for j in user_dict[key]:
                if i==j:
                    continue
                if j not in C[i[0]].keys():
                    C[i[0]][j[0]]=0
                C[i[0]][j[0]]+=1      # C[i[0]][j[0]]表示电影两两之间的相似度，eg：同时评论过电影1和电影2的用户数
    for i,related_item in C.items():
        for j,cij in related_item.items():
            W[i][j]=cij/math.sqrt(N[i]*N[j]) 
    return W


def recommondation(user_id, user_dict, K):
    rank = defaultdict(int)
    l = list()
    W = itemCF(user_dict)
    for i,score in user_dict[user_id]: # i为特定用户的电影id，score为其相应评分
        for j,wj in sorted(W[i].items(),key = lambda x:x[1],reverse=True)[0:K]: #sorted()的返回值为list,list的元素为元组
            if j in user_dict[user_id]:
                continue
            rank[j]+=score*wj # 先找出用户评论过的电影集合，对每一部电影id，假设其中一部电影id1,找出与该电影最相似的K部电影，计算出在id1下用户对每部电影的兴趣度，接着迭代整个用户评论过的电影集合，求加权和，再排序，可推荐出前n部电影，我这里取10部。
    l = sorted(rank.items(),key = lambda x:x[1],reverse=True)[0:10]
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
            movieNum = int(info[0])
            movieName = info[1]
            if item == movieNum:
                movieNameList.append(movieName)
#                print(movieName)
    return movieNameList   
    
    
rates = readFile('ratings.dat')
user_dict,movie_dict = createDict(rates)
#W = itemCF(user_dict)
rank = recommondation(1, user_dict, 10)
movieNameList = getMovieList(rank)