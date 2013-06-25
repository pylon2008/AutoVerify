# coding=GBK

import sys
sys.path.append('C:\Python27\Lib\site-packages\pytesser')

import Image,ImageEnhance,ImageFilter,ImageGrab
from pytesser import *

def filter_line(im):
    w,h = im.size
    cc = []
    for x in range(w):
        for y in range(h):
            c = (x,y)
            color = im.getpixel(c)
            #if color[0]>253 and color[1]>253 and color[2]>253:
            #print color
            if color[0]>100 and color[1]<200 and color[2]<200:
                color = (0, 0, 0)
                im.putpixel(c, color)
            else:
                color = (255, 255, 255)
                im.putpixel(c, color)

def get_code_str_from_image_qq(image_name):
    im = Image.open(image_name)
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(3)
    filter_line(im)
    codestr = image_to_string(im)
    return codestr

if __name__=='__main__':
    codeStr = get_code_str_from_image_qq("test.bmp")
    print codeStr
    raw_input("按任何键退出程序。")
