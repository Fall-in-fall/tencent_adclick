from validFFM import validFFM
import csv_2_ffm

def getFinalField():
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
     'userID_preAction',
     'userIDappID_preAction',
     'positionIDconnectionType_preAction',
     'positionIDconnectionType_ratio',
     'positionIDconnectionType_preClickCount',
     'positionIDadID_preAction',
     'positionIDadID_ratio',
     'positionIDeducation_preClickCount',
     'positionIDadvertiserID_ratio']
    return copyField[:]


def validFinal():
    trainFile='../data/temp/train_preAction_allIDField_4_addUserField.csv'
    field=getFinalField() ; numField=[  ]
    # for f in field:
    #         numField.append(''.join(newField)+'_ratio')
    print 'field :', field
    print 'numField :',numField

    t=str(150) ; k=str(8) ; l=str(0.00002)

    assignCMDPara=' -t {t} -k {k} -l {l} -s 4 -r 0.02 '.format(t=t,k=k,l=l)
    validFFM(trainFile=trainFile,paras=assignCMDPara,field=field,numField=numField)

if __name__=="__main__":
    validFinal()#66

  # 58      0.10549      0.10658
  # 59      0.10546      0.10660
  # 60      0.10543      0.10656
  # 61      0.10541      0.10656
  # 62      0.10539      0.10657
  # 63      0.10536      0.10656
  # 64      0.10533      0.10655
  # 65      0.10531      0.10651
  # 66      0.10528      0.10651
  # 67      0.10526      0.10652
  # 68      0.10523      0.10652
  # 69      0.10521      0.10652
  # 70      0.10518      0.10652
  # 71      0.10516      0.10651
  # 72      0.10513      0.10651
  # 73      0.10511      0.10651
  # 74      0.10508      0.10651
  # 75      0.10506      0.10651
  # 76      0.10503      0.10652
  # 77      0.10501      0.10653
  # 78      0.10499      0.10652
  # 79      0.10496      0.10653
  # 80      0.10494      0.10652
  # 81      0.10491      0.10653
  # 82      0.10489      0.10653
  # 83      0.10486      0.10654
  # 84      0.10484      0.10653
  # 85      0.10482      0.10654
  # 86      0.10479      0.10656
  # 87      0.10477      0.10657
  # 88      0.10474      0.10656