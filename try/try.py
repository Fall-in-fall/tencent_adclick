#--coding:utf-8--
from pandas import *
ad=read_csv('./data/ad.csv')
app_categories=read_csv('./data/app_categories.csv')
position=read_csv('./data/position.csv')
user=read_csv('./data/user.csv')
user_app_actions=read_csv('./data/user_app_actions.csv')
user_installedapps=read_csv('./data/user_installedapps.csv')
train=read_csv('./data/train.csv')
test=read_csv('./data/test.csv')
#----------------------


train['conversionTime']=train['conversionTime'].fillna( 0 )

