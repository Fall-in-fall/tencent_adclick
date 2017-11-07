#--coding:utf-8--
from pandas import *
# D:/workspace/PycharmProjects/a/tencent_adclick/data/
import numpy as np

#合并user,ad,position中的特征到同一个文件
def m_p_u_amc():

    #-------------generate m_p_u_amc test csv
    user=read_csv('../data/user.csv')
    ad=read_csv('../data/ad.csv') ; app_categories=read_csv('../data/app_categories.csv')
    ad_merge_cate=merge(ad,app_categories,on='appID',how='left')
    position=read_csv('../data/position.csv')

    trainCSV = read_csv('../data/train.csv')
    testCSV = read_csv('../data/test.csv')

    #-------to train csv
    m_p = merge(trainCSV,position,on='positionID',how='left')
    m_p_u = merge(m_p,user,on='userID',how='left')
    m_p_u_amc = merge(m_p_u,ad_merge_cate,on='creativeID',how='left')
    m_p_u_amc.to_csv('../data/m_p_u_amc.csv',index=False)
    #-------to test csv
    test_m_p = merge(testCSV,position,on='positionID',how='left')
    test_m_p_u = merge(test_m_p,user,on='userID',how='left')
    test_m_p_u_amc = merge(test_m_p_u,ad_merge_cate,on='creativeID',how='left')
    test_m_p_u_amc.to_csv('../data/test_m_p_u_amc.csv',index=False)

#部分取值较少的特征onehot化
def onehot_m_p_u_amc():
    train = read_csv('../data/m_p_u_amc.csv')
    test = read_csv('../data/test_m_p_u_amc.csv')
    cate_features=['connectionType','telecomsOperator','sitesetID','positionType',
               'gender','education','marriageStatus','haveBaby',
               #hometown,residence,camgaignID,advertiserID,appID 数值太稀疏待处理
               'appPlatform' #,appCategory 数值太稀疏待处理
               ]
    get_dummies(train,columns = cate_features).to_csv('../data/onehot_'+'m_p_u_amc'+'.csv',index=False)
    get_dummies(test,columns = cate_features).to_csv('../data/onehot_'+'test_m_p_u_amc'+'.csv',index=False)

#丢掉最后一天的数据
def cut_onehot_And_m_p_u_amc():
    # 1513m约等于25h，所以直接丢掉最后一天  #probConvTime4=1513 # 转化时间分钟95%位置
    def cutLastTrain(data,name,cutTime=300000):
        data['conversionTime']=data['conversionTime'].fillna( 0 )
        data['conversionTime'].astype(np.int)
        data['clickTime'].astype(np.int)

        cut_data = data[
            (data['conversionTime']!=0) |
            (data['clickTime']<cutTime) ] #!(a&b) = !a|!b   注意单个条件都要加括号，因为&优先级低会造成歧义
        cut_data.to_csv('../data/cut_' + name + '.csv',index=False)
    cutLastTrain( read_csv('../data/m_p_u_amc.csv') ,'m_p_u_amc')
    cutLastTrain( read_csv('../data/onehot_m_p_u_amc.csv') ,'onehot_m_p_u_amc')

#所有特征onehot化，爆掉
def allonehot_m_p_u_amc():
    train = read_csv('../data/m_p_u_amc.csv')
    test = read_csv('../data/test_m_p_u_amc.csv')
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
               'hometown','residence',  'adID',
                   'camgaignID','advertiserID','appID',
               'appPlatform' ,'appCategory'
               ]
    get_dummies(train,columns = cate_features).to_csv('../data/allonehot_'+'m_p_u_amc'+'.csv',index=False)
    get_dummies(test,columns = cate_features).to_csv('../data/allonehot_'+'test_m_p_u_amc'+'.csv',index=False)

#部分取值较少的特征onehot化
def small_allonehot_m_p_u_amc():
    train = read_csv('../data/m_p_u_amc.csv')
    test = read_csv('../data/test_m_p_u_amc.csv')
    def ageMap(age):
        if age<=5: return 0 # 有改动 5->0
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
    get_dummies(train,columns = cate_features).to_csv('../data/small_allonehot_'+'m_p_u_amc'+'.csv',index=False)
    print 'get_dummies test'
    get_dummies(test,columns = cate_features).to_csv('../data/small_allonehot_'+'test_m_p_u_amc'+'.csv',index=False)

