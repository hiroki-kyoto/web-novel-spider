#coding=utf8

# save webpage with given url
# USING PYTHON 2

from urllib2 import urlopen
from urllib2 import URLError
import time
from HTMLParser import HTMLParser
import re

MAX_TRIAL = 30
SLEEP_TIME = 1
CONTENT_BEGIN = '<div id=\"content\">'
CONTENT_END = '</div>'

TITLE_BEGIN = '<h1>'
TITLE_END = '</h1>'

NEXT_CHAPTER_BEGIN = '</a> &rarr; <a href=\"'
NEXT_CHAPTER_END = '\">'

SOURCE_CODECS = 'GB2312'
TARGET_CODECS = 'UTF-8'

def encode(bytes):
	return bytes.encode(TARGET_CODECS)

def decode(re_data): 
	try:
		re_data = re_data.decode(SOURCE_CODECS)
	except Exception as error:  
		print error  
		print 'delete illegal string, try again...'
		pos = re.findall(r'decodebytesinposition([\d]+)-([\d]+):illegal',str(error).replace(' ',''))  
		if len(pos)==1:  
			re_data = re_data[0:int(pos[0][0])]+re_data[int(pos[0][1]):]  
			re_data = decode(re_data)  
			return re_data
	return re_data

def save_as_text(url, file):
	_counter = 0
	while _counter<MAX_TRIAL:
		try:
			f = urlopen(url)
		except URLError as err:
			_counter += 1
			if _counter==MAX_TRIAL:
				print("Connection totally failed!")
				raise err
			else:
				print('Connection failed, try again : %s' % _counter)
				time.sleep(SLEEP_TIME)
		else:
			_counter = MAX_TRIAL
	
	html = f.read()
	f.close()
	
	# decode html to unicode bytes
	html = decode(html)
	
	# add chapter segment
	f = open(file, 'at+')
	f.write('\n\n')
	parser = HTMLParser()
	
	# title
	s = html.find(TITLE_BEGIN)
	assert(s>=0)
	s += len(TITLE_BEGIN)
	e = html[s:].find(TITLE_END)
	assert(e>=0)
	e += s
	title = html[s:e]
	f.write(encode(title))
	f.write('\n')
	
	# content
	s = html.find(CONTENT_BEGIN)
	assert(s>=0)
	s += len(CONTENT_BEGIN)
	e = html[s:].find(CONTENT_END)
	assert(e>=0)
	e += s
	txt = html[s:e]
	txt = parser.unescape(txt)
	txt = txt.replace('<br />', '\n')
	txt = txt.replace('\t', '')
	txt = txt.replace('\r\n', '\n')
	txt = txt.replace('\n\n', '\n')
	txt = txt.replace('\n\n', '\n')
	f.write(encode(txt))
	
	# close file
	f.flush()
	f.close()
	
	# return the next page url
	s = html.find(NEXT_CHAPTER_BEGIN)
	assert(s>=0)
	s += len(NEXT_CHAPTER_BEGIN)
	e = html[s:].find(NEXT_CHAPTER_END)
	assert(e>=0)
	e += s
	
	return html[s:e]

def main():
	base_url = 'http://www.some_novel_site/book_id/'
	page_id = 'chapter_id.html'
	file_name = 'path_to_save_content.txt'
	print('saving novel content to : %s ' % file_name)
	print('Fetching page %s ...' % page_id)
	while page_id.find('html')>=0:
		page_id = save_as_text(base_url+page_id, file_name)
		print('Fetching page %s ...' % page_id)
		time.sleep(1)

main()
