# -*- encoding:utf-8 -*-
import collections
from csv import DictReader
from datetime import datetime
import numpy as np

#默认输入以csv结尾的文件，否则出错。输出以ffm结尾的同名文件
#test不带instanceID，只包含field中的列
def to_ffm_backup(inputTrain,inputTest,field,postfix='postfix'):
    # 为特征名建立编号, filed
    def field_index(x):
        index = field.index(x)
        return index

    # 为特征值建立编号
    table = collections.defaultdict(lambda: 0)
    def getIndices(key):
        indices = table.get(key)
        if indices is None:
            indices = len(table)
            table[key] = indices
        return indices

    outputTrain = inputTrain[0:-4]+'_'+ postfix +'.ffm'
    outputTest = inputTest[0:-4]+'_'+ postfix +'.ffm'
    feature_indices = set()
    with open(outputTrain, 'w') as fo:
        #DictReader 空列字典值为 key:''
        for e, row in enumerate(DictReader(open(inputTrain))):
            features = []
            for k, v in row.items(): #每一行是一个字典
                if k in field:
                    if len(v) > 0:
                        idx = field_index(k)
                        kv = k + ':' + v
                        features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
                        feature_indices.add(kv + '\t' + str(getIndices(kv)))
            if e % 100000 == 0:
                print(datetime.now(), 'creating file '+outputTrain, e)
            fo.write('{0} {1}\n'.format(row['label'], ' '.join('{0}'.format(val) for val in features)))
    fo.close()
    with open(outputTest, 'w') as fo2:
        for t, row in enumerate(DictReader(open(inputTest))):
            features = []
            for k, v in row.items():
                if k in field:
                    if len(v) > 0:
                        idx = field_index(k)
                        kv = k + ':' + v
                        #因为ffm的所有特征都是onehot特征，每一个ffm特征都是filed:；
                        #判断测试集中的特征取值是否存在于训练集。对于训练集没有的特征值是不能加入的。
                        if kv + '\t' + str(getIndices(kv)) in feature_indices:
                            features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
            if t % 100000 == 0:
                print(datetime.now(), 'creating file '+outputTest, t)
            fo2.write('{0} {1}\n'.format(row['label'], ' '.join('{0}'.format(val) for val in features)))
    fo2.close()
    logfile='../log/toffmlog-'+postfix
    with open(logfile, 'w') as fo3:
        fo3.write(','.join(field))
    fo3.close()

#返回对numField中的列的特征值的scaler字典 {field:scaler}
def numFeatureMinMax(inputTrain,numField):
    vdict=collections.defaultdict(lambda: [])
    for row in DictReader(open(inputTrain)):
        for f in numField:
            if row.has_key(f) and len(row[f])>0: #这里要判空
                vdict[f].append( float( row[f]) )
    from sklearn.preprocessing import MinMaxScaler

    scalerDict={}
    for k,vlist in vdict.items():
        ori2minmaxDict={}
        scaler=MinMaxScaler()
        minmaxVlist=scaler.fit_transform(vlist)
        scalerDict[k]=scaler
    return scalerDict
#print numFeatureMinMax('../data/mergeAll.csv',['appSum'])

