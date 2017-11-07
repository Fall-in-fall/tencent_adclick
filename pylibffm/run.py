# -*- encoding:utf-8 -*-
import subprocess
import csv_2_ffm
import ffm
import validFFM
import pandas as pd
# cmd = 'python csv_2_ffm.py'
# subprocess.call(cmd, shell=True)

# cmd = 'python ffm.py'
# subprocess.call(cmd, shell=True)
def getBaseField():
    copyField=['positionID',
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
    ]
    return copyField[:]
def concatResult(rf1,rf2,addr='../submit/splitRun.csv'):
    rd1=pd.read_csv(rf1)
    rd2=pd.read_csv(rf2)
    result=pd.concat([rd1,rd2],axis=0).sort_values('instanceID')
    result.to_csv(addr,index=False)
    print len(result)

#----------------------------
def run_userIDappID_1():
    ori11Field=copyField[:]
    oriTrain = '../data/temp/train_preAction_userID,appID_5_.csv'
    oriTest = '../data/temp/test_preAction_userID,appID_5_.csv'
    ori11Field.append('preAction') ; numField=[]
    postfix='m_p_u_amc_s{feat}_preAction_appIDuserID_5'.format(feat=str(len(ori11Field)))
    csv_2_ffm.to_ffm(oriTrain,oriTest,ori11Field,numField=numField,postfix= postfix)

    trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'
    t=str(150)
    k=str(8)
    l=str(0.00002)
    resultName = '../submit/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    ffm.runffm(trainFile,testFile,resultName,assignCMDPara)

def run_userIDappID_2():
    ori11Field=copyField[:]
    oriTrain = '../data/temp/train_preAction_userID,appID_5_.csv'
    oriTest = '../data/temp/test_preAction_userID,appID_5_.csv'
    ori11Field.extend(['preAction','preClickCount','preClickDist','preConvCount','preConvDist'])
    numField=['preClickCount','preClickDist','preConvCount','preConvDist']
    postfix='m_p_u_amc_s{feat}_preAction_appIDuserID_5'.format(feat=str(len(ori11Field)))
    csv_2_ffm.to_ffm(oriTrain,oriTest,ori11Field,numField=numField,postfix= postfix)
    trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'
    t=str(150)  ;k=str(8)  ;l=str(0.00002)
    resultName = '../submit/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    ffm.runffm(trainFile,testFile,resultName,assignCMDPara)


def runUserID_1():
    ori11Field=copyField[:]
    oriTrain = '../data/temp/train_preAction_userID_5.csv'
    oriTest = '../data/temp/test_preAction_userID_5.csv'

    ori11Field.append('preAction')
    #ori11Field.extend(['preAction','preClickCount','preClickDist','preConvCount','preConvDist'])
    #numField=['preClickCount','preClickDist','preConvCount','preConvDist']

    postfix='m_p_u_amc_s{feat}_preAction_appIDuserID_5'.format(feat=str(len(ori11Field)))
    csv_2_ffm.to_ffm(oriTrain,oriTest,ori11Field,numField=numField,postfix= postfix)

    trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'
    t=str(150) ; k=str(8) ;l=str(0.00002)
    resultName = '../submit/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    ffm.runffm(trainFile,testFile,resultName,assignCMDPara)

def run_para(oriTrain,oriTest,field,postfix,numField):
    csv_2_ffm.to_ffm(oriTrain,oriTest,ori11Field,numField=numField,postfix= postfix)
    trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'
    t=str(150) ; k=str(8) ;l=str(0.00002)
    resultName = '../submit/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    ffm.runffm(trainFile,testFile,resultName,assignCMDPara)


def preClickRun():
    field=['positionID','connectionType','telecomsOperator','positionType','gender','education','adID',
                'camgaignID','advertiserID','appID','appCategory','preAction']
    def onceRun(day):
        oriTrain = '../data/temp/train_preAction_{day}.csv'.format(day=day)
        oriTest = '../data/temp/test_preAction_19.csv'
        postfix='m_p_u_amc_s{feat}_preAction_{day}'.format(feat=str(len(field)),day=day)
        csv_2_ffm.to_ffm(oriTrain,oriTest,field,numField=[],postfix= postfix)
        trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
        testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'
        t=str(150)
        k=str(8)
        l=str(0.00002)
        resultName = '../submit/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
        assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
        ffm.runffm(trainFile,testFile,resultName,assignCMDPara)
    for i in xrange(20,31):
        onceRun(i)


def oriInRun():
    oriTrain = '../data/sample/recent20.csv'
    oriTest = '../data/sample/test_oldPositionIDadID.csv'
    postfix='oldPositionIDadID_recent20_s{feat}'.format(feat=str(len(ori11Field)))
    csv_2_ffm.to_ffm(oriTrain,oriTest,ori11Field,numField=[],postfix= postfix)

    trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'
    t=str(150)
    k=str(8)
    l=str(0.00002)
    resultName ='../data/sample/result/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    instanceID=pd.read_csv(oriTest)['instanceID'].tolist()
    return ffm.runffm(trainFile,testFile,resultName,assignCMDPara,instanceID=instanceID)

