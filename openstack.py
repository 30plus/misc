#!/usr/bin/env python3
# Clone openstack and keep the local copy up-to-date

import pycurl,os
from io import BytesIO
from bs4 import BeautifulSoup

buf = BytesIO()
src_root = os.getcwd()

curl = pycurl.Curl()
curl.setopt(curl.URL, 'http://git.openstack.org/cgit')
curl.setopt(curl.WRITEDATA, buf)
curl.perform()
curl.close()

content = buf.getvalue()
soup = BeautifulSoup(content, 'html.parser')

def has_class(tag):
	return tag.name == 'td' and tag.has_attr('class')

update_log = open('/tmp/update.log', 'w')
for tag in soup.find_all(has_class):
	if tag['class'][0] == 'reposection':
		os.chdir(src_root)
		repo = tag.string
		if os.path.isfile(repo):
			print('Replace file ' + repo + ' to make room for cloning.')
			os.remove(repo)
		if not os.path.exists(repo):
			print('Creating new directory: ' + repo + '.')
			os.mkdir(repo)
		os.chdir(repo)

	elif tag['class'][0] == 'sublevel-repo':
		url = 'git://git.openstack.org/' + tag.a['title']
		repo = tag.a['title']
		repo_dir = repo[repo.index('/')+1:]

		print(repo, end='\n', file=update_log, flush=True)

		if os.path.isfile(repo_dir):
			print('Replace file ' + repo + ' to make room for cloning.')
			os.remove(repo_dir)
		if os.path.exists(repo_dir):
			os.chdir(repo_dir)
			print('Updating repo: ' + repo + '.')
			os.system('git pull')
			os.chdir('..')
		else:
			print('Cloning repo: ' + repo + '.')
			os.system('git clone --recursive ' + url)
update_log.close()
