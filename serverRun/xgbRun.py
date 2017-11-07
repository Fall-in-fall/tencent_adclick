#--coding:utf-8--
from pandas import *
import xgboost as xgb


def xgbGridMpuamc(istry=False):
    print 'loading data'
    if istry:
        train = read_csv('../data/m_p_u_amc.csv',nrows=1000)
        test = read_csv('../data/test_m_p_u_amc.csv',nrows=1000)
    else:
        train = read_csv('../data/m_p_u_amc.csv')
        test = read_csv('../data/test_m_p_u_amc.csv')
    #处理数据
    print 'processing data'
    instanceIDSet = test['instanceID']  ;  labelset=train['label']
    delTrainCols = ['conversionTime','positionID','userID', 'creativeID','label']
    delTestCols =  ['instanceID',    'positionID','userID', 'creativeID','label']
    for i in delTrainCols: del train[i]
    for j in delTestCols: del test[j]
    #colTemdel=['hometown','residence',]
    #验证train和test列是否对应
    trainCols=train.columns ; testCols=test.columns
    if len(trainCols)!=len(testCols):
        raise Exception(str(len(trainCols))+'!='+str(len(testCols)))
    for i in xrange(0,len(trainCols)):
        if trainCols[i]!=testCols[i]:
            raise Exception(trainCols[i]+'!='+testCols[i])
    print trainCols

    #拟合，网格搜索
    print 'fit and predict' ; from sklearn.model_selection import GridSearchCV
    print "start gridSerach.."  ;
    turned_parameter1={'n_estimators':[60,80,100,120,150,200],'learning_rate':[0.01,0.02,0.05,0.08,0.1]}
    gs1=GridSearchCV(xgb.XGBClassifier(),turned_parameter1,cv=11,scoring="neg_log_loss")
    gs1.fit(train,labelset)
    print 'n_estimators and learning_rate best:',(gs1.best_params_)
    turned_parameter2={ 'max_depth':[4,6,8,10,12,15]}
    gs2=GridSearchCV(xgb.XGBClassifier(**gs1.best_params_),turned_parameter2,cv=11,scoring="neg_log_loss")
    gs2.fit(train,labelset)
    print 'max_depth best: ',(gs2.best_params_)

    finalPara=gs1.best_params_.copy() ; finalPara.update(gs2.best_params_)
    print 'finalPara: ',finalPara
    xgblogitre=xgb.XGBClassifier(**finalPara)
    xgblogitre.fit(train,labelset)

    #预测，写入文件
    if xgblogitre.classes_[1]==1:prob = xgblogitre.predict_proba(test)[:,1]
    else: prob = xgblogitre.predict_proba(test)[:,0]
    resultDF=DataFrame() ; resultDF['instanceID']=instanceIDSet ; resultDF['prob']=prob
    import datetime ; timestr=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    preName='try_xgb_grid_mpuamc'if istry else 'xgb_grid_mpuamc'
    resultDF.to_csv('../submit/'+preName+'_'+timestr+'.csv',index=False)

def xgbIniAppNum(istry=False):
    print 'loading data'
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

    #处理数据
    print 'processing data'
    instanceIDSet = test['instanceID']  ;  labelset=train['label']
    delTrainCols = ['conversionTime','positionID','userID', 'creativeID','label']
    delTestCols =  ['instanceID',    'positionID','userID', 'creativeID','label']
    for i in delTrainCols: del train[i]
    for j in delTestCols: del test[j]
    #colTemdel=['hometown','residence',]
    #验证train和test列是否对应
    trainCols=train.columns ; testCols=test.columns
    if len(trainCols)!=len(testCols):
        raise Exception(str(len(trainCols))+'!='+str(len(testCols)))
    for i in xrange(0,len(trainCols)):
        if trainCols[i]!=testCols[i]:
            raise Exception(trainCols[i]+'!='+testCols[i])
    print trainCols
    #----
    xgblogitre=xgb.XGBClassifier()
    xgblogitre.fit(train,labelset)
    #预测，写入文件
    if xgblogitre.classes_[1]==1:prob = xgblogitre.predict_proba(test)[:,1]
    else: prob = xgblogitre.predict_proba(test)[:,0]
    resultDF=DataFrame() ; resultDF['instanceID']=instanceIDSet ; resultDF['prob']=prob
    import datetime ; timestr=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    preName='try_xgb_appNumc'if istry else 'xgb_appNumc'
    resultDF.to_csv('../submit/'+preName+'_'+timestr+'.csv',index=False)