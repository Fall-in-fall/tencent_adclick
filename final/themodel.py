#--coding:utf-8--
from pandas import *
from sklearn.linear_model import LogisticRegression

def ini_logitre(trainCSV,testCSV):
    #---------------处理特征，生成pd_feature_set，labelseries
    train_except_list = ['conversionTime','positionID','userID', 'creativeID','label','adID']
    pd_feature_set = trainCSV[ [ x for x in trainCSV.columns if x not in train_except_list ] ]
    labelseries=trainCSV['label']
    #---------------处理特征 生成test_feature_set-------------------
    test_except_list = ['positionID','userID', 'creativeID','adID']
    test_feature_set= testCSV[ [ x for x in testCSV.columns if x not in test_except_list ] ]
    #---------------输入pd_feature_set，labelseries，拟合模型，返回对生成test_feature_set的预测结果
    #检查训练集测试集列名是否对应
    trainCols=pd_feature_set.columns ; testCols=test_feature_set.columns
    if len(trainCols)!=len(testCols): raise Exception('len(trainCols)!=len(testCols)')
    for i in xrange(0,len(trainCols)):
        if trainCols[i]!=testCols[i]:
            raise Exception('trainCols[i]'+'!='+testCols[i])
    #------------拟合，预测-----
    logitre=LogisticRegression()
    logitre.fit(pd_feature_set,labelseries)
    print logitre.classes_
    if logitre.classes_[1]==1:return logitre.predict_proba(test_feature_set)[:,1]
    else: return logitre.predict_proba(test_feature_set)[:,0]

def pca_ini_logitre(trainCSV,testCSV):
    #---------------处理特征，生成pd_feature_set，labelseries
    train_except_list = ['conversionTime','positionID','userID', 'creativeID','label','adID']
    pd_feature_set = trainCSV[ [ x for x in trainCSV.columns if x not in train_except_list ] ]
    labelseries=trainCSV['label']
    #---------------处理特征 生成test_feature_set-------------------
    test_except_list = ['positionID','userID', 'creativeID','adID']
    test_feature_set= testCSV[ [ x for x in testCSV.columns if x not in test_except_list ] ]
    #---------------输入pd_feature_set，labelseries，拟合模型，返回对生成test_feature_set的预测结果
    #检查训练集测试集列名是否对应
    trainCols=pd_feature_set.columns ; testCols=test_feature_set.columns
    if len(trainCols)!=len(testCols): raise Exception('len(trainCols)!=len(testCols)')
    for i in xrange(0,len(trainCols)):
        if trainCols[i]!=testCols[i]:
            raise Exception(trainCols[i]+'!='+testCols[i])
    #-------------PCA------------------
    import sklearn.preprocessing as preprocessing
    from sklearn.decomposition import PCA
    #标准化
    sdscaler = preprocessing.StandardScaler()
    sd_train_feature_set=sdscaler.fit_transform(pd_feature_set)
    sd_test_feature_set=sdscaler.transform(test_feature_set)

    pca_process=PCA(n_components=30)
    pca_train = pca_process.fit_transform(sd_train_feature_set)
    pca_test = pca_process.transform(sd_test_feature_set)
    #------------拟合，预测-----
    logitre=LogisticRegression()
    logitre.fit(pca_train,labelseries)
    print logitre.classes_
    if logitre.classes_[1]==1:return logitre.predict_proba(pca_test)[:,1]
    else: return logitre.predict_proba(pca_test)[:,0]

def sd_ini_logitre(trainCSV,testCSV):
    #---------------处理特征，生成pd_feature_set，labelseries
    train_except_list = ['conversionTime','positionID','userID', 'creativeID','label','adID']
    pd_feature_set = trainCSV[ [ x for x in trainCSV.columns if x not in train_except_list ] ]
    labelseries=trainCSV['label']
    #---------------处理特征 生成test_feature_set-------------------
    test_except_list = ['positionID','userID', 'creativeID','adID']
    test_feature_set= testCSV[ [ x for x in testCSV.columns if x not in test_except_list ] ]
    #---------------输入pd_feature_set，labelseries，拟合模型，返回对生成test_feature_set的预测结果
    #检查训练集测试集列名是否对应
    trainCols=pd_feature_set.columns ; testCols=test_feature_set.columns
    if len(trainCols)!=len(testCols): raise Exception('len(trainCols)!=len(testCols)')
    for i in xrange(0,len(trainCols)):
        if trainCols[i]!=testCols[i]:
            raise Exception(trainCols[i]+'!='+testCols[i])
    #-------------PCA------------------
    import sklearn.preprocessing as preprocessing
    #标准化
    sdscaler = preprocessing.StandardScaler()
    sd_train_feature_set=sdscaler.fit_transform(pd_feature_set)
    sd_test_feature_set=sdscaler.transform(test_feature_set)
    #------------拟合，预测-----
    logitre=LogisticRegression()
    logitre.fit(sd_train_feature_set,labelseries)
    print logitre.classes_
    if logitre.classes_[1]==1:return logitre.predict_proba(sd_test_feature_set)[:,1]
    else: return logitre.predict_proba(sd_test_feature_set)[:,0]