def newInRun():
    newInField=ori11Field[:]
    newInField.extend( [ "hometown" ,"residence","sitesetID","appPlatform" "hourTime","appSum"] )
    oriTrain = '../data/sample/mergeAll_recent20.csv'
    oriTest = '../data/sample/test_newPositionIDadID.csv'
    postfix='newPositionIDadID_recent20_s{feat}'.format(feat=str(len(newInField)))
    csv_2_ffm.to_ffm(oriTrain,oriTest,ori11Field,numField=[],postfix= postfix)

    trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'
    t=str(150)
    k=str(8)
    l=str(0.00002)
    resultName = '../data/sample/result/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    instanceID=pd.read_csv(oriTest)['instanceID'].tolist()
    return ffm.runffm(trainFile,testFile,resultName,assignCMDPara,instanceID=instanceID)

def splitRun():
    rf1=oriInRun()
    rf2=newInRun()
    concatResult(rf1,rf2,'../submit/splitRun_adIDpositionID_recent20.csv')
#splitRun()

def joinXgbFmmRun(n):
    trainFile = '../data/concat/xgb{n}_s11.ffm'.format(n=n)
    testFile = '../data/concat/test_xgb{n}_s11.ffm'.format(n=n)

    xgbTrain='../data/concat/xgb_trainFeature_FFMlibsvm_1_{n}'.format(n=n)
    s11Train='../data/concat/m_p_u_amc_selected11.ffm'
    #csv_2_ffm.joinOriXGB(xgbTrain,s11Train,trainFile)

    xgbTest='../data/concat/xgb_testFeature_FFMlibsvm_1_{n}'.format(n=n)
    s11Test='../data/concat/test_m_p_u_amc_selected11.ffm'
    #csv_2_ffm.joinOriXGB(xgbTest,s11Test,testFile)

    # t=str(150)
    # k=str(8)
    # l=str(0.00002)
    # resultName = '../submit/ffm_joinXgb{n}-11_t{t}_k{k}_l{l}'.format(n=n,t=t,k=k,l=l)
    # assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    # return ffm.runffm(trainFile,testFile,resultName,assignCMDPara)

    #
    t=str(200)
    k=str(12)
    l=str(0.000005)
    resultName = '../submit/ffm_joinXgb{n}-11_t{t}_k{k}_l{l}'.format(n=n,t=t,k=k,l=l)
    assignCMDPara=' -t {t} -k {k} -l {l} -s 3 -r 0.02 '.format(t=t,k=k,l=l)
    return ffm.runffm(trainFile,testFile,resultName,assignCMDPara)


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


def combRun():
    #--------------------55个组合特征 + 原始11特征使用--------------
    field=combAllFeat()[0:55]
    field.extend(ori11Field)

    oriTrain = '../data/ori_and_11twoComb.csv'
    oriTest = '../data/test_ori_and_11twoComb.csv'
    postfix='11+55_s{feat}'.format(feat=str(len(field)))
    # csv_2_ffm.to_ffm(oriTrain,oriTest,field,numField=[],postfix= postfix)

    trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'

    k=str(16)
    l=str(0.000001)

    #-200次迭代
    t=str(200)
    resultName = '../submit/ffmresult_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    ffm.runffm(trainFile,testFile,resultName,assignCMDPara)
    #-300次迭代
    # t=str(300)
    # resultName = '../submit/ffmresult_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
    # assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    # ffm.runffm(trainFile,testFile,resultName,assignCMDPara)
    # #-400次迭代
    # t=str(400)
    # resultName = '../submit/ffmresult_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(ori11Field)))
    # assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    # ffm.runffm(trainFile,testFile,resultName,assignCMDPara)


    # #--------------------55个组合特征使用------------------
    # # oriTrain = '../data/m_p_u_amc_only11twoComb.csv'
    # # oriTest = '../data/test_m_p_u_amc_only11twoComb.csv'

    # featNum=55
    # # field=combAllFeat()[0:featNum]
    # # #csv_2_ffm.to_ffm(oriTrain,oriTest,field,numField=[],postfix=str(featNum))
    # #
    # trainFile = '../data/m_p_u_amc_only11twoComb'+'_'+str(featNum)+'.ffm'
    # testFile = '../data/test_m_p_u_amc_only11twoComb'+'_'+str(featNum)+'.ffm'
    # # #- 400次迭代
    # # t = str(400)
    # # resultName = '../submit/ffmresult_m_p_u_amc_only11twoComb'+'_'+str(featNum) +'_t'+t
    # # assignCMDPara='ffm-train.exe -l 0.00002 -k 8 -t '+ t +' -r 0.02 -s 4'
    # # ffm.runffm(trainFile,testFile,resultName,assignCMDPara)
    # #- 500次迭代-
    # featNum=55
    # t = str(500)
    # k = str(8)
    # resultName = '../submit/ffm_m_p_u_amc_only11twoComb'+'_'+str(featNum) +'_t'+t +'_k_'+k
    # assignCMDPara='ffm-train.exe -l 0.00002 ' + ' -k '+ k +' -t '+ t +' -r 0.02 -s 4'
    # ffm.runffm(trainFile,testFile,resultName,assignCMDPara)

if __name__=='__main__':
    run()