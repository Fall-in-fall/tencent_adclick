# -*- encoding:utf-8 -*-
import subprocess
import csv_2_ffm
import ffm
# cmd = 'python csv_2_ffm.py'
# subprocess.call(cmd, shell=True)

# cmd = 'python ffm.py'
# subprocess.call(cmd, shell=True)

# field=['positionID',
# 'connectionType',
# 'telecomsOperator',
# 'positionType',
# 'gender',
# 'education',
# 'adID',
# 'camgaignID',
# 'advertiserID',
# 'appID',
# 'appCategory',
# ]

# oriTrain = '../data/m_p_u_amc-sub-appID-0.2.csv'
# oriTest = '../data/test_m_p_u_amc.csv'
# csv_2_ffm.to_ffm(oriTrain,oriTest,field,numField=[],postfix='selected11')

# trainFile = '../data/m_p_u_amc-sub-appID-0.2_selected11.ffm'
# testFile = '../data/test_m_p_u_amc_selected11.ffm'
# resultName = '../submit/ffmresult_m_test_m_p_u_amc_sub-appID-0.2_selected11_50'
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

oriTrain = '../data/m_p_u_amc_only11twoComb.csv'
oriTest = '../data/test_m_p_u_amc_only11twoComb.csv'

featNum=22
field=combAllFeat()[0:featNum]
csv_2_ffm.to_ffm(oriTrain,oriTest,field,numField=[],postfix=str(featNum))

trainFile = '../data/m_p_u_amc_only11twoComb'+'_'+str(featNum)+'.ffm'
testFile = '../data/test_m_p_u_amc_only11twoComb'+'_'+str(featNum)+'.ffm'
t = str(250)
resultName = '../submit/ffmresult_ori_and_11twoComb'+'_'+str(featNum) +'_t'+t
assignCMDPara='./ffm-train -l 0.00002 -k 4 -t '+ t +' -r 0.02 -s 8'
ffm.runffm(trainFile,testFile,resultName,assignCMDPara)
#--------------------------

