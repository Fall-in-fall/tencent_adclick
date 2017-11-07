# -*- encoding:utf-8 -*-
from pandas import *
import os
import subprocess
import csv_2_ffm

#根据测试集的considerFeat对训练集进行采样
def sampleTrain(train,test,considerFeat=['positionID','adID']):
    indexSet=set()
    kvStringSet=set()
    for item_i,v in test.iterrows():
        kvList=[]
        for col_i in xrange(0,len(considerFeat)):
            kvList.append(str(col_i) + ':' + str( int( v[considerFeat[col_i] ]) )  )
        kvStringSet.add(','.join(kvList))
    print 'kvStringSet size: ',len(kvStringSet)
    for item_i,v in train.iterrows():
        kvList=[]
        for col_i in xrange(0,len(considerFeat)):
            kvList.append(str(col_i) + ':' + str( int( v[considerFeat[col_i] ]) )  )
        rowkvString=','.join(kvList)
        if rowkvString in kvStringSet:
            indexSet.add(item_i)
    print len(indexSet),len(train)
    return train.loc[indexSet]

def splitTrainTest(trainFile,day=280000,isSample=True):
    print 'splitTrainTest start'
    data = read_csv(trainFile)
    print data.columns
    train = data[data['clickTime']<day]
    test = data[ (data['clickTime']>=day) &(data['clickTime']<day+10000) ]
    if isSample:
        train=sampleTrain(train,test)
    trainAddr = trainFile[0:-4]+'split_{day}_{isSample}_train.csv'.format(day=str(day/10000), isSample='sample' if isSample else '')
    testAddr = trainFile[0:-4]+'split_{day}_test.csv'.format(day=str(day/10000))
    print 'splitTrainTest write file'
    train.to_csv(trainAddr,index=False)
    test.to_csv(testAddr,index=False)
    return trainAddr,testAddr

def validFFM(trainFile='../data/sample/m_p_u_amc.csv',predictFile='',resultName='../submit/ffmv',paras='-l 0.00002 -k 8 -t 100 -r 0.02 -s 8',isStop=False,onlyValid=True,field=[],numField=[]):
    timestr= datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    modelFile = './valid/ffm-model-'+ resultName.split('/')[-1] +'_'+ ('stop' if isStop else 'nostop')   +'_'+ timestr
    resultOut = './valid/ffm-out-' + timestr
    start = datetime.now()

    if isStop and not onlyValid: raise Exception('autostop must with valied')

    #生成划分----------------------
    trainAddr, testAddr = splitTrainTest(trainFile)
    csv_2_ffm.to_ffm(trainAddr,testAddr,field,numField=numField,postfix= 'valid')
    trainFileName,testFileName=(trainAddr[0:-4]+'_valid.ffm',testAddr[0:-4]+'_valid.ffm')

    #训练，验证----------------------
    if onlyValid:  paras += ' -p '+ testFileName
    if isStop:   paras += ' --auto-stop'
    trainCMD = 'ffm-train.exe '+paras + ' {trainData} {model}'.format(trainData=trainFileName,model=modelFile)
    print trainCMD
    subprocess.call(trainCMD,shell=True)
    #trainInfo = os.popen(trainCMD).readlines()  #执行该命令 #读取命令行的输出到一个list

    if not onlyValid:
        validOut = './valid/tempout/validTempOut-' + timestr
        testCMD = 'ffm-predict.exe {testData} {model} {out}'.format(testData=testFileName,model=modelFile,out=validOut)
        subprocess.call(testCMD,shell=True)
        #testInfo = os.popen(testCMD).readlines()

    #训练完后进行最终提交预测------------------------------------
    # resultFile = resultName  +'_'+ ('stop' if isStop else 'nostop')   +'_'+ timestr  +'.csv'
    # predictCMD= 'ffm-predict.exe {predictData} {model} {out}'.format(predictData=predictFile,model=modelFile,out=resultOut)
    # subprocess.call(predictCMD,shell=True)
    # print 'writing submit result : ',resultFile
    # with open(resultFile, 'w') as fo:
    #     fo.write('instanceID,prob\n')
    #     for t, row in enumerate(open(resultOut), start=1):
    #         fo.write('{0},{1}'.format(t, row))

    #记录运行结果与参数
    #备用，找到同时打印并记录控制台输出的方法后用
    trainInfo =[]; testInfo=[]

    logFile = '../log/ffm-log-' + resultName.split('/')[-1] +'_'+ timestr
    for i in xrange(0,len(trainInfo)): trainInfo[i] = trainInfo[i].decode('gbk').encode('utf-8')
    for j in xrange(0,len(testInfo)):  testInfo[j] = testInfo[j].decode('gbk').encode('utf-8')
    print trainInfo
    print testInfo
    timeCostInfo = '时间: {0}'.format(datetime.now() - start)
    with open(logFile,'w') as fo2:
        fo2.write(trainCMD)
        fo2.writelines(trainInfo)
        fo2.writelines(testInfo)
        fo2.write(timeCostInfo)
    print(timeCostInfo)

    #删除划分文件
    #rmcmd = 'rm {splitTran} {splitTest}'.format(splitTran=trainFileName,splitTest=testFileName)
    # subprocess.call(rmcmd,shell=True)
    #print os.popen(rmcmd).readlines()

def splitIndex(trainData='',dayCount=10):
    all=len(open(trainData).readlines())
	#valSet = trainData[(trainData['clickTime']<valDay+10000)&(trainData['clickTime']>=valDay)]
	#3415131-3113362=301769
	#train = trainData[trainData['clickTime']<valDay]
	#3113362 rows
	#return len(train),len(valSet)
    trainSize=(all/dayCount)*(dayCount-1)
    return trainSize,all-trainSize
def split2File(ffmAddr,train_size,test_size):
    from sklearn.model_selection import train_test_split
    ffmdata=open(ffmAddr).readlines()
    train,test = ( ffmdata[0:train_size] , ffmdata[train_size:train_size+test_size] )
    if len(train)!=train_size or len(test)!=test_size: raise Exception('wrong splited ffm')
    a=file(ffmAddr+'-split_train','w')
    a.writelines(train) ; a.close()
    b=file(ffmAddr+'-split_test','w')
    b.writelines(test) ; b.close()
    return ffmAddr+'-split_train',ffmAddr+'-split_test'


