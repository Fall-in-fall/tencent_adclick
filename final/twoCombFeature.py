# -*- encoding:utf-8 -*-
from pandas import *
import xgboost as xgb
import collections
import matplotlib.pylab as plt

def genTowoComb(addr,testAddr,field):
    # 为特征值建立编号
    tableDict= collections.defaultdict(lambda: {})
    def getIndices(col,key,isTest=False):
        if tableDict.get(col) is None:
            tableDict[col]=collections.defaultdict(lambda: 0)
        table=tableDict.get(col)
        indices = table.get(key)
        if indices is None:
            if isTest:
                indices=0
            else:
                indices = len(table)+1
                table[key] = indices
        return indices

    data=read_csv(addr)
    testData=read_csv(testAddr)
    #------------------------process train data---------------------------
    oriCols=data.columns.tolist()
    oriCols.remove('label')
    for x in xrange(0,len(field)-1):
        for y in xrange(x+1,len(field)):
            c1=field[x] ; c2=field[y]
            data[c1+'_'+c2] = data.apply(lambda x: getIndices(c1+'_'+c2, str(int(x[c1]))+'_'+str(int(x[c2])) ,False), axis='columns')
    for col in oriCols:
        del data[col]
    print len(data.columns) 
    data.to_csv(addr[0:-4]+'_only11twoComb'+'.csv',index=False)

    #--------------------process testDat----------------------------------
    testOriCols=testData.columns.tolist()
    testOriCols.remove('instanceID') ; testOriCols.remove('label')
    for m in xrange(0,len(field)-1):
        for n in xrange(m+1,len(field)):
            c1=field[m] ; c2=field[n]
            testData[c1+'_'+c2] = testData.apply(lambda x: getIndices(c1+'_'+c2, str(int(x[c1]))+'_'+str(int(x[c2])) ,True), axis='columns')
    for tcol in testOriCols:
        del testData[tcol]
    print len(testData.columns)
    testData.to_csv(testAddr[0:-4]+'_only11twoComb'+'.csv',index=False)

def genFile():
    train='../data/m_p_u_amc.csv'
    test='../data/test_m_p_u_amc.csv'
    field=['positionID', 'connectionType', 'telecomsOperator', 'positionType', 'gender','education',
            'adID', 'camgaignID','advertiserID', 'appID', 'appCategory']
    genTowoComb(train,test,field)

def xgbFeatureImportance():
    genFile()

    addr='../data/m_p_u_amc_only11twoComb.csv'
    data=read_csv(addr)
    labelSet=data['label']
    del data['label']
    featureSet=data

    n=3000 ; r=0.08 ; m=5
    gbclf=xgb.XGBClassifier(n_estimators=n,learning_rate=r,max_depth=m,gamma=0,subsample=0.9,colsample_bytree=0.5)
    gbclf.fit(featureSet,labelSet)

    feat_imp = Series(gbclf.booster().get_fscore()).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances').get_figure().savefig('../data/FIS.jpg')
    plt.ylabel('Feature Importance Score')
    plt.show()

#xgbFeatureImportance()








