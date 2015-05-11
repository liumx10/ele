#coding=utf-8
#!/usr/env python

import urllib2
import codecs
from BeautifulSoup import BeautifulSoup
import chardet

def get_keywords(word, name):
    url = "http://baike.baidu.com/search/word?word=" + urllib2.quote(word.encode('utf-8')) + "&pic=1&sug=1&enc=utf-8"
    
    result = urllib2.urlopen(url).read().decode("utf-8")
    parsed_html = BeautifulSoup(result)

    result = str(parsed_html.body.find("div", attrs={
        'class': "card-summary-content"
        }) )

    result = result.replace('href=\"/', 'href=\"http://www.baike.baidu.com/')
    f = codecs.open(name, 'w', "utf-8")
    f.write(unicode(str(result), 'utf-8'))
    f.close()
    