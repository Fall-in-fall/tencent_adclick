#--coding:utf-8--
from pandas import *
import xgboost as xgb

# base='D:\workspace\PycharmProjects\\a\\tencent_adclick\\data\\'
# trainFile=base+'m_p_u_amc.csv'; testFile=base+'test_m_p_u_amc.csv'
# train=read_csv(trainFile) ; test=read_csv(testFile) ;

#特征下样本与正例分布分析
#返回 总样本，正样本，比例
# targetCol   sum   posSum     ratio
def posRatio(oriData,targetCol=''):
    targetDF=oriData[[targetCol,"label"]]
    #分类总数统计
    allCount = targetDF.groupby(targetCol).count()
    allCount.reset_index(inplace=True)
    #分类正样本总数统计
    posInsCount = targetDF[targetDF['label']==1].groupby(targetCol).count()
    posInsCount.reset_index(inplace=True)
    temp=merge(allCount,posInsCount,on=targetCol,how='left')
    temp.rename(columns={"label_x":"sum","label_y":"posSum"},inplace=True)
    temp["ratio"]=temp.apply(lambda x : float(x['posSum'])/x['sum'],axis='columns')
    return temp
#两特征联立分析
def doublePosRatio(oriData,t1,t2):
    targetDF=oriData[[t1,t2,"label"]]
    #分类总数统计
    allCount = targetDF.groupby([t1,t2]).count()
    allCount.reset_index(inplace=True)
    #分类正样本总数统计
    posInsCount = targetDF[targetDF['label']==1].groupby([t1,t2]).count()
    posInsCount.reset_index(inplace=True)

    temp=merge(allCount,posInsCount,on=[t1,t2],how='left')
    temp.rename(columns={"label_x":"sum","label_y":"posSum"},inplace=True)
    temp["ratio"]=temp.apply(lambda x : float(x['posSum'])/x['sum'],axis='columns')
    return temp

# oriData=read_csv('../data/m_p_u_amc.csv')
# print doublePosRatio(oriData,'appPlatform','appCategory')

#按照列targetCol的正负样本分布进行子采样
def subsample(ratio=0.2,targetCol='appID',fileaddr='../data/mergeAll.csv'):
    oriData=read_csv(fileaddr)
    resultIndex=[]
    for x in oriData.groupby(targetCol).count().index:
        xData=oriData[oriData[targetCol]==x]
        posX=xData[ xData['label']==1 ]
        posNum=int(len(posX)*ratio)
        if posNum>0:
            resultIndex.extend( posX.sample(posNum).index.tolist() )
        negX=xData[ xData['label']==0 ]
        negNum=int(len(negX)*ratio)   #仍然采用相乘的方式，避免比正样本多采
        if negNum>0:
            resultIndex.extend( negX.sample(negNum).index.tolist() )
    targetaddr= fileaddr[0:-4]+'-sub-'+targetCol+'-'+str(ratio)+'.csv'
    oriData.loc[resultIndex].to_csv(targetaddr, index=False)
    print len(oriData),len(resultIndex),len(oriData)*ratio

#subsample(ratio=0.2,targetCol='appID',fileaddr='../data/m_p_u_amc.csv')

def zipsubmmit(data,name):
    data.to_csv('../subdata/submission.csv')
    with zipfile.ZipFile(name+'.zip','w') as fout:
        fout.write('submission.csv',compress_type=zipfile.ZIP_DEFLATED)
    cmd = 'rm ../subdata/submission.csv'
    subprocess.call(cmd, shell=True)

def statHourConvRatio(dayData,day=300000):
    #a=ori[ (ori['clickTime']<310000) & (ori['clickTime']>300000) ]
    #float(a[a['label']==1 ].size)/(a[a['label']==0 ].size)
    #
    def convRatio(hd):
        total=(hd[hd['label']==0 ].size)
        if total==0:
            return 0
        else: return float(hd[hd['label']==1 ].size)/total
    allStat={}
    h=0
    for h in xrange(100,2500,100):
        beforeTime=day+h
        cudata = dayData[ dayData['clickTime']< beforeTime ]
        conv = convRatio(cudata)
        allStat[beforeTime]=conv
        print str(beforeTime),conv
        del cudata
    return allStat

def statDayConvRatio(data,start=170000):
    #oristat=statDayConvRatio(ori)
    #np.mean(oristat.values())
    def convRatio(hd):
        total=(hd[hd['label']==0 ].size)
        if total==0:
            return 0
        else: return float(hd[hd['label']==1 ].size)/total
    allStat={}
    for d in xrange(10000,150000,10000):
        beforeTime=start+d
        cudata = data[ (data['clickTime']< beforeTime) &  (data['clickTime']>=beforeTime-10000)]
        conv = convRatio(cudata)
        allStat[( (beforeTime/10000) -1)]=conv
        print str( (beforeTime/10000) -1),conv
        del cudata
    return allStat

