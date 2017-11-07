#--coding:utf-8--
from pandas import *
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import collections

def timeDiff(strnow,strpre,unit=['day',1]):
    minute=( int(strnow[4:6])- int(strpre[4:6]) )
    time = 1440*( int(strnow[0:2])- int(strpre[0:2]) )+\
               60*( int(strnow[2:4]) - int(strpre[2:4]) )+ minute
    if unit[0]=='day':
        result=time/(1440*unit[1])
    elif unit[0]=='hour':
        result=time/(60*unit[1])
    elif unit[0]=='minute':
        result=time/(unit[1])
    else: raise  Exception('wrong time unit !')
    return result+1

def preAction(preData,nowData,fieldListList):
    # 用字典为每个field组合维护它的一个字典——记录一个field组合下的样本time和label情况的字典
    fieldKvStringDict=collections.defaultdict(lambda: collections.defaultdict(lambda: []))
    printCut = len(preData)/5
    for item_i,v in preData.iterrows(): #遍历每行
        for field in fieldListList: #为每个field组合更新它的字典
            kvStringDict= fieldKvStringDict[''.join(field)] #取得当前field组合的字典
            #查看当前行field上的值，更新字典
            kList=[]
            for col_i in xrange(0,len(field)):
                kList.append( str( int( v[field[col_i] ]) )  )
            kString=','.join(kList)
            kvStringDict[kString].append( '-'.join( [ str( int(v['clickTime']) )  ,str(int(v['label'])) ]) )
        if item_i % printCut == 0:
                print(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), 'creating kvStringDict ', item_i)
    #建立新列
    for field in fieldListList:
        nowData[''.join(field)+'_preAll'] = Series(dtype=str)
        nowData[''.join(field)+'_preAction'] = Series(dtype=int)
        nowData[''.join(field)+'_preClickCount'] = Series(dtype=int) #前面总的点击次数
        nowData[''.join(field)+'_preClickDist']=Series(dtype=int) #前一次点击，间隔时间
        nowData[''.join(field)+'_preConvCount'] = Series(dtype=int) #前面总的转化次数
        nowData[''.join(field)+'_preConvDist']=Series(dtype=int) #前一次转化，间隔时间
    # nowData['sameAppID']=Series(dtype=int) #上一次是否有相同app
    # nowData['sameCate']=Series(dtype=int) #上一次是否有相同app类别

    now_printCut = len(nowData)/3
    for item_i,v in nowData.iterrows():
        for field in fieldListList: #为每个field组合更新它的字典
            kvStringDict=fieldKvStringDict[''.join(field)]
            kList=[]
            for col_i in xrange(0,len(field)):
                kList.append( str( int( v[field[col_i] ]) )  )
            kString=','.join(kList)
            kv = kvStringDict[ kString ]
            preClickValue=','.join(kv)
            nowData[''.join(field)+'_preAll'].set_value(item_i,preClickValue)
            if kString[0:2]=='0,' or kString.__contains__(',0'): #包含0的为未知，一律视作不一样,置preClickValue空以设actionV为1
                preClickValue='' ; print kString
            if preClickValue=='':
                actionV=1   #之前未点击
            else: #之前有点击
                if preClickValue.__contains__('-1'):
                    actionV=3  #点击且转化
                    preConvList = [ k for k in kv if k.__contains__('-1')]
                    nowData[''.join(field)+'_preConvCount'].set_value(item_i, len(preConvList)) #前面总的转化次数
                    lastConvTime = preConvList[-1].split('-')[0]
                    preConvDist = timeDiff( str(int(v['clickTime'])),lastConvTime)
                    nowData[''.join(field)+'_preConvDist'].set_value(item_i,preConvDist) #距离上次转化时间间隔
                else :
                    actionV=2  #点击未转化
                nowData[''.join(field)+'_preClickCount'].set_value(item_i,len(kv) ) #前面总的点击次数
                lastClickTime=kv[-1].split('-')[0]
                preClickTimeDist = timeDiff( str(int(v['clickTime'])),lastClickTime)
                nowData[''.join(field)+'_preClickDist'].set_value(item_i,preClickTimeDist) #距离上次点击时间间隔
            nowData[''.join(field)+'_preAction'].set_value(item_i,actionV)
        if item_i % now_printCut == 0:
                print(datetime.now().strftime('%Y-%m-%d-%H-%M-%S' ), 'creating features ', item_i)
    return nowData
