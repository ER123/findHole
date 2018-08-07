using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.IO;

using Emgu.CV;
using Emgu.Util;
using Emgu.CV.CvEnum;
using Emgu.CV.Structure;

namespace findCircle_vs2013
{
    class Program
    {      
        static void Main(string[] args)
        {
            string picsPath = "E:\\video_shot\\videos\\picsColor\\picsColor_.txt";
            StreamReader sr = new StreamReader(picsPath, Encoding.Default);
            string line;
            while ((line = sr.ReadLine()) != null)
            {
                string imgPath = line.ToString();
                Console.WriteLine(imgPath);

                Mat image = CvInvoke.Imread(imgPath, LoadImageType.Color);

                findContours(image);
            }

            //Capture capture = new Capture("E:\\video_shot\\videos\\16_25_22.264");
            ////Capture capture = new Capture("E:\\video_shot\\videos\\16_35_19.264");
            ////Capture capture = new Capture("E:\\video_shot\\videos\\16_35_24.264");
            ////Capture capture = new Capture("E:\\video_shot\\videos\\16_45_19.264");
            //int idx = 0;
            //while(true)
            //{
            //    Mat frame = capture.QueryFrame();
            //    idx += 1;
            //    if (frame != null)
            //    {
            //        Mat image = frame;
            //        if (idx % 472 == 0)
            //        {
            //            findContours(image);
            //        }
            //    }
            //}            
        }
        public static void findContours(Mat image)
        {
            Mat grayImage = new Mat();
            CvInvoke.CvtColor(image, grayImage, Emgu.CV.CvEnum.ColorConversion.Bgr2Gray);
                        
            Rectangle ROI = new Rectangle(280, 80, 800, 800);
            Mat imageROI = new Mat(grayImage, ROI);

            Mat cannyImage = new Mat();
            CvInvoke.Canny(imageROI, cannyImage, 100, 600);
            CvInvoke.Imshow("cannyImage", cannyImage);
            
            //Mat edge = new Mat();
            //CvInvoke.Canny(threshImage, edge, 30, 200);
            Emgu.CV.Util.VectorOfVectorOfPoint contours = new Emgu.CV.Util.VectorOfVectorOfPoint();
            Emgu.CV.IOutputArray hierarchy = new Mat();
            CvInvoke.FindContours(cannyImage, contours, null, Emgu.CV.CvEnum.RetrType.List, Emgu.CV.CvEnum.ChainApproxMethod.ChainApproxSimple);

            Point[][] con1 = contours.ToArrayOfArray();
            PointF[][] con2 = Array.ConvertAll<Point[], PointF[]>(con1, new Converter<Point[], PointF[]>(PointToPointF));

            Mat contoursImage = new Mat(image, ROI);
            for (int i = 0; i < contours.Size; i++)
            {
                Rectangle rect = new Rectangle();
                rect = CvInvoke.BoundingRectangle(contours[i]);
                double areaRect = rect.Width * rect.Height;

                CircleF circle = CvInvoke.MinEnclosingCircle(con2[i]);
                //CvInvoke.Circle(contoursImage, new Point((int)circle.Center.X, (int)circle.Center.Y), (int)circle.Radius, new MCvScalar(255, 0, 120), 1);

                if (isCircleCenter(circle) && isRectCenter(rect) && areaRect > 240000)
                {
                    CvInvoke.DrawContours(contoursImage, contours, i, new MCvScalar(0, 0, 255), 1);
                    CvInvoke.Circle(contoursImage, new Point((int)circle.Center.X, (int)circle.Center.Y), 2, new MCvScalar(0, 0, 255), 2);
                    //CvInvoke.Circle(contoursImage, new Point((int)circle.Center.X, (int)circle.Center.Y), (int)circle.Radius, new MCvScalar(255, 0, 120), 1);
                    CvInvoke.Rectangle(contoursImage, rect, new MCvScalar(255, 0, 0), 1);
                    Emgu.CV.Util.VectorOfPoint v = findCutPoint(contours[i], rect);
                }
            }
            CvInvoke.Imshow("contoursImage", contoursImage);

            CvInvoke.WaitKey(0);            
            CvInvoke.DestroyAllWindows();
            image.Dispose();
        }
        public static Emgu.CV.Util.VectorOfPoint findCutPoint(Emgu.CV.Util.VectorOfPoint contours, Rectangle rect)
        {
            Emgu.CV.Util.VectorOfPoint res = new Emgu.CV.Util.VectorOfPoint();
            int max_X = 0;
            int max_Y = 0;
            int min_X = 800;
            int min_Y = 800;
            int max_X_idx, max_Y_idx, min_X_idx, min_Y_idx;
            for (int i = 0; i < contours.Size; i++)
            {
                if(contours[i].X > max_X)
                {
                    max_X_idx = i;
                    max_X = contours[i].X;
                }
                if(contours[i].Y > max_Y)
                {
                    max_Y_idx = i;
                    max_Y = contours[i].Y;
                }
                if (contours[i].X > min_X)
                {
                    min_X_idx = i;
                    min_X = contours[i].X;
                }
                if (contours[i].Y > min_Y)
                {
                    min_Y_idx = i;
                    min_Y = contours[i].Y;
                }
            }
            System.Drawing.Point[] p0 = new Point(contours[min_Y].X, contours[min_Y].Y);
            res.Push(p0);

        }
        public static bool isCircleCenter(CircleF circle)
        {
            if (circle.Center.X > 350 && circle.Center.X < 410 && circle.Center.Y > 400 && circle.Center.Y < 485)
                return true;
            else 
                return false;
        }
        public static bool isRectCenter(Rectangle rect)
        {
            double centerX = rect.X + rect.Width / 2;
            double centerY = rect.Y + rect.Height / 2;
            if (centerX > 350 && centerX < 410 && centerY > 400 && centerY < 485)
                return true;
            else
                return false;
        }
        public static PointF[] PointToPointF(Point[] pf)
        {
            PointF[] aaa = new PointF[pf.Length];
            int num = 0;
            foreach (var point in pf)
            {
                aaa[num].X = (int)point.X;
                aaa[num++].Y = (int)point.Y;
            }
            return aaa;
        }

