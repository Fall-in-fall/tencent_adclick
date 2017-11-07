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
    fieldListList=[['userID','appID'],['userID','adID'],
                   ['userID','advertiserID'],
                   ['userID','appCategory'],
                   ['userID'],['appID'],['adID'],['appCategory'],['advertiserID']
                   ]
    fieldListListstr=fieldListListstr=','.join( [''.join(f) for f in fieldListList]  )
    fixDay=190000
    train='../data/temp/train_preAction_{field}_{fixDay}.csv'.format(field=fieldListListstr,fixDay=fixDay)
    test='../data/temp/test_preAction_{field}_{fixDay}.csv'.format(field=fieldListListstr,fixDay=fixDay)

    field=getBaseField()
    addField=['userID',['userID','appID'],['userID','adID']]
    for newField in addField: #为每个field组合更新它的字典
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')

    print 'field :', field
    numField=[ f for f in field if f.__contains__('_preClickCount') or f.__contains__('_preConvCount') ]
    postfix='actionNumfield_s{feat}_{addField}'.format(feat=len(field),
                                                    addField=','.join( [''.join(f) for f in addField]  ))
    print 'numField :',numField
    run_para(train,test,field=field,numField=numField,postfix=postfix)