#deprecated
def sdAppNumAndFlag():
    onehottrain = read_csv('../data/dealCols_small_allonehot_m_p_u_amc.csv')
    onehottest = read_csv('../data/dealCols_small_allonehot_test_m_p_u_amc.csv')
    appNum = read_csv('../data/user_appNum.csv')
    mean=appNum['appNum'].mean() ; std=appNum['appNum'].std()
    appNum['appNum'] = appNum['appNum'].apply(lambda x: float(x-mean)/std if x >0 else 0)

    appNum_onehot_m_p_u_amc=merge(onehottrain,appNum,on='userID',how='left')
    appNum_onehot_m_p_u_amc['appNum']=appNum_onehot_m_p_u_amc['appNum'].fillna(0)
    # 这样实际上有小bug。标准化后如果原值等于均值则转换后值为0，缺失值也值为0。这样实际上是默认缺失的appNum用均值填补了。
    isNoNum = appNum_onehot_m_p_u_amc['appNum'].apply(lambda x:0 if x!=0 else 1)
    appNum_onehot_m_p_u_amc['isNoNum']=isNoNum
    appNum_onehot_m_p_u_amc.to_csv('../data/appNumAndFlag_dealCols_small_allonehot_m_p_u_amc.csv',index=False)


    appNum_onehot_test_m_p_u_amc=merge(onehottest,appNum,on='userID',how='left')
    appNum_onehot_test_m_p_u_amc['appNum']=appNum_onehot_test_m_p_u_amc['appNum'].fillna(0)
    test_isNoNum = appNum_onehot_test_m_p_u_amc['appNum'].apply(lambda x:0 if x!=0 else 1)
    appNum_onehot_test_m_p_u_amc['isNoNum']=test_isNoNum
    appNum_onehot_test_m_p_u_amc.to_csv('../data/appNumAndFlag_dealCols_small_allonehot_test_m_p_u_amc.csv',index=False)

#deprecated
def dealColsAndRunOnly01(istry=False):
    if istry:
        train = read_csv('../data/m_p_u_amc.csv',nrows=1500)
        test = read_csv('../data/test_m_p_u_amc.csv',nrows=1500)
    else:
        train = read_csv('../data/m_p_u_amc.csv')
        test = read_csv('../data/test_m_p_u_amc.csv')
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
    prefix='try_'if istry else ''
    #dumtrain.to_csv('../data/'+prefix+'dealCols_small_allonehot_m_p_u_amc.csv',index=False)
    #dumtest.to_csv('../data/'+prefix+'dealCols_small_allonehot_test_m_p_u_amc.csv',index=False)

    del train,test
    del dumtrain['label'],dumtest['label'],dumtest['instanceID']

    #以下运行只选取转换过的01特征，之前的temprun没有去掉这些特征,themodel里面是去掉了后面3个的，
    #所以之前标准化影响很大，而没有去掉的ID特征标准化本身就没啥意义
    # 在dealCol过程中应该删除的包括 clickTime，conversionTime
    for delcol in ['hometown','residence', 'adID',       'positionID','userID', 'creativeID'   ]:
        del dumtrain[delcol ],dumtest[delcol] #去掉非01特征

    trainset=dumtrain.as_matrix()
    testset=dumtest.as_matrix()
    del dumtrain,dumtest


    print 'fit and predict'
    from sklearn.linear_model import LogisticRegression
    logitre=LogisticRegression()
    logitre.fit(trainset,labelset)
    if logitre.classes_[1]==1:prob = logitre.predict_proba(testset)[:,1]
    else: prob = logitre.predict_proba(testset)[:,0]

    resultDF=DataFrame() ; resultDF['instanceID']=testInstanceId ; resultDF['prob']=prob
    import datetime ; timestr=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    preName='only01_smallResult'
    resultDF.to_csv('../submit/'+prefix+preName+'_'+timestr+'.csv',index=False)

