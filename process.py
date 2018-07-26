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

def findcontours(img_open):	
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
				#print("c_min:", c_min)
				cv2.drawContours(img_draw, c_min, -1, (0, 0 ,0), cv2.FILLED)
			max_area = area
			max_cnt = cnt
		else:
			c_min = []
			c_min.append(cnt)
			#print("c_min:", c_min)
			cv2.drawContours(img_draw, c_min, -1, (0, 0 ,0), cv2.FILLED)	
	c_max.append(max_cnt)
	cv2.drawContours(img_draw, c_max, -1, (255, 255, 255), thickness=-1)
	cv2.imshow("contours", img_draw)

	#再次寻找轮廓
	img_contours, contours, hierarchy = cv2.findContours(img_draw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#print("len contours", len(contours[0]))
	return contours

def getDistance(p1, p2):
	return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def findCorner(contours):
	res_idx = []
	icount = len(contours[0])
	#print(icount)
	fmax = -1
	imax = -1
	bsatar = False
	for c in contours:
		#print(len(c))
		for i in range(len(contours[0])):
			pa = contours[0][(i+icount-7)%icount][0]
			pb = contours[0][(i+icount+7)%icount][0]
			pc = contours[0][i][0]

			fa = getDistance(pa, pb)
			fb = getDistance(pa, pc) + getDistance(pb, pc)
			fang = np.float32(fa/fb)
			fsharp = 1 - fang

			if fsharp>0.1:
				bsatar = True
				if fsharp > fmax:
					fmax = fsharp
					imax = i
					res_idx.append(imax)
			else:
				if bsatar:
					#res_idx.append(imax)
					imax = -1
					fmax = -1
					bsatar = False

	return contours, res_idx


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

	return  coord_contours, coord_corner

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
	threshold = 5
	coord = []
	for i in range(4):
		dis = getDistance((coord1[i*2], coord1[i*2+1]), (coord2[i*2], coord2[i*2+1]))
	
		if dis<threshold and np.abs(coord1[i*2]-coord2[i*2])<threshold and np.abs(coord1[i*2+1]-coord2[i*2+1])<threshold:
			coord_x = (coord1[i*2]+coord2[i*2])/2
			coord_y = (coord1[i*2+1]+coord2[i*2+1])/2
			coord.append(int(coord_x))
			coord.append(int(coord_y))
		else:
			coord.append(coord1[i*2])
			coord.append(coord1[i*2+1])

	return coord

def perspective(contours, image):

	rect = cv2.minAreaRect(contours[0])
	box = cv2.boxPoints(rect)
	box = np.int0(box)

	xs = np.min(box, axis=0)[0]
	xe = np.max(box, axis=0)[0]
	ys = np.min(box, axis=0)[1]
	ye = np.max(box, axis=0)[1]

	pts_dst = np.float32([[xs, ys], [xe, ys], [xe, ye], [xs, ye]])
	pts_src = np.float32([[coord[0], coord[1]], [coord[4], coord[5]] ,[coord[2], coord[3]], [coord[6], coord[7]] ])

	M = cv2.getPerspectiveTransform(pts_src, pts_dst)
	warp = cv2.warpPerspective(image, M, (image.shape[1],image.shape[0]), cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, cv2.BORDER_REPLICATE)

	return warp

if __name__ == '__main__':
	'''
	path = "E:\\video_shot\\videos\\targetPics"
	f = open("E:\\video_shot\\videos\\targetPics.txt", "w")
	for path, d, fileList in os.walk(path):
		for file in fileList:
			if file.endswith(".jpg"):
				f.write(os.path.join(path, file))
				f.write("\n")
	f.close()
	'''
	savePics = False
	
	f = open("E:\\video_shot\\videos\\list.txt", "r")
	fileList = f.readlines()

	dir = "E:\\video_shot\\videos\\targetPics\\"

	for file in fileList:
		file = file.strip().split(" ")
		img = cv2.imread(file[0])
		print("image:", file[0])

		img_blur = myblur(img) #图像形态学变换
		contours = findcontours(img_blur) #寻找轮廓		
		contours, idx = findCorner(contours) #找到支撑角和轮廓点

		coord1, coord2 = findCoord(contours, idx) #转换轮廓坐标和支撑角坐标
		coord = checkCoord(coord1, coord2) #从支撑角和轮廓点选出合适的顶角点
		print("coord", coord)
		warp = perspective(contours, img)#透视变换

		#print(idx)
		for i in idx:
			cv2.circle(img, (contours[0][i][0][0], contours[0][i][0][1]), 10, (0, 0, 255), 1)
		for i in range(4):
			cv2.circle(img, (int(coord[i*2]), int(coord[i*2+1])), 6, (0, 255, 0), -1)
		cv2.drawContours(img, contours,  -1, (0, 255, 255), thickness=1)
		cv2.imshow("warp", img)

		warp_blur = myblur(warp)
		contours = findcontours(warp_blur)
		#透视变换后再找到合适的顶角点
		contours, idx = findCorner(contours)
		coord1, coord2 = findCoord(contours, idx)
		coord = checkCoord(coord1, coord2)
	
		rect = warp[coord[1]:coord[3]+1, coord[0]:coord[2]+1, :]
		rect = cv2.resize(rect,(850,850))
		cv2.imshow("rect",rect)
		#cv2.imwrite("E:\\video_shot\\videos\\pics\\coord_warp_rect.jpg", rect)

		#for i in range(4):
		#	cv2.circle(warp, (int(coord[i*2]), int(coord[i*2+1])), 6, (0, 255, 0), -1)
		#cv2.imshow("coordwarp", warp)

		if savePics:
			filePath, fileName = os.path.split(file[0])
			fileName0, fileNmaeExt = os.path.splitext(fileName)
			savePath = os.path.join(dir, fileName)
			cv2.imwrite(savePath, rect)

		#cv2.imwrite("E:\\video_shot\\videos\\pics\\coord_warp.jpg", warp)
		if cv2.waitKey(0) & 0xFF == ord('q'):
			break
	
	f.close()