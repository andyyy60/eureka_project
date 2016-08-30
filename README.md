# Animal Recognition Using Convolutional Neural Networks and k-Nearest-Neighbors

Repository for the project "Where is the bear?" a tool that aims to classify animals from the [Sedgwick Reserve](http://sedgwick.nrs.ucsb.edu/) using different machine learning libraries. Classifying these images along with information such as temperature and time/date taken can provide a unique insight in the hidden world of wildlife.

## Getting Started

These instructions have been tested only in Ubuntu 14.04 (Trusty) and Ubuntu 15.10 (Wily)

Setting up OPENCV 3.1 to recognize temperature values of Sedgwick Camera Traps.



### Camera types:
```
	BUSHNELL BONE CANYON / BONET ---> Camera 1
```
![Alt text](https://raw.githubusercontent.com/andyyy60/ocr_knn/master/caffe/data/BoneT_2014-05-30_19-05-53_038.JPG)
````
	HC500 HYPERFIRE / MAIN ---> Camera 2
````
![Alt text](https://raw.githubusercontent.com/andyyy60/ocr_knn/master/caffe/data/Main_2013-09-18_14-07-12_9062.JPG)

````
	RECONYX / BONEH ---> Camera 3
````
![Alt text](https://raw.githubusercontent.com/andyyy60/ocr_knn/master/caffe/data/BoneH_2015-08-27_09-27-31_7589.JPG)

### Prerequisities

	INSTALLING OPENCV 3.1:	
```
	sudo apt-get -y update
	sudo apt-get -y install build-essential cmake git pkg-config
	sudo apt-get -y install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev
	sudo apt-get -y install libgtk2.0-dev
	sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
	sudo apt-get -y install libatlas-base-dev gfortran
	sudo apt-get -y install python2.7-dev
	pip install numpy
	cd ~
	git clone https://github.com/Itseez/opencv.git
	cd opencv
	git checkout 3.1.0
	cd ~
	git clone https://github.com/Itseez/opencv_contrib.git
	cd opencv_contrib
	git checkout 3.1.0
	cd ~/opencv
	mkdir build
	cd build
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
		-D CMAKE_INSTALL_PREFIX=/usr/local \
		-D INSTALL_C_EXAMPLES=OFF \
		-D INSTALL_PYTHON_EXAMPLES=ON \
		-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
		-D BUILD_EXAMPLES=ON ..
	make -j8
	sudo make install
	sudo ldconfig
```
### Installing

Clone this repo into your machine:
```
git clone https://github.com/andyyy60/ocr_knn/
```

cd into task3
```
cd ocr_knn/initial_tasks/task3/
```

Assuming OpenCV 3.1 has been installed correctly

```
Run:

	python crop_and_recognize [-pictype] [-path to image]
    
    	output example: "Temp is: 64"
```


Usage as a module:

```
	EXPORT PYTHONPATH=.:ocr_knn/initial_tasks/task3
	import crop_and_recognize
	
	call: #fname is full path to JPG file, its filename, with extension
	    print "Using newocr, image name is: {0}".format(fname)
	    if pictype == 1:
	        temp = crop_and_recognize.run_c3(fname, 'ocr_knn/flask_ocr/backend/data/data_files/camera_3/‘)
	
	    if pictype == 2:
	        temp = crop_and_recognize.run_c2(fname, 'ocr_knn/flask_ocr/backend/data/data_files/camera_2/‘)
	
	    if pictype == 3:
	        temp = crop_and_recognize.run_c1(fname, 'ocr_knn/flask_ocr/backend/data/data_files/camera_1/‘)
	
	    print "Temp is: {0}".format(temp)
```
