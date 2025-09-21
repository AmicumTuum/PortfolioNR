from skimage import data
from skimage import filters
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import numpy as np
from skimage.color import rgb2hsv
import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray


# plt.figure(figsize=(15, 15))
# coffee = data.coffee()
# plt.subplot(1, 2, 1)
# plt.imshow(coffee)
# plt.show()



# plt.figure(figsize=(15, 15))
# coffee = data.coffee()
# plt.subplot(1, 2, 1)
# plt.imshow(coffee)
# gray_coffee = rgb2gray(coffee)
# plt.subplot(1, 2, 2)
# plt.imshow(gray_coffee, cmap="gray")
# plt.show()
# io.imsave("coffee.png", coffee)


# plt.figure(figsize=(15, 15))
# coffee = data.coffee()
# plt.subplot(1, 2, 1)
# plt.imshow(coffee)
# hsv_coffee = rgb2hsv(coffee)
# plt.subplot(1, 2, 2)
# hsv_coffee_colorbar = plt.imshow(hsv_coffee)
# plt.colorbar(hsv_coffee_colorbar, fraction=0.046, pad=0.04)
# plt.show()


# coffee = data.coffee()
# gray_coffee = rgb2gray(coffee)
# plt.figure(figsize=(15, 15))

# for i in range(10):
#     binarized_gray = (gray_coffee > i*0.1)*1
#     plt.subplot(5,2,i+1)
#     plt.title("Threshold: >"+str(round(i*0.1,1)))
#     plt.imshow(binarized_gray, cmap = 'gray')

# plt.tight_layout()
# plt.show()


# plt.figure(figsize=(15, 15))
# coffee = data.coffee()
# gray_coffee = rgb2gray(coffee)
# threshold = filters.threshold_otsu(gray_coffee)
# binarized_coffee = (gray_coffee > threshold)*1
# plt.subplot(2,2,1)
# plt.title("Threshold: >"+str(threshold))
# plt.imshow(binarized_coffee, cmap = "gray")
# threshold = filters.threshold_niblack(gray_coffee)
# binarized_coffee = (gray_coffee > threshold)*1
# plt.subplot(2,2,2)
# plt.title("Niblack Thresholding")
# plt.imshow(binarized_coffee, cmap = "gray")
# threshold = filters.threshold_sauvola(gray_coffee)
# plt.subplot(2,2,3)
# plt.title("Sauvola Thresholding")
# plt.imshow(threshold, cmap = "gray")
# binarized_coffee = (gray_coffee > threshold)*1
# plt.subplot(2,2,4)
# plt.title("Sauvola Thresholding - Converting to 0's and 1's")
# plt.imshow(binarized_coffee, cmap = "gray")
# plt.show()


# astronaut = data.astronaut()
# gray_astronaut = rgb2gray(astronaut)
# gray_astronaut_noiseless = gaussian(gray_astronaut, 1)
# x1 = 220 + 100*np.cos(np.linspace(0, 2*np.pi, 500))
# x2 = 100 + 100*np.sin(np.linspace(0, 2*np.pi, 500))
# snake = np.array([x1, x2]).T
# astronaut_snake = active_contour(gray_astronaut_noiseless, snake)
# fig = plt.figure(figsize=(10, 10))
# ax = fig.add_subplot(111)
# ax.imshow(gray_astronaut_noiseless)
# ax.plot(astronaut_snake[:, 0],  astronaut_snake[:, 1], '-b', lw=5)
# ax.plot(snake[:, 0], snake[:, 1], '--r', lw=5)
# plt.show()