def dayCount(data):
    start=170000
    for d in xrange(10000,150000,10000):
        beforeTime=start+d
        cudata = data[ (data['clickTime']< beforeTime) &  (data['clickTime']>= beforeTime-10000)]
        stat = cudata.size
        print str( (beforeTime/10000) -1),stat
        del cudata

def sampleTrainByTest(trainFile='../data/m_p_u_amc.csv',testFile='../data/test_m_p_u_amc.csv',
                      considerFeat=['adID']):#onsiderFeat=['positionID','adID','camgaignID']
    train=read_csv(trainFile) ; test=read_csv(testFile)
    indexSet=set()

    kvStringSet=set()
    for item_i,v in test.iterrows():
        kvList=[]
        for col_i in xrange(0,len(considerFeat)):
            kvList.append(str(col_i) + ':' + str( int( v[considerFeat[col_i] ]) )  )
        kvStringSet.add(','.join(kvList))

    print len(kvStringSet)

    for item_i,v in train.iterrows():
        kvList=[]
        for col_i in xrange(0,len(considerFeat)):
            kvList.append(str(col_i) + ':' + str( int( v[considerFeat[col_i] ]) )  )
        rowkvString=','.join(kvList)
        if rowkvString in kvStringSet:
            indexSet.add(item_i)
    print len(indexSet),len(train)
    return train.loc[indexSet]

#测试集中出现的训练集中未出现的 联立特征
def combNewInTest(trainFile='../data/m_p_u_amc.csv',testFile='../data/test_m_p_u_amc.csv',
                      considerFeat=['adID','positionID']): # considerFeat=['positionID','adID','camgaignID']
    train=read_csv(trainFile) ; test=read_csv(testFile)
    indexSet=set()
    kvStringSet=set()
    for item_i,v in train.iterrows():
        kvList=[]
        for col_i in xrange(0,len(considerFeat)):
            kvList.append(str(col_i) + ':' + str( int( v[considerFeat[col_i] ]) )  )
        kvStringSet.add(','.join(kvList))

    print len(kvStringSet)

    for item_i,v in test.iterrows():
        kvList=[]
        for col_i in xrange(0,len(considerFeat)):
            kvList.append(str(col_i) + ':' + str( int( v[considerFeat[col_i] ]) )  )
        rowkvString=','.join(kvList)
        if rowkvString not in kvStringSet:
            indexSet.add(item_i)

    print len(indexSet),len(test)
    return test.loc[indexSet],test.loc[oldIndexSet]

# considerFeat=['positionID']
# sampleTrainByTest(considerFeat=considerFeat)\
#     .to_csv('../data/sampleTrainByTest_{feat}.csv'.format(feat=''.join(considerFeat) ),index=False)

#测试集中出现的训练集中未出现的id
def singleAllNewInTest(trainFile='../data/m_p_u_amc.csv',testFile='../data/test_m_p_u_amc.csv'):
    train=read_csv(trainFile) ; test=read_csv(testFile)
    mayField=['positionID', 'adID', 'camgaignID', 'advertiserID', 'appID', 'appCategory' ]
    resultDict={}
    allNewIndexSet=set()
    for field in mayField:
        setTrain = set(train[field].unique().tolist())
        setTest  = set(test[field].unique().tolist())
        newInSet = setTest - (setTest&setTrain)
        count=0
        for i,v in test.iterrows():
            if v[field] in newInSet:
                count+=1
                allNewIndexSet.add(i)
        print field,len(setTrain),len(newInSet),count
    print len(allNewIndexSet)
    oriIndexSet=set(test.index.tolist())
    # test.loc[allNewIndexSet].to_csv('../data/newInTest.csv',index=False)
    # test.loc[oriIndexSet-allNewIndexSet].to_csv('../data/otherInTest.csv',index=False)
    #return allNewIndexSet


def dropLast(trainFile='../data/m_p_u_amc.csv',dropTime=301700):
    train=read_csv(trainFile) ;
    return train[train['clickTime']<301600]

def recentData(trainFile='',startTime=200000):
    train=read_csv(trainFile) ;
    return train[train['clickTime']>startTime]

recentData('../data/train_eliminated.csv').to_csv('../data/train_eliminated_recent20.csv',index=False)

def selectDay(trainFile='../data/m_p_u_amc.csv',exceptDay=[190000]):
    train=read_csv(trainFile) ;
    allIndex=[]
    for ed in xrange(170000,310000,10000):
        if ed not in exceptDay:
            allIndex.extend( train[ (train['clickTime']>=ed) & (train['clickTime']<ed+10000)].index.tolist() )
    print len(allIndex),len(train)
    return train.loc[allIndex]

# newTrain=recentData()
# newTrain.to_csv('../data/recentData_20.csv',index=False)

def dropPreservePos():
    dropIndexSet=set()