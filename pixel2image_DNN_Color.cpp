#include <cv.h>
#include <highgui.h>
#include <iostream>
#include <sstream>
#include <string>
#include <fstream>
#include <dirent.h>
#include <vector>

using namespace std;

#define IMAGE_WIDE	40
#define IMAGE_LENGTH	30
#define CHANNELS	3

int main(int argc, char* argv[])
{
	if(argc != 4){
		cout << "Usage: pixel2image_DNN.cpp [Inputdat] [Output_dir] [Lines_dim]" << endl;
		exit(1);
	}

	int lines_dim = atoi(argv[3]);

	double *DNN_image_tmp;
	DNN_image_tmp = new double[lines_dim * IMAGE_WIDE * IMAGE_LENGTH * CHANNELS];

	char *DNN_image;
	DNN_image = new char[lines_dim * IMAGE_WIDE * IMAGE_LENGTH * CHANNELS];

	//ファイルの読み込み
	std::ifstream DNN_image_dat;
	DNN_image_dat.open(argv[1]);
	if(DNN_image_dat.is_open()){
		//std::cout << "SOM_feature:successfully opened."<< std::endl;
		for(int i = 0; i < lines_dim * IMAGE_WIDE * IMAGE_LENGTH * CHANNELS; i++){
			DNN_image_dat >> DNN_image_tmp[i];
		}
	} else {
		 std::cout << "DNN_image_dat:not found" << std::endl;
		 return 0;
	}

	//正規化されているデータを戻す
	for(int i = 0; i < lines_dim * IMAGE_WIDE * IMAGE_LENGTH * CHANNELS; i++){
		//DNN_image_tmp[i] = ( (DNN_image_tmp[i] - 0.10)/0.80 ) * 255;//[0.1 0.9]で正規化されていた
		DNN_image_tmp[i] = DNN_image_tmp[i] * 255;//[0.1 0.9]で正規化されていた
	}

	for(int i = 0; i < lines_dim * IMAGE_WIDE * IMAGE_LENGTH * CHANNELS; i++){
		DNN_image[i] = char(DNN_image_tmp[i]);
	}

	//pixelデータをimageデータに変換
	IplImage* DNN_image_out[lines_dim];
	int count = 0;
	char filename[128];
	for(int i = 0; i < lines_dim; i++){
		DNN_image_out[i] = cvCreateImage(cvSize(IMAGE_WIDE, IMAGE_LENGTH), IPL_DEPTH_8U, 3);
		for(int k = 0; k < IMAGE_LENGTH; k++){	//縦
			for(int l = 0; l < IMAGE_WIDE; l++){	//横
				DNN_image_out[i]->imageData[(k * IMAGE_WIDE + l)*3 +0] = DNN_image_tmp[(k * IMAGE_WIDE + l)*3 + 0 + i*(IMAGE_WIDE * IMAGE_LENGTH * CHANNELS)];
				DNN_image_out[i]->imageData[(k * IMAGE_WIDE + l)*3 +1] = DNN_image_tmp[(k * IMAGE_WIDE + l)*3 + 1 + i*(IMAGE_WIDE * IMAGE_LENGTH * CHANNELS)];
				DNN_image_out[i]->imageData[(k * IMAGE_WIDE + l)*3 +2] = DNN_image_tmp[(k * IMAGE_WIDE + l)*3 + 2 + i*(IMAGE_WIDE * IMAGE_LENGTH * CHANNELS)];
			}
		}

		sprintf(filename,"%s/DNN_image%03d.bmp",argv[2],i);
		cvSaveImage(filename,DNN_image_out[i]);
	}

	 return 0;

}

