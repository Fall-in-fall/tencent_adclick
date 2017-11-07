#--coding:utf-8--
from pandas import *
import xgboost as xgb
import numpy as np
import matplotlib.pylab as plt
from sklearn import cross_validation, metrics   #Additional     scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search

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
    final=oriData.loc[resultIndex]
    final.to_csv(targetaddr, index=False)
    print len(oriData),len(resultIndex),len(oriData)*ratio
    return final

def trainProcess(trainData):
    # trainData.fillna(0)
    # testData.fillna(0)
    removedFeatures=["clickTime","conversionTime","hometown" ,"residence",#appID
                     "creativeID","userID",
                     "haveBaby","age","marriageStatus","sitesetID","appPlatform"]
    labelCol="label"
    featureCols=[x for x in trainData.columns if x != labelCol and x not in removedFeatures]
    print featureCols
    trainFeatures=trainData[featureCols]
    trainLabels=trainData[labelCol]
    return trainFeatures,trainLabels

def modelfit(alg, dtrain,dlabel,useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(dtrain.values, label=dlabel.values)
        print 'gen xgtrain'
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds,
            metrics='logloss', early_stopping_rounds=early_stopping_rounds)
        print cvresult
        alg.set_params(n_estimators=cvresult.shape[0])
    #Fit the algorithm on the data
    print 'fit'
    alg.fit(dtrain, dlabel,eval_metric='logloss')
    #Predict training set:
    dtrain_predprob = alg.predict_proba(dtrain)[:,1]

    #Print model report:
    print "\nModel Report"
    print "logloss: %f" % metrics.log_loss(dlabel, dtrain_predprob)

    feat_imp = Series(alg.booster().get_fscore()).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances').get_figure()\
        .savefig('../data/fig/FIS_{time}.jpg'.format(time= datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
    plt.ylabel('Feature Importance Score')
    plt.show()

if __name__=="__main__":
    data=read_csv('../data/m_p_u_amc.csv')
    #data=subsample(ratio=0.2,targetCol='appID',fileaddr='../data/m_p_u_amc.csv')
    trainFeatures,trainLabels = trainProcess(data)
    xgb1 = xgb.XGBClassifier(
         learning_rate =0.1,
         n_estimators=1000,
         max_depth=5,
         min_child_weight=1,
         gamma=0,
         subsample=1,
         colsample_bytree=0.8,
         objective= 'binary:logistic',
         nthread=2,
         seed=27)
    modelfit(xgb1, trainFeatures,trainLabels,useTrainCV=False)
