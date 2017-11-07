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
    t=str(95) ; k=str(8) ; l=str(0.00002)
    resultName = '../submit/ffm_'+ postfix  + '_t{t}_k{k}_l{l}'.format(t=t,k=k,l=l,feat=str(len(field)))
    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    ffm.runffm(trainFile,testFile,resultName,assignCMDPara)

if __name__=='__main__':
    userAppField=[ ['userID','appID'], ['userID']]

    additionalField=[
                     #['positionID','adID'],['positionID','education'],['positionID','gender'],
                     #['positionID','camgaignID'],
        #['positionID','connectionType'],
       # ['positionID','advertiserID'],
                     #['education','adID'],['education','gender'],['gender','adID'],
                     #['positionID'],['adID'],['appID'],['appCategory'],['advertiserID'],['camgaignID']
                    ]
    fieldListListstr='userAllAndisInstalled'
    train='../data/temp/train_preAction_allIDField_4_addUserField.csv'
    test='../data/temp/test_preAction_allIDField_4_addUserField.csv'
    field=getBaseField()
    numField=[]
    for newField in userAppField:
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')
    for newField in additionalField:
            # field.append(''.join(newField)+'_preAction')
            # field.append(''.join(newField)+'_preClickCount')
            # field.append(''.join(newField)+'_preConvCount')
            field.append(''.join(newField)+'_ratio')
            #
            # numField.append(''.join(newField)+'_preClickCount')
            # numField.append(''.join(newField)+'_preConvCount')
            numField.append(''.join(newField)+'_ratio')
    field.append('isInstalled')
    print 'field :', field
    print 'numField :',numField
    postfix='userAppAddIsInstalled_s{feat}_{addField}'.format(feat=len(field), addField=fieldListListstr )
    run_para(train,test,field=field,numField=numField,postfix=postfix,isToCSV=False)

 #  84      0.10539      0.10471
 #  85      0.10538      0.10470
 #  86      0.10536      0.10470
 #  87      0.10535      0.10470
 #  88      0.10534      0.10469
 #  89      0.10533      0.10469
 #  90      0.10531      0.10468
 #  91      0.10530      0.10468
 #  92      0.10529      0.10468
 #  93      0.10528      0.10467
 #  94      0.10527      0.10467
 #  95      0.10526      0.10466
 #  96      0.10525      0.10466
 #  97      0.10524      0.10465
 #  98      0.10522      0.10465
 #  99      0.10521      0.10464
 # 100      0.10520      0.10465
 # 101      0.10519      0.10464
 # 102      0.10518      0.10464

