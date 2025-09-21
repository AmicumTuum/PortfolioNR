from PIL import Image
from PIL import ImageFilter
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import cv2

## 1
## 1
# img = Image.open("sky1.jpg") 
# img.paste( (255, 0, 0), (0, 0, 100, 100) ) 
# img.show()
 
## 2
# img = Image.open("sky2.jpg") 
# img.paste( (0, 128, 0), img.getbbox() ) 
# img.show()


## 2
## 1
# img = Image.open("sky2.jpg") 
# img2 = img.resize((400,340))
# print(img2.size)
# img.paste((0,255,255), (9,9,211,161))
# img.paste(img2, (10,10))
# img.show()


## 2
# img = Image.open("sky1.jpg")
# white = Image.new("RGB", (img.size[0], 100), (255, 255, 255))
# mask = Image.new("L", (img.size[0], 100), 64)
# img.paste(white, (0,0), mask)
# img.show()

## 3
# img = Image.open("sky2.jpg")
# box = (200, 200, 800, 800)
# region = img.crop(box)
# region = region.transpose(Image.Transpose.ROTATE_180)
# img.paste(region, box)
# img.show()

## 3
# image = cv2.imread("sky1.jpg")
# height = image.shape[0]
# width = image.shape[1]
# cv2.line(image, (0,0), (width-500, height-500), (0,0,255), 12)
# imS = cv2.resize(image, (960, 540))
# cv2.imshow('InitialMagnification', imS)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

## 4
# img = Image.open("sky2.jpg")
# filters = {ImageFilter.BLUR, ImageFilter.CONTOUR, ImageFilter.DETAIL, ImageFilter.EDGE_ENHANCE, ImageFilter.EDGE_ENHANCE_MORE, ImageFilter.EMBOSS,  ImageFilter.FIND_EDGES, ImageFilter.SHARPEN, ImageFilter.SMOOTH, ImageFilter.SMOOTH_MORE}
# for i in filters:
#     img2 = img.filter(i)
#     img2.show()

## 5
# img = array(Image.open("sky2.jpg").convert('L'))
# figure()
# gray()
# contour(img, origin='image')
# axis('equal')
# axis('off')
# plt.show()

## 6
# load image as grayscale
# img = cv2.imread('rock.jpg')

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # threshold input image using otsu thresholding as mask and refine with morphology
# ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
# kernel = np.ones((9,9), np.uint8)
# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# # put mask into alpha channel of result
# result = img.copy()
# result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
# result[:, :, 3] = mask

# # save resulting masked image
# cv2.imwrite('GRAF.png', result)

# img1 = Image.open('wall.jpg')
# img2 = Image.open('GRAF.png')
# img1.paste(img2, (550, 180), mask=img2)
# img1.show()