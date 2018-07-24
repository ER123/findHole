import os
import cv2

def copyPics(labelPath, picsPath):
	for path, d, fileList in os.walk(labelPath):
		for fileName in fileList:
			if fileName.endswith(".txt"):
				picName, extension = os.path.splitext(fileName)
				picPath = os.path.join(picsPath, picName+".jpg")
				if os.path.exists(picsPath):
					img = cv2.imread(picPath, 0)
					cv2.imwrite(os.path.join(labelPath, picName+".jpg"), img)

def genTrainAndVar(picspath):
	f0 = open(os.path.join(picspath, "train.txt"), "w")
	f1 = open(os.path.join(picspath, "var.txt"), "w")
	for path, d, fileList in os.walk(picspath):
		for fileName in fileList:
			if fileName.endswith('.jpg'):
				f0.write(os.path.join(path, fileName) + "\n")

	f0.close()
	f1.close()

imgPath = "E:\\video_shot\\pics\\1_360.jpg"
img = cv2.imread(imgPath, 0)
img = cv2.resize(img, (512,512))
cv2.imwrite("E:\\video_shot\\pics\\1_360_resize1.jpg", img)

if __name__ == '__main__':
	labelPath = "E:\\video_shot\\labels"
	picsPath = "E:\\video_shot\\pics"
	#copyPics(labelPath, picsPath)
	#genTrainAndVar("E:\\video_shot\\YOLO\\labels")