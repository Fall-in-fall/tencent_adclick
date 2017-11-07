#--coding:utf-8--
from pandas import *
from themodel import *

def submit(dataFunc,preFunc,preName=''):

    trainCSV,testCSV=dataFunc()
    #--------------
    instanceID=testCSV['instanceID']
    del testCSV['instanceID'],testCSV['label']
    resultDF=DataFrame()
    resultDF['instanceID']=instanceID
    resultDF['prob']=preFunc(trainCSV,testCSV)

    import datetime ; timestr=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    resultDF.to_csv('../submit/'+preName+'_'+timestr+'.csv',index=False)

def m_p_u_amcData():
    train = read_csv('../data/m_p_u_amc.csv')
    test = read_csv('../data/test_m_p_u_amc.csv')
    return (train,test)

def oneHotData():
    train = read_csv('../data/onehot_m_p_u_amc.csv')
    test = read_csv('../data/onehot_test_m_p_u_amc.csv')
    return (train,test)

def cutOneHotData():
    train = read_csv('../data/cut_onehot_m_p_u_amc.csv')
    test = read_csv('../data/onehot_test_m_p_u_amc.csv')
    return (train,test)

def allOneHotData():
    train = read_csv('../data/allonehot_m_p_u_amc.csv')
    test = read_csv('../data/allonehot_test_m_p_u_amc.csv')
    return (train,test)

def dealCols_small_allOneHotData():
    train = read_csv('../data/dealCols_small_allonehot_m_p_u_amc.csv')
    test = read_csv('../data/dealCols4_small_allonehot_test_m_p_u_amc.csv')

    return (train,test)

def waitingRun():
    import time,os
    while True:
        if os.path.exists('../data/dealCols_small_allonehot_m_p_u_amc.csv'):
            submit(dealCols_small_allOneHotData,sd_haveadID_ini_logitre,preName='sd_dealCols_small_all_haveadID_onehot')
            break;
        else:
            time.sleep(120)


#submit(dealCols_small_allOneHotData,sd_haveadID_ini_logitre,preName='sd_dealCols_small_all_haveadID_onehot')