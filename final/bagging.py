# -*- encoding:utf-8 -*-
import collections
from csv import DictReader
from datetime import datetime
import numpy as np
from pandas import *
from datetime import datetime


def bagging(fileList,weight,target):
    for f in fileList:
        f.readline()
    cuID=1
    stopFlag=False
    with open(target,'w') as fo:
        fo.write('instanceID,prob\n')
        while True:
            lines=[]
            for f in fileList:
                temp=f.readline()
                if not temp:
                    stopFlag=True ; break
                else: lines.append( temp.strip() )
            if stopFlag:break
            finalresult=0
            for ri in xrange(0,len(lines)):
                finalresult+=float(lines[ri].split(',')[1])*weight[ri]
            fo.write(str(cuID)+','+str(finalresult)+'\n')
            cuID+=1
        fo.close()

def doBagging():
    f1=open('../data/bagging/3-3-0.102566-submission-w8,2_bagging_102662&10349_2017-06-05-17-10-05.csv')
    f2=open('../data/bagging/0.1031-2-xgb_500_2017-06-07-09-42-46_.csv')


    fileList = [f1,f2]
    weight = [0.85,0.15] ; strweight=','.join( [str(i)[2:] for i in weight ])
    target='../submit/w{ratio}_bagging_102566&1031_{time}.csv'\
        .format(ratio=strweight,time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S' ))
    bagging(fileList,weight,target)
    return target

def doBagging2():
    f1=open('../data/bagging/3-0.102662-ffm_mergeAppUser_s17_preAction_190000_no_Dist_noNum_t150_k8_l2e-05_2017-06-04-14-41-36.csv')
    f2=open('../data/bagging/103425-ffm_3sha_1002017-06-05-12-14-42.csv')

    fileList = [f1,f2]
    weight = [0.7,0.3] ; strweight=','.join( [str(i)[2:] for i in weight ])
    target='../submit/w{ratio}_bagging_102662&103425_{time}.csv'\
        .format(ratio=strweight,time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S' ))
    bagging(fileList,weight,target)
    return target

def doBagging3():
    f1=open('../data/bagging/3-0.102662-ffm_mergeAppUser_s17_preAction_190000_no_Dist_noNum_t150_k8_l2e-05_2017-06-04-14-41-36.csv')
    f2=open('../data/bagging/103145-lgbm_270_2017-06-07-04-00-32_1.03145.csv')
    f3=open('../data/bagging/103425-ffm_3sha_1002017-06-05-12-14-42.csv')

    fileList = [f1,f2,f3]
    weight = [0.5,0.3,0.2] ; strweight=','.join( [str(i)[2:] for i in weight ])
    target='../submit/w{ratio}_bagging_102662&103425_{time}.csv'\
        .format(ratio=strweight,time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S' ))
    bagging(fileList,weight,target)
    return target

doBagging()

def reviseTest(submitFile,markFile):
    submit = read_csv(submitFile)
    test_mark = read_csv(markFile)
    newSubmit = merge(submit,test_mark,on='instanceID',how='left')
    # newSubmit['newProb'] = newSubmit.apply(
    #     lambda x: x['prob']*0.5 if  str(x['preClick']).__contains__('-1')
    #         else  x['prob']*0.9 if not isnull(x['preClick']) else x['prob'], axis='columns')
    def giveWeight(x):
        if not isnull(x['preClick']): #因为pandas中的nansplit之后也会长度为1，所以必须先进行isnull判断
            strPreClick = str(x['preClick'])
            lenClick = len(str(x['preClick']).split(','))
            if lenClick > 3 and not strPreClick.__contains__('-1'):
                result = x['prob']*0.5
            else:result = x['prob']*0.8
        else: result= x['prob']
        return result



    newSubmit['newProb'] = newSubmit.apply(lambda x: giveWeight(x), axis='columns')
    result=newSubmit[['instanceID','newProb']]
    result.rename(columns={'newProb':'prob'},inplace=True)
    # for i,v in newSubmit.iterrows():
    #     if v['prob']!=v['newProb']:
    #         print v['prob'],v['newProb']
    return result
#
# reviseTest('../submit/w7,3_bagging_102662&10349_2017-06-05-17-01-39.csv',
#            '../data/sample/test/test_appIDmarkPreClick.csv')\
#     .to_csv('../submit/3&5_8_w7,3_bagging_102662&10349_2017-06-05-17-01-39.csv',index=False)
