#!/usr/bin/env python3
# Clone Enlightenment and keep the local copy up-to-date

import pycurl,os
from io import BytesIO
from bs4 import BeautifulSoup

buf = BytesIO()
src_root = os.getcwd()

curl = pycurl.Curl()
curl.setopt(curl.URL, 'https://git.enlightenment.org')
curl.setopt(curl.WRITEDATA, buf)
curl.perform()
curl.close()

content = buf.getvalue()
soup = BeautifulSoup(content, 'html.parser')
skip_repo = False

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
		if repo[0] == '~':
			skip_repo = True
		elif not os.path.exists(repo):
			print('Creating new directory: ' + repo + '.')
			os.mkdir(repo)
			skip_repo = False
		os.chdir(repo)

	elif tag['class'][0] == 'sublevel-repo':
		if skip_repo == True:
			continue

		url = 'git://git.enlightenment.org/' + tag.a['title']
		repo = tag.a['title']
		repo_dir = repo[repo.rindex('/')+1:-4]

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
