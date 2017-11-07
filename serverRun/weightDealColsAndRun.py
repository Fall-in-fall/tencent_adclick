#--coding:utf-8--
from pandas import *

def divTime(data): #返回以30分钟为单位的时间差的负数
    conv=str(int(data['conversionTime'])) ; click=str(int(data['clickTime']))
    if conv=='0':
        return 0
    minute=( int(conv[4:6])- int(click[4:6]) )/30+1
    ys = 48*( int(conv[0:2])- int(click[0:2]) )+\
               2*( int(conv[2:4]) - int(click[2:4]) )+ minute
    if ys==0:
        raise Exception('error divTime!')
    return float(-ys)

def genWeight(df):
    weight = ( df[ ['clickTime','conversionTime'] ].fillna( 0 ) )\
        .apply( lambda x:divTime(x) , axis='columns' )
    #weight = scaleMap(weight.replace( 0,weight.min() ),1,2)
    weight=innerEqualScaleWeight(weight)
    return weight

def innerEqualScaleWeight(data):
    from math import sqrt
    posSampleMin=data[data!=0].min()
    #权值转换，负样本保持0，正样本取对数降低比例差距
    if posSampleMin.min()<0:  #如果权值是负数将负数权值处理为正数权值，最小权值为1，并且保持权值之间的大小比例不变
        newdata = data.apply(lambda x:0 if x==0 else sqrt( posSampleMin / float(x)) )
    else:
        newdata = data.apply(lambda x:0 if x==0 else sqrt(float(x) / posSampleMin) )
    #正样本总权值=正样本总数*1 (总权值保持不变)
    print 'max and min',newdata.max(),newdata[newdata!=0].min()
    total_weight=newdata[newdata!=0].count()
    print 'total_weight',total_weight
    #单位权值
    unitWeight = total_weight/newdata.sum()
    print 'unitWeight',unitWeight
    return newdata.apply(lambda x: unitWeight*x if  x!=0 else 1)

def weightDealColsAndRun(istry=False):
    #,nrows=1000
    if istry:
        train = read_csv('../data/m_p_u_amc.csv',nrows=50000)
        test = read_csv('../data/test_m_p_u_amc.csv',nrows=50000)
    else:
        train = read_csv('../data/m_p_u_amc.csv')
        test = read_csv('../data/test_m_p_u_amc.csv')
    weight=genWeight(train)
    if istry:
        print weight[weight!=1]
        max=weight.max(); min=weight.min()
        print '0.24',weight[(weight<0.24)&(weight!=1)].count()
        print '1.4',weight[weight>1.4].count()
        print weight[weight!=1].count()

    def ageMap(age):
        if age<=5: return 5
        elif age<=12: return 12
        elif age<=15: return 15
        elif age<=18: return 18
        elif age<=23: return 23
        elif age<=26: return 26
        elif age<=30: return 30
        elif age<=35: return 35
        elif age<=40: return 40
        elif age<=50: return 50
        elif age<=60: return 60
        else: return 80

    train['age'] = train['age'].map(lambda x: ageMap(x) )
    test['age'] = test['age'].map(lambda x: ageMap(x)   )

    cate_features=['connectionType','telecomsOperator','sitesetID','positionType',
               'age','gender','education','marriageStatus','haveBaby',
               #'hometown','residence',  'adID',
                   'camgaignID',
                   'advertiserID','appID',
               'appPlatform' ,'appCategory'
               ]
    print 'get_dummies train'
    dumtrain=get_dummies(train,columns = cate_features)
    print 'get_dummies test'
    dumtest=get_dummies(test,columns = cate_features)

    trainCols=dumtrain.columns ; testCols=dumtest.columns

    for traincol in trainCols:
        if traincol not in testCols:
            del dumtrain[traincol]

    for testcol in testCols:
        if testcol not in trainCols:
            del dumtest[testcol]

    trainCols=dumtrain.columns ; testCols=dumtest.columns
    if len(trainCols)!=len(testCols):
        raise Exception(str(len(trainCols))+'!='+str(len(testCols)))
    for i in xrange(0,len(trainCols)):
        if trainCols[i]!=testCols[i]:
            raise Exception(trainCols[i]+'!='+testCols[i])
    print len(trainCols)

    testInstanceId=test['instanceID']
    labelset=train['label']
    dumtest['instanceID'] = testInstanceId

    del train,test
    del dumtrain['label'],dumtest['label'],dumtest['instanceID']
    trainset=dumtrain.as_matrix()
    testset=dumtest.as_matrix()
    del dumtrain,dumtest

    #标准化
    from sklearn.preprocessing import StandardScaler
    sdscaler = StandardScaler()
    sd_trainset=sdscaler.fit_transform(trainset)
    sd_testset=sdscaler.transform(testset)
    del trainset,testset

    print 'fit and predict'
    from sklearn.linear_model import LogisticRegression
    logitre=LogisticRegression()
    logitre.fit(sd_trainset,labelset,sample_weight=weight)
    if logitre.classes_[1]==1:prob = logitre.predict_proba(sd_testset)[:,1]
    else: prob = logitre.predict_proba(sd_testset)[:,0]

    print len(testInstanceId),len(prob)
    resultDF=DataFrame() ; resultDF['instanceID']=testInstanceId ; resultDF['prob']=prob
    import datetime ; timestr=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    preName='try_weight_sd_smallResult'if istry else 'weight_sd_smallResult'
    resultDF.to_csv('../submit/'+preName+'_'+timestr+'.csv',index=False)

weightDealColsAndRun(False)