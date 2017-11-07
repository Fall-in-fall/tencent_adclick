#===========================================
# -*- coding: utf-8 -*-                  
#@Time     :2017/6/7 3:42               
#@Author   :HJH                          
#@File     :localxgb.py                   
#===========================================
import pandas as pd
def dataProcessing(dataFile1,dataFile2):
    trainData=pd.read_csv(dataFile1)
    testData=pd.read_csv(dataFile2)

    """
    处理trainData
    """
    # removedFeatures=["clickTime","conversionTime","appID","hometown","residence"]
    feats=['positionID',
     'connectionType',
     'telecomsOperator',
     'positionType',
     'gender',
     'education',
     'adID',
     'camgaignID',
     'advertiserID',
     'appID',
     'appCategory',
     'userID_preAction',
     'userIDappID_preAction',
     'positionIDconnectionType_preAction',
     'positionIDconnectionType_ratio']

    labelCol="label"
    # featureCols=[x for x in trainData.columns if x != labelCol and x not in removedFeatures]
    print "all raw features:",feats
    trainFeatures=trainData[feats]
    trainLabels=trainData[labelCol]

    print trainFeatures.shape,trainLabels.shape

    """
    处理testData
    """
    testID="instanceID"
    testFeatures=testData[feats]
    testIns=testData[testID]
    print testFeatures.shape
    print testFeatures.columns
    return trainFeatures,trainLabels,testFeatures,testIns

import xgboost as xgb
def pre(trainFeatures,trainLabels,testFeatures,testIns,n):
    print "start xgboost.."
    xgblf=xgb.XGBClassifier(learning_rate=0.08,n_estimators=n,max_depth=7,gamma=0,subsample=0.9,colsample_bytree=0.5)
    print "start fit.."
    xgblf.fit(trainFeatures,trainLabels)
    print "get y_pre_train.."
    y_pred_xgb=xgblf.predict_proba(testFeatures)[:,1]
    resultDF=pd.DataFrame()
    resultDF["instanceID"]=testIns
    resultDF["prob"]=y_pred_xgb

    import datetime ; timestr=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    resultDF.to_csv("../submit/"+"final_xgb_onlyaddposconnactionratio"+str(n)+"_"+timestr+"_"+".csv",index=False)



if __name__=="__main__":
    print "load data.."
    dataPath="../data/temp/train_preAction_allIDField_4_addUserField.csv"
    testPath="../data/temp/test_preAction_allIDField_4_addUserField.csv"
    trainFeatures,trainLabels,testFeatures,testIns=dataProcessing(dataPath,testPath)
    print "allFeats:",trainFeatures.columns
    pre(trainFeatures,trainLabels,testFeatures,testIns,300)
