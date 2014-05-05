#!/usr/bin/env python
#-*-coding:utf-8-*-

import urllib
import urllib2
import os
import re
from bs4 import BeautifulSoup

def downloadFile(fileNo, name, dirname):
    try:
        fileName = './' + dirname + '/' + name + '.pdf'
        url = 'http://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/' + fileNo + '.pdf'
        print "start to download %s" % fileName
        urllib.urlretrieve(url, fileName)
    except Exception:
        print "File is not existed."
    else:
        print "finish to download %s" % fileName

def mkDirs(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)

def getPaperNo(url):
    response = urllib2.urlopen(url)
    html = response.read()
    paperNames = []
    namePattern = re.compile(r'<a class="pdf-icon tooltip" href=.*">')
    names = namePattern.findall(html)
    for name in names:
        name = name.replace('<a class="pdf-icon tooltip" href="/pubs/archive/', '').replace('.pdf">', '').strip()
        paperNames.append(name)
    return paperNames

def getDirUrls(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    dirNames = []
    urls = soup.find_all('li', {'class':"expand fill"})
    for url in urls:
        urlstr = str(url.find('a'))
        urlpattern = re.compile(r'<a href=".*">')
        urlstr = urlpattern.findall(urlstr)[0].replace('<a href="', '').replace('">', '')
        dirNames.append(urlstr)
    return dirNames

if __name__ == '__main__':
    google_url_papers = "http://research.google.com/pubs/papers.html"
    paperDirs = getDirUrls(google_url_papers)
    for dirUrl in paperDirs:
        dirName = dirUrl.replace('/pubs/', '').replace('.html', '')
        mkDirs(dirName)
        abDirUrl = 'http://research.google.com' + dirUrl
        paperNameInDir = getPaperNo(abDirUrl)
        for name in paperNameInDir:
            downloadFile(name, name, dirName)