def to_ffm(inputTrain,inputTest,field,numField=[],postfix='postfix',startidx=101):
    print field
    # 为特征名建立编号, filed
    indexDict={}
    cuIndex=[0] #python2中嵌套函数只能能够访问外部的mutable对象，如{},[]。
    # http://blog.csdn.net/viease/article/details/44490471。Python的数据类型分为mutable（可变） 和 immutable （不可变）mutable : list ,dict ； inmutable : int , string , float ,tuple...
    def field_index(x):
        if not indexDict.has_key(x):
            cuIndex[0]+=1
            indexDict[x]=cuIndex[0]
        return indexDict[x]

    # 为特征值建立编号
    table = collections.defaultdict(lambda: 0)
    def getIndices(key):
        indices = table.get(key)
        if indices is None:
            indices = len(table)
            table[key] = indices
        return indices
    if len(numField)>0:
        scalerDict = numFeatureMinMax(inputTrain,numField)
    if postfix!='':postfix='_'+postfix
    outputTrain = inputTrain[0:-4] + postfix +'.ffm'
    outputTest = inputTest[0:-4] + postfix +'.ffm'
    feature_indices = set()

    with open(outputTrain, 'w') as fo:
        #DictReader 空列字典值为 key:''
        for e, row in enumerate(DictReader(open(inputTrain))):
            features = []
            for k, v in row.items(): #每一行是一个字典
                if k in numField:
                    if len(v) > 0:
                        idx = field_index(k)
                        scaleV=float( scalerDict[k].transform( np.array([float(v)] ).reshape(-1,1) ) )
                        features.append('{f}:0:{v}'.format(f=idx,v=scaleV))
                        feature_indices.add(k + str(0)) #遇到的数值型特征记录
                elif k in field or (len(field)==0 and k!='label'):
                    if len(v) > 0 :
                        idx = field_index(k)
                        kv = k + ':' + v
                        features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
                        feature_indices.add(kv + '\t' + str(getIndices(kv))) #遇到的类别型特征记录
            if e % 100000 == 0:
                print(datetime.now(), 'creating file '+outputTrain, e)
            fo.write('{0} {1}\n'.format(row['label'], ' '.join('{0}'.format(val) for val in features)))
    fo.close()
    with open(outputTest, 'w') as fo2:
        for t, row in enumerate(DictReader(open(inputTest))):
            features = []
            for k, v in row.items():
                if k in numField:
                    if len(v) > 0:
                        idx = field_index(k)
                        if k + str(0) in feature_indices:
                            scaleV=float( scalerDict[k].transform( np.array([float(v)] ).reshape(-1,1) ) )
                            features.append('{f}:0:{v}'.format(f=idx,v=scaleV))
                elif k in field or (len(field)==0 and k!='instanceID'and k!='label'):
                    if len(v) > 0 :
                        idx = field_index(k)
                        kv = k + ':' + v
                        #因为ffm的所有特征都是onehot特征，每一个ffm特征都是filed:；
                        #判断测试集中的特征取值是否存在于训练集。对于训练集没有的特征值是不能加入的。
                        if kv + '\t' + str(getIndices(kv)) in feature_indices:
                            features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
            if t % 100000 == 0:
                print(datetime.now(), 'creating file '+outputTest, t)
            fo2.write('{0} {1}\n'.format(row['label'], ' '.join('{0}'.format(val) for val in features)))
    fo2.close()
    print 'len indexDict : ',len(indexDict)
    logfile='../log/toffmlog-'+postfix
    with open(logfile, 'w') as fo3:
        fo3.write(','.join(field))
    fo3.close()

