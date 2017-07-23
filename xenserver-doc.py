#!/usr/bin/env python3
# Retrieve the newest documents of XenServer
import pycurl,os
from io import BytesIO
from bs4 import BeautifulSoup

buf = BytesIO()

curl = pycurl.Curl()
curl.setopt(curl.URL, 'https://docs.citrix.com/en-us/xenserver/current-release.html')
curl.setopt(curl.WRITEDATA, buf)
curl.perform()
curl.close()

content = buf.getvalue()
soup = BeautifulSoup(content, 'html.parser')

def has_class(tag):
	return tag.name == 'div' and tag.has_attr('class') and tag['class'][0] == 'dl-doc-downloads'

update_log = open('/tmp/update.log', 'w')
for tag in soup.find_all(has_class):
	doc_file = tag.a['href']
	print(doc_file[doc_file.rindex('/')+1:])
	os.system('wget -nv -c https://docs.citrix.com' + doc_file)
	print(doc_file[doc_file.rindex('/')+1:], end='\n', file=update_log, flush=True)

update_log.close()
