import os
import cv2
import numpy as np 

def myblur(image):
	#img_src = cv2.imread(file)
	img_src = image
	#cv2.imshow("img_src", img_src)
	#img_blur = cv2.blur(img_src, ksize=(3,3))
	img_gary = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
	
	ret, img_bin = cv2.threshold(img_gary, 120, 255, cv2.THRESH_BINARY)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	img_open = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
	#cv2.imshow("img_open", img_open)

	return img_open

def findcontours(image):
	img_open = myblur(image)
	img_contours, contours, hierarchy = cv2.findContours(img_open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#print("len contours1", len(contours[0]))
	img_draw = img_open

	#只保留面积最大的区域
	c_max = []
	max_area = 0
	max_cnt = 0
	for i in range(len(contours)):
		cnt = contours[i]
		#print(cnt)
		area = cv2.contourArea(cnt)
		if (area>max_area):
			if max_area != 0:
				c_min = []
				c_min.append(max_cnt)
				cv2.drawContours(img_draw, c_min, -1, (0, 0 ,0), cv2.FILLED)
			max_area = area
			max_cnt = cnt
		else:
			c_min = []
			c_min.append(cnt)
			cv2.drawContours(img_draw, c_min, -1, (0, 0 ,0), cv2.FILLED)	
	c_max.append(max_cnt)
	cv2.drawContours(img_draw, c_max, -1, (255, 255, 255), thickness=-1)
	#cv2.imshow("contours", img_draw)

	#再次寻找轮廓
	img_contours, contours, hierarchy = cv2.findContours(img_draw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#print("len contours", len(contours[0]))
	return contours

def affine(image):
	#print("affine file", file)
	#img_src = cv2.imread(file)
	img_src = image
	contours = findcontours(image)

	#print(len(contours[0]))
	for c in contours:
		rect = cv2.minAreaRect(c)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		
		ROI = img_src.copy()
		M_rotate = cv2.getRotationMatrix2D((rect[0][0], rect[0][1]), rect[2], 1)
		ROI = cv2.warpAffine(ROI, M_rotate, (ROI.shape[1], ROI.shape[0]))
		cv2.imshow("ROI_warpAffine", ROI)
		ROI_src = ROI.copy()
		ROI_src1 = ROI.copy()
		#cv2.circle(img_src, (contours[0][0][0][0], contours[0][0][0][1]), 4, (255, 255, 0), 2)
		#for i in range(1, len(contours[0])):
		#	cv2.circle(img_src, (contours[0][i][0][0], contours[0][i][0][1]), 2, (0, int(0+i/2.0), 255), -1)
		#cv2.imshow("pointSRC", img_src)

		contours_new = findcontours(ROI)
		for c_new in contours_new:
			rect_new = cv2.minAreaRect(c_new)
			box_new = cv2.boxPoints(rect_new)
			box_new = np.int0(box_new)

			xs = np.min(box_new, axis=0)[0]
			xe = np.max(box_new, axis=0)[0]
			ys = np.min(box_new, axis=0)[1]
			ye = np.max(box_new, axis=0)[1]
			print("box_new:",box_new)
			print("xs,ys,xe,ye:",xs,ys,xe,ye)
			target = ROI[ys:ye, xs:xe]
			target = target.copy()
			cv2.imshow("target", target)
			#cv2.imwrite("E:\\video_shot\\videos\\pics\\7_4200_target.jpg", target)

			#left_bottom_x, left_bottom_y, right_bottom_x, right_bottom_y = findCoord(contours_new)
			#print(left_bottom_x, left_bottom_y, right_bottom_x, right_bottom_y)

			#pentagram = contours_new[0] 
			#leftmost = tuple(pentagram[:,0][pentagram[:,:,0].argmin()])  
			#rightmost = tuple(pentagram[:,0][pentagram[:,:,0].argmax()]) 
			#upmost = tuple(pentagram[:,0][pentagram[:,:,1].argmin()])  
			#downmost = tuple(pentagram[:,0][pentagram[:,:,1].argmax()])   
			#print(leftmost, rightmost, upmost, downmost)
			#cv2.circle(ROI, leftmost, 5, (0, 255, 0), -1)
			#cv2.circle(ROI, rightmost, 5, (0, 255, 0), -1)
			#cv2.circle(ROI, upmost, 5, (0, 255, 0), -1)
			#cv2.circle(ROI, downmost, 5, (0, 255, 0), -1)
			#print(contours_new)
			#print(contours_new[0][1][0][0])
			
			cv2.circle(ROI, (contours_new[0][0][0][0], contours_new[0][0][0][1]), 4, (255, 255, 0), 2)
			for i in range(1, len(contours_new[0])):
				cv2.circle(ROI, (contours_new[0][i][0][0], contours_new[0][i][0][1]), 2, (0, int(0+i/2.0), 255), -1)
				#cv2.circle(ROI, (left_bottom_x, left_bottom_y), 5, (0, 255, 0), -1)
			cv2.imshow("pointROI", ROI)

	#for i in range(len(contours_new[0])):
	#	contours_new[0][i][0][0] = contours_new[0][i][0][0] - xs
	#for i in range(len(contours_new[0])):
	#	contours_new[0][i][0][1] = contours_new[0][i][0][1] - ys

	return contours_new, ROI_src

def findCorner(image):
	contours, image = affine(image)
	#cv2.imshow("conor_src", image)
	res_idx = []
	icount = len(contours[0])
	fmax = -1
	imax = -1
	bsatar = False
	for c in contours:
		for i in range(len(contours[0])):
			pa = contours[0][(i+icount-7)%icount][0]
			pb = contours[0][(i+icount+7)%icount][0]
			pc = contours[0][i][0]
			#print("pa, pb, pc:",pa, pb, pc)

			fa = getDistance(pa, pb)
			fb = getDistance(pa, pc) + getDistance(pb, pc)
			fang = np.float32(fa/fb)
			fsharp = 1 - fang

			if fsharp>0.05:
				bsatar = True
				if fsharp > fmax:
					fmax = fsharp
					imax = i
			else:
				if bsatar:
					res_idx.append(imax)
					cv2.circle(image, (contours[0][imax][0][0], contours[0][imax][0][1]), 4, (0, 0, 255), 1)
					imax = -1
					fmax = -1
					bsatar = False
	cv2.imshow("corner", image)

	return contours, res_idx


def getDistance(p1, p2):
	return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def findCoord(contours, idx):
	coord = []
	idx_coord = 0
	for i in (idx):
		x = contours[0][idx][idx_coord][0][0]
		y = contours[0][idx][idx_coord][0][1]
		idx_coord += 1
		coord.append([x,y])
	#print(coord)

	coord_corner = findMinCoord(coord)

	contours_temp = []
	for i in range(len(contours[0])):
		x = contours[0][i][0][0]
		y = contours[0][i][0][1]
		contours_temp.append([x,y])
	#print(contours_temp)

	coord_contours = findMinCoord(contours_temp)

	return coord_corner, coord_contours

def findMinCoord(coord):
	coord_temp0 = np.zeros(len(coord))
	coord_temp1 = np.zeros(len(coord))
	for i in range(len(coord)):
		coord_temp0[i] = coord[i][0] + coord[i][1]
		coord_temp1[i] = coord[i][0] - coord[i][1]

	left_top = np.where(coord_temp0 == np.min(coord_temp0, axis=0))
	right_bottom = np.where(coord_temp0 == np.max(coord_temp0, axis=0))
	right_top = np.where(coord_temp1 == np.max(coord_temp1, axis=0))
	left_bottom = np.where(coord_temp1 == np.min(coord_temp1, axis=0))

	left_top_x = coord[left_top[0][0]][0]
	left_top_y = coord[left_top[0][0]][1]
	right_bottom_x = coord[right_bottom[0][0]][0]
	right_bottom_y = coord[right_bottom[0][0]][1]
	right_top_x = coord[right_top[0][0]][0]
	right_top_y = coord[right_top[0][0]][1]
	left_bottom_x = coord[left_bottom[0][0]][0]
	left_bottom_y = coord[left_bottom[0][0]][1]

	res = [left_top_x,left_top_y,right_bottom_x,right_bottom_y,right_top_x,right_top_y,left_bottom_x,left_bottom_y]

	return res

def checkCoord(coord1, coord2):
	coord = np.zeros(len(coord1))
	for i in range(4):
		dis = getDistance((coord1[i*2], coord1[i*2+1]), (coord2[i*2], coord2[i*2+1]))
		print(dis)
		if dis<15 and np.abs(coord1[i*2]-coord2[i*2])<15 and np.abs(coord1[i*2+1]-coord2[i*2+1])<15:
			coord_x = (coord1[i*2]+coord2[i*2])//2
			coord_y = (coord1[i*2+1]+coord2[i*2+1])//2
			coord[i*2] = coord_x 
			coord[i*2+1] = coord_y
		else:
			coord[i*2] = coord1[i*2]
			coord[i*2+1] = coord1[i*2+1]

	return coord

def hough(image):
	gary = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gary,50,200)
	cv2.imshow("gray", gary)
	lines = cv2.HoughLinesP(edges,1,np.pi/180,30,minLineLength=100,maxLineGap=10)
	lines1 = lines[:,0,:]#提取为为二维
	for x1,y1,x2,y2 in lines1[:]: 
		cv2.line(image,(x1,y1),(x2,y2),(255,0,0),2)
	cv2.imshow("line:", image)


if __name__ == '__main__':
	file = "C:\\Users\\ER\Desktop\\test_code\\1_2400.jpg"
	img = cv2.imread(file)

	contours_new, ROI_src = affine(img)

	contours, idx = findCorner(img)
	coord1, coord2 = findCoord(contours, idx)
	coord = checkCoord(coord1, coord2)

	print("coord1:", coord1)
	print("coord2:",coord2)
	for i in range(4):
		cv2.circle(ROI_src, (coord1[i*2], coord1[i*2+1]), 4, (0,255,0),-1)
		cv2.circle(ROI_src, (coord2[i*2], coord2[i*2+1]), 4, (0,0,255),-1)
		cv2.circle(img, (coord1[i*2], coord1[i*2+1]), 4, (0,255,0),-1)
		cv2.circle(img, (coord2[i*2], coord2[i*2+1]), 4, (0,0,255),-1)
		cv2.circle(ROI_src, (int(coord[i*2]), int(coord[i*2+1])), 6, (255, 0, 0), -1)

	cv2.imshow("coord", ROI_src)
	cv2.imwrite("C:\\Users\\ER\Desktop\\test_code\\1_2400_coord.jpg", ROI_src)
	cv2.imshow("coord_yuan", img)
	cv2.imwrite("C:\\Users\\ER\Desktop\\test_code\\1_2400_coord1.jpg", img)
	#hough(img)
	cv2.waitKey(0)

