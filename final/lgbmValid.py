#--coding:utf-8--
import lightgbm
from pandas import *
from sklearn.metrics import log_loss
import scipy as sp

def splitTrainTest(trainFile,day=280000,isSample=True):
    print 'splitTrainTest start'
    data = read_csv(trainFile)
    train = data[data['clickTime']<day]
    test = data[ (data['clickTime']>=day) &(data['clickTime']<day+10000) ]
    return train,test

def dataProcessing(train,test,field,isAll=False):
    print field
    trainFeatures=train[field]
    trainLabels=train['label']
    testFeatures=test[field]
    testLabels=test['label']
    del train,test
    print trainFeatures.columns
    print len(trainFeatures.columns)
    return trainFeatures,trainLabels,testFeatures,testLabels

def pre2(trainFeatures,trainLabels,testFeatures,testIns,preName,n,r,m):
    print "pre2.."
    gbclf=lightgbm.LGBMClassifier(n_estimators=n,learning_rate=r,max_depth=m,subsample=0.9,colsample_bytree=0.5
                            ,nthread=4)#verbose=0,max_leaf_nodes=8,loss="deviance"

    print "pre2 fit start.."
    gbclf.fit(trainFeatures,trainLabels)
    print "pre2 predict start.."
    y_pred_gbdt=gbclf.predict_proba(testFeatures)[:,1]
    return y_pred_gbdt
    # resultDF=pd.DataFrame()
    # resultDF["instanceID"]=testIns
    # resultDF["prob"]=y_pred_gbdt


def getBaseField():
    field=['positionID','connectionType','telecomsOperator','positionType','gender','education','adID',
                    'camgaignID','advertiserID','appID','appCategory']
    return field[:]

def gegetTrainTestField(trainFile):
    userAppField=[['userID','appID'], ['userID']]
    field=getBaseField()
    additionalField=[
        #              ['positionID','adID'],['positionID','education'],['positionID','gender'],
        #              ['positionID','camgaignID'],
        # ['positionID','connectionType'],
        # ['positionID','advertiserID'],
        #              ['education','adID'],['education','gender'],['gender','adID'],
        #              ['positionID'],['adID'],['appID'],['appCategory'],['advertiserID'],['camgaignID']
                    ]
    fieldstr='userAllAndOtherRatio'

    #trainFile='../data/m_p_u_amc.csv'
    train,test=splitTrainTest(trainFile)
    field=getBaseField()
    for newField in userAppField:
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')
    #for newField in additionalField:
            # field.append(''.join(newField)+'_preAction')
            # field.append(''.join(newField)+'_preClickCount')
            # field.append(''.join(newField)+'_preConvCount')
            #field.append(''.join(newField)+'_ratio')
    return train,test,field

def getStatField():
    userAppField=[['userID','appID'], ['userID']]

    field=getBaseField()
    additionalField=[
                     ['positionID','adID'],['positionID','education'],['positionID','gender'],
                     ['positionID','camgaignID'],
        ['positionID','connectionType'],
        ['positionID','advertiserID'],
                     ['education','adID'],['education','gender'],['gender','adID'],
                     ['positionID'],['adID'],['appID'],['appCategory'],['advertiserID'],['camgaignID']
                    ]
    fieldstr='userAllAndOtherRatio'
    field=getBaseField()
    for newField in userAppField:
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')
    for newField in additionalField:
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')
            field.append(''.join(newField)+'_ratio')
    return field

def logloss(act, pred):
  epsilon = 1e-15
  pred = sp.maximum(epsilon, pred)
  pred = sp.minimum(1-epsilon, pred)
  ll = sum(act*sp.log(pred) + sp.subtract(1,act)*sp.log(sp.subtract(1,pred)))
  ll = ll * -1.0/len(act)
  return ll

# D:/workspace/PycharmProjects/a/tencent_adclick/data/
def temp(train,day,field,para=[200,0.08,5],baseField=[]):
    print ','.join([f for f in field if f not in baseField])
    otrainFeatures=train[field]
    otrainLabels=train['label']
    trainindex = train[train['clickTime']<day].index
    testindex = train[ (train['clickTime']>=day) &(train['clickTime']<day+10000) ].index

    trainFeatures=otrainFeatures.loc[trainindex]
    trainLabels=otrainLabels.loc[trainindex]
    testFeatures=otrainFeatures.loc[testindex]
    testLabels=otrainLabels.loc[testindex]

    result=pre2(trainFeatures,trainLabels,testFeatures,testLabels,'lgbm_{field}'.format(field='userApp'),para[0],para[1],para[2]);print logloss(testLabels,result)
#
# if __name__=="__main__":
#     trainFile='../data/temp/train_preAction_allIDField_4_addUserField_isInstalled_addRatio.csv'
#     train,test,field = getTrainTestField(trainFile)
#
#     trainFeatures,trainLabels,testFeatures,testLabels=dataProcessing(train,test,getStatField())
#     result=pre2(trainFeatures,trainLabels,testFeatures,testLabels,'lgbm_{field}'.format(field='userApp'),180,0.08,5);print logloss(testLabels,result)
