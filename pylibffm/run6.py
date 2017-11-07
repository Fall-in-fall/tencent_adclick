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

if __name__=='__main__':
    userAppField=[ ['userID','appID'], ['userID']]

    additionalField=[ ['userID','positionID'], ['userID','adID'],
                      ['userID','advertiserID'],['userID','appCategory'],['userID','camgaignID'] ]
    fieldListListstr='userAllAndCombAction'
    fixDay=190000
    train='../data/temp/train_preAction_allUserAndCombs_190000.csv'
    test='../data/temp/test_preAction_allUserAndCombs_190000.csv'
    field=getBaseField()
    for newField in userAppField:
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')
    for newField in additionalField:
            field.append(''.join(newField)+'_preAction')

    print 'field :', field
    numField=[  ]
    print 'numField :',numField
    postfix='actionNumfield_s{feat}_{addField}'.format(feat=len(field), addField=fieldListListstr )
    run_para(train,test,field=field,numField=numField,postfix=postfix)

