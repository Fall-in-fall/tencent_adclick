#--coding:utf-8--
from pandas import *
import collections
from datetime import datetime

def idTestRatio(col='adID',trainFile='../data/m_p_u_amc.csv',testFile='../data/test_m_p_u_amc.csv',):
    # stat=idTestRatio('adID',base+'m_p_u_amc.csv',base+'test_m_p_u_amc.csv')
    train=read_csv(trainFile) ; test=read_csv(testFile)
    idTestSet = set(test[col].unique().tolist())
    stat={}
    for ed in xrange(170000,310000,10000):
        daySet = set(train[ (train['clickTime']>=ed) & (train['clickTime']<ed+10000)][col].unique().tolist())
        stat[ed]= float(len(daySet&idTestSet))/( len(daySet|idTestSet) )
    return stat

def drop(dataFile,field=['userID','positionID','creativeID']):
    data=read_csv(dataFile)
    print 'ori length',len(data)
    data_dup=data[data.duplicated(field,keep=False)]#重复样本
    print 'duplicated *2',len(data_dup)
    print 'positive duplicated',len(data_dup[data_dup['label']==1])
    #重复样本按label和时间升序后，保留最后出现去重。从而保留重复中的较后出现的正样本。
    afterIndex=data_dup.sort_values(['label','clickTime']).drop_duplicates(field,keep='last').index.tolist()
    print 'droped duplicated ',len(afterIndex)
    i_data_nodup=data[data.duplicated(field,keep=False)==False].index.tolist()#非重复样本索引
    print 'non-duplicated',len(i_data_nodup)
    newIndex=afterIndex[:] ; newIndex.extend(i_data_nodup)
    newData=data.loc[newIndex]
    print len(newData)+len(data_dup)-len(afterIndex),len(data_dup)-len(afterIndex)
    return newData

    # drop('../data/sample/m_p_u_amc.csv')\
    #     .to_csv('../data/sample/dropUPC_m_p_u_amc.csv',index=False)

#对测试集样本寻找在训练集中出现的与其相同field的样本，并记录训练集中样本的clickTime和label
def testPreClicktMark(trainFile,testFile,field=['userID','appID']):
    train=read_csv(trainFile) ; test=read_csv(testFile)
    kvStringDict=collections.defaultdict(lambda: [])
    for item_i,v in train.iterrows():
        kvList=[]
        for col_i in xrange(0,len(field)):
            kvList.append( str( int( v[field[col_i] ]) )  )
        kString=','.join(kvList)
        kvStringDict[kString].append( '-'.join( [ str( int(v['clickTime']) )  ,str(int(v['label'])) ]) )
        if item_i % 100000 == 0:
                print(datetime.now(), 'creating kvStringDict ', item_i)

    print len(kvStringDict)
    test['preClick']=Series(dtype=str)
    for item_i,v in test.iterrows():
        kvList=[]
        for col_i in xrange(0,len(field)):
            kvList.append( str( int( v[field[col_i] ]) )  )
        kString=','.join(kvList)
        kv = kvStringDict[ kString ]
        preClickValue = ','.join(kv)
        test['preClick'].set_value(item_i,preClickValue)
        if item_i % 100000 == 0:
                print(datetime.now(), 'creating preClick ', item_i)
    print test[test['preClick']>''] ; print len(test[test['preClick']>''])
    return test[['instanceID','preClick']]

#testPreClicktMark('../data/m_p_u_amc.csv', '../data/test_m_p_u_amc.csv').to_csv('../data/sample/test_appIDmarkPreClick.csv',index=False)


def pos(test_mark):
    indexSet=set()
    countDict=collections.defaultdict(lambda: 0)#用字典记录每种点击次数出现的样本数
    for item_i,v in test_mark.iterrows():

        countDict[count]+=1
        indexSet.add(item_i)
        if item_i==100000:
            break
    print countDict
    #return test_mark.loc[indexSet]

#统计testPreClicktMark中的正点击次数对应的样本数
#可用str(v['preClick']).__contains__('-1')#取得包含'-1'的为正点击
def countClickAll(test_mark):
    indexSet=set()
    countDict=collections.defaultdict(lambda: 0)
    for item_i,v in test_mark.iterrows():
        if not isnull(v['preClick']):
            count=len(str(v['preClick']).split(','))
            countDict[count]+=1
            indexSet.add(item_i)
        else: countDict[0]+=1
    print countDict