        public static void nouse(Mat image)
        {
            //Emgu.CV.Util.VectorOfMat splitImage = new Emgu.CV.Util.VectorOfMat();
            //CvInvoke.Split(image, splitImage);
            //var vms = splitImage.GetOutputArray();
            //Mat res0 = vms.GetMat(0);
            //Mat res1 = vms.GetMat(1);
            //Mat res2 = vms.GetMat(2);
            //CvInvoke.Imshow("res0", res0);
            //CvInvoke.Imshow("res1", res1);
            //CvInvoke.Imshow("res2", res2);

            //Emgu.CV.CvInvoke.Rectangle(image, ROI, new Emgu.CV.Structure.MCvScalar(0, 255, 0), 3);
            //CvInvoke.Imshow("ROI", imageROI);

            //Mat grayImage = new Mat();
            //CvInvoke.CvtColor(imageROI, grayImage, Emgu.CV.CvEnum.ColorConversion.Bgr2Gray);
            //CvInvoke.Imshow("grayImage", grayImage);

            //Mat blurImage = new Mat();
            //Mat GaussianImage = new Mat();
            //CvInvoke.Blur(grayImage, blurImage, new Size(3, 3), new Point(-1, 1));
            ////CvInvoke.Imshow("blurImage", blurImage);
            //CvInvoke.GaussianBlur(grayImage, GaussianImage, new Size(3, 3), 3);
            ////CvInvoke.Imshow("GaussianBlur", GaussianImage);
            //Mat threshImage = new Mat();
            //CvInvoke.Threshold(grayImage, threshImage, 100, 255, ThresholdType.Binary);
            ////CvInvoke.Imshow("threshImage", threshImage);
            //Mat struct_element = CvInvoke.GetStructuringElement(ElementShape.Rectangle, new Size(5, 5), new Point(-1, -1));
            //Mat daliteImage = new Mat();
            //CvInvoke.Dilate(threshImage, daliteImage, struct_element, new Point(-1, -1), 1, BorderType.Default, new MCvScalar(0, 0, 0));
            ////CvInvoke.Imshow("Dilate", daliteImage);
            //Mat openImage = new Mat();
            //CvInvoke.MorphologyEx(threshImage, openImage, MorphOp.Open, struct_element, new Point(-1, -1), 1, BorderType.Default, new MCvScalar(0, 0, 0));
            ////CvInvoke.Imshow("close", openImage);
            Mat grayImage = new Mat();
            CvInvoke.CvtColor(image, grayImage, Emgu.CV.CvEnum.ColorConversion.Bgr2Gray);
            Emgu.CV.Util.VectorOfMat splitImage = new Emgu.CV.Util.VectorOfMat();
            CvInvoke.Split(image, splitImage);
            //CvInvoke.Imshow("B", splitImage[0]);
            //CvInvoke.Imshow("G", splitImage[1]);
            //CvInvoke.Imshow("R", splitImage[2]);
            var vms = splitImage.GetOutputArray();
            Mat res0 = vms.GetMat(0);
            Mat res1 = vms.GetMat(1);
            Mat res2 = vms.GetMat(2);
            CvInvoke.Imshow("res0", res0);
            CvInvoke.Imshow("res1", res1);
            CvInvoke.Imshow("res2", res2);
            Console.WriteLine(res2.Size);

            Rectangle ROI = new Rectangle(280, 80, 800, 800);
            Mat imageROI = new Mat(image, ROI);
            Console.WriteLine(imageROI.NumberOfChannels);


            Mat cannyImage = new Mat();
            CvInvoke.Canny(grayImage, cannyImage, 100, 600);
            CvInvoke.Imshow("cannyImage", cannyImage);

            //Mat threshImage = new Mat();
            //CvInvoke.Threshold(cannyImage, threshImage, 160, 255, ThresholdType.Binary);

            Mat edge = new Mat();
            Emgu.CV.Util.VectorOfVectorOfPoint contours = new Emgu.CV.Util.VectorOfVectorOfPoint();
            Emgu.CV.IOutputArray hierarchy = new Mat();
            CvInvoke.FindContours(cannyImage, contours, null, Emgu.CV.CvEnum.RetrType.List, Emgu.CV.CvEnum.ChainApproxMethod.ChainApproxSimple);

            Mat contoursImage = new Mat(image, ROI);
            //double max_area = 0;
            //int max_idx = 0;

            Point[][] con1 = contours.ToArrayOfArray();
            PointF[][] con2 = Array.ConvertAll<Point[], PointF[]>(con1, new Converter<Point[], PointF[]>(PointToPointF));

            for (int i = 0; i < contours.Size; i++)
            {
                Rectangle rect = new Rectangle();
                double area = CvInvoke.ContourArea(contours[i]);
                rect = CvInvoke.BoundingRectangle(contours[i]);
                double areaRect = rect.Height * rect.Width;
                if (areaRect < 2500)
                {
                    CvInvoke.Rectangle(contoursImage, rect, new MCvScalar(170, 205, 120), -1);
                }
                //if (area > 0 && area < 40000)
                //{
                //rect = CvInvoke.BoundingRectangle(contours[i]);
                //CvInvoke.Rectangle(contoursImage, rect, new MCvScalar(0, 255, 255), 1);

                //CircleF circle = CvInvoke.MinEnclosingCircle(con2[i]);
                //CvInvoke.Circle(contoursImage, new Point((int)circle.Center.X, (int)circle.Center.Y), (int)circle.Radius, new MCvScalar(255, 0, 120), 1);

                //CvInvoke.DrawContours(contoursImage, contours, i, new MCvScalar(0, 0, 0), 1);
                //}
                //CvInvoke.DrawContours(contoursImage, contours, i, new MCvScalar(255, 0, 255), 1);

                //if (area > max_area)
                //{
                //    max_area = area;
                //    max_idx = i;
                //}

            }
            //double areaMax = CvInvoke.ContourArea(contours[max_idx]);
            //Console.WriteLine(areaMax);
            //CvInvoke.DrawContours(contoursImage, contours, max_idx, new MCvScalar(0, 0, 255), 2);

        }
    }
}
