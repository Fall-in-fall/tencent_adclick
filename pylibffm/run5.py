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

def addUserUserAppRatioNum():
    fieldListList=[['userID','appID'], ['userID'] ]
    fieldListListstr=fieldListListstr=','.join( [''.join(f) for f in fieldListList]  )

    train='../data/temp/train_addRatio_0toNan.csv'
    test='../data/temp/test_addRatio_0toNan.csv'

    field=getBaseField()
    for newField in fieldListList:
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')
            field.append(''.join(newField)+'_ratio')

    postfix='addRatioNum_s{feat}_{field}_0toNan'.format(feat=len(field),
                                                        field=fieldListListstr)
    print 'field :', field
    numField=[ f for f in field if f.__contains__('_ratio')]
    print 'numField :',numField
    run_para(train,test,field=field,numField=numField,postfix=postfix,isToCSV=True)

def addSingleAll(fieldList):
    fieldListList=[['userID','appID'], ['userID'], fieldList]
    fieldListListstr=fieldListListstr=','.join( [''.join(f) for f in fieldListList]  )

    train='../data/temp/train_addRatio_0toNan.csv'
    test='../data/temp/test_addRatio_0toNan.csv'

    field=getBaseField()
    for newField in fieldListList:
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')
            #field.append(''.join(newField)+'_ratio')

    postfix='addAll_s{feat}_{field}_0toNan'.format(feat=len(field),
                                                        field=fieldListListstr)
    print 'field :', field
    numField=[ f for f in field if f.__contains__('_ratio')]
    print 'numField :',numField
    run_para(train,test,field=field,numField=numField,postfix=postfix,isToCSV=True)

def addSingleAction(fieldList):
    fieldListList=[['userID','appID'], ['userID'], fieldList]
    fieldListListstr=fieldListListstr=','.join( [''.join(f) for f in fieldListList]  )

    train='../data/temp/train_addRatio_0toNan.csv'
    test='../data/temp/test_addRatio_0toNan.csv'

    field=getBaseField()
    for newField in fieldListList:
            field.append(''.join(newField)+'_preAction')
            # field.append(''.join(newField)+'_preClickCount')
            # field.append(''.join(newField)+'_preConvCount')
            #field.append(''.join(newField)+'_ratio')

    postfix='user,userAppAlladdAction_s{feat}_{field}_0toNan'.format(feat=len(field),
                                                        field=fieldListListstr)
    print 'field :', field
    numField=[ f for f in field if f.__contains__('_ratio')]
    print 'numField :',numField
    run_para(train,test,field=field,numField=numField,postfix=postfix,isToCSV=True)

def addMultiAction(extendfieldListList):
    fieldListList=[['userID','appID'], ['userID']]
    fieldListList.extend(extendfieldListList)
    fieldListListstr=fieldListListstr=','.join( [''.join(f) for f in fieldListList]  )

    train='../data/temp/train_addRatio_0toNan.csv'
    test='../data/temp/test_addRatio_0toNan.csv'

    field=getBaseField()
    for newField in fieldListList:
            field.append(''.join(newField)+'_preAction')
            # field.append(''.join(newField)+'_preClickCount')
            # field.append(''.join(newField)+'_preConvCount')
            #field.append(''.join(newField)+'_ratio')

    postfix='user,userAppAlladdAction_s{feat}_{field}'.format(feat=len(field),
                                                        field=fieldListListstr)
    print 'field :', field
    numField=[ f for f in field if f.__contains__('_ratio')]
    print 'numField :',numField
    run_para(train,test,field=field,numField=numField,postfix=postfix,isToCSV=True)

def addEachIDAll(extendfieldListList):
    fieldListList=[['userID','appID'], ['userID']]
    fieldListList.extend(extendfieldListList)
    fieldListListstr=','.join( [''.join(f) for f in fieldListList]  )
#userIDpositionID,adIDpositionID,positionIDadd_positionID,adID,appID,appCategory,advertiserID,camgaignID
    train='../data/temp/train_addRatio_0toNan_all.csv'
    test='../data/temp/test_addRatio_0toNan_all.csv'

    field=getBaseField()
    for newField in fieldListList:
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')
            #field.append(''.join(newField)+'_ratio')

    postfix='addEachIDAll_s{feat}_{field}'.format(feat=len(field),
                                                        field=fieldListListstr)
    print 'field :', field
    numField=[ f for f in field if f.__contains__('_ratio')]
    print 'numField :',numField
    run_para(train,test,field=field,numField=numField,postfix=postfix,isToCSV=True)

def addEachIDRatioNum(extendfieldListList):
    orifieldListList=[['userID','appID'], ['userID']]
    fieldListListstr=','.join( [''.join(f) for f in extendfieldListList]  )
#userIDpositionID,adIDpositionID,positionIDadd_positionID,adID,appID,appCategory,advertiserID,camgaignID
    train='../data/temp/train_addRatio_0toNan_all_addRatio.csv'
    test='../data/temp/test_addRatio_0toNan_all_addRatio.csv'

    field=getBaseField()
    for newField in orifieldListList:
            field.append(''.join(newField)+'_preAction')
            field.append(''.join(newField)+'_preClickCount')
            field.append(''.join(newField)+'_preConvCount')

    for newField in extendfieldListList:
        field.append(''.join(newField)+'_ratio')

    postfix='oriActionaddEachIDRatio_s{feat}_{field}'.format(feat=len(field),
                                                        field=fieldListListstr)
    print 'field :', field
    numField=[ f for f in field if f.__contains__('_ratio')]
    print 'numField :',numField
    run_para(train,test,field=field,numField=numField,postfix=postfix,isToCSV=True)

if __name__=='__main__':
    # addUserUserAppRatioNum()
    #
    # addSingleAll(['userID','appCategory'])
    # addSingleAll(['userID','adID'])
    # addSingleAll(['userID','advertiserID'])
    #
    # addSingleAction(['userID','appCategory'])
    # addSingleAction(['userID','adID'])
    # addSingleAction(['userID','advertiserID'])
    #
    # addMultiAction([ ['userID','appCategory'],['userID','adID'], ['userID','advertiserID'] ])

    addEachIDRatioNum([ ['positionID'],['adID'],['appID'] ])