import os
import cv2

gray = cv2.imread("E:\\video_shot\\pics\\7_11400.jpg", 0)

circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=300)
#输出返回值，方便查看类型
print(circles)
#输出检测到圆的个数
print(len(circles[0]))

print('-------------我是条分割线-----------------')
#根据检测到圆的信息，画出每一个圆
for circle in circles[0]:
    #圆的基本信息
    print(circle[2])
    #坐标行列
    x=int(circle[0])
    y=int(circle[1])
    #半径
    r=int(circle[2])
    #在原图用指定颜色标记出圆的位置
    img=cv2.circle(gray,(x,y),r,(0,0,255),-1)
#显示新图像
cv2.imshow('res',img)
cv2.waitKey(0)