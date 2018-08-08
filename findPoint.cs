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
            string picsPath = "E:\\video_shot\\videos\\picsColor\\picsColor.txt";
            StreamReader sr = new StreamReader(picsPath, Encoding.Default);
            string line;
            int count = 0;
            while ((line = sr.ReadLine()) != null)
            {
                string imgPath = line.ToString();
                Console.WriteLine(imgPath);

                Mat image = CvInvoke.Imread(imgPath, LoadImageType.Color);
                Mat imageDraw = new Mat();
                image.CopyTo(imageDraw);
                Point[] cutPoint = findContours(image);
                if(cutPoint[0].X == 0)
                {
                    continue;
                }
                else
                {
                    for(int i =0;i < 4; i++)
                    {
                        Console.WriteLine(cutPoint[i].X);
                        Console.WriteLine(cutPoint[i].Y);
                        CvInvoke.Circle(imageDraw, new Point(cutPoint[i].X + 280, cutPoint[i].Y + 80), 2, new MCvScalar(0, 0, 255), 2);
                    }
                }
                //findContours(image);
                CvInvoke.Imshow("imageDraw", imageDraw);
                CvInvoke.WaitKey(0);
                count += 1;
            }

            ////Capture capture = new Capture("E:\\video_shot\\videos\\16_25_22.264");
            ////Capture capture = new Capture("E:\\video_shot\\videos\\16_35_19.264");
            //Capture capture = new Capture("E:\\video_shot\\videos\\16_35_24.264");
            ////Capture capture = new Capture("E:\\video_shot\\videos\\16_45_19.264");
            //int idx = 0;
            //while (true)
            //{
            //    Mat frame = capture.QueryFrame();
            //    idx += 1;
            //    if (frame != null)
            //    {
            //        Mat image = frame;
            //        if (idx % 24 == 0)
            //        {
            //            findContours(image);
            //        }
            //    }
            //}            
        }
        public static Point[] findContours(Mat image)
        {
            Point[] ps = new Point[4];
            for (int i =0;i < 4;i++)
            {
                ps[i].X = 0;
                ps[i].Y = 0;
            }
            DateTime start = DateTime.Now;

            Mat grayImage = new Mat();
            CvInvoke.CvtColor(image, grayImage, Emgu.CV.CvEnum.ColorConversion.Bgr2Gray);
                        
            Rectangle ROI = new Rectangle(280, 80, 800, 800);
            Mat imageROI = new Mat(grayImage, ROI);
            Mat imageROIBGR = new Mat(image, ROI);

            Mat cannyImage = new Mat();
            CvInvoke.Canny(imageROI, cannyImage, 100, 600);
            //CvInvoke.Imshow("cannyImage", cannyImage);
            
            //Mat edge = new Mat();
            //CvInvoke.Canny(threshImage, edge, 30, 200);
            Emgu.CV.Util.VectorOfVectorOfPoint contours = new Emgu.CV.Util.VectorOfVectorOfPoint();
            Emgu.CV.IOutputArray hierarchy = new Mat();
            CvInvoke.FindContours(cannyImage, contours, null, Emgu.CV.CvEnum.RetrType.List, Emgu.CV.CvEnum.ChainApproxMethod.ChainApproxSimple);

            Rectangle rect = new Rectangle();
            double areaRect = 0.0;
            
            CvInvoke.FindContours(cannyImage, contours, null, Emgu.CV.CvEnum.RetrType.List, Emgu.CV.CvEnum.ChainApproxMethod.ChainApproxSimple);

            Point[][] con1 = contours.ToArrayOfArray();
            PointF[][] con2 = Array.ConvertAll<Point[], PointF[]>(con1, new Converter<Point[], PointF[]>(PointToPointF));

            Mat contoursImage = new Mat(image, ROI);
            //int flag = 0;
            //CvInvoke.Circle(contoursImage, new Point(390, 464), 30, new MCvScalar(0, 0, 255), 1);
            //CvInvoke.Rectangle(contoursImage, new Rectangle(370,430,50,50), new MCvScalar(0, 0, 255), 1);
            for (int i = 0; i < contours.Size; i++)
            {
                rect = CvInvoke.BoundingRectangle(contours[i]);
                areaRect = rect.Width * rect.Height;

                CircleF circle = CvInvoke.MinEnclosingCircle(con2[i]);
                //CvInvoke.Circle(contoursImage, new Point((int)circle.Center.X, (int)circle.Center.Y), (int)circle.Radius, new MCvScalar(255, 0, 120), 1);

                if (isCircleCenter(circle) && isRectCenter(rect) && areaRect > 300000)// && flag == 0)
                {
                    //flag = 1;
                    //CvInvoke.DrawContours(contoursImage, contours, i, new MCvScalar(0, 0, 255), 1);
                    //CvInvoke.Circle(contoursImage, new Point((int)circle.Center.X, (int)circle.Center.Y), 2, new MCvScalar(0, 0, 255), 2);
                    //CvInvoke.Circle(contoursImage, new Point((int)circle.Center.X, (int)circle.Center.Y), (int)circle.Radius, new MCvScalar(255, 0, 120), 1);
                    //CvInvoke.Rectangle(contoursImage, rect, new MCvScalar(255, 0, 0), 1);
                    ps = findCutPoint(contours[i]);
                    //for (int k = 0; k < 4; k++)
                    //{
                    //    CvInvoke.Circle(contoursImage, ps[k], 2, new MCvScalar(0, 255, 255), 2);
                    //}
                }
            }
            DateTime end = DateTime.Now;
            TimeSpan ts = end.Subtract(start);
            Console.WriteLine("DateTime {0}ms.", ts.TotalMilliseconds);

            //CvInvoke.Imshow("contoursImage", contoursImage);
            //CvInvoke.WaitKey(0);            
            //CvInvoke.DestroyAllWindows();
            image.Dispose();

            return ps;
        }
        public static Point[] findCutPoint(Emgu.CV.Util.VectorOfPoint contours)
        {
            Point[] con1 = contours.ToArray();
            Array.Sort(con1, compareY);

            int size = con1.Length;
            int top_x = con1[0].X;
            int top_y = con1[0].Y;
            int bottom_x = con1[size - 1].X;
            int bottom_y = con1[size - 1].Y;
            int top_x_count = 1;
            int bottom_x_count = 1;
            int flag1 = 0;
            for (int i = 1; i<size/10; i++)
            {
                if (top_y == con1[i].Y)
                {
                    flag1 = 1;
                    top_x_count += 1;
                    top_x += con1[i].X;
                }
                if(bottom_y == con1[size -1 - i].Y)
                {
                    flag1 = 1;
                    bottom_x_count += 1;
                    bottom_x += con1[size - 1 - i].X;
                }
                if (flag1 == 0)
                    break;
            }
            float top_x_temp = (float)(top_x * 1.0F / top_x_count * 1.0);
            float bottom_x_temp = (float)(bottom_x * 1.0F / bottom_x_count * 1.0);
            
            Point[] con2 = con1;
            Array.Sort(con2, compareX);
            int left_x = con2[0].X;
            int left_y = con2[0].Y;
            int right_x = con2[size - 1].X;
            int right_y = con2[size - 1].Y;
            int left_y_count = 1;
            int right_y_count = 1;
            int flag2 = 0;
            for (int i = 1; i < size / 10; i++)
            {
                if (left_x == con2[i].X)
                {
                    flag2 = 1;
                    left_y_count += 1;
                    left_y += con2[i].Y;
                }
                if (right_x == con2[size - 1 - i].X)
                {
                    flag2 = 1;
                    right_y_count += 1;
                    right_y += con2[size - 1 - i].Y;
                }
                if(flag2 == 0)
                    break;
            }
            float left_y_temp = left_y*1.0F / (float)(left_y_count*1.0F);
            float right_y_temp = right_y*1.0F / (float)right_y_count*1.0F;

            System.Drawing.Point[] p1 = new Point[4];
            p1[0].X = (int)top_x_temp;
            p1[0].Y = top_y;
            p1[1].X = right_x;
            p1[1].Y = (int)right_y_temp;
            p1[2].X = (int)bottom_x_temp;
            p1[2].Y = bottom_y;
            p1[3].X = left_x;
            p1[3].Y = (int)left_y_temp;
            
            return p1;
        }
        public static int compareX(Point a, Point b)
        {
            if (a.X >= b.X)
                return 1;
            else
                return -1;
        }
        public static int compareY(Point a, Point b)
        {
            if (a.Y >= b.Y)
                return 1;
            else
                return -1;
        }
        public static bool isCircleCenter(CircleF circle)
        {
            if (circle.Center.X > 360 && circle.Center.X < 420 && circle.Center.Y > 434 && circle.Center.Y < 494)
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
        public static PointF[] PointToPointF(Point[] ppf)
        {
            PointF[] pf = new PointF[ppf.Length];
            int num = 0;
            foreach (var point in ppf)
            {
                pf[num].X = (int)point.X;
                pf[num++].Y = (int)point.Y;
            }
            return pf;
        }
    }
}
