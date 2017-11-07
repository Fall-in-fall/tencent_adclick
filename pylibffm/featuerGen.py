#--coding:utf-8--
from pandas import *
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import collections

def preAction(preData,nowData,fieldListList):
    # 用字典为每个field组合维护它的一个字典——记录一个field组合下的样本time和label情况的字典
    fieldKvStringDict=collections.defaultdict(lambda: collections.defaultdict(
                                                  lambda: collections.defaultdict(lambda: 0)))
    printCut = len(preData)/5
    for item_i,v in preData.iterrows(): #遍历每行
        for field in fieldListList: #为每个field组合更新它的字典
            kvStringDict= fieldKvStringDict[''.join(field)] #取得当前field组合的字典
            #查看当前行field上的值，更新字典
            kList=[]
            for col_i in xrange(0,len(field)):
                kList.append( str( int( v[field[col_i] ]) )  )
            kString=','.join(kList)
            labelInfo = int(v['label'])
            if labelInfo==1: kvStringDict[kString]['conv']+=1
            kvStringDict[kString]['click']+=1 #点击总是+1
        if item_i % printCut == 0:
                print(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), 'creating kvStringDict ', item_i)
    #建立新列
    for field in fieldListList:
        nowData[''.join(field)+'_preAction'] = Series(dtype=int)
        nowData[''.join(field)+'_preClickCount'] = Series(dtype=int) #前面总的点击次数
        nowData[''.join(field)+'_preConvCount'] = Series(dtype=int) #前面总的转化次数
        nowData[''.join(field)+'_ratio'] = Series(dtype=float) #前面总的转化率
    now_printCut = len(nowData)/3
    for item_i,v in nowData.iterrows():
        for field in fieldListList: #为每个field组合更新它的字典
            kvStringDict=fieldKvStringDict[''.join(field)]
            kList=[]
            for col_i in xrange(0,len(field)):
                colV=v[field[col_i] ]
                kList.append( str( int( colV ) )  )
            #没有单独处理可能为缺失默认值0的情况，认为就是0值的就是同类
            kString=','.join(kList)
            kv = kvStringDict[ kString ]
            clickCount=kv['click'] ; convCount=kv['conv']
            if clickCount>0:
                nowData[''.join(field)+'_preClickCount'].set_value(item_i, clickCount) #前面总的转化次数
            if convCount>0:
                nowData[''.join(field)+'_preConvCount'].set_value(item_i, convCount) #前面总的转化次数

            nowData[''.join(field)+'_ratio'].set_value(item_i,(float(convCount)/clickCount) if clickCount>0 else 0)

            if convCount>0:     actionV=3
            elif clickCount>0:  actionV=2
            else :              actionV=1
            nowData[''.join(field)+'_preAction'].set_value(item_i,actionV)

        if item_i % now_printCut == 0:
                print(datetime.now().strftime('%Y-%m-%d-%H-%M-%S' ), 'creating features ', item_i)
    return nowData
#fixDay前次动作参考周期
#field前次动作粒度
def preActionFeature(trainFile='../data/m_p_u_amc.csv',testFile='../data/test_m_p_u_amc.csv',fieldListList=[['userID']],fixDay=0,postfix=''):
    import warnings ; warnings.filterwarnings("ignore")
    timestr=datetime.now().strftime('%Y-%m-%d-%H-%M-%S' )
    print 'filed: ',fieldListList
    train=read_csv(trainFile)
    newTrain=DataFrame()
    #fixDay<30则按往前fixDay时间内计算特征，否则从fixDay开始按往前所有时间内数据计算
    startTime =  170000+fixDay*10000  if fixDay<30 else fixDay
    print 'fixDay startTime : ',fixDay,startTime
    for day in xrange(startTime,310000,10000):
        print day
        if fixDay<30: #按周期采样
            preData = train[(train['clickTime']>=day-fixDay*10000)&(train['clickTime']<day)]
            nowData = train[ (train['clickTime']>=day) & (train['clickTime']<day+10000) ]
        else: #不按周期采样。一律取前面所有的
            preData = train[train['clickTime']<day]
            nowData = train[ (train['clickTime']>=day) & (train['clickTime']<day+10000) ]

        nowData = preAction(preData,nowData,fieldListList)
        newTrain=concat([newTrain,nowData],axis=0)
    print 'new length should be equal',len(train[train['clickTime']>=startTime]), len(newTrain)
    fieldListListstr=','.join( [''.join(f) for f in fieldListList]  )

    newTrain.to_csv('../data/temp/train_preAction_{postfix}_{fixDay}.csv'
                    .format(postfix=postfix,fixDay=fixDay),index=False)

    test=read_csv(testFile)
    preData_test = train[train['clickTime']>=(310000-fixDay*10000)] \
        if fixDay<30 else train
    newTest= preAction(preData_test,test,fieldListList)
    newTest.to_csv('../data/temp/test_preAction_{postfix}_{fixDay}.csv'
                    .format(postfix=postfix,fixDay=fixDay),index=False)
    return newTrain,newTest

