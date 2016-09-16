##Web API for Temperature Recognition of Sedgwick cameras##

####Types of cameras allowed and resolution


	pictype = 1 | BUSHNELL BONE CANYON / BONET | 3264 x 2448 px
	pictype = 2 | HC500 HYPERFIRE / MAIN | 1920 x 1080 px AND HC600 HYPERFIRE 2048 x 1536
	pictype = 3 | RECONYX / BONEH | 3776 x 2124 px

####USE:
	to use the API service via cURL:
	
	curl -i -X POST -F files=@<file.jpg>  --form "filename=<file.jpg>" --form "pictype=<1-3>" http://<IP:ADDRESS>:<PORT>/upload

####SAMPLE:

 curl -i -X POST -F files=@BoneT_2014-05-30_19-05-53_038.JPG --form "filename=temp.jpg" --form "pictype=1" http://169.231.235.107:5000/upload

####RESPONSE:

{
  	"temperature": 64
}


### Usage in python with Requests

def get_temp(image_path):
	import requests
	IP = 'localhost'
	PORT = '8080' #depends on your chosen port in app.run(host='0.0.0.0',port=8080) in flask)
	            
	fname = 'test.jpg'
	pictype = '2'   
	remote_fname = 'temp.jpg' 
	url = 'http://{0}:{1}/upload'.format(IP,PORT)
	payload = {'filename': remote_fname, 'pictype': pictype}
	#print url
	#print payload   
	try:                
	    files = {'files': image_path}
	    resp = requests.post(url, files=files, data=payload)
	    if resp.status_code == 200: 
	        jresp = resp.json()
	        temp = jresp['temperature']
	    else:           
	        print 'Error, status code {0}'.format(resp.status_code)
	        temp = -9999
	except Exception as e: 
	    print e         
	    temp = -9999    
	print 'Temperature: {0}'.format(temp)