#每个特征值说明只有两列的FM格式
def toFM(inputTrain,inputTest,field,postfix='postfix',startidx=101):

    indexDict={}
    cuIndex=[0] #python2中嵌套函数只能能够访问外部的mutable对象，如{},[]。
    # http://blog.csdn.net/viease/article/details/44490471。Python的数据类型分为mutable（可变） 和 immutable （不可变）mutable : list ,dict ； inmutable : int , string , float ,tuple...
    def field_index(x):
        if not indexDict.has_key(x):
            cuIndex[0]+=1
            indexDict[x]=cuIndex[0]
        return indexDict[x]

    outputTrain = inputTrain[0:-4]+'_'+ postfix +'.fm'
    outputTest = inputTest[0:-4]+'_'+ postfix +'.fm'
    feature_indices = set()
    with open(outputTrain, 'w') as fo:
        #DictReader 空列字典值为 key:''
        for e, row in enumerate(DictReader(open(inputTrain))):
            features = []
            for k, v in row.items(): #每一行是一个字典
                if k in field:
                    if len(v) > 0:
                        idx = field_index(k)
                        kv = k + ':' + v
                        features.append('{0}:{1}'.format(idx, v))
                        feature_indices.add(kv)
            if e % 100000 == 0:
                print(datetime.now(), 'creating file '+outputTrain, e)
            fo.write('{0} {1}\n'.format(row['label'], ' '.join('{0}'.format(val) for val in features)))
    fo.close()
    with open(outputTest, 'w') as fo2:
        for t, row in enumerate(DictReader(open(inputTest))):
            features = []
            for k, v in row.items():
                if k in field:
                    if len(v) > 0:
                        idx = field_index(k)
                        kv = k + ':' + v
                        if kv in feature_indices:
                            features.append('{0}:{1}'.format(idx, v))
            if t % 100000 == 0:
                print(datetime.now(), 'creating file '+outputTest, t)
            fo2.write('{0} {1}\n'.format(row['label'], ' '.join('{0}'.format(val) for val in features)))
    fo2.close()
    logfile='../log/toFMlog-'+postfix
    with open(logfile, 'w') as fo3:
        fo3.write(','.join(field))
    fo3.close()

def joinOriXGB(oriFile,xgbFile,targetFile='../data/joinOriXGB_v2.ffm'):
    ori=open(oriFile)
    xgb=open(xgbFile)
    t=0
    with open(targetFile,'w') as fo:
        while True:
            oriLine=ori.readline().strip()
            xgbLine=xgb.readline().strip()
            xgbLine=' '.join(xgbLine.split(' ')[1:])
            if  oriLine and  xgbLine:
                fo.write(oriLine+' '+xgbLine+'\n')
            else:
                if oriLine or xgbLine:
                    raise Exception('different length !')
                break
            t+=1
            if t % 100000 == 0: print(datetime.now(), 'creating file '+targetFile, t)
    ori.close() ; xgb.close()
    fo.close()

# joinOriXGB('../data/concat/m_p_u_amc_selected11.ffm',
#            '../data/concat/xgb_trainFeature_FFMlibsvm_1_30.ffm','../data/concat/s11_xgbs11n30.ffm')
# joinOriXGB('../data/concat/test_m_p_u_amc_selected11.ffm',
#            '../data/concat/xgb_testFeature_FFMlibsvm_1_30.ffm','../data/concat/test_s11_xgbs11n30-30.ffm')

#field = ['clickTime', 'creativeID', 'userID', 'positionID', 'connectionType', 'telecomsOperator']
#
# 所有需要转换的特征
# field = ['connectionType','telecomsOperator','sitesetID','positionType',
#                'age',
#          'gender','education','marriageStatus','haveBaby',
#                #'hometown','residence',
#                #'adID',
#                    'camgaignID',
#                    'advertiserID','appID',
#                'appPlatform', #'appCategory',
#                'cate_level_1','cate_level_2','appSum',
#                 'hourTime'
#                ]
# #指定数值型特征
# # numField=['appSum']
#trainSet='../data/m_p_u_amc_only11twoComb.csv'
#testSet='../data/test_m_p_u_amc_only11twoComb.csv'
#toFM(trainSet,testSet,field,postfix='FM_selected_101start')
#removeField=["label","clickTime","conversionTime","hometown" ,"residence",#appID
                     # "creativeID","userID",
                     # "haveBaby","age","marriageStatus"]
# field=['positionID',
# 'connectionType',
# 'telecomsOperator',
# 'positionType',
# 'gender',
# 'education',
# 'adID',
# 'camgaignID',
# 'advertiserID',
# 'appID',
# 'appCategory',
# ]


#to_ffm(trainSet,testSet,field,numField=[],postfix='')
#joinOriXGB('../data/test_m_p_u_amc_cubest_s11.ffm','../data/test_m_p_u_amc_cubest_s11.ffm','../data/joinOriXGB_v2.ffm')

