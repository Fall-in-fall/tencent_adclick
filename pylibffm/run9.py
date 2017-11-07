# -*- encoding:utf-8 -*-
import subprocess
import csv_2_ffm
import ffm
import validFFM
import pandas as pd

from featuerGen_backup import merge_appID_userID,preActionFeature2

def getFinalField():
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
     'userID_preAction',
     'userIDappID_preAction',
     'positionIDconnectionType_preAction',
     'positionIDconnectionType_ratio',
     'positionIDconnectionType_preClickCount',
     'positionIDadID_preAction',
     'positionIDadID_ratio',
     'positionIDeducation_preClickCount',
     'positionIDadvertiserID_ratio']
    return copyField[:]


def run_para(oriTrain,oriTest,field,numField,postfix,isToCSV=True):
    #if isToCSV: csv_2_ffm.to_ffm(oriTrain,oriTest,field,numField=numField,postfix= postfix)
    trainFile = oriTrain[0:-4]+ '_'+ postfix  +'.ffm'
    testFile =  oriTest[0:-4]+  '_'+ postfix  +'.ffm'
    t=str(150) ; k=str(8) ; l=str(0.00002)
    resultName = '../submit/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    ffm.runffm(trainFile,testFile,resultName,assignCMDPara)

def finalNoNum():

    train='../data/temp/train_preAction_allIDField_4_addUserField.csv'
    test='../data/temp/test_preAction_allIDField_4_addUserField.csv'
    field=getFinalField() ; numField=[  ]
    print 'field :', field
    print 'numField :',numField
    postfix='finalNoNum_s{feat}'.format(feat=len(field))
    run_para(train,test,field=field,numField=numField,postfix=postfix)

def finalRatioNum():
    train='../data/temp/train_preAction_allIDField_4_addUserField.csv'
    test='../data/temp/test_preAction_allIDField_4_addUserField.csv'
    field=getFinalField() ; numField=[  ]
    for f in field:
        numField.append(''.join(f)+'_ratio')
    print 'field :', field
    print 'numField :',numField
    postfix='finalRatioNum_s{feat}'.format(feat=len(field))
    run_para(train,test,field=field,numField=numField,postfix=postfix)

def finalClickNum():
    train='../data/temp/train_preAction_allIDField_4_addUserField.csv'
    test='../data/temp/test_preAction_allIDField_4_addUserField.csv'
    field=getFinalField() ; numField=[  ]
    for f in field:
        numField.append(''.join(f)+'_preClickCount')
    print 'field :', field
    print 'numField :',numField
    postfix='finalClickNum_s{feat}'.format(feat=len(field))
    run_para(train,test,field=field,numField=numField,postfix=postfix)

def finalRatioClickNum():
    train='../data/temp/train_preAction_allIDField_4_addUserField.csv'
    test='../data/temp/test_preAction_allIDField_4_addUserField.csv'
    field=getFinalField() ; numField=[  ]
    for f in field:
        numField.append(''.join(f)+'_ratio')
        numField.append(''.join(f)+'_preClickCount')
    print 'field :', field
    print 'numField :',numField
    postfix='finalRatioClickNum_s{feat}'.format(feat=len(field))
    run_para(train,test,field=field,numField=numField,postfix=postfix)

if __name__=='__main__':
    # finalNoNum()
    # finalRatioNum()
    finalClickNum()
    finalRatioClickNum()
    #提交之后，取结果最好那个，调个参。

