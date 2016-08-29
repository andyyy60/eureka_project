##Web API for Temperature Recognition of Sedgwick cameras##

	Types of cameras allowed and resolution
	
	
	pictype = 1 | BUSHNELL BONE CANYON / BONET
	pictype = 2 | HC500 HYPERFIRE / MAIN 
	pictype = 3 | RECONYX / BONEH
	
	USE:
		to use the API service via cURL:
		
		curl -i -X POST -F files=@<file.jpg>  --form "filename=<file.jpg>" --form "pictype=<1-3>" http://169.231.235.107:5000/upload
	
