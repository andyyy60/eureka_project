##Web API for Temperature Recognition of Sedgwick cameras##

	Types of cameras allowed and resolution
	
	
	pictype = 1 | BUSHNELL BONE CANYON / BONET | 3264 x 2448 px
	pictype = 2 | HC500 HYPERFIRE / MAIN | 1920 x 1080 px
	pictype = 3 | RECONYX / BONEH | 3776 x 2124 px
	
	USE:
		to use the API service via cURL:
		
		curl -i -X POST -F files=@<file.jpg>  --form "filename=<file.jpg>" --form "pictype=<1-3>" http://169.231.235.107:5000/upload
	
	SAMPLE:
	
	 curl -i -X POST -F files=@BoneT_2014-05-30_19-05-53_038.JPG --form "filename=temp.jpg" --form "pictype=1" http://169.231.235.107:5000/upload

	RESPONSE:
	
	{
  		"temperature": 64
	}
