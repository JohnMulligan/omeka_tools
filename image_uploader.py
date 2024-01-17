from env import omeka_api_base_url,key_identity,key_credential
import json
import sys
import os
import urllib
import requests

item_id=int(sys.argv[1])
images_basepath=sys.argv[2]

d=open('images.tsv','r')
t=d.read()
d.close()

filenames=[l.strip() for l in t.split('\n') if t!='']

missing_files=0
for fname in filenames:
	if not os.path.exists(os.path.join(images_basepath,fname)):
		print("file does not exist:",fname)
		missing_files+=1
		
if missing_files>0:
	print("missing %d files" %missing_files)
	exit()

for fname in filenames:
	print(fname)
	data = {
		"o:ingester": "upload", 
		"file_index": "0", 
		"o:item": {"o:id": int(item_id)}
	}
	
	headers = {
		'Content-type': 'application/json'
	}
	
	params={
		'key_identity':key_identity,
		'key_credential':key_credential
	}
	
	fpath=os.path.join(images_basepath,fname)
	
	this_url=omeka_api_base_url+'media'
	files = [('data', (None, json.dumps(data), 'application/json')),('file[0]', (fname, open(fpath,'rb'),'image'))]
	response = requests.post(this_url, params=params, files=files)
	print(response)
	
