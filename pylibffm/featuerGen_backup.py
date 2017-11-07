#--coding:utf-8--
from pandas import *
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import collections

def userTfidf(train,test):
    # train = pd.read_csv('../data/train.csv')
    # test = pd.read_csv('../data/test.csv')
    user_installedapps = read_csv('../data/user_installedapps.csv')
    user_installedapps = user_installedapps.groupby('userID').agg(lambda x:' '.join(['app'+str(s) for s in x.values])).reset_index()

    user_id_all = concat([train.userID,test.userID],axis=0)
    user_id_all = DataFrame(user_id_all,columns=['userID'])
    #先去重，拟合tfidf
    user_installedapps = merge(user_id_all.drop_duplicates(),user_installedapps,on='userID',how='left')
    user_installedapps = user_installedapps.fillna('Missing')

    tfv = TfidfVectorizer()
    tfv.fit(user_installedapps.appID)
    #不去重的原始数据转换tfidf，拼接上去
    user_installedapps = merge(user_id_all,user_installedapps,on='userID',how='left')
    user_installedapps = user_installedapps.fillna('Missing')
    user_installedapps_tfv = tfv.transform(user_installedapps.appID)
    user_installedapps_tfv.shape

def timeDiff(strnow,strpre,unit=['hour',1]):
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

def preAction2(preData,nowData,field):
    kvStringDict=collections.defaultdict(lambda: [])
    printCut = len(preData)/5
    for item_i,v in preData.iterrows():
        kList=[]
        for col_i in xrange(0,len(field)):
            kList.append( str( int( v[field[col_i] ]) )  )
        kString=','.join(kList)
        kvStringDict[kString].append( '-'.join( [ str( int(v['clickTime']) )  ,str(int(v['label'])) ]) )
        if item_i % printCut == 0:
                print(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), 'creating kvStringDict ', item_i)
    nowData['preAll'] = Series(dtype=str)
    nowData['preAction'] = Series(dtype=int)
    nowData['preClickCount'] = Series(dtype=int) #前面总的点击次数
    nowData['preClickDist']=Series(dtype=int) #前一次点击，间隔时间
    nowData['preConvCount'] = Series(dtype=int) #前面总的转化次数
    nowData['preConvDist']=Series(dtype=int) #前一次转化，间隔时间
    # nowData['sameAppID']=Series(dtype=int) #上一次是否有相同app
    # nowData['sameCate']=Series(dtype=int) #上一次是否有相同app类别

    now_printCut = len(nowData)/3
    for item_i,v in nowData.iterrows():
        kList=[]
        for col_i in xrange(0,len(field)):
            kList.append( str( int( v[field[col_i] ]) )  )
        kString=','.join(kList)
        kv = kvStringDict[ kString ]
        preClickValue=','.join(kv)
        nowData['preAll'].set_value(item_i,preClickValue)
        if kString[0:2]=='0,' or kString.__contains__(',0'): #包含0的为未知，一律视作不一样,置preClickValue空以设actionV为1
            preClickValue='' ; print kString
        if preClickValue=='':
            actionV=1   #之前未点击
        else: #之前有点击
            if preClickValue.__contains__('-1'):
                actionV=3  #点击且转化
                preConvList = [ k for k in kv if k.__contains__('-1')]
                nowData['preConvCount'].set_value(item_i, len(preConvList)) #前面总的转化次数
                lastConvTime = preConvList[-1].split('-')[0]
                preConvDist = timeDiff( str(int(v['clickTime'])),lastConvTime)
                nowData['preConvDist'].set_value(item_i,preConvDist) #距离上次转化时间间隔
            else :
                actionV=2  #点击未转化
            nowData['preClickCount'].set_value(item_i,len(kv) ) #前面总的点击次数
            lastClickTime=kv[-1].split('-')[0]
            preClickTimeDist = timeDiff( str(int(v['clickTime'])),lastClickTime)
            nowData['preClickDist'].set_value(item_i,preClickTimeDist) #距离上次点击时间间隔
            #转化和点击要一并记录，待补充
        nowData['preAction'].set_value(item_i,actionV)
        if item_i % now_printCut == 0:
                print(datetime.now().strftime('%Y-%m-%d-%H-%M-%S' ), 'creating features ', item_i)
    print len(nowData[ nowData['preAction']>1 ]),len(nowData)
    return nowData

#fixDay前次动作参考周期
#field前次动作粒度
def preActionFeature2(trainFile='../data/m_p_u_amc.csv',testFile='../data/test_m_p_u_amc.csv',field=['userID'],fixDay=0):

    import warnings ; warnings.filterwarnings("ignore")
    timestr=datetime.now().strftime('%Y-%m-%d-%H-%M-%S' )
    print 'filed: ',field
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

        nowData = preAction2(preData,nowData,field)
        newTrain=concat([newTrain,nowData],axis=0)
    print 'new length should be equal',len(train[train['clickTime']>=startTime]), len(newTrain)

    newTrain.to_csv('../data/temp/train_preAction_{field}_{fixDay}.csv'
                    .format(field=''.join(field),fixDay=fixDay),index=False)

    test=read_csv(testFile)
    preData_test = train[train['clickTime']>=(310000-fixDay*10000)] \
        if fixDay<30 else train
    newTest= preAction2(preData_test,test,field)
    newTest.to_csv('../data/temp/test_preAction_{field}_{fixDay}.csv'
                    .format(field=''.join(field),fixDay=fixDay),index=False)
    return newTrain,newTest


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

