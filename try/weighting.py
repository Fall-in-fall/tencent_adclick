#--coding:utf-8--
from pandas import *
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.cross_validation import  cross_val_score,cross_val_predict
import numpy as np
pd_m_p_u_amc = read_csv('../data/m_p_u_amc.csv')
except_feature_list = ['conversionTime','positionID','userID', 'creativeID','label','adID']
pd_feature_set = pd_m_p_u_amc[ [ x for x in pd_m_p_u_amc.columns if x not in except_feature_list ] ]
labelseries=pd_m_p_u_amc['label']

def divTime(data): #返回时间差的负数
        conv=str(int(data['conversionTime'])) ; click=str(int(data['clickTime']))
        if conv=='0':
            return 0
        minute=( int(conv[4:6])- int(click[4:6]) )/10+1
        ys = 144*( int(conv[0:2])- int(click[0:2]) )+\
                   6*( int(conv[2:4]) - int(click[2:4]) )+ minute
        if ys==0:
            raise Exception('error divTime!')
        return float(-ys)
def scaleMap(seriesdata,newmin,mewmax):#将一个区间的数据映射到另一个区间上
    #http://blog.csdn.net/touch_dream/article/details/62076236
    result= (seriesdata-seriesdata.min())* \
           ( (mewmax-newmin) / ( seriesdata.max()-seriesdata.min() ) )+newmin
    return result

#应用条件：正样本数小于负样本数。输入的正样本原始权值全正或全负，不允许混合（没有意义）。负样本原始权值一律为0。
#返回结果：将所有负样本权值设为1。正样本权值保持原始大小关系，最小为1。正负样本负样本具有相同的权值总和
#方法：提取正样本。将原始最小权值的实例的新权值分配1，剩余的权值先给所有剩余实例分配1，再按照它们原始权值的比例分配剩下的权值
def equalScaleWeight(data):
    posdata=data[data!=0] #所有正样本
    #权值转换，负样本保持0，正样本最小为1
    if posdata.min()<0:  #如果权值是负数将负数权值处理为正数权值，最小权值为1，并且保持权值之间的大小比例不变
        newdata = data.apply(lambda x:0 if x==0 else posdata.min() / float(x) )
        posdata = posdata.min()/posdata
    else:
        newdata = data.apply(lambda x:0 if x==0 else float(x) / posdata.min() )
        posdata = posdata/posdata.min()
    #负样本总权值=正样本总权值
    total_weight=data[data==0].count()
    #对正样本计算排除min之后的总权值
    rest_total_weight=total_weight - posdata[posdata==posdata.min()].count()
    posnotmin=posdata[posdata>posdata.min()]
    #非min实例的1权值要加上的额外分配权值
    singleadded_weight = float( rest_total_weight - posnotmin.count() ) / posnotmin .sum()
    return newdata.apply(lambda x:singleadded_weight*x+1 if x>posdata.min()and x!=0 else 1)

#保持负样本权值都为1，正样本权值总和为正样本数，但各个样本所占比例不同
def innerEqualScaleWeight(data):
    from math import sqrt
    posSampleMin=data[data!=0].min()
    #权值转换，负样本保持0，正样本取开方降低比例差距
    if posSampleMin.min()<0:  #如果权值是负数将负数权值处理为正数权值，最小权值为1，并且保持权值之间的大小比例不变
        newdata = data.apply(lambda x:0 if x==0 else sqrt( posSampleMin / float(x)) )
    else:
        newdata = data.apply(lambda x:0 if x==0 else sqrt(float(x) / posSampleMin) )
    #正样本总权值=正样本总数*1 (总权值保持不变)
    total_weight=newdata[newdata!=0].count()
    print 'total_weight',total_weight
    #单位权值
    unitWeight = total_weight/newdata.sum()
    print 'unitWeight',unitWeight
    return newdata.apply(lambda x: unitWeight*x if  x!=0 else 1)

def genWeight(df):
    weight = ( df[ ['clickTime','conversionTime'] ].fillna( 0 ) )\
        .apply( lambda x:divTime(x) , axis='columns' )
    #weight = scaleMap(weight.replace( 0,weight.min() ),1,2)
    weight=equalScaleWeight(weight)
    return weight

weight=genWeight( pd_m_p_u_amc )

print weight[ (weight>1) ].count()

weighted_pd_m_p_u_amc=pd_m_p_u_amc
weighted_pd_m_p_u_amc['weight']=weight
weighted_pd_m_p_u_amc.to_csv('../data/weighted_pd_m_p_u_amc.csv',index=False)
# print weight[ (weight>1) & (weight<70) ].count()
# if raw_input()==0: exit()
#--------------------使用加权样本训练测试
logitre=LogisticRegression()
fit_params={'sample_weight': weight }

cate_features=['connectionType','telecomsOperator','sitesetID','positionType',
               'gender','education','marriageStatus','haveBaby',
               #hometown,residence,camgaignID,advertiserID,appID 数值太稀疏待处理
               'appPlatform' #,appCategory 数值太稀疏待处理
               ]
pd_feature_set=get_dummies(pd_feature_set,columns =cate_features)
score3 = cross_val_score(logitre,pd_feature_set, labelseries,fit_params=fit_params,cv=10, scoring='neg_log_loss')
print score3 ; print score3.sum()
#-------------no weight
# [-0.1344314  -0.12372916 -0.11756826 -0.1162727  -0.11647042 -0.11661963
#  -0.11775322 -0.11867357 -0.12054443 -0.12505423]
# -1.20711701172

#-------------weighted + except adID