import sys
sys.path.append("C:\Python27\Lib\site-packages\pamie20")
import cPAMIE

def get_qq_num():
    ie = cPAMIE.PAMIE('http://zc.qq.com/chs/index.html')
    print ie

    #ie.Navigate('http://zc.qq.com/chs/index.html')
    document=ie.Document
    document.getElementById("nick").click()
    #time.sleep(0.2)
    document.getElementById("nick").value="pylon2888"

##    ie.SetTextBox('John','nick',0)
##    ie.SetTextBox('Doe','lastname',0)
##    ie.SetTextBox('1020 State Street','Addline1',0)
##    ie.SetTextBox('Suite #16','Addline2',0)
##    ie.SetTextBox('San Mateo','city',0)
##    ie.SetListBox('CA','state',0)
##    ie.SetTextBox('90210','zip',0)

##    ie.ClickButton('Submit',0)

if __name__=='__main__':
    get_qq_num()
