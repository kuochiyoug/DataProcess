#include <cv.h>
#include <highgui.h>
#include <iostream>
#include <sstream>
#include <string>
#include <fstream>
#include <dirent.h>
#include <vector>

using namespace std;

string get_pixels(IplImage*);//指定画像の画素値を文字列で返す
string DoubleToString(double num);

int main(int argc, char* argv[])
{
  IplImage *src_img=0;
  IplImage *small_img=0;
  string small_file;

  if(argc != 3){
    cout << "Usage: gazou_kakou.cpp [InputImg] [OutputFile]" << endl;
    exit(1);
  }

  src_img = cvLoadImage (argv[1], CV_LOAD_IMAGE_COLOR);    //カラーでピクセル値を求める
  //src_img = cvLoadImage(argv[1],CV_LOAD_IMAGE_GRAYSCALE);//グレースケールでピクセル値を求める
  if (src_img == 0){
    cout << "Can't open " << argv[1] << endl;
    exit (-1);
  }
 
  const int w = src_img->width;
  const int h = src_img->height;

  small_img = cvCreateImage(cvSize((int)(w*0.025),(int)(h*0.025)), IPL_DEPTH_8U,3);
  //small_img = cvCreateImage(cvSize((int)(w*0.1),(int)(h*0.1)), IPL_DEPTH_8U,1);
  
    // 縮小 
  cvResize(src_img, small_img,CV_INTER_CUBIC);

  ofstream of_small(argv[2]);
  
  of_small << get_pixels(small_img);

  of_small.close();

  cvReleaseImage (&src_img);
  cvReleaseImage(&small_img);
  return 0;
}


string get_pixels(IplImage *img)
{
  uchar ch;
  double color;
  int x,y,k;
  string data("");
  for(y=0;y<img->height;y++){
    for(x=0;x<img->width;x++){
      for(k=0;k<img->nChannels;k++){
	ch = (img->imageData)[img->widthStep*y + img->nChannels*x + k];
	color = (double)ch/255.0;
	data += DoubleToString(color);
	data += " ";
      }
    }
  }

  return data;
}

string DoubleToString(double num)
{
  stringstream ss;
  ss << num;
  return ss.str();
}