#fixDay前次动作参考周期
#field前次动作粒度
def preActionFeature(trainFile='../data/m_p_u_amc.csv',testFile='../data/test_m_p_u_amc.csv',fieldListList=[['userID']],fixDay=0):

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

    newTrain.to_csv('../data/temp/train_preAction_{field}_{fixDay}.csv'
                    .format(field=fieldListListstr,fixDay=fixDay),index=False)

    test=read_csv(testFile)
    preData_test = train[train['clickTime']>=(310000-fixDay*10000)] \
        if fixDay<30 else train
    newTest= preAction(preData_test,test,fieldListList)
    newTest.to_csv('../data/temp/test_preAction_{field}_{fixDay}.csv'
                    .format(field=fieldListListstr,fixDay=fixDay),index=False)
    return newTrain,newTest

# fieldListList=[['userID','appID'],['userID','adID'],['userID','advertiserID'],['userID','appCategory'],
#                ['userID'],['appID'],['adID'],['advertiserID'],['appCategory'] ]
#
# preActionFeature(fieldListList=fieldListList,fixDay=190000)

def mergeField(beFile,beTestFile,toBeFieldListList,fixDay):
    fieldListListstr= ','.join( [''.join(f) for f in toBeFieldListList]  )
    nowData=read_csv(beFile)
    test_nowData=read_csv(beTestFile)
    for field in toBeFieldListList:
        train=read_csv('../data/temp/train_preAction_{field}_{fixDay}.csv'.format(field=fieldListListstr,fixDay=fixDay))
        test=read_csv('../data/temp/test_preAction_{field}_{fixDay}.csv'.format(field=fieldListListstr,fixDay=fixDay))

        nowData[''.join(field)+'_preAction'] = train[''.join(field)+'_preAction']
        nowData[''.join(field)+'_preClickCount'] = train[''.join(field)+'_preClickCount']
        nowData[''.join(field)+'_preConvCount'] = train[''.join(field)+'_preConvCount']
        nowData[''.join(field)+'_ratio'] = train[''.join(field)+'_ratio']

        test_nowData[''.join(field)+'_preAction'] = test[''.join(field)+'_preAction']
        test_nowData[''.join(field)+'_preClickCount'] = test[''.join(field)+'_preClickCount']
        test_nowData[''.join(field)+'_preConvCount'] = test[''.join(field)+'_preConvCount']
        test_nowData[''.join(field)+'_ratio'] = test[''.join(field)+'_ratio']

    print nowData.columns
    print len(nowData.columns),len(toBeFieldListList)*4
    nowData.to_csv(beFile[0:-4]+'add_'+fieldListListstr+'.csv',index=False)
    test_nowData.to_csv(beTestFile[0:-4]+'add_'+fieldListListstr+'.csv',index=False)
    return beFile[0:-4]+'add_'+fieldListListstr+'.csv',beTestFile[0:-4]+'add_'+fieldListListstr+'.csv'

lastFiel=mergeField('../data/temp/train_addRatio_0toNan.csv','../data/temp/test_addRatio_0toNan.csv',
           [['userID','positionID'],['adID','positionID'],['positionID']],fixDay=190000)

final=mergeField(lastFiel[0],lastFiel[1],
          [['positionID'],['adID'],['appID'],['appCategory'],['advertiserID'],['camgaignID']],fixDay=2)
print final




def merge_appID_userID(userIDFile,appIDFile,newFile):
    mergeField=['preAction','preClickCount','preClickDist','preConvCount','preConvDist']
    appIDpreData=read_csv(appIDFile) ; userIDpreData=read_csv(userIDFile)
    if len(appIDpreData)!=len(userIDpreData) :
        print len(appIDpreData),len(userIDpreData)
        raise Exception('wrong with different length')
    for field in mergeField:
        userIDpreData['app_'+field]=appIDpreData[field]
    userIDpreData.to_csv(newFile,index=False)
    return newFile

def cutTrain():
    train=read_csv('../data/temp/train_preAction_19.csv')
    for day in xrange(200000,310000,10000):
        train[train['clickTime']>=day]\
            .to_csv('../data/temp/train_preAction_{day}.csv'.format(day=str(day/10000)),index=False )
#cutTrain()

# def getSet():
#     actionDayDict=collections.defaultdict(lambda: set())
#
#     actions = read_csv('../data/user_app_actions.csv')
#     for day in xrange(17,310000,10000):