#deprecated
def dealColsAndRun():
    #,nrows=1000
    train = read_csv('../data/m_p_u_amc.csv')
    test = read_csv('../data/test_m_p_u_amc.csv')

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
    dumtest.to_csv('../data/dealCols_small_allonehot_test_m_p_u_amc.csv',index=False)
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
    logitre.fit(sd_trainset,labelset)
    if logitre.classes_[1]==1:prob = logitre.predict_proba(sd_testset)[:,1]
    else: prob = logitre.predict_proba(sd_testset)[:,0]

    print len(testInstanceId),len(prob)
    resultDF=DataFrame() ; resultDF['instanceID']=testInstanceId ; resultDF['prob']=prob
    import datetime ; timestr=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    preName='sd_smallResult'
    resultDF.to_csv('../submit/'+preName+'_'+timestr+'.csv',index=False)

#deprecated
def appNumAndFlag_small_onehot_m_p_u_amc(istry=False):
    #,nrows=1000
    if istry:
        train = read_csv('../data/m_p_u_amc.csv',nrows=1000)
        test = read_csv('../data/test_m_p_u_amc.csv',nrows=1000)
    else:
        train = read_csv('../data/m_p_u_amc.csv')
        test = read_csv('../data/test_m_p_u_amc.csv')
    appNum = read_csv('../data/user_appNum.csv')

    train = merge(train,appNum,on='userID',how='left')
    train['appNum']=train['appNum'].fillna(0)
    train_isNoNum = train['appNum'].apply(lambda x:0 if x!=0 else 1)
    train['isNoNum'] = train_isNoNum

    test = merge(test,appNum,on='userID',how='left')
    test['appNum']=test['appNum'].fillna(0)
    test_isNoNum = test['appNum'].apply(lambda x:0 if x!=0 else 1)
    test['isNoNum'] = test_isNoNum

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
    #dumtest['instanceID'] = testInstanceId
    #--------------
    del train,test
    del dumtrain['label'],dumtest['label']  #,dumtest['instanceID']
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
    logitre.fit(sd_trainset,labelset)
    if logitre.classes_[1]==1:prob = logitre.predict_proba(sd_testset)[:,1]
    else: prob = logitre.predict_proba(sd_testset)[:,0]

    print len(testInstanceId),len(prob)
    resultDF=DataFrame() ; resultDF['instanceID']=testInstanceId ; resultDF['prob']=prob
    import datetime ; timestr=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    preName='try_appNumAndFlag_sd_smallResult' if istry else 'appNumAndFlag_sd_smallResult'
    resultDF.to_csv('../submit/'+preName+'_'+timestr+'.csv',index=False)


# 增加cate的一级特征-done
# 返回cate_level_1,cate_level_2
def appCateFeature():
    appCate=read_csv('../data/app_categories.csv')
    def fill(x):
        x=str(x) ; return x+'0'*(3-len(x))
    appCate['cate_level_1']=appCate['appCategory'].apply(lambda x: int(fill(x)[0]))
    appCate['cate_level_2']=appCate['appCategory'].apply(lambda x: int(fill(x)) )
    del appCate['appCategory']
    appCate.to_csv('../data/2level_app_categories.csv',index=False)

#done安装app总数，安装最多的一级类目,二级类目(如果没有明显多的就置0)-#只返回类别下app数大于1，并且app数并列最大的不超过2个，否则视为没有特别偏好，返回0
#返回appSum，fav_cate_1，fav_cate_2

