# -*- encoding:utf-8 -*-
import collections
from csv import DictReader
from datetime import datetime
import numpy as np
def joinOriXGB(oriFile,xgbFile,targetFile='../data/joinOriXGB.ffm'):

    ori=open(oriFile)
    xgb=open(xgbFile)
    t=0
    with open(targetFile,'w') as fo:
        while True:
            oriLine=ori.readline().strip()
            xgbLine=xgb.readline().strip()
            if  oriLine and  xgbLine:
                fo.write(oriLine+' '+xgbLine+'\n')
            else:
                if oriLine or xgbLine:
                    raise Exception('different length !')
                break
            t+=1
            if t % 100000 == 0: print(datetime.now(), 'creating file '+targetFile, t)
    ori.close() ; xgb.close()
    fo.close()

if __name__=="__main__":
    import sys
    ori=sys.argv[1]
    xgb=sys.argv[2]
    target=sys.argv[3]
    joinOriXGB(ori,xgb,target)
