# -*- encoding:utf-8 -*-
import subprocess
import csv_2_ffm
import ffm
import validFFM
import pandas as pd

from featuerGen_backup import merge_appID_userID,preActionFeature2

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


def run_para(oriTrain,oriTest,field,numField,postfix,isToCSV=True):
    if isToCSV: csv_2_ffm.to_ffm(oriTrain,oriTest,field,numField=numField,postfix= postfix)
    trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'
    t=str(150) ; k=str(8) ; l=str(0.00002)
    resultName = '../submit/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    ffm.runffm(trainFile,testFile,resultName,assignCMDPara)


def runFixDay(fixDay,isToCSV=True,isGenFeature=True):
    if isGenFeature:
        #preActionFeature(field=['userID','appID'],fixDay=fixDay)
        preActionFeature(field=['userID'],fixDay=fixDay)

    # field_12=getBaseField() ; field_12.append('preAction')
    # numField_12=[]
    field_16=getBaseField() ; field_16.extend(['preAction','preClickCount','preClickDist','preConvCount','preConvDist'])
    numField_16=['preClickCount','preClickDist','preConvCount','preConvDist']
    #
    # userIDappIDTrain = '../data/temp/train_preAction_userIDappID_{fixDay}.csv'.format(fixDay=fixDay)
    # userIDappIDTest = '../data/temp/test_preAction_userIDappID_{fixDay}.csv'.format(fixDay=fixDay)

    userIDTrain = '../data/temp/train_preAction_userID_{fixDay}.csv'.format(fixDay=fixDay)
    userIDTest = '../data/temp/test_preAction_userID_{fixDay}.csv'.format(fixDay=fixDay)

    # userIDappID_postfix_12 = 'base_s{feat}_preAction_appIDuserID_{fixDay}'.format(feat=str(len(field_12)),fixDay=fixDay)
    # userIDappID_postfix_16 = 'base_s{feat}_preAction_appIDuserID_{fixDay}'.format(feat=str(len(field_16)),fixDay=fixDay)
    #userID_postfix_12 = 'base_s{feat}_preAction_userID_{fixDay}'.format(feat=str(len(field_12)),fixDay=fixDay)
    userID_postfix_16 = 'base_s{feat}_preAction_userID_{fixDay}'.format(feat=str(len(field_16)),fixDay=fixDay)

    # run_para(userIDappIDTrain,userIDappIDTest,field_12,numField_12,userIDappID_postfix_12,isToCSV=isToCSV)
    # run_para(userIDappIDTrain,userIDappIDTest,field_16,numField_16,userIDappID_postfix_16,isToCSV=isToCSV)

    #run_para(userIDTrain,userIDTest,field_12,numField_12,userID_postfix_12,isToCSV=isToCSV)
    run_para(userIDTrain,userIDTest,field_16,numField_16,userID_postfix_16,isToCSV=isToCSV)

def mergeRun(field_21,numField_21,fixDay,addPostfix='',needMerge=True,toffm=True):


    # merge_train = merge_appID_userID('../data/temp/train_preAction_userID_{fixDay}.csv'.format(fixDay=fixDay),
    #                              '../data/temp/train_preAction_userIDappID_{fixDay}.csv'.format(fixDay=fixDay),
    #                              '../data/temp/merge_appID_userID_{fixDay}.csv'.format(fixDay=fixDay))
    # merge_test = merge_appID_userID('../data/temp/test_preAction_userID_{fixDay}.csv'.format(fixDay=fixDay),
    #                                   '../data/temp/test_preAction_userIDappID_{fixDay}.csv'.format(fixDay=fixDay),
    #                                   '../data/temp/merge_test_appID_userID_{fixDay}.csv'.format(fixDay=fixDay))

    merge_train='../data/temp/old/merge_appID_userID_{fixDay}.csv'.format(fixDay=fixDay)
    merge_test='../data/temp/old/merge_test_appID_userID_{fixDay}.csv'.format(fixDay=fixDay)

    postfix='mergeAppUser_s{feat}_preAction_{fixDay}_{addPostfix}'.format(feat=str(len(field_21)),fixDay=fixDay,addPostfix=addPostfix)
    toffm=False
    if toffm:csv_2_ffm.to_ffm(merge_train,merge_test,field_21,numField=numField_21,postfix= postfix)
    trainFile = merge_train[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  merge_test[0:-4]+  '_'+ postfix  +'.ffm'
    t=str(120) ; k=str(8) ; l=str(0.00002)
    resultName = '../submit/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(field_21)))

    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    ffm.runffm(trainFile,testFile,resultName,assignCMDPara)


if __name__=='__main__':
    #runFixDay(200000,isToCSV=False)
    #runFixDay(210000,isToCSV=True)


    # runFixDay(5,isToCSV=True,isGenFeature=False)
    # runFixDay(190000,isToCSV=True)
    # runFixDay(180000,isToCSV=True)
    # mergeRun(5)
    # preActionFeature(field=['userID'],fixDay=200000)
    # preActionFeature(field=['userID','appID'],fixDay=200000)
    # mergeRun(200000)
    # preActionFeature(field=['userID'],fixDay=210000)
    #preActionFeature2(field=['userID','appID'],fixDay=210000)


    field_21=getBaseField() ; field_21.extend(['preAction','preClickCount',#'preClickDist',
                                               'preConvCount',#,'preConvDist'\
                           'app_preAction','app_preClickCount',#'app_preClickDist',
                                               'app_preConvCount'#,'app_preConvDist'
                                               ])
    numField_21=[
       # 'preClickCount','preClickDist','preConvCount',#'preConvDist',
        #          'app_preClickCount','app_preClickDist','app_preConvCount'#,'app_preConvDist'
                 ]
    # mergeRun(field_21,numField_21,fixDay=190000,addPostfix='no_Dist_noNum')
    # mergeRun(field_21,numField_21,fixDay=200000,addPostfix='no_Dist_noNum')
    print 'numField:',numField_21
    mergeRun(field_21,numField_21,fixDay=190000,addPostfix='no_Dist_noNum',toffm=False)
    #preActionFeature(fieldListList=['userID'],fixDay=190000)


