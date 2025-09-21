from PIL import Image 
import io 

## 1
## 2
# img = Image.open("images/sky1.jpg")
# img.show() 

## 3
# img1 = Image.open("sky2.jpg") 
# img1 = img1.convert("L") 
# img1.show()

## 4
# f = open("sky2.jpg", "rb") 
# img2 = Image.open(f) 
# img2.show() 
# f.close() 

# # 5
# f = open("sky1.jpg", "rb") 
# # Сохраните изображение в переменной: 
# i = f.read()
# f.close() 
# # Закрываем файл 
# # Передаем объект: 
# img = Image.open(io.BytesIO(i))
# # выводим изображение на экран:
# img.show()


## 2
## 1
# img = Image.open("images/sky1.jpg") 
# print(img.size, img.format, img.mode,end="\n")
# print(img.info)

## 2
# img = Image.open("images/sky2.jpg")
# print(img.mode)

## 3
# img = Image.open("images/sky2.jpg")
# print(img.size)

## 4
# img = Image.open("images/sky2.jpg")
# print(img.getbbox())


# # 3
# # 1
# img = Image.open("images/sky2.jpg")
# obj = img.load() 
# for i in range(150):
#     for j in range(150):
#         obj[i, j] = (255, 0, 0)
# img.show()  

# # 2
# img = Image.open("images/sky1.jpg")
# obj = img.load() 
# for i in range(150):
#     for j in range(150):
#         img.putpixel((i, j), (0, 0, 255)) 
# print(img.getpixel((120, 120)))
# img.show() 


## 4
## 1
# img = Image.open("images/sky2.jpg")
# print(img.mode)
# img.show()
# R, G, B = img.split()
# mask = Image.new("L", img.size, 128)
# img2 = Image.merge("RGBA", (R, G, B, mask))
# print(img2.mode)
# img2.show()

## 2
# img = Image.open("images/sky1.jpg")
# print(img.mode)
# img2 = img.convert("RGBA")
# print(img2.mode)
# img2.show()
# pil_im = Image.open('images/sky1.jpg').convert('L')
# pil_im.show()

## 3
# img = Image.open("images/sky1.jpg")
# print(img.mode)
# img2 = img.convert("P", None, Image.FLOYDSTEINBERG, Image.ADAPTIVE, 128)
# print(img2.mode)


# # 5
## 1
# img = Image.open("images/sky2.jpg")
# img.save("savedsky.jpg") 
# img.save("savedsky.png", "PNG") 
# f = open("images/sky2.png", "wb")
# img.save(f, "PNG")
# f.close()


## 6
## 1
# img = Image.new("RGB", (100, 100)) 
# img.show()

## 2
# img = Image.new("RGB", (100,100), (255,0,0))
# img.show()

## 3
# img = Image.new("RGB", (100,100), "green")
# img.show()

## 4
# img = Image.new("RGB", (100, 100), "#4a412a") 
# img.show() 

## 5
# img = Image.new("RGB", (100, 100), "white") 
# img.show() 

## 6
# img = Image.new("RGB", (320, 240), "silver") 
# img.show() 

## 7
# img = Image.new("RGB", (320, 240), "rgb(205, 100,200)") 
# img.show() 

## 8
# img = Image.new("RGB", (320, 240), "rgb(10%, 100%,40%)") 
# img.show() 

## 9
# img = Image.new("RGB", (640, 480), "rgb(205, 100,200)") 
# img.show() 
# for x in range(640): 
#     for y in range(480): 
#         img.putpixel((x,y),(0,160,0)) 
# img.save("okno.png", "PNG") 
# img.show() 

## 10
# img = Image.new("RGB", (640, 480), "rgb(205, 100,200)") 
# img.show() 
# for x in range(640): 
#     for y in range(480): 
#         img.putpixel((x,y),(((x//3),((x+y)//6), y//3)))
# img.save("okno.png", "PNG") 
# img.show() 