#include <opencv2\imgproc\imgproc.hpp>
#include <opencv2\opencv.hpp>
#include <math.h>

using namespace cv;
using namespace std; 

cv::Mat myblur(cv::Mat image)
{
	cv::Mat image_gray;
	cv::cvtColor(image, image_gray, CV_RGB2GRAY);
	cv::Mat image_bin;
	cv::threshold(image_gray, image_bin, 120, 255, THRESH_BINARY);
	cv::Mat image_open;
	cv::Mat element = cv::getStructuringElement(MORPH_RECT, cv::Size(3, 3));
	cv::morphologyEx(image_bin, image_open, MORPH_OPEN, element);

	return image_open;
}

vector<vector<cv::Point> > findContours(cv::Mat image)
{
	vector<vector<cv::Point> > contours;
	vector<Vec4i> hierarchy;
	cv::findContours(image, contours, hierarchy, RETR_CCOMP, CHAIN_APPROX_SIMPLE);
	cv::Mat image_temp;
	image.copyTo(image_temp);

	//cv::drawContours(image_temp, contours, -1, cv::Scalar(255, 255, 255), CV_FILLED);
	//cv::imshow("first draw", image_temp);

	int max_area = 0;
	int max_cnt = 0;
	for (int i = 0; i < contours.size(); i++)
	{
		double area = contourArea(contours[i]);
		if (area > max_area)
		{
			Scalar color(0, 0, 0);
			cv::drawContours(image, contours, i, color, CV_FILLED);
			max_area = area;
			max_cnt = i;
		}
		else
		{
			Scalar color(0, 0, 0);
			cv::drawContours(image, contours, i, color, CV_FILLED);
		}
	}
	std::cout << "max_cnt:" << max_cnt << endl;
	Scalar color(255, 255, 255);
	cv::drawContours(image, contours, max_cnt, color, CV_FILLED);
	
	cv::findContours(image, contours, hierarchy, RETR_CCOMP, CHAIN_APPROX_SIMPLE);

	return contours;
}

double getDistance(cv::Point2f p1, cv::Point2f p2)
{
	return sqrt((p1.x - p2.x)*(p1.x - p2.x) + (p1.y - p2.y)*(p1.y - p2.y));
}

vector<cv::Point> findCorner(vector<vector<cv::Point> > contours)
{
	vector<cv::Point> bigestContour;
	vector<cv::Point> corners;
	int corners_num = 0;
	cv::Point p;
	for (int i = 0; i < contours[0].size(); i++)
	{
		p.x = contours[0][i].x;
		p.y = contours[0][i].y;
		bigestContour.push_back(p);
	}

	int icount = bigestContour.size();
	float fmax = -1;//用于保存局部最大值
	int   imax = -1;
	bool  bstart = false;
	for (int i = 0; i<bigestContour.size(); i++){
		Point2f pa = (Point2f)bigestContour[(i + icount - 7) % icount];
		Point2f pb = (Point2f)bigestContour[(i + icount + 7) % icount];
		Point2f pc = (Point2f)bigestContour[i];
		//两支撑点距离
		float fa = getDistance(pa, pb);
		float fb = getDistance(pa, pc) + getDistance(pb, pc);
		float fang = fa / fb;
		float fsharp = 1 - fang;
		if (fsharp>0.05){
			bstart = true;
			if (fsharp>fmax){
				fmax = fsharp;
				imax = i;
				corners.push_back(bigestContour[imax]);
			}
		}
		else{
			if (bstart){
				imax = -1;
				fmax = -1;
				bstart = false;
			}
		}
	}

	return corners;
}

vector<cv::Point> findMinCoord(vector<cv::Point> contours)
{
	vector<int> add;
	vector<int> minus;

	vector<cv::Point> res;

	for (int i = 0; i < contours.size(); ++i)
	{
		int add_temp = contours[i].x + contours[i].y;
		int minus_temp = contours[i].x - contours[i].y;

		add.push_back(add_temp);
		minus.push_back(minus_temp);
	}
	int add_max = 0;
	int add_min = INT_MAX;
	int minus_max = 0;
	int minus_min = 0;
	int add_max_idx = 0;
	int add_min_idx = 0;
	int minus_max_idx = 0;
	int minus_min_idx = 0;
	for (int i = 0; i < contours.size(); i++)
	{
		if (add[i] >= add_max)
		{
			add_max = add[i];
			add_max_idx = i;
		}
		if (add[i] <= add_min)
		{
			add_min = add[i];
			add_min_idx = i;
		}
		if (minus[i] >= minus_max)
		{
			minus_max = minus[i];
			minus_max_idx = i;
		}
		if (minus[i] <= minus_min)
		{
			minus_min = minus[i];
			minus_min_idx = i;
		}
	}

	res.push_back(contours[add_min_idx]);////左上角
	res.push_back(contours[add_max_idx]);////右下角
	res.push_back(contours[minus_min_idx]);///左下角
	res.push_back(contours[minus_max_idx]);///右上角

	return res;
}

vector<cv::Point> checkPoint(vector<cv::Point> coord1, vector<cv::Point> coord2)
{
	int threshold = 5;
	vector<cv::Point> res;
	for (int i = 0; i < 4; i++)
	{
		float dis = getDistance(coord1[i], coord2[i]);
		cv::Point p;
		if (dis < threshold)
		{
			p.x = int((coord1[i].x + coord2[i].x) / 2);
			p.y = int((coord1[i].y + coord2[i].y) / 2);
		}
		else
		{
			p.x = int(coord1[i].x);
			p.y = int(coord1[i].y);
		}
		res.push_back(p);
	}
	return res;
}

vector<cv::Point> changeContorus(vector<vector<cv::Point> > contours)
{
	vector<cv::Point> cornersFromContours;
	cv::Point p;
	for (int i = 0; i < contours[0].size(); i++)
	{
		p.x = contours[0][i].x;
		p.y = contours[0][i].y;
		cornersFromContours.push_back(p);
	}
	return cornersFromContours;
}

vector<cv::Point> Corners(cv::Mat image)
{
	if (image.cols <= 0 || image.rows <= 0 || image.channels() != 3)
	{
		cout << "PICTURE ERROR!" << endl;
		exit(-1);
	}

	cv::Mat image_open = myblur(image);//图像模糊

	vector<vector<cv::Point> > contours = findContours(image_open);///找到边界

	vector<cv::Point> cornersFromContours = changeContorus(contours);///把坐标点存到Vector中
	vector<cv::Point> minCorners1 = findMinCoord(cornersFromContours);///找到四个顶角

	vector<cv::Point> corners = findCorner(contours);///在轮廓点中找到支撑角
	vector<cv::Point> minCorners2 = findMinCoord(corners);///在支撑角中找到四个顶角

	vector<cv::Point> coord = checkPoint(minCorners1, minCorners2);///确定坐标

	return coord;
}

int main()
{
	string file = "E:\\video_shot\\videos\\pics\\6_1800.jpg";
	cv::Mat image = cv::imread(file);

	vector<cv::Point> coord = Corners(image);

	std::cout << "coord: " << endl;
	for (int i = 0; i < coord.size(); i++)
	{
		std::cout << coord[i].x << " " << coord[i].y << endl;
		cv::circle(image, cv::Point(coord[i].x, coord[i].y), 4, cv::Scalar(0, 0, 255), -1);
	}
	cv::imshow("image", image);

	cv::waitKey(0);
	return 0;
}