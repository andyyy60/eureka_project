**Temperature recognition using Optical Character Recognition with k-Nearest-Neighbor**

**Assuming OpenCV 3.1 has been installed correctly**

1. Clone this repository to your machine
	
    git clone https://github.com/andyyy60/ocr_knn
    
    cd ocr_knn/initial_tasks/task3/
    
2. Running:
	
    python crop_and_recognize [-pictype] [-path to image]
 	
    
    output example: "Temp is: 64"


		usage as a module:
		
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
