import wikipedia
import urllib.request
import urllib
import sys
from mwclient import Site

'''
wikipedia.set_lang("ja")
print(wikipedia.page(urllib.parse.unquote("2011 MD")).content)


site = Site('ar.wikipedia.org')
page = site.pages[urllib.parse.unquote("%D8%A3%D8%A8%D9%84_%D8%AA%D9%8A_%D9%81%D9%8A_%2B")]
text = page.text()
print(text)
'''
print(urllib.parse.unquote("%D8%A3%D8%A8%D9%84_%D8%AA%D9%8A_%D9%81%D9%8A_%2B"))