def sd_haveadID_ini_logitre(trainCSV,testCSV):
    #---------------处理特征，生成pd_feature_set，labelseries
    train_except_list = ['conversionTime','positionID','userID', 'creativeID','label'] #与sd_ini_logitre区别在于有无adID,testCSV删了label，之前忘删了，囧    
    labelseries=trainCSV['label']
    tcol=trainCSV.columns
    for i in train_except_list:
        if i in tcol:
            del trainCSV[i]
	pd_feature_set = trainCSV
    #---------------处理特征 生成test_feature_set-------------------
    test_except_list = ['positionID','userID', 'creativeID'] #与sd_ini_logitre区别在于有无adID
    for j in test_except_list:
        del testCSV[j]
    test_feature_set= testCSV
    #---------------输入pd_feature_set，labelseries，拟合模型，返回对生成test_feature_set的预测结果
    #检查训练集测试集列名是否对应
    trainCols=pd_feature_set.columns ; testCols=test_feature_set.columns
    if len(trainCols)!=len(testCols):
        raise Exception(str(len(trainCols))+'!='+str(len(testCols)))
    for i in xrange(0,len(trainCols)):
        if trainCols[i]!=testCols[i]:
            raise Exception(trainCols[i]+'!='+testCols[i])
    #-------------PCA------------------
    import sklearn.preprocessing as preprocessing
    #标准化
    sdscaler = preprocessing.StandardScaler()
    sd_train_feature_set=sdscaler.fit_transform(pd_feature_set)
    sd_test_feature_set=sdscaler.transform(test_feature_set)
    #------------拟合，预测-----
    logitre=LogisticRegression()
    logitre.fit(sd_train_feature_set,labelseries)
    print logitre.classes_
    if logitre.classes_[1]==1:return logitre.predict_proba(sd_test_feature_set)[:,1]
    else: return logitre.predict_proba(sd_test_feature_set)[:,0]

def haveadID_ini_logitre(trainCSV,testCSV):
    #---------------处理特征，生成pd_feature_set，labelseries
    train_except_list = ['conversionTime','positionID','userID', 'creativeID','label'] #与sd_ini_logitre区别在于有无adID,testCSV删了label，之前忘删了，囧
    labelseries=trainCSV['label']
    for i in train_except_list:
        if i in tcol:
            del trainCSV[i]
	pd_feature_set = trainCSV
    #---------------处理特征 生成test_feature_set-------------------
    test_except_list = ['positionID','userID', 'creativeID'] #与sd_ini_logitre区别在于有无adID
    for j in test_except_list:
        del testCSV[j]
    test_feature_set= testCSV
    #---------------输入pd_feature_set，labelseries，拟合模型，返回对生成test_feature_set的预测结果
    #检查训练集测试集列名是否对应
    trainCols=pd_feature_set.columns ; testCols=test_feature_set.columns
    if len(trainCols)!=len(testCols):
        raise Exception(str(len(trainCols))+'!='+str(len(testCols)))
    for i in xrange(0,len(trainCols)):
        if trainCols[i]!=testCols[i]:
            raise Exception(trainCols[i]+'!='+testCols[i])
    #------------拟合，预测-----
    logitre=LogisticRegression()
    logitre.fit(sd_train_feature_set,labelseries)
    print logitre.classes_
    if logitre.classes_[1]==1:return logitre.predict_proba(pd_feature_set)[:,1]
    else: return logitre.predict_proba(test_feature_set)[:,0]
#----------------------------------



