#--coding:utf-8--
from pandas import *
import matplotlib.pyplot as plt

# ad=read_csv('../data/ad.csv')
# print 'ad',len(ad)
# app_categories=read_csv('../data/app_categories.csv')
# print 'app_categories',len(app_categories)
# position=read_csv('../data/position.csv')
# print 'position',len(position)
# user=read_csv('../data/user.csv')
# print 'user',len(user)
# user_app_actions=read_csv('../data/user_app_actions.csv')
# print 'user_app_actions',len(user_app_actions)
# user_installedapps=read_csv('../data/user_installedapps.csv')
# print 'user_installedapps',len(user_installedapps)
# train=read_csv('../data/train.csv')
# print 'train',len(train)
# test=read_csv('../data/test.csv')
# print 'test',len(test)

train=read_csv('../data/train.csv')

# conversionTime=train['conversionTime']
# len1 = len(conversionTime)
# len2 = len(conversionTime.dropna())
#
# print len1,len2,float(len1)/len2

#统计平均转化时间
def convTime(data): #返回时间差的负数
        conv=str(int(data['conversionTime'])) ; click=str(int(data['clickTime']))
        if conv=='0':
            return 0
        minute= int(conv[4:6])- int(click[4:6])
        hour_minute=  60*( int(conv[2:4]) - int(click[2:4]) )
        day_minute = 1440*( int(conv[0:2])- int(click[0:2]) )
        ys=day_minute+hour_minute+minute
        if ys==0:
            raise Exception('error divTime!')
        return float(-ys)

weight = ( train[ ['clickTime','conversionTime'] ].fillna( 0 ) )\
        .apply( lambda x:convTime(x) , axis='columns' )


