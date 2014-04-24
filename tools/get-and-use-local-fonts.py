#!/usr/bin/env python

import re
import urllib2

input  = "_fontbox.scss.in"
output = "_fontbox.scss"

def readURL(url):
    return urllib2.urlopen(urllib2.Request(url, None, {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'})).read()

def writeFile(path, content):
    with open(path, 'w') as f:
        f.write(content)

with open(input, 'r') as f, open(output, 'w') as outputF:
    for line in f:
        line = line[:-1] # remove eol
        if re.match(r'^ *@import url', line):
            url = re.sub(r'^ *@import url\(([^)]*)\);.*', r'\1', line)
            remote = readURL(url)
            def processUrlInRemote(x):
                fonturl = x.group(1)
                format = x.group(2)
                fontfilename = re.sub(r'.*/', '', fonturl)
                fontfilecontent = readURL(fonturl)
                targetFile = 'local-fonts/'+fontfilename
                writeFile(targetFile, fontfilecontent)
                print 'GOT:'+fontfilename
                return 'url(%s) %s, %s' % (targetFile, format, x.group(0))
            updatedRemote = re.sub(r'url\(([^)]*)\) +(format\([^)]*\))', processUrlInRemote, remote)
            outputF.write(updatedRemote)
        else:
            outputF.write(line)
