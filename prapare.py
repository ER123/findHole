import cv2
import os
import numpy as np 

def praProcess(file):
	img = cv2.imread(file, 0)
	assert len(img.shape) == 2

	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] > 120.0:
				img[i][j] = 255
			else:
				img[i][j] = 0.0
	cv2.imshow("img_0_1", img)

	return img 

	'''
	#霍夫变换
	circles= cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,param1=30,param2=3,minRadius=5,maxRadius=30)
	for circle in circles[0]:
		#圆的基本信息
		print(circle[2])
		#坐标行列
		x=int(circle[0])
		y=int(circle[1])
		#半径
		r=int(circle[2])
		#在原图用指定颜色标记出圆的位置
		gray1=cv2.circle(img,(x,y),r,(0,0,255),-1)
	#显示新图像
	#cv2.imshow('res',gray1)
	#cv2.waitKey(0) 
	'''
	#滤波
	img_blur = cv2.blur(img, ksize=(3,3))
	img_canny = cv2.Canny(img_blur, 5, 40)
	cv2.imshow("canny", img_canny)
	cv2.imshow("src", img_blur)
	cv2.waitKey(0)


def diff(file1, file2):
	img1 = cv2.imread(file1, 0)
	img2 = cv2.imread(file2, 0)

	img1 = praProcess(file1)
	img2 = praProcess(file2)
	img = img1 - img2	

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	img_open = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

	cv2.imshow("res", img)
	cv2.imshow("res1", img_open)
	cv2.waitKey(0)

def CornerHarris(file):
	#img = cv2.imread(file, 0)
	img = praProcess(file)
	cv2.imshow("src", img)
	img = np.float32(img)
	img = cv2.cornerHarris(img, 2, 3, 0.05, cv2.BORDER_DEFAULT)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	img_open = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)

	cv2.imshow("cornerHarris", img_open)
	cv2.waitKey(0)

	
	img = cv2.imread(file)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img = praProcess(file)
	gray = np.float32(img)

	# 输入图像必须是 float32 ,最后一个参数在 0.04 到 0.05 之间
	dst = cv2.cornerHarris(gray,2,3,0.04)

	#result is dilated for marking the corners, not important
	dst = cv2.dilate(dst,None)

	# Threshold for an optimal value, it may vary depending on the image.
	#img[dst>0.02*dst.max()]=[0,0,255]

	cv2.imshow('dst',img)
	if cv2.waitKey(0) & 0xff == 27:
		cv2.destroyAllWindows()

if __name__ == '__main__':
	file = "E:\\video_shot\\pics\\7_11400.jpg"

	file1="E:\\video_shot\\pics\\8_12600.jpg"
	file2="E:\\video_shot\\pics\\8_13200.jpg"

	#praProcess(file)#二值化
	#diff(file1, file2)#差分，开运算

	CornerHarris(file)

	
import cv2
import os
import numpy as np 

def praProcess(file):
	img = cv2.imread(file, 0)
	#img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	assert len(img.shape) == 2

	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] > 136.0:
				img[i][j] = 0
			else:
				img[i][j] = 255

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	img_open = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	cv2.imshow("img_open", img_open)

	img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	cv2.imshow("img_close", img_close)

	img_close = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
	cv2.imshow("img_close", img_close)

	img_close = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
	cv2.imshow("img_close", img_close)

	img_close_dilate = cv2.morphologyEx(img_close, cv2.MORPH_DILATE, kernel)
	img_close_dilate = cv2.morphologyEx(img_close_dilate, cv2.MORPH_DILATE, kernel)
	img_close_dilate = cv2.morphologyEx(img_close_dilate, cv2.MORPH_DILATE, kernel)

	cv2.imshow("img_close_dilate", img_close_dilate)

	image, contours, hierarchy = cv2.findContours(img_close_dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	for i in range(0,len(contours)): 
		x, y, w, h = cv2.boundingRect(contours[i])  
		cv2.rectangle(image, (x,y), (x+w,y+h), (150,150,255), 2)

	cv2.imshow("contours", image)

	cv2.waitKey(0)
	return img 

	'''
	#霍夫变换
	circles= cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,param1=30,param2=3,minRadius=5,maxRadius=30)
	for circle in circles[0]:
		#圆的基本信息
		print(circle[2])
		#坐标行列
		x=int(circle[0])
		y=int(circle[1])
		#半径
		r=int(circle[2])
		#在原图用指定颜色标记出圆的位置
		gray1=cv2.circle(img,(x,y),r,(0,0,255),-1)
	#显示新图像
	#cv2.imshow('res',gray1)
	#cv2.waitKey(0) 
	'''
	#滤波
	img_blur = cv2.blur(img, ksize=(3,3))
	img_canny = cv2.Canny(img_blur, 5, 40)
	cv2.imshow("canny", img_canny)
	cv2.imshow("src", img_blur)
	cv2.waitKey(0)


def diff(file1, file2):
	img1 = cv2.imread(file1, 0)
	img2 = cv2.imread(file2, 0)

	img1 = praProcess(file1)
	img2 = praProcess(file2)
	img = img1 - img2	

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	img_open = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

	cv2.imshow("res", img)
	cv2.imshow("res1", img_open)
	cv2.waitKey(0)

def CornerHarris(file):
	#img = cv2.imread(file, 0)
	img = praProcess(file)
	cv2.imshow("src", img)
	img = np.float32(img)
	img = cv2.cornerHarris(img, 2, 3, 0.05, cv2.BORDER_DEFAULT)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	img_open = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)

	cv2.imshow("cornerHarris", img_open)
	cv2.waitKey(0)

	
	img = cv2.imread(file)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img = praProcess(file)
	gray = np.float32(img)

	# 输入图像必须是 float32 ,最后一个参数在 0.04 到 0.05 之间
	dst = cv2.cornerHarris(gray,2,3,0.04)

	#result is dilated for marking the corners, not important
	dst = cv2.dilate(dst,None)

	# Threshold for an optimal value, it may vary depending on the image.
	#img[dst>0.02*dst.max()]=[0,0,255]

	cv2.imshow('dst',img)
	if cv2.waitKey(0) & 0xff == 27:
		cv2.destroyAllWindows()

if __name__ == '__main__':
	file = "C:\\Users\\ER\\Desktop\\mima.jpg"
	#file = "E:\\video_shot\\pics\\7_11400.jpg"

	#file1="E:\\video_shot\\pics\\8_12600.jpg"
	#file2="E:\\video_shot\\pics\\8_13200.jpg"

	praProcess(file)#二值化
	#diff(file1, file2)#差分，开运算	

	#CornerHarris(file)
