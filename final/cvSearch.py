#--coding:utf-8--
from pandas import *
import xgboost as xgb
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.cross_validation import  cross_val_score,cross_val_predict
import sklearn.preprocessing as preprocessing
from sklearn.decomposition import PCA
#df1=DataFrame(np.random.randint(0,10,size=(4,3)),columns=['a','b','c'])
#D:/workspace/PycharmProjects/a/tencent_adclick/
from sklearn.grid_search import GridSearchCV

def trainProcess(trainData):
    # trainData.fillna(0)
    # testData.fillna(0)
    removedFeatures=["clickTime","conversionTime","hometown" ,"residence",#appID
                     "creativeID","userID",
                     "haveBaby","age","marriageStatus"]
    labelCol="label"
    featureCols=[x for x in trainData.columns if x != labelCol and x not in removedFeatures]
    trainFeatures=trainData[featureCols]
    trainLabels=trainData[labelCol]
    return trainFeatures,trainLabels

data=read_csv('../data/mergeAll-sub-appID-0.2.csv')
trainFeatures,trainLabels = trainProcess(data)

gbclf=xgb.XGBClassifier(n_estimators=n,learning_rate=r,max_depth=m,gamma=0,subsample=0.9,colsample_bytree=0.5)
turned_parameter=[{"n_estimators":[600,650,700,750]}]
print "start gridSerach.."
gs_clf=GridSearchCV(gbclf,turned_parameter,cv=3,scoring="neg_log_loss")
print "start fit.."
gs_clf.fit(trainFeatures,trainLabels)
print "best parameters set found:"
print (gs_clf.best_params_)
y_pred_gbdt=gs_clf.predict_proba(testFeatures)[:,1]

