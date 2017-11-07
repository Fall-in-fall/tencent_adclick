#--coding:utf-8--
import pandas as pd
import xgboost as xgb


def dataProcessing(dataFile,dataFile2,field,isAll=False):


    trainData=pd.read_csv(dataFile)
    testData=pd.read_csv(dataFile2)

    if isAll:
        field=testData.columns.tolist()
        field.remove('label');field.remove('instanceID')

    trainFeatures=trainData[field]
    trainLabels=trainData['label']

    testFeatures=testData[field]
    testIns=testData['instanceID']

    del trainData,testData
    print trainFeatures.columns
    print len(trainFeatures.columns)
    return trainFeatures,trainLabels,testFeatures,testIns


#数值真实预测：gbdt
def pre2(trainFeatures,trainLabels,testFeatures,testIns,preName,n,r,m):
    print "pre2.."
    gbclf=xgb.XGBClassifier(n_estimators=n,learning_rate=r,max_depth=m,gamma=0,subsample=0.9,colsample_bytree=0.5
                            )#verbose=0,max_leaf_nodes=8,loss="deviance"

    print "pre2 fit start.."
    gbclf.fit(trainFeatures,trainLabels)
    print "pre2 predict start.."
    y_pred_gbdt=gbclf.predict_proba(testFeatures)[:,1]
    resultDF=pd.DataFrame()
    resultDF["instanceID"]=testIns
    resultDF["prob"]=y_pred_gbdt
    print "pre2 start write.."
    import datetime ; timestr=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    resultDF.to_csv("../submit/" +str(n) + "_"+str(r) +"_" +str(m)+ "_"+ preName+  "_" + timestr+"_"+".csv",index=False)

def combAllFeat():
    return [
         'positionID_adID',         #1
         'positionID_education',    #2
         'positionID_telecomsOperator',#3
         'positionID_gender',       #4
         'positionID_camgaignID',   #5
         'positionID_connectionType',  #6
         'positionID_positionType',    #7
         'education_adID', #8
         'positionID_advertiserID',#9
         'telecomsOperator_adID',#10
         'positionID_appID',#11

         'education_camgaignID',#12

         'telecomsOperator_education',#13
         'gender_adID',#14

         'positionID_appCategory',#15

         'gender_education',#16
         'telecomsOperator_camgaignID',#17
         'gender_camgaignID',#18
         'connectionType_adID',#19
         'connectionType_education',#20
         'telecomsOperator_gender',#21
         'education_advertiserID',#22
         'positionType_education',#23
         'positionType_adID',#24
         'education_appCategory',#25
         'education_appID',#26
         'connectionType_telecomsOperator',#27
         'connectionType_gender',#28
         'connectionType_camgaignID',#29
         'telecomsOperator_advertiserID',#30
         'telecomsOperator_positionType',#31
         'gender_advertiserID',#32
         'telecomsOperator_appCategory',#33
         'adID_camgaignID',#34
         'positionType_gender',#35
         'positionType_camgaignID',#36
         'telecomsOperator_appID',#37
         'gender_appCategory',#38
         'connectionType_advertiserID',#39
         'connectionType_positionType',#40
         'gender_appID',#41
         'camgaignID_advertiserID',#42
         'connectionType_appCategory',#43
         'connectionType_appID',#44
         'adID_advertiserID',#45
         'positionType_advertiserID',#46
         'camgaignID_appID',#47
         'positionType_appCategory',#48
         'advertiserID_appID',#49
         'positionType_appID',#50
         'adID_appID',#51
         'camgaignID_appCategory',#52
         'appID_appCategory',#53
         'adID_appCategory',#54
         'advertiserID_appCategory',#55
    ]


def getBaseField():
    field=['positionID','connectionType','telecomsOperator','positionType','gender','education','adID',
                    'camgaignID','advertiserID','appID','appCategory']
    return field[:]


if __name__=="__main__":


    field=getBaseField()
    field.extend([ 'uf'+str(i) for i in range(0,20) ])

    dataPath='../data/mpuamc_userVector.csv'
    testData='../data/test_mpuamc_userVector.csv'
    trainFeatures,trainLabels,testFeatures,testIns=dataProcessing(dataPath,testData,field)

    pre2(trainFeatures,trainLabels,testFeatures,testIns,'xgb_{field}'.format(field='base11_uv20'),2600,0.08,5)
    pre2(trainFeatures,trainLabels,testFeatures,testIns,'xgb_{field}'.format(field='base11_uv20'),3500,0.08,5)
    pre2(trainFeatures,trainLabels,testFeatures,testIns,'xgb_{field}'.format(field='base11_uv20'),4000,0.08,5)


