#--coding:utf-8--
from pandas import *
from sklearn.isotonic import IsotonicRegression as IR
import subprocess
from datetime import datetime

def runffm(targetFFM='',modelFile=''):
    timestr= datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    tempOut = '../data/calibration/ffm-out-calibration_' + modelFile.split('/')[-1]
    resultFile ='../data/calibration/'+ modelFile.split('/')[-1] +'_predict4train_'+ timestr+'.csv'
    start = datetime.now()
    testCMD = 'ffm-predict.exe {testData} {model} {out}'.format(testData=targetFFM,model=modelFile,out=tempOut)
    print testCMD
    #subprocess.call(testCMD,shell=True)
    #写入最终结果
    instanceID=[]
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
    print('时间: {0}'.format(datetime.now() - start))
    return resultFile

trainResult = runffm('../data/calibration/ffmTrain-102662.ffm',
       '../data/calibration/ffm-model-102662')



p_train_all=read_csv(trainResult)['prob']
oriTrain=read_csv('../data/train.csv')
sameTrain=oriTrain[ oriTrain['clickTime']>=190000].reset_index()
print len(sameTrain),len(p_train_all)
part_sameTrain=sameTrain[(sameTrain['clickTime']>=200000)&(sameTrain['clickTime']<290000)]

p_train=p_train_all.loc[part_sameTrain.index]
y_train=part_sameTrain['label']

ir = IR()
ir.fit( p_train, y_train )

oriResult=read_csv('../data/calibration/ffm_mergeAppUser_s17_preAction_190000_no_Dist_noNum_t150_k8_l2e-05_2017-06-05-20-58-00.csv')
p_test=oriResult['prob']
p_calibrated = ir.transform( p_test )   # or ir.fit( p_test ), that's the same thing

oriResult['new_prob']=Series(p_calibrated)
oriResult.to_csv('../data/calibration/calib_temp.csv',index=False)
oriResult['nozero_new_prob']=oriResult.apply(lambda x: x['new_prob'] if x['new_prob'] >0
                                             else x['prob'] ,axis='columns' )

del oriResult['prob'],oriResult['new_prob']
oriResult.rename(columns={'nozero_new_prob':'prob'},inplace=True)
oriResult.to_csv('../data/calibration/calib_submit.csv',index=False)