def installedAppFeature(istry=False):
    if istry:
        instApp=read_csv('../data/user_installedapps.csv',nrows=10000)
    else:
        instApp=read_csv('../data/user_installedapps.csv')
    #appSum
    appSum=instApp.groupby('userID').count()
    appSum.reset_index(inplace=True)
    appSum.rename(columns={'appID':'appSum'}, inplace = True)
    def maxNum(arr): #maxNum([1,2,3,4,5,7,0,1,5,4])
        stat={}
        for i in arr:
            if not stat.has_key(i):
                stat[i]=1
            else: stat[i]=stat[i]+1
        if stat.has_key(0): del stat[0]
        maxKey=0 ; maxVal=0 ;cuMaxCount=0
        for x in stat.items():
            if x[1]>maxVal:
                maxKey=x[0] ; maxVal=x[1] ;cuMaxCount=0
            elif x[1]==maxVal:
                cuMaxCount+=1
        #传入的类别只有0的会被删除并且最终返回0
        #print maxVal,cuMaxCount,len(arr),float(cuMaxCount)/len(arr)
        #return maxKey,maxVal,cuMaxCount,len(arr),float(maxVal)/len(arr),float(cuMaxCount)/len(arr)
        # maxVal=userCate1['cate_level_1'].apply(lambda x: int(x[1:-1].split(',')[1]))
        #只返回类别下app数大于1，并且app数并列最大的不超过2个，否则视为没有特别偏好，返回0
        return maxKey  if maxVal>1 and cuMaxCount<3 else 0

    #fav_cate_1
    appLevelCate=read_csv('../data/2level_app_categories.csv')
    userCate1=merge(instApp,appLevelCate,on='appID',how='left')[ ['userID','cate_level_1'] ].\
        groupby('userID').agg(maxNum)
    userCate1.reset_index(inplace=True)
    userCate1.rename(columns={'cate_level_1':'fav_cate_1'},inplace=True)
    #fav_cate_2
    oriCate=read_csv('../data/app_categories.csv')
    userCate2 = merge(instApp,oriCate,on='appID',how='left')[['userID','appCategory']].\
        groupby('userID').agg(maxNum)
    userCate2.reset_index(inplace=True)
    userCate2.rename(columns={'appCategory':'fav_cate_2'},inplace=True)
    # userCate2['ready_cate'] = mInstCate[ ['cate_level_1','cate_level_2'] ].apply(lambda x: 0 if x['cate_level_2']==0 else \
    #     int(str(x['cate_level_1'])  +'0'*(2-len(str(x['cate_level_2']))  ) + str(x['cate_level_2']) ),axis ='columns' )

    temp=merge(appSum,userCate1,on='userID',how='left')
    temp=merge(temp,userCate2,on='userID',how='left')
    #appSum.to_csv('../data/userFavCate.csv',index=False)
    return temp
# 最近30天安装总数，最近安装时间(第几天)，最近安装app的一级和二级类别共四个个特征
# 使用特征时缺失值应置为0,并增加缺失标志位
# 返回actionSum,recentDay,recent_level_1,recent_level_2
def appActionFeature(istry=False):
    if istry:
        actions = read_csv('../data/user_app_actions.csv',nrows=10000)
    else:
        actions = read_csv('../data/user_app_actions.csv')
    appCate = read_csv('../data/app_categories.csv')
    oneLevelCate = read_csv('../data/2level_app_categories.csv')

    actions = merge(actions,oneLevelCate,on='appID',how='left')
    actions = merge(actions,appCate,on='appID',how='left')
    del actions['cate_level_2'],appCate,oneLevelCate

    timeDay = range(17,32,1)
    resultList=[]
    #final=DataFrame(columns=['beforeDay','userID','actionSum','recentDay','recent_level_1','recent_level_2'])

    def constructFeature(beforeDay, actions):
        userIDgroup=actions.groupby('userID')
        #最近总行为数
        _actSum = userIDgroup.count().reset_index()[['userID','appID']]
        _actSum.rename(columns={'appID':'actSum'},inplace=True)

        _otherFeatures=userIDgroup.agg(lambda x:x.iloc[-1]).reset_index()
        _otherFeatures['installTime']=_otherFeatures['installTime'].apply(lambda x: int(str(x)[0]) if len(str(x))<6 else int(str(x)[0:2]))
        _otherFeatures.rename(columns={'installTime':'recentDay','cate_level_1':'recent_level_1','appCategory':'recent_level_2'},inplace=True)
        #不要忘了beforeDay特征
        _otherFeatures['beforeDay']=beforeDay

        return merge( _actSum, _otherFeatures,on='userID',how='left').\
            reindex( columns=['beforeDay','userID','actSum','recentDay','recent_level_1','recent_level_2'])
        # maxInsTime = userIDgroup.max().reset_index()[['userID','installTime']]
        # maxInsTime.rename(columns={'installTime':'maxInsTime'},inplace=True)
        #最近行为时间(天)
        # _recentDay = DataFrame() ; _recentDay['userID'] = maxInsTime['userID']
        # _recentDay['recentDay'] = maxInsTime['maxInsTime'].apply(lambda x: int(str(x)[0]) if len(str(x))<6 else int(str(x)[0:2]) )
        #数据默认按时间排序，所以返回group最后一行。否则要寻找最大time所在行
        #_cateLevel=userIDgroup.agg(lambda x:x.iloc[-1])[['userID','cate_level_1','appCategory']]
        # _cateLevel=merge(actions,maxInsTime,on='userID',how='left')
        # _cateLevel['isMax']=_cateLevel.apply(lambda x:1 if x['installTime']==x['maxInsTime'] else 0,axis ='columns')
        # _cateLevel[_cateLevel['isMax']==1][['userID','cate_level_1','appCategory']]

        # temp=merge(_actSum,_recentDay,on='userID',how='left')
        # temp=merge(temp,_cateLevel,on='userID',how='left')

    for day in timeDay:
        resultList.append( constructFeature( day,actions[ actions['installTime']<(day*10000) ] )  )
    #将特征加入训练数据方法，备用
    def actFeatureMerge2train(train,actionFeatures):
        train['beforeDay']=train['clickTime'].apply(lambda x:int(str(x)[0:2]))
        merge(train,actionFeatures,on=['userID','beforeDay'],how='left' )
    #trainBase = read_csv('../data/train.csv')[['userID','clickTime']]
    #actFeatureMerge2train(trainBase,actionFeatures)

    return concat(resultList)

