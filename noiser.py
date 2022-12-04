import cv2
import numpy as np
import datetime
import os
import copy
import time
import argparse
import math
from PIL import Image

parser = argparse.ArgumentParser(description='text2image')
parser.add_argument("-p", "--pic", type=str, help="picture to add noise to", default=None, dest='fyl')
parser.add_argument("-n", "--np", type=int, help="number of pixels to randomize", default=100, dest='numpix')
parser.add_argument("-t", "--top", type=int, help="top y coordinate of region", default=1, dest='top')
parser.add_argument("-l", "--left", type=int, help="left x coord of region", default=1, dest='left')
parser.add_argument("-b", "--bottom", type=int, help="bottom y coord of region", default=511, dest='bottom')
parser.add_argument("-r", "--right", type=int, help="right x coord of region", default=511, dest='right')
parser.add_argument("-s", "--source", type=str, help="source image", default=None, dest='source')

args = parser.parse_args()
fyl=args.fyl
if fyl is None:
    exit()
numpix=args.numpix
top=args.top
left=args.left
source=args.source
bottom=args.leftbottom=args.bottom
right=args.right
if source is not None:
    im2 = Image.open(source)



image1=cv2.imread(fyl)

# for noisy circle
# x=r*math.cos(theta)
# y=r*math.sin(theta)

for fzl in range(1,numpix):
    xpos=np.random.randint(left,right)
    ypos=np.random.randint(top,bottom)
    
    r=np.random.randint(0, 255)
    g=np.random.randint(0, 255)
    b=np.random.randint(0, 255)
    if source is not None:
        rgb1=im2.getpixel((xpos,ypos))
        rgb2=im2.getpixel((xpos+1,ypos))
        rgb3=im2.getpixel((xpos,ypos+1))
        rgb4=im2.getpixel((xpos+1,ypos+1))
        r1,g1,b1=rgb1 
        r2,g2,b2=rgb2
        r3,g3,b3=rgb3
        r4,g4,b4=rgb4 #r3=rgb3[0] #r4=rgb4[0]
        image1[ypos,xpos]=[b1, g1, r1]
        image1[ypos,xpos+1]=[b2, g2, r2]
        image1[ypos+1,xpos]=[b3, g3, r3]
        image1[ypos+1,xpos+1]=[b4, g4, r4]
    else:
        image1[ypos,xpos]=[b, g, r]
        image1[ypos,xpos+1]=[b, g, r]
        image1[ypos+1,xpos]=[b, g, r]
        image1[ypos+1,xpos+1]=[b, g, r]
        

   # image1[ypos,xpos]=[b, g, r]
   # image1[ypos,xpos+1]=[b, g, r]
   # image1[ypos+1,xpos]=[b, g, r]
   # image1[ypos+1,xpos+1]=[b, g, r]
    

cv2.imwrite(fyl, image1)

