# coding=GBK

import sys
sys.path.append('C:\Python27\Lib\site-packages\pytesser')

import win32com.client, win32inet, win32file
import time, os
import Image,ImageEnhance,ImageFilter,ImageGrab
from pytesser import *
from ctypes import *


def get_code_str_from_image_qq(image_name):
##    im = Image.open(image_name)
##    im.show("test")
    im = ImageGrab.grab()
    im.show("tt.bmp")
##    im.filter(ImageFilter.BLUR).save("filter_BLUR.jpeg")
##    im.filter(ImageFilter.CONTOUR).save("filter_CONTOUR.jpeg")
##    im.filter(ImageFilter.DETAIL).save("filter_DETAIL.jpeg")
##    im.filter(ImageFilter.EDGE_ENHANCE).save("filter_EDGE_ENHANCE.jpeg")
##    im.filter(ImageFilter.EDGE_ENHANCE_MORE).save("filter_EDGE_ENHANCE_MORE.jpeg")
##    im.filter(ImageFilter.EMBOSS).save("filter_EMBOSS.jpeg")
##    im.filter(ImageFilter.FIND_EDGES).save("filter_FIND_EDGES.jpeg")
##    im.filter(ImageFilter.SMOOTH).save("filter_SMOOTH.jpeg")
##    im.filter(ImageFilter.SMOOTH_MORE).save("filter_SMOOTH_MORE.jpeg")
##    im.filter(ImageFilter.SHARPEN).save("filter_SHARPEN.jpeg")
    
##    im = Image.open(image_name)
##    im = im.filter(ImageFilter.MedianFilter())
##    im.save("1_MedianFilter.jpeg")
##    enhancer = ImageEnhance.Contrast(im)
##    im = enhancer.enhance(4)
##    im.save("2_ImageEnhance.jpeg")
##    im = im.filter(ImageFilter.MaxFilter(3))
##    im = im.filter(ImageFilter.ModeFilter(3))
##    
##    im.save("2_1_MaxFilter.jpeg")
##    im = im.convert('1')
##    im.save("3_convert_1.jpeg")
##    im = im.filter(ImageFilter.MinFilter(3))
##    im = im.filter(ImageFilter.MaxFilter(3))
##    #im = im.filter(ImageFilter.MaxFilter(3))
##    im.save("4_convert_1.jpeg")
##
##    
##
##    codestr = image_to_string(im)
##    print 'codestr:', codestr
##    codestr = image_file_to_string(processImagePath)
##    codestr = image_file_to_string('C:\\temp\\fnord.tif')
##    img = Image.open('C:\\temp\\phototest.tif')
##    text = image_to_string(img)
##    print 'text: ', text
    return 'aabb'

def is_line_pt_color(color):
    value = 10
    if color[0]<value and color[1]<value and color[2]<value:
        return True
    else:
        return False

def is_pt_has_edge(im, x, y):
    w,h = im.size
    cc = [\
        (x-1,y),\
        (x+1,y),\
        (x,y-1),\
        (x,y+1)\
        ]
    counter = 0
    for c in cc:
        xx = c[0]
        yy = c[1]
        if xx>=0 and xx<w and yy>=0 and yy<h:
            color = im.getpixel((xx,yy))
            if color[0]>210 and color[1]>210 and color[2]>210:
                counter += 1

    if counter>=2:
        return True
    return False
    
def filter_line(im):
    w,h = im.size
    cc = []
    for x in range(w):
        for y in range(h):
            color = im.getpixel((x,y))
            if x==75 and y==16:
                print color
            if is_line_pt_color(color):
                if is_pt_has_edge(im, x, y):
                    c = (x,y)
                    cc += [c]
                    color = (255, 255, 255)
                    im.putpixel(c, color)


##    for c in cc:
##        color = (255, 255, 255)
##        im.putpixel(c, color)
    
def get_code_str_from_image_yy(image_name):
    im = Image.open(image_name)
    
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(4)
    newName = "0_ImageEnhance.jpeg"
    im.save(newName)
    im = Image.open(newName)

    im = im.filter(ImageFilter.MedianFilter())
    newName = "1_0_MedianFilter.jpeg"
    im.save(newName)
    im = Image.open(newName)


    
    filter_line(im)
    filter_line(im)
    filter_line(im)
    filter_line(im)
    filter_line(im)
    filter_line(im)
    newName = "1_ImageEnhance.jpeg"
    im.save(newName)
    im = Image.open(newName)


    im = im.convert('1')
    newName = "3_convert_1.jpeg"
    im.save(newName)
    im = Image.open(newName)


##    im = im.filter(ImageFilter.MaxFilter(3))
##    im = im.filter(ImageFilter.ModeFilter(3))
##    
##    im.save("2_1_MaxFilter.jpeg")
##    im = im.convert('1')
##    im.save("3_convert_1.jpeg")
##    im = im.filter(ImageFilter.MinFilter(3))
##    im = im.filter(ImageFilter.MaxFilter(3))
##    #im = im.filter(ImageFilter.MaxFilter(3))
##    im.save("4_convert_1.jpeg")

    

    codestr = image_to_string(im)
    print 'codestr:', codestr
##    codestr = image_file_to_string(processImagePath)
##    codestr = image_file_to_string('C:\\temp\\fnord.tif')
##    img = Image.open('C:\\temp\\phototest.tif')
##    text = image_to_string(img)
##    print 'text: ', text
    return 'aabb'

def test_uuy():
    UU = windll.LoadLibrary('UUWiseHelper')

    # 初始化函数调用
    setSoftInfo = UU.uu_setSoftInfoW
    login = UU.uu_loginW
    recognizeByCodeTypeAndPath = UU.uu_recognizeByCodeTypeAndPathW
    getResult = UU.uu_getResultW
    uploadFile = UU.uu_UploadFileW
    getScore = UU.uu_getScoreW
    # 初始化函数调用

    user_i = ""
    passwd_i = ""

    s_id = c_int(91219)   # 授权 ID
    s_key = c_wchar_p('b6ef521449e2456fae07be997572f6b6')  # 授权Key
    user = c_wchar_p(user_i)  # 授权用户名
    passwd = c_wchar_p(passwd_i)  # 授权密码

    pic_file_path = "test.jpeg"

    ret = setSoftInfo(s_id, s_key)		#设置软件ID和KEY，仅需要调用一次即可，不需要每次上传图片都调用一次，特殊情况除外，比如当成脚本执行的话
    print ret
    ret = login(user, passwd)		#用户登录，仅需要调用一次即可，不需要每次上传图片都调用一次，特殊情况除外，比如当成脚本执行的话
    print ret

    if ret > 0:
        print('login ok, user_id:%d' % ret)  #登录成功返回用户ID
    else:
        print('login error')
        sys.exit(0)

    ret = getScore(user, passwd)  #获取用户当前剩余积分
    print('The Score of User : %s  is :%d' % (user.value, ret))

    result=c_wchar_p("")
    code_id = recognizeByCodeTypeAndPath(c_wchar_p(pic_file_path),c_int(3004),result)
    if code_id <= 0:
        print('get result error ,ErrorCode: %d' % code_id)
    else:
        print("the resultID is :%d result is %s" % (code_id,result))  #识别结果为宽字符类型 c_wchar_p,运用的时候注意转换一下
        if result!=c_wchar_p(u"PHCY"):
            rr = UU.uu_reportError(code_id)
            print "recognize error: ", rr

    raw_input('press any  Enter key to exit')

    
if __name__=='__main__':
    test_uuy()
##    imgName = "getimage.bmp"
##    code = get_code_str_from_image_qq(imgName)
##    print code