#转换clickTime只取小时信息为特征
def clicHourFeature(addr):
    train = read_csv(addr)
    train['hourTime']=train['clickTime'].apply(lambda x: int(str(x)[2:4])+1)

#合并appCateFeature，installedAppFeature，appActionFeature，clicHourFeature合并到m_p_u_amc
#m_p_u_amc，test_m_p_u_amc改名为joinTrain，joinTest
def mergeAll(istry=False):
    if istry:
        trainAll=read_csv('../data/joinTrain.csv',nrows=10000)
    else:
        trainAll=read_csv('../data/joinTrain.csv')
    testAll=read_csv('../data/joinTest.csv')
    del trainAll['appCategory'],testAll['appCategory']

    #2levelCate_feature
    appCate = read_csv('../data/2level_app_categories.csv')
    trainAll = merge(trainAll,appCate, on='appID', how='left' )
    testAll = merge(testAll,appCate, on='appID', how='left' )
    del appCate

    #installed_feature
    installed_feature=  read_csv('../data/userFavCate.csv') #installedAppFeature(istry)
    trainAll = merge(trainAll,installed_feature, on='userID', how='left' )
    testAll = merge(testAll,installed_feature, on='userID', how='left' )

    del installed_feature
    #act_features
    act_features= read_csv('../data/appActionFeature.csv')  #appActionFeature(istry)
    trainAll['beforeDay']=trainAll['clickTime'].apply(lambda x:int(str(x)[0:2]))
    trainAll=merge(trainAll,act_features,on=['userID','beforeDay'],how='left' )

    testAll['beforeDay']=testAll['clickTime'].apply(lambda x:int(str(x)[0:2]))
    testAll = merge(testAll,act_features,on=['userID','beforeDay'],how='left' )

    del trainAll['beforeDay'],testAll['beforeDay']
    del act_features
    
    #click_hour_feature 返回一天的点击在第几个小时，1-24
    trainAll['hourTime']=trainAll['clickTime'].apply(lambda x: int(str(x)[2:4])+1)
    testAll['hourTime']=testAll['clickTime'].apply(lambda x: int(str(x)[2:4])+1)

    trainAll.to_csv('../data/mergeAll.csv',index=False)
    testAll.to_csv('../data/test_mergeAll.csv',index=False)

# appCateFeature()#生成'../data/2level_app_categories.csv'
# installedAppFeature().to_csv('../data/userFavCate.csv',index=False)
# appActionFeature().to_csv('../data/appActionFeature.csv',index=False)
#istry参数
mergeAll(False)


