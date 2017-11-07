# -*- encoding:utf-8 -*-
import subprocess
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

def runffm(trainFile='',testFile='',resultName='',assignCMDPara='ffm-train.exe -l 0.00002 -k 8 -t 100 -r 0.02 -s 8',
           instanceID=[],model=''):
    timestr= datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    tempOut = './ffm-out-' + resultName.split('/')[-1] +'_'+ timestr
    resultFile = resultName +'_'+ timestr+'.csv'
    start = datetime.now()
    #训练 #windowsCMDpre = './ffm-train.exe' #linuxCMDpre = './ffm-train'
    #——命令参数
    if model=='':
        modelFile = './ffm-model-' + resultName.split('/')[-1] +'_'+ timestr
        if assignCMDPara!='':
            trainCMD ='ffm-train.exe '+ assignCMDPara + ' {trainData} {model}'.format(trainData=trainFile,model=modelFile)
        print trainCMD
        #trainInfo = os.popen(trainCMD) .readlines()  #执行该命令 #读取命令行的输出到一个list
        subprocess.call(trainCMD,shell=True)
    else:
        trainCMD=''
        modelFile=model
    #预测
    if trainCMD.__contains__('.exe') or trainCMD=='':
        if trainCMD.__contains__('-32.exe'):
            testCMD = 'ffm-predict-32.exe {testData} {model} {out}'.format(testData=testFile,model=modelFile,out=tempOut)
        else:testCMD = 'ffm-predict.exe {testData} {model} {out}'.format(testData=testFile,model=modelFile,out=tempOut)
    else:testCMD = './ffm-predict {testData} {model} {out}'.format(testData=testFile,model=modelFile,out=tempOut)
    #testInfo = os.popen(testCMD) .readlines()
    print testCMD
    subprocess.call(testCMD,shell=True)
    #写入最终结果
    if len(instanceID)==0:
        with open(resultFile, 'w') as fo:
            fo.write('instanceID,prob\n')
            for t, row in enumerate(open(tempOut), start=1):
                fo.write('{0},{1}'.format(t, row))
    else:
        with open(resultFile, 'w') as fo:
            fo.write('instanceID,prob\n')
            for t, row in enumerate(open(tempOut), start=0):
                fo.write('{0},{1}'.format(instanceID[t], row))

    #记录参数
    logFile = '../log/ffm-log-' + resultFile[0:-4].split('/')[-1]
    trainInfo=[] ; testInfo=[] #以后备用打印控制台信息
    for i in xrange(0,len(trainInfo)):  trainInfo[i] = trainInfo[i].decode('gbk').encode('utf-8')
    for i in xrange(0,len(testInfo)):   testInfo[i] = testInfo[i].decode('gbk').encode('utf-8')
    print trainInfo
    print testInfo
    with open(logFile,'w') as fo2:
        fo2.write(trainCMD)
        fo2.writelines(trainInfo)
        fo2.writelines(testInfo)
    #cmd = 'rm {path}model {path}test.out {path}train.ffm {path}test.ffm'.format(path=path)
    #subprocess.call(cmd, shell=True)
    print('时间: {0}'.format(datetime.now() - start))
    return resultFile
# def addInstanceID():
#     timestr= datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
#     tempOut = './ffmresult_xgbFFMlibsvm100'
#     resultFile='../submit/hjh_ffm_'+timestr+'.csv'
#     with open(resultFile, 'w') as fo:
#         fo.write('instanceID,prob\n')
#         for t, row in enumerate(open(tempOut), start=1):
#             fo.write('{0},{1}'.format(t, row))