# allFieldListList=[
#                       ['userID','appID'],['userID','positionID'], ['userID','adID'],
#                       ['userID','advertiserID'],['userID','appCategory'],['userID','camgaignID'] ,
#                      # ['positionID','adID'],['positionID','education'],['positionID','gender'],
#                      # ['positionID','camgaignID'],['positionID','connectionType'],['positionID','advertiserID'],
#                     ['userID']
#                      # ['education','adID'],['education','gender'],['gender','adID'],
#                      # ['positionID'],['adID'],['appID'],['appCategory'],['advertiserID'],['camgaignID']
#                 ]

#preActionFeature(fieldListList=allFieldListList,fixDay=190000,postfix='allUserAndCombs')


def addRatio(trainFile='',testFile='',fieldListList=''):

    trainFile='../data/temp/train_preAction_allIDField_4_addUserField_isInstalled.csv'
    testFile='../data/temp/test_preAction_allIDField_4_addUserField_isInstalled.csv'

    fieldListList=[
        ['userID'],['userID','appID']]

    train=read_csv(trainFile) ; test=read_csv(testFile)
    #train.fillna(-1,inplace=True) ; test.fillna(-1,inplace=True)
    #train.astype(int) ; test.astype(int)
    for field in fieldListList:
        fieldString=''.join(field)
        train[fieldString+'_ratio'] = train.apply(
            lambda x: 0 if  x[fieldString+'_preClickCount']==0 or isnull(x[fieldString+'_preClickCount'])
            else float(x[fieldString+'_preConvCount'])/x[fieldString+'_preClickCount'],axis='columns')
        test[fieldString+'_ratio'] = test.apply(
            lambda x: 0 if  x[fieldString+'_preClickCount']==0 or isnull(x[fieldString+'_preClickCount'])
            else float(x[fieldString+'_preConvCount'])/x[fieldString+'_preClickCount'],axis='columns')
    #del train['Unnamed: 0'],train['Unnamed: 0.1']
    train.to_csv( trainFile[0:-4] + '_addRatio.csv',index=False)
    print 'train tocsv finished'
    #del test['Unnamed: 0'],test['Unnamed: 0.1']
    test.to_csv( testFile[0:-4] + '_addRatio.csv',index=False)
addRatio()

def zero2nan():
    import numpy as np
    train=read_csv('../data/temp/train_addRatio.csv') ; test=read_csv('../data/temp/test_addRatio.csv')
    fieldListList=[['userID','appID'],['userID','adID'],['userID','advertiserID'],['userID','appCategory'],
                ['userID'],['appID'],['adID'],['advertiserID'] ]
    field=[]
    for newField in fieldListList:
                field.append(''.join(newField)+'_preAction')
                field.append(''.join(newField)+'_preClickCount')
                field.append(''.join(newField)+'_preConvCount')
    for f in field:
        train[f].replace(0,np.nan,inplace=True)
        test[f].replace(0,np.nan,inplace=True)
    train.to_csv('../data/temp/train_addRatio_0toNan.csv',index=False)
    test.to_csv('../data/temp/test_addRatio_0toNan.csv',index=False)
def cutTrain():
    train=read_csv('../data/temp/train_preAction_19.csv')
    for day in xrange(200000,310000,10000):
        train[train['clickTime']>=day]\
            .to_csv('../data/temp/train_preAction_{day}.csv'.format(day=str(day/10000)),index=False )
def bucketAcition():
    fieldListList=[
        ['positionID'],['adID'],['appID'],['appCategory'],['advertiserID'],['camgaignID']
    ]
    train=read_csv('train_addRatio_0toNan_all.csv') ; test=read_csv('test_addRatio_0toNan_all.csv')

def mergeUserAndOther(otherStartDay):
    userData=read_csv('../data/temp/train_preAction_allUserAndCombs_190000.csv')
    test_userData=read_csv('../data/temp/test_preAction_allUserAndCombs_190000.csv')
    userData=userData[userData['clickTime']>=otherStartDay].reset_index()
    test_userData=test_userData[test_userData['clickTime']>=otherStartDay].reset_index()

    otherData=read_csv('../data/temp/train_preAction_allIDField_4.csv')
    test_otherData=read_csv('../data/temp/test_preAction_allIDField_4.csv')
    userField=[ ['userID','appID'], ['userID']]

    if len(userData)!=len(otherData):raise Exception('wrong length')

    for f in userField:
        print f
        otherData[''.join(f)+'_preAction'] = userData[''.join(f)+'_preAction']
        otherData[''.join(f)+'_preClickCount'] = userData[''.join(f)+'_preClickCount']
        otherData[''.join(f)+'_preConvCount'] = userData[''.join(f)+'_preConvCount']

        test_otherData[''.join(f)+'_preAction'] = test_userData[''.join(f)+'_preAction']
        test_otherData[''.join(f)+'_preClickCount'] = test_userData[''.join(f)+'_preClickCount']
        test_otherData[''.join(f)+'_preConvCount'] = test_userData[''.join(f)+'_preConvCount']
    otherData.to_csv('../data/temp/train_preAction_allIDField_4_addUserField.csv',index=False)
    test_otherData.to_csv('../data/temp/test_preAction_allIDField_4_addUserField.csv',index=False)

mergeUserAndOther(210000)