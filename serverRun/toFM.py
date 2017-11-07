# -*- encoding:utf-8 -*-
# -*- encoding:utf-8 -*-
import collections
from csv import DictReader
from datetime import datetime
import numpy as np


#每个特征值说明只有两列的FM格式，并且列名编号要按顺序
def toFM(inputTrain,inputTest,field,postfix='postfix',startidx=101):

    indexDict={}
    cuIndex=[101] #python2中嵌套函数只能能够访问外部的mutable对象，如{},[]。
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

# 所有需要转换的特征
field = ['connectionType','telecomsOperator','sitesetID','positionType',
               'age','gender','education','marriageStatus','haveBaby',
               #'hometown','residence',
               #'adID',
                   'camgaignID',
                   'advertiserID','appID',
               'appPlatform', #'appCategory',
               'cate_level_1','cate_level_2','appSum',
                'hourTime'
               ]

if __name__=="__main__":
    import sys
    inputTrain=sys.argv[1]
    inputTest=sys.argv[2]
    toFM(inputTrain,inputTest,field)
