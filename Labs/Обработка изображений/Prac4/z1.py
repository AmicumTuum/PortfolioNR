from PIL import Image 
import cv2
import matplotlib.pyplot as plt

## 1
# img = Image.open("images/sky1.jpg") 
# img.show() 
# for x in range(img.size[0]): 
#     for y in range(img.size[1]): 
#         r,g,b = img.getpixel((x,y)) 
#         img.putpixel((x,y),(b,r,g)) 
# img.show() 

## 2
# img = Image.open("images/sky2.jpg") 
# R, G, B = img.split()
# img2 = Image.merge("RGB", (R, G, B))
# print(img2.mode)
# img2.show()

## 3
im = cv2.imread("images/sky1.jpg")
vals = im.mean(axis=2).flatten()
b, bins, patches = plt.hist(vals, 255)
plt.xlim([0,255])
plt.show()


## 4
## 1
# img = Image.open("images/sky2.jpg")
# img2 = img.copy()
# img2.show()
## 2
# img = Image.open("images/sky1.jpg")
# print(img.size)
# img.thumbnail((400,300), Image.Resampling.LANCZOS)
# print(img.size)
# img = Image.open("images/sky2.jpg")
# img.thumbnail((400,100), Image.Resampling.LANCZOS)
# print(img.size)
## 3
# img = Image.open("images/sky2.jpg")
# print(img.size)
# img.show() 
# newsize = (400, 400)
# imgnr = img.resize(newsize)
# print(imgnr.size)
# imgnr.show()


## 5
## 1
# img = Image.open("images/sky1.jpg")
# img2 = img.crop([0, 0, 400, 400])
# img.load()
# print(img2.size)

## 2
# img = Image.open("images/sky2.jpg")
# print(img.size)
# img.show()
# box = (200, 100, 600, 700)
# img2 = img.crop(box)
# newsize = (400,400)
# img2nr = img2.resize(newsize)
# img2nr.show()


## 6
## 1
# img = Image.open("images/sky1.jpg")
# print(img.size)
# img2 = img.rotate(90)
# print(img2.size)
# img3 = img.rotate(45, Image.Dither.NONE)
# print(img3.size)
# img4 = img.rotate(45, expand=True)
# print(img4.size)

## 2
# img = Image.open("images/sky2.jpg")
# img2 = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
# img2.show()
# img3 = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
# img3.show()
# img4 = img.transpose(Image.Transpose.ROTATE_90)
# img4.show()
# img5 = img.transpose(Image.Transpose.ROTATE_180)
# img5.show()