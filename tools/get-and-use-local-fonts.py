#!/usr/bin/env python3
import re
import urllib.request

input  = "_fontbox.scss.in"
output = "_fontbox.scss"

def readURL(url):
    r = urllib.request.urlopen(urllib.request.Request(url, None, {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'}))
    return r.read()

def writeFile(path, content):
    with open(path, 'wb') as f:
        f.write(content)

with open(input, 'r') as f, open(output, 'w') as outputF:
    for line in f:
        line = line[:-1] # remove eol
        if re.match(r'^ *@import url', line):
            url = re.sub(r'^ *@import url\(([^)]*)\);.*', r'\1', line)
            remote = readURL(url).decode('utf-8')
            def processUrlInRemote(x):
                fonturl = x.group(1)
                protocolrelatived = re.sub(r'url\(https?://', r'url(//', x.group(0))
                format = x.group(2)
                fontfilename = re.sub(r'.*/', '', fonturl)
                fontfilecontent = readURL(fonturl)
                targetFile = 'local-fonts/'+fontfilename
                writeFile(targetFile, fontfilecontent)
                print('GOT:'+fontfilename)
                return 'url({}) {}, {}'.format(targetFile, format, protocolrelatived)
            updatedRemote = re.sub(r'url\(([^)]*)\) +(format\([^)]*\))', processUrlInRemote, remote)
            outputF.write(updatedRemote)
        else:
            outputF.write(line)
