#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=0
#

import sys
import urllib2
import optparse
import re
import unicodedata
import codecs
import StringIO
import time
import hashlib

URL_LIST = { 
	'cu': 'http://www18.atwiki.jp/imas_cg/pages/13.html',
	'co': 'http://www18.atwiki.jp/imas_cg/pages/14.html',
	'pa': 'http://www18.atwiki.jp/imas_cg/pages/15.html'
}

ITEM_PTN  = re.compile('<!--([0-9]+)-([0-9]+)-->(.*)')
TAG_PTN   = re.compile('<.*?>')

def fetch_data(attr):
	sys.stderr.write("Fetch wiki page...\n")
	agent = 'imascg-' + hashlib.md5(str(time.time())).hexdigest()
	req = urllib2.Request(URL_LIST[attr], None, { 'User-Agent': agent })
	f = codecs.getreader('utf-8')(urllib2.urlopen(req))
	return f

def getdata(attr, file):
	BIRTH_PTN = re.compile('([0-9]+)/([0-9]+)')
	SIZE_PTN  = re.compile('([0-9]+)-([0-9]+)-([0-9]+)')
	
#	f = fetch_data(attr):
#	for line in f.readlines():
#		pass

def print_header():
	HEADERS = (u'属性', u'アイドル名', u'レアリティ', u'レベル上限', u'親愛度上限',
				u'攻', u'守', u'コスト', u'1コスト攻', u'1コスト守', u'特技')
	str = ','.join(HEADERS)
	print str.encode(sys.getfilesystemencoding())
		
def pretty_print(record):
	UNEXPECTED_STRING = (u'アイドル名', u'名前', u'今日', u'[[]]', u'??', u'')
	if record[1] not in UNEXPECTED_STRING:
		str = ','.join(record)
		print str.encode(sys.getfilesystemencoding())

def main():
	
	parser = optparse.OptionParser()
	parser.add_option('-a', '--attr', dest='attribute', action='store', choices=['cu', 'co', 'pa'],
		help='Choice attribute: cu/co/pa. all attributes are enabled if no option.')
	parser.add_option('--no-header', dest='header', action='store_false', default=True,
        help='Prevent to writer header.')

	(options, args) = parser.parse_args()

	if options.header:
		print_header()

	if options.attribute is None:
		attr_list = URL_LIST.keys()
	else:
		attr_list = [ options.attribute ]

	for attr in attr_list:
		f = fetch_data(attr)
		record = [''] * 11
		record[0] = attr
		count = -1
		sys.stderr.write("Processing...\n")
		for line in f.readlines():
			m = ITEM_PTN.search(line)
			if m is not None:
				(row, col, val) = (int(m.group(1)), int(m.group(2)), TAG_PTN.sub('', m.group(3)))
				if col == 0:
					pretty_print(record)

				record[col+1] = unicodedata.normalize('NFKC', val)

				if count > row:
					pretty_print(record)
					break
				count = row
		f.close()

if __name__ == '__main__':

	main()